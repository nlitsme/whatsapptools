from __future__ import division, print_function
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import subprocess
import javaobj
import re
import os
import sys
import datetime
from binascii import a2b_hex

import twisted.web.client
import twisted.web.http_headers
from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ProcessProtocol
from twisted.internet.defer import Deferred
import twisted.enterprise.adbapi

import sqlite3

class WhatsappFiles:
    def get(self, path, savepath):
        print("getting %s  ->  %s" % (path, savepath))

        #reactor.spawnProcess(ProcessProtocol(), "/usr/local/bin/adb", ["adb", "pull", "/storage/emulated/0/WhatsApp/" + path, savepath])
        subprocess.Popen(["adb", "pull", "/storage/emulated/0/WhatsApp/" + path, savepath])


class Record:
    """ baseclass for creating an object with attributes from database columns """
    def __init__(self, desc, row):
        for d, v in zip(desc, row):
            setattr(self, d[0], v)
    def __repr__(self):
        s = ""
        for k in dir(self):
            if k[0]!='_':
                v = getattr(self, k)
                s += " " + k + ":" + str(v)
        return s
    def __str__(self):
        return self.__repr__()


class Contact(Record):
    """ object holding information for a contact """
    def __init__(self, desc, row):
        super().__init__(desc, row)

        fullname = self.given_name
        if self.family_name:
            fullname += " " + self.family_name
        self.names = set((self.display_name, fullname, self.sort_name))
        self.names.discard("")
        self.names.discard(None)
        self.names.discard(self.wa_name)

    def isgroup(self):
        return self.jid.endswith("@g.us")

    def isuser(self):
        return self.jid.endswith("@s.whatsapp.net")

    def isbcast(self):
        return self.jid=="status@broadcast"

    def name(self):
        if self.isgroup():
            return self.display_name
        elif self.isbcast():
            return ""
        elif self.isuser():
            l = [ self.wa_name ] if self.wa_name else []
            l.extend(self.names)

            return ", ".join(l)
        else:
            raise Exception("unknown contact type")


class Message(Record):
    """ object holding information for a message """
    def __init__(self, desc, row):
        super().__init__(desc, row)

        self.obj = None
        if self.thumb_image:
            try:
                self.obj = javaobj.loads(self.thumb_image)
            except Exception as e:
                print(e, msg[19])
                pass
        self.sender = self.remote_resource or self.key_remote_jid


class AsyncWhatsappDatabase:
    def __init__(self, basepath):
        self.msgstore = twisted.enterprise.adbapi.ConnectionPool('sqlite3', database=os.path.join(basepath, 'msgstore.db'), cp_max=1, check_same_thread=False)
        self.wa = twisted.enterprise.adbapi.ConnectionPool('sqlite3', database=os.path.join(basepath, 'wa.db'), cp_max=1, check_same_thread=False)


        # use twisted.enterprise.adbapi

    # media_wa_type
    #  '1'     image/jpeg
    #  '2'     audio/aac,    audio/ogg,    audio/ogg; codecs=opus
    #  '3'     video/mp4
    #  '4'     VCARD
    #  '8'     voice call
    #  '9'     document
    #  '13'    video/mp4
    #  '14'    multiple vcards in rawdata

    def getmessagesafter(self, mid, msgcb):
        """ return messages larger then the specified `mid` """
        def runquery(conn):
            c = conn.cursor()
            
            for row in c.execute("select * from messages where _id > ?", mid):
                reactor.callLater(0, msgcb, Message(c.description, row))

        return self.msgstore.runWithConnection(runquery)

    def getcontacts(self, ctcb):
        """ return all contacts """
        def runquery(conn):
            c = conn.cursor()
            
            for row in c.execute("select * from wa_contacts"):
                print("..")
                reactor.callLater(0, ctcb, Contact(c.description, row))

        return self.wa.runWithConnection(runquery)


class WhatsappDatabase:
    """
    Synchronous (non-twisted) interface to the whatsapp databases
    in the specified `basepath`

    Methods exist for getting:
     * messages after `id`
     * messages with a specific id
     * contacts with a specific jid
     * contacts with a specific id
     * all contacts
    """
    def __init__(self, basepath):
        self.msgstore = sqlite3.connect(os.path.join(basepath, 'msgstore.db'))
        self.wa = sqlite3.connect(os.path.join(basepath, 'wa.db'))

        # use twisted.enterprise.adbapi

    # media_wa_type
    #  '1'     image/jpeg
    #  '2'     audio/aac,    audio/ogg,    audio/ogg; codecs=opus
    #  '3'     video/mp4
    #  '4'     VCARD
    #  '8'     voice call
    #  '9'     document
    #  '13'    video/mp4
    #  '14'    multiple vcards in rawdata

    def getmessagesafter(self, mid):
        """ return messages larger then the specified `mid` """
        c = self.msgstore.cursor()
        
        for row in c.execute("select * from messages where _id > ?", [mid]):
            yield Message(c.description, row)

    def getmessage(self, mid):
        """ return one message """
        c = self.msgstore.cursor()
        
        c.execute("select * from messages where _id=?", [mid])
        row = c.fetchone()
        return Message(c.description, row)

    def getcontacts(self):
        """ return all contacts """
        c = self.wa.cursor()
        
        for row in c.execute("select * from wa_contacts"):
            yield Contact(c.description, row)

    def getcontact(self, cid):
        """ return a single contact, either by id, or jid """
        c = self.wa.cursor()
        
        if type(cid)==str:
            c.execute("select * from wa_contacts where jid=?", [cid])
        else:
            c.execute("select * from wa_contacts where _id=?", [cid])
        row = c.fetchone()
        return Contact(c.description, row)


if sys.version_info[0] == 2:
    def myord(x):
        return ord(x)
else:
    def myord(x):
        return x

def j2b(val):
    def tounsignedbyte(x):
        return x+256 if x<0 else x
    return bytes(tounsignedbyte(_) for _ in val)



class WhatsappMediaDownloader:
    """
    object for downloading media for a whatsapp message
    """
    def __init__(self):
        self.agent =  twisted.web.client.Agent(reactor)

    class MediaDecryptor(Protocol):
        """ encrypted media downloader protocol """
        def __init__(self, cipher):
            print("httpdn.init")
            self.finished = Deferred()
            self.plaindata = b''
            self.cipherdata = b''
            self.cipher = cipher

        def connectionMade(self):
            print("httpdn.conn")

        def dataReceived(self, data):
            print("httpdn.data", data)
            cipherdata = self.cipherdata + data
            chunklen = rounddown(len(cipherdata), cipher.block_size)
            if chunklen:
                self.plaindata += cipher.decrypt(cipherdata[:chunklen])
            self.cipherdata = cipherdata[chunklen:]

        def connectionLost(self, reason):
            print("httpdn.lost", reason)
            if not reason.check(twisted.web.client.ResponseDone):
                print("ERR")
                reason.printTraceback()

            pad = myord(self.plaindata[-1])
            if self.plaindata[-pad:] != self.plaindata[-1:] * pad:
                print("invalid padding")
            self.plaindata = self.plaindata[:-pad]

            self.finished.callback(self.plaindata)

    class MediaDownloader(Protocol):
        """ plaintext media downloader protocol """
        def __init__(self):
            print("httpdn.init")
            self.finished = Deferred()
            self.plaindata = b''

        def connectionMade(self):
            print("httpdn.conn")

        def dataReceived(self, data):
            print("httpdn.data", data)
            self.plaindata += data

        def connectionLost(self, reason):
            print("httpdn.lost", reason)
            if not reason.check(twisted.web.client.ResponseDone):
                print("ERR")
                reason.printTraceback()
            self.finished.callback(self.plaindata)

    def savemedia(self, req, msg, cb):
        """ save the media from the request `req` """ 

        if hasattr(msg.obj, 'cipherKey') and msg.obj.cipherKey:
            downloader = self.MediaDecryptor(AES.new(j2b(msg.obj.cipherKey), mode=AES.MODE_CBC, IV=j2b(msg.obj.iv)))
        else:
            downloader = self.MediaDownloader()

        def printerr(*args):
            print("save:err", args)
            log.err(*args)
            cb(None)
        downloader.finished.addCallback(cb)
        downloader.finished.addErrback(printerr)

        def httpresponse(res):
            print("save.resp")
            res.deliverBody(downloader)

        req.addCallback(httpresponse)
        req.addErrback(printerr)

    def get(self, msg, readycb):
        """ top level message media downloader """
        print("geturl", msg.media_url)
        req = self.agent.request(b'GET', msg.media_url.encode('utf-8'))
        self.savemedia(req, msg, readycb)


class ApplicationState:
    def __init__(self, fn):
        self.db = sqlite3.connect(fn)
        self.initdb()
    def initdb(self):
        self.execute("create table if not exists kvints ( key text primary key, value integer )")
        self.execute("create table if not exists kvstrs ( key text primary key, value text )")
    def execute(self, sql, args=[]):
        cursor = self.db.cursor()

        print("exec local query: %s, %s" % (sql, args))
        result = cursor.execute(sql, args)
        print("lastrow = %d, rowcount=%d" % (cursor.lastrowid, cursor.rowcount))
        return result

    def query(self, sql, args=[]):
        result = None
        for row in self.execute(sql, args):
            for _ in row:
                result = _

        return result

    def getint(self, key):
        return self.query("select value from kvints where key=?", [key])
    def setint(self, key, value):
        self.execute("update kvints set value=? where key=?", [value, key])
        self.db.commit()
    def makeint(self, key, value):
        self.execute("insert into kvints (key, value) values (?, ?)", [key, value])
        self.db.commit()
    def getstr(self, key):
        return self.query("select value from kvstrs where key=?", [key])
    def setstr(self, key, value):
        self.execute("update kvstrs set value=? where key=?", [value, key])
        self.db.commit()
    def makestr(self, key, value):
        self.execute("insert stro kvstrs (key, value) values (?, ?)", [key, value])
        self.db.commit()

    @property
    def lastmessage(self):
        print("get val")
        val = self.getint("lastmessage")
        if val is None:
            self.makeint("lastmessage", 0)
            return 0
        return val

    @lastmessage.setter
    def lastmessage(self, val):
        print("set val")
        self.setint("lastmessage", val)

def extfrommime(tp):
    if tp == 'image/jpeg':
        return '.jpg'
    if tp == 'video/mp4':
        return '.mp4'
    if tp == 'audio/ogg':
        return '.ogg'
    if tp == 'audio/aac':
        return '.aac'
    if tp == 'application/msword':
        return '.doc'
    if tp == 'application/pdf':
        return '.pdf'

class Downloader:
    """ the downloader app """
    def __init__(self, dbdir, outdir):
        self.appstate = ApplicationState("downloader.db")
        self.downloader = WhatsappMediaDownloader()
        self.database = WhatsappDatabase(dbdir)
        self.adbfiles = WhatsappFiles()

        self.outdir = outdir

        self.byid = self.loadcontacts()

    # build contact table
    def loadcontacts(self):
        byid = {}
        for ct in self.database.getcontacts():
            byid[ct.jid] = ct.name()
        print("found %d contacts" % len(byid))

        return byid

    def findname(self, jid):
        if jid in self.byid:
            return self.byid[jid]
        return jid

    def createsavedir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    def makepath(self, msg):
        t = datetime.datetime.fromtimestamp(msg.timestamp/1000)
        name = self.findname(msg.key_remote_jid)

        self.createsavedir(os.path.join(self.outdir, name))
        basepath = os.path.join(self.outdir, name, t.strftime("%Y%m%d-%H%M%S"))

        def stripname(name):
            for x in ". ", "<", ">", "/":
                i = name.find(x)
                if i>=0:
                    name = name[:i]
            return name

        if msg.media_name or msg.media_caption:
            basepath, ext = os.path.splitext(basepath + " " + stripname(msg.media_name or msg.media_caption))
        elif msg.media_mime_type:
            ext = extfrommime(msg.media_mime_type)
        else:
            print(msg)
            ext = ".dat"

        for i in range(10000):
            name = "%s-%04d%s" % (basepath, i, ext)
            if sys.version_info < (3, 0):
                # has race condition
                if not os.path.exists(name):
                    with open(name, "w"):
                        return name
            else:
                # no race condition
                try:
                    with open(name, "x"):
                        return name
                except FileExistsError:
                    pass


    def processmessage(self, msg):
        print("processing", msg._id)

        savepath = self.makepath(msg)
        def savedata(data):
            with open(savepath, "wb") as fh:
                fh.write(data)

        if msg.thumb_image and hasattr(msg.thumb_image, "file") and hasattr(msg.thumb_image.file, "path"):
            print(byid.get(msg.sender, msg.sender), msg.data or msg.media_caption, msg.thumb_image.file.path, sep="\t")
            self.adbfiles.get(msg.thumb_image.file.path, savepath)
        elif msg.media_url and msg.media_url != 'call_screen_presented':
            self.downloader.get(msg, savedata)


    def processnewmessages(self):
        for msg in self.database.getmessagesafter(self.appstate.lastmessage):
            self.processmessage(msg)
            self.appstate.lastmessage = msg._id
        print("done")

def main():
    if len(sys.argv)!=2:
        print("Usage: grabmsgs <dbdir>")
        return
    d = Downloader(sys.argv[1], "saved")
    d.processnewmessages()

    reactor.run()

if __name__ == '__main__':
    main()
