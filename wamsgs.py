from __future__ import print_function, division
"""
Script which checks if there are any new images on the attached phone,
which are not yet in any of the sdcard storage directories. these images
are then copied to the sdcard storage.
Then whatsapp is checked for new images as well. new images are downloaded
and decrypted and saved in the sdcard storage.
"""
import subprocess
import datetime
import re
import javaobj  # javaobj-py3
import os.path
import sys
from binascii import a2b_hex
from Crypto.Cipher import AES

import requests

import os
if sys.version_info[0] == 2:
    import scandir
    os.scandir = scandir.scandir

def adb(cmd, *args, stdin=None):
    pipe = subprocess.Popen(["adb", cmd, *args], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if stdin:
        out, err = pipe.communicate(input=stdin.encode('utf-8'))
    else:
        out, err = pipe.communicate()
    e = pipe.wait(5)

    return out

def adbshell(cmd):
    return adb("shell", stdin=cmd)

def j2a(val):
    def tounsignedbyte(x):
        return x+256 if x<0 else x
    return "".join("%02x" % tounsignedbyte(_) for _ in val)
def j2b(val):
    def tounsignedbyte(x):
        return x+256 if x<0 else x
    return bytes(tounsignedbyte(_) for _ in val)


def dumpjavaobj(pobj, level=0):
    for attr in dir(pobj):
        if attr in ('classdesc', 'get_class', 'annotations'):
            continue
        if attr.startswith('__') and attr.endswith('__'):
            continue
        val = getattr(pobj, attr)
        if isinstance(val, javaobj.JavaByteArray):
            print('    ' * level + attr, type(val), j2a(val), sep="\t")
        else:
            print('    ' * level + attr, type(val), val, sep="\t")
        if isinstance(val, javaobj.JavaObject) and not isinstance(val, javaobj.JavaByteArray):
             dumpjavaobj(val, level+1)

def noneint(x):
    return int(x) if x else None
def nonefloat(x):
    return float(x) if x else None
def nonestr(x):
    return x.decode('utf-8', 'ignore') if x else None
def nonestamp(x):
    return datetime.datetime.fromtimestamp(int(x)/1000) if x else None
def decodeobj(x):
    if x == b'NULL':
        return
    x = x.strip(b"X'\"")
    if not x:
        return
    return javaobj.loads(a2b_hex(x))

class WhatsappMessage:
    def __init__(self, row):
        self.media_url = nonestr(row[2])
        self._id = noneint(row[0])
        self.key_remote_jid = nonestr(row[1])
        self.key_from_me = noneint(row[2])
        self.key_id = nonestr(row[3])
        self.status = noneint(row[4])
        self.needs_push = noneint(row[5])
        self.data = nonestr(row[6])
        self.timestamp = nonestamp(row[7])
        self.media_url = nonestr(row[8])
        self.media_mime_type = nonestr(row[9])
        self.media_wa_type = noneint(row[10])
        self.media_size = noneint(row[11])
        self.media_name = nonestr(row[12])
        self.media_caption = nonestr(row[13])
        self.media_hash = nonestr(row[14])
        self.media_duration = noneint(row[15])
        self.origin = noneint(row[16])
        self.latitude = nonefloat(row[17])
        self.longitude = nonefloat(row[18])
        self.thumb_image = decodeobj(row[19])
        self.remote_resource = nonestr(row[20])
        self.received_timestamp = noneint(row[21])
        self.send_timestamp = noneint(row[22])
        self.receipt_server_timestamp = noneint(row[23])
        self.receipt_device_timestamp = noneint(row[24])
        self.read_device_timestamp = noneint(row[25])
        self.played_device_timestamp = noneint(row[26])
        self.raw_data = nonestr(row[27])
        self.recipient_count = noneint(row[28])
        self.participant_hash = nonestr(row[29])
        self.starred = noneint(row[30])
        self.quoted_row_id = noneint(row[31])
        self.mentioned_jids = nonestr(row[32])
        self.multicast_id = nonestr(row[33])
        self.edit_version = noneint(row[34])
        self.media_enc_hash = nonestr(row[35])
        self.payment_transaction_id = row[36]
        self.forwarded = noneint(row[37])
        self.preview_type = noneint(row[38])
        self.send_count = noneint(row[39])
    def messagetype(self):
        mt = [
            "message",                   #  0
            "image",                     #  1
            "audio",                     #  2
            "video",                     #  3
            "vcard",                     #  4
            "location",                  #  5
            None,                        #  6
            "system",                    #  7
            None,                        #  8
            "document",                  #  9
            "voice call",                # 10
            "waiting for message",       # 11
            None,                        # 12
            "animated gif",              # 13
            None,                        # 14
            "deleted message",           # 15
            "live location",             # 16
            None,                        # 17
            None,                        # 18
            None,                        # 19
            "sticker",                   # 20
            None,                        # 21
            None,                        # 22
            "product",                   # 23
            "invite",                    # 24
            "most_recent_image",         # 25
            "most_recent_document",      # 26
            "hydrated text",             # 27
            "most_recent_video",         # 28
            "most_recent_gif",           # 29
            "most_recent_location",      # 30
            None,                        # 31
            None,                        # 32
            None,                        # 33
            "image34",                   # 34
        ]
        watype = self.media_wa_type
        if watype == 0:
            return self.specialtype()
        elif watype<0:
            return "unknown_wa_type(%d)" % watype
        elif watype>=len(mt):
            return "unknown_wa_type(%d)" % watype
        elif mt[watype] is None:
            return "unknown_wa_type(%d)" % watype
        elif self.media_mime_type:
            return mt[watype] + ":" + self.media_mime_type
        else:
            return mt[watype]

    def specialtype(self):
        mt = [
            "text",                                                #  0
            "group_subject_changed_by_name",                     #  1
            None,                                                #  2
            None,                                                #  3
            "list_recipient_added",                              #  4
            "group_participant_left_you",                        #  5
            "photo_removed_by_you",                              #  6
            "list_recipient_removed",                            #  7
            "cannot_send_to_group_not_member",                   #  8
            "you_created_list_unnamed",                          #  9
            "chat_changed_number_new",                           # 10
            "group_created_by_name",                             # 11
            "list_recipients_added",                             # 12
            None,                                                # 13
            "list_recipients_removed",                           # 14
            "group_participant_promoted_you",                    # 15
            "group_participant_demoted_you",                     # 16
            "group_ended_you",                                   # 17
            "identity_changed_name",                             # 18
            "broadcast_encryption_state_change",                 # 19
            "group_participant_joined_by_link_you",              # 20
            "invite_link_revoked",                               # 21
            "vlevel_transition_none_to_unknown",                 # 22
            "vlevel_transition_none_to_high",                    # 23
            "vlevel_transition_low_or_unknown_to_high",          # 24
            "vlevel_transition_high_to_low_or_unknown",          # 25
            "vlevel_transition_any_to_none",                     # 26
            "group_description_deleted_by_name",                 # 27
            "group_participant_changed_number_known_name",       # 28
            "group_restrict_enabled_sys_msg_you",                # 29
            "group_restrict_disabled_sys_msg_you",               # 30
            "group_announcement_enabled_sys_msg_you",            # 31
            "group_announcement_disabled_sys_msg_you",           # 32
            "failed_announcement_group_send_msg_not_admin",      # 33
            "vlevel_transition_none_to_low",                     # 34
            "vlevel_transition_unknown_to_low",                  # 35
            "vlevel_transition_low_to_unknown",                  # 36
            "payment",                                           # 37
            None,                                                # 38
            "payment pending",                                   # 39
            "payments_setup_account_reminder_msg_text",          # 40
            "payments_send_payment_reminder_msg_text",           # 41
            "payments_invite_system_message",                    # 42
            None,                                                # 43
            "payment failed",                                    # 44
            None,                                                # 45
            "vlevel_transition_none_to_low_and_unknown_v2",      # 46
            "vlevel_transition_none_to_high_v2",                 # 47
            "vlevel_transition_low_or_unknown_to_high_v2",       # 48
            "vlevel_transition_high_to_low_or_unknown_v2",       # 49
            "vlevel_transition_any_to_none_v2",                  # 50
            "group_participants_you_invited_names",              # 51
            "your_invite_used_by_user_plural",                   # 52
            "group_no_frequently_forwarded_enabled_sys_msg_you", # 53
            "group_no_frequently_forwarded_disabled_sys_msg_you",# 54
            "vlevel_transition_high_to_high_v2",                 # 55
        ]
        msgtype  = self.media_size
        if msgtype<0:
            return "unknown_msg_type(%d)" % msgtype
        elif msgtype>=len(mt):
            return "unknown_msg_type(%d)" % msgtype
        elif mt[msgtype] is None:
            return "unknown_msg_type(%d)" % msgtype
        else:
            return mt[msgtype]

    def __repr__(self):
        return "MESSAGE(%s):%s;%s;%s" % (self.messagetype(), self.key_id, self.key_remote_jid, self.data)

class WhatsappReceipt:
    def __init__(self, row):
        self._id = noneint(row[0])
        self.chat_id = row[1]
        self.msg_id = row[2]
        self.member_id = row[3]
        self.rcpt_time = nonestamp(row[4])
        self.read_time = nonestamp(row[5])
        self.play_time = nonestamp(row[6])
    def __repr__(self):
        return "RECEIPT:%s;%s;%s" % (self.chat_id, self.msg_id, self.member_id)

class WhatsappGroupMember:
    def __init__(self, row):
        self._id = noneint(row[0])
        self.chat_id = row[1]
        self.member_id = row[2]
        self.isadmin = int(row[3])
        self.pending = int(row[4])
        self.sentkey = int(row[5])
    def __repr__(self):
        return "MEMBER:%s;%s" % (self.chat_id, self.member_id)

class WhatsappContact:
    """
        wa:wa_contacts 
        jid                --   <phonenr>-<timestamp>@g.us   or   <phonenr>@s.whatsapp.net
        phone_type         0, 1, 2, 6, 12
        phone_label
        display_name
        number
        status_timestamp
        status
        given_name
        family_name
        wa_name
        sort_name
        nickname
        company
    """


    def __init__(self, row):
        self.jid = nonestr(row[0])
        self.phone_type = noneint(row[1])
        self.phone_label = nonestr(row[2])
        self.display_name = nonestr(row[3])
        self.number = nonestr(row[4])
        self.status_timestamp = nonestamp(row[5])
        self.status = nonestr(row[6])
        self.given_name = nonestr(row[7])
        self.family_name = nonestr(row[8])
        self.wa_name = nonestr(row[9])
        self.sort_name = nonestr(row[10])
        self.nickname = nonestr(row[11])
        self.company = nonestr(row[12])
    def __repr__(self):
        return "CONTACT:%s;%s" % (self.jid, self.display_name)


class WhatsappDatabase:
    """
    adb:/data/data/com.whatsapp/databases
    /Users/itsme/myprj/whatsapp/db20190730-184709
    """
    def __init__(self, dbroot):
        if dbroot.startswith("adb:"):
            self.useadb = True
            self.dbroot = dbroot[4:]
        else:
            self.useadb = False
            self.dbroot = dbroot

    def whatsappquery(self, sql, dbname = "msgstore.db"):
        if self.useadb:
            result = adbshell("su root sqlite3 -ascii %s/%s \"%s\"" % (self.dbroot, dbname, sql))
        else:
            result = subprocess.check_output(["sqlite3", "-ascii", "%s/%s" % (self.dbroot, dbname),  sql])

        return [ [ col for col in row.split(b"\x1f") ] for row in result.rstrip(b"\x1e").split(b"\x1e") ]

    def getwhatsappmessages(self):
        """
    _id:  unique row id
    key_remote_jid:
       <phonenumber>-<timestamp>@g.us
       <phonenumber>@s.whatsapp.net
       <phonenumber>-<32bytehash>@temp
    key_from_me: 0 or 1
    key_id:   (unique)
        20 nyble string
        32 nyble string
        8 .. 10 digit string
    status: 0, 4, 5, 6, 10, 12, 13
    needs_push: 0
    data: ... chat message content.
    timestamp: unix * 1000 + msec
    media_url
        path
        url
        mmg-fna.whatsapp.net ... enc
    media_mime_type:
        application/pdf
        application/vnd.ms-excel.sheet.macroenabled.12
        application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
        application/vnd.openxmlformats-officedocument.wordprocessingml.document
        audio/ogg; codecs=opus
        image/jpeg
        image/webp
        video/mp4
    media_wa_type: 0 1 2 3 4 5 9 10 11 13 15 16 20
    media_size: size, or  some status flag?
    media_name: ???
    media_caption:  text
    media_hash:
    media_duration:  number
    origin: 0 1 3
    latitude:  floatnumber
    longitude: floatnumber
    thumb_image:  binary data
    remote_resource: jid of remote user
    received_timestamp:  timestamp
    send_timestamp: -1
    receipt_server_timestamp: -1 or timestamp
    receipt_device_timestamp: -1 or timestamp
    read_device_timestamp: None, -1 or timestamp
    played_device_timestamp: -1 or 0
    raw_data: None
    recipient_count: number
    participant_hash:  6 byte base64 encoded string
    starred: 0, or None
    quoted_row_id:   index into messages_quotes table
    mentioned_jids: comma separated list of jid's
    multicast_id
    edit_version: 0, 7
    media_enc_hash: 32 byte b64 encoded hash
    payment_transaction_id: None
    forwarded: 0, 1, 2, 0x40, 0x41, 0x42
    preview_type: 0, 1
    send_count: 1, 2, 3, None


    --- media_mime_type, media_wa_type:
    sqlite3  db20190729-173244/msgstore.db "select media_wa_type , media_mime_type from messages"
    0|                         -- message
    1|                        
    1|image/jpeg               -- image
    2|audio/ogg; codecs=opus   -- ptt, audio
    3|video/mp4                -- video
    4|                         -- vcard
    5|                         -- location
    6  ?
    7|                         -- system
    8  ?
    9|application/pdf          -- document
    9|application/vnd.ms-excel.sheet.macroenabled.12
    9|application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
    9|application/vnd.openxmlformats-officedocument.wordprocessingml.document
    10|                        -- (missed) voice call
    11|                        -- 'waiting for message'
    12  ?
    13|video/mp4               -- animated gif
    14  ?
    15|                        -- message was deleted,   media_name = deleted msgid
    16|                        -- live location
    17  ?
    18  ?
    19                         --   ? crypto error ?
    20|image/webp              -- 'sticker'
    21  ?
    22  ?
    23                         -- product
    24                         -- invite
    25                         -- 📷 conversations_most_recent_image
    26                         -- 📄 conversations_most_recent_document
    27                         -- *  ?hydrated title text / highly structured message?
    28                         -- 🎥  conversations_most_recent_video
    29                         -- 👾  conversations_most_recent_gif
    30                         -- 📌  conversations_most_recent_location
    31
    32
    33  ?
    34                         -- image

    --- media_wa_type == 0: media_size is a flag:
      1  group_subject_changed_by_name                     
      2                                                    
      3                                                    
      4  list_recipient_added                              
      5  group_participant_left_you                        
      6  photo_removed_by_you                              
      7  list_recipient_removed                            
      8  cannot_send_to_group_not_member                   
      9  you_created_list_unnamed                          
     10  chat_changed_number_new                           
     11  group_created_by_name                             
     12  list_recipients_added                             
     13                                                    
     14  list_recipients_removed                           
     15  group_participant_promoted_you                    
     16  group_participant_demoted_you                     
     17  group_ended_you                                   
     18  identity_changed_name                             
     19  broadcast_encryption_state_change                 
     20  group_participant_joined_by_link_you              
     21  invite_link_revoked                               
     22  vlevel_transition_none_to_unknown                 
     23  vlevel_transition_none_to_high                    
     24  vlevel_transition_low_or_unknown_to_high          
     25  vlevel_transition_high_to_low_or_unknown          
     26  vlevel_transition_any_to_none                     
     27  group_description_deleted_by_name                 
     28  group_participant_changed_number_known_name       
     29  group_restrict_enabled_sys_msg_you                
     30  group_restrict_disabled_sys_msg_you               
     31  group_announcement_enabled_sys_msg_you            
     32  group_announcement_disabled_sys_msg_you           
     33  failed_announcement_group_send_msg_not_admin      
     34  vlevel_transition_none_to_low                     
     35  vlevel_transition_unknown_to_low                  
     36  vlevel_transition_low_to_unknown                  
     37  payment                                           
     38                                                    
     39  payment pending                                   
     40  payments_setup_account_reminder_msg_text          
     41  payments_send_payment_reminder_msg_text           
     42  payments_invite_system_message                    
     43                                                    
     44  payment failed                                    
     45                                                    
     46  vlevel_transition_none_to_low_and_unknown_v2      
     47  vlevel_transition_none_to_high_v2                 
     48  vlevel_transition_low_or_unknown_to_high_v2       
     49  vlevel_transition_high_to_low_or_unknown_v2       
     50  vlevel_transition_any_to_none_v2                  
     51  group_participants_you_invited_names              
     52  your_invite_used_by_user_plural                   
     53  group_no_frequently_forwarded_enabled_sys_msg_you 
     54  group_no_frequently_forwarded_disabled_sys_msg_you
     55  vlevel_transition_high_to_high_v2                 
    """
        msgs = self.whatsappquery("select _id, key_remote_jid, key_from_me, key_id, status, needs_push, data, timestamp, media_url, media_mime_type, media_wa_type, media_size, media_name, media_caption, media_hash, media_duration, origin, latitude, longitude, quote(thumb_image), remote_resource, received_timestamp, send_timestamp, receipt_server_timestamp, receipt_device_timestamp, read_device_timestamp, played_device_timestamp, raw_data, recipient_count, participant_hash, starred, quoted_row_id, mentioned_jids, multicast_id, edit_version, media_enc_hash, payment_transaction_id, forwarded, preview_type, send_count from messages")

        return [ WhatsappMessage(_) for _ in msgs ]

    def getwhatsappreceipts(self):
        rcpts = self.whatsappquery("select _id, key_remote_jid, key_id, remote_resource, receipt_device_timestamp, read_device_timestamp, played_device_timestamp from receipts")
        return [ WhatsappReceipt(_) for _ in rcpts ]

    def getwhatsappmembers(self):
        rcpts = self.whatsappquery("select _id, gjid, jid, admin, pending, sent_sender_key from group_participants")
        return [ WhatsappGroupMember(_) for _ in rcpts ]


    def getwhatsappcontacts(self):
        cts = self.whatsappquery("select jid, phone_type, phone_label, display_name, number, status_timestamp, status, given_name, family_name, wa_name, sort_name, nickname, company from wa_contacts", "wa.db")
        return [ WhatsappContact(_) for _ in cts ]


def DownloadMessage(msg):
    cipher = None
    if hasattr(msg.obj, 'cipherKey'):
        cipher = AES.new(j2b(msg.obj.cipherKey), mode=AES.MODE_CBC, IV=j2b(msg.obj.iv))

    r = requests.get(msg.media_url, allow_redirects=True)
    if cipher:
        return cipher.decrypt(r.content[:-10])
    return r.content


def check_whatsapp(wa):
    print(wa.getwhatsappmessages())
    print(wa.getwhatsappreceipts())
    print(wa.getwhatsappmembers())
    print(wa.getwhatsappcontacts())

#   def getfn(msg):
#       txt = repr(msg)
#       if txt.find("/")>=0:
#           return txt[txt.rfind("/")+1:]

#   wamsgs = getwhatsappmedia()

#   savedwa = getwamedia()

#   newmsgs = set(_ for _ in (getfn(_) for _ in wamsgs) if _) - set(savedwa)

#   wamsgs = [ _ for _ in wamsgs if getfn(_) in newmsgs ]
#   if not wamsgs:
#       print("No new whatsapp imgs")
#       return

#   maxdate = max(_.timestamp for _ in wamsgs)
#   t = datetime.datetime.fromtimestamp(maxdate/1000)
#   savedir = os.path.join(save_sdcard_name, t.strftime("wa%y%m%d-%H%M"))

#   try:
#       os.mkdir(savedir)
#       os.mkdir(os.path.join(savedir, "niet"))
#   except Exception as e:
#       print("mkdir: %s" % e)


#   for msg in wamsgs:
#       fn = msg.getfilename()
#       fn = fn[fn.rfind("/")+1:]
#       filename = os.path.join(savedir, fn)

#       data = DownloadMessage(msg)
#       print("saved wamsg to %s" % filename)
#       with open(filename, "wb") as fh:
#           fh.write(data)

def parse_datetime(txt, ymdhms):
    """
    convert a string  YYYY-mm-dd HH:MM:SS to a datetime object.
    Any number of consequetive elements starting from the right may be absent, 
    values are substituted from the ymdhms argument.
    """
    f = re.split(r'[-/: ]+', txt)
    if f == ['']:
        f = []

    f = [ int(_) for _ in f ] + ymdhms[len(f):]

    return datetime.datetime(*f)

def parse_date_range(txt):
    """
    Ranges can be specified in several ways:

    * using ".." as range separator
        date1 .. date2
        date1 ..
        .. date2
      The range is inclusive.
    * using " - " as separator:
        yy-mm - yy-mm   : 20yy-mm-01 .. 20yy-mm-31
        yy/mm-yy/mm
    * dates can be specified with varying resolution:
        yyyy      :  a range of yyyy-01-01 .. yyyy-12-31
        yyyy-mm   :  a range of yyyy-mm-01 .. yyyy-mm-31

    """
    if txt.find("..")>=0:
        start, end = txt.split("..", 1)
        return parse_datetime(start, (1, 1, 1, 0, 0, 0)), parse_datetime(end, (9999, 12, 31, 23, 59, 59))
    if txt.find(" - ")>=0:
        start, end = txt.split(" - ", 1)
        return parse_datetime(start, (1, 1, 1, 0, 0, 0)), parse_datetime(end, (9999, 12, 31, 23, 59, 59))
    if 0 <= txt.find("/") < txt.find("-")  or 0 <= txt.find("-") < txt.find("/"):
        start, end = txt.split("-", 1)
        return parse_datetime(start, (1, 1, 1, 0, 0, 0)), parse_datetime(end, (9999, 12, 31, 23, 59, 59))
    return parse_datetime(txt, (1, 1, 1, 0, 0, 0)), parse_datetime(txt, (9999, 12, 31, 23, 59, 59))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='List whatsapp messages.')
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument('--chat', '-c', type=str, help='Which chat to list messages from, matched by substring, on id and name.')
    parser.add_argument('--savedir', '-s', type=str, help='Save media to the specified directory.')
    parser.add_argument('--members', '-m', action='store_true', help='List group members in a chat.')
    parser.add_argument('--listchats', '-l', action='store_true', help='List chats / contacts.')
#    parser.add_argument('--messages', '-m', action='store_true', help='List messages in a chat.')
    parser.add_argument('--daterange', '-d', type=str, help='List messages in date range.')
    parser.add_argument('--dbroot', '-p', type=str, help='Path to the db.')
    args = parser.parse_args()

    wa = WhatsappDatabase(args.dbroot)

    check_whatsapp(wa)
    return 0
    if args.members:
        list_members(wa, args.chat)
    elif args.listchats:
        list_chats(wa)
    else:
        list_messages(wa, args.chat, parse_date_range(args.date))

    return 0

sys.exit(main())

