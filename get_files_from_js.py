#!/usr/bin/python3
import re
import urllib.request
import urllib.parse
import http.cookiejar
import json
from datetime import datetime, timezone, timedelta
import binascii
import zlib

"""
Extract referenced files, version numbers and timestamps from
the whatsapp javascript.


serviceworker.js
    t.default = {
        version: "2.2218.8",
        hashedResources: [...],
        unhashedResources: [...],
        l10n: {
            locales: {
                ...
            },
            styles: {}
        },
        releaseDate: 1653347266148
    }

bootstrap_main, bootstrap_qr
    new Worker(\S+ + "...")
    {dir:"LTR",children:"2.2232.7"}
    appVersion:"2.2222.8"

app.XXX.js
    VERSION_BASE:"2.2027.10"
      ... also has ...}[e]||e)+"."+(...

localtes/*.js
     fetch("/emoji_suggestions/\S+.json?v=2.2206.4")

lazy_loaded_low_priority_components
    {dir:"LTR",children:"2.2232.7"}

early_error_handling.XXX.js
    ((0,i.parseUASimple)(n,"2.2218.7"))
    const p="2.2203.3",

index.HEX.worker.js
    appVersion:"2.2206.4"

runtime
    t.u = e => (({
        NUM: "<path>",
        ...
    } [e] || e) + "." + {
        NUM: "<HEXNUM>",
        ...
    } [e] + ".js"),
    t.miniCssF = e => ({
        NUM: "<path>",
        ...
    } [e] + "." + {
        NUM: "<HEXNUM>",
        ...
    } [e] + ".css"),
"""

def get(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def decode_svc(js):
    """
    get info from serviceworker.js file
    """
    class SvcInfo:
        def __init__(self):
            self.version = None
            self.releaseDate = None
            self.hashedResources = []
            self.unhashedResources = []
            self.locales = []
            self.styles = []

    def splitresources(r):
        return re.split(r'",\s*"', r[1:-1], flags=re.DOTALL)
    def splitlocales(r):
        """
        "\S+":"localtes/...",
        """
        if not r:
            return []
        return re.findall(r'"\S*?":\s*"(\S*?)"', r)

    info = SvcInfo()
    js = re.sub(r'\n\s+', '', js)
    if m := re.search(r'''
                      \{
                      \s*"?version"?:\s*"(\S*?)",
                      \s*"?hashedResources"?:\s*\[(.*?)\],
                      \s*"?unhashedResources"?:\s*\[(.*?)\]
                        (?:,
                          \s*"?l10n"?:\s*\{\s*"?locales"?:\s*\{(.*?)\},\s*"?styles"?:\s*\{(.*?)\}\s*\},
                          \s*"?releaseDate"?:\s*(\d+))?
                      \s*\}''', js, re.DOTALL|re.VERBOSE):
        info.version = m[1]
        info.hashedResources = splitresources(m[2])
        info.unhashedResources = splitresources(m[3])
        info.locales = splitlocales(m[4])
        info.styles = splitlocales(m[5])
        info.releaseDate = datetime.fromtimestamp(int(m[6])/1000) if m[6] else None

        return info

def getworkers(jstext):
    """
    get workers info from bootstrap_qr and bootstrap_main

    TODO: appVersion
    """
    return re.findall(r'new Worker\(\s*\S+?\s*\+\s*"(\S+?)\"\s*\)', jstext)

def getruntime(jstext):
    """
    extract resources from runtime.*.js
    """
    for m in re.finditer(r'e=>\(\(?(\{\S+?\})\[e\](?:\|\|e\))?\+"\."\+(\{\S+?\})\[e\]\+"(\.\w+)"\)', jstext):
        part1 = eval(m[1])
        part2 = eval(m[2])
        ext = m[3]
        for k in set(part1.keys()) | set(part2.keys()):
            yield part1.get(k, str(k)) + "." + part2.get(k, "?") + ext

def getversion(jstext):
    if m := re.search(r'appVersion"?:\s*"(\d\.\d\S*?)"', jstext):
        return m[1]
    if m := re.search(r'"LTR",\s*"?children"?:\s*"(\d\.\d\S*?)"', jstext):
        return m[1]
    if m := re.search(r'VERSION_BASE"?:\s*"(\d\.\d\S*?)"', jstext):
        return m[1]
    if m := re.search(r'emoji_suggestions/\S+?\.json?v=(\d\.\d\S*?)"', jstext):
        return m[1]
    if m := re.search(r'parseUASimple\(\s*\w+,\s*"(\d\.\d\S*?)"', jstext):
        return m[1]
    if m := re.search(r'\bversion"?:\s*"(\d\.\d\S*?)"', jstext):
        return m[1]

def decompress(data):
    d = zlib.decompressobj(wbits=47)
    res = d.decompress(data)
    if not d.eof:
        print("WARN: incomplete gzipped data")
    return res

def is_unsupported_page(txt):
    return txt.startswith('<!DOCTYPE html>') and txt.find("URL=/unsupportedbrowser") > 0

def is_archive_wrapper_page(txt):
    return txt.startswith('<!DOCTYPE html>') and txt.find("<title>Wayback Machine</title>") > 0 and txt.find('<iframe id="playback" src="https://web.archive.org') > 0

def main():
    import argparse
    parser = argparse.ArgumentParser(description='get whatsapp source')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('FILES', nargs='*')
    args = parser.parse_args()


    if not args.FILES:
        svctext = get("https://web.whatsapp.com/serviceworker.js")

        svc = decode_svc(svctext)
        print(svc.version, svc.releaseDate)
        print(svc.hashedResources)
        print(svc.unhashedResources)
        print(svc.locales)
        print(svc.styles)
    else:
        for fn in args.FILES:
            try:
                if fn.endswith('.http'):
                    continue
                with open(fn, "rb") as fh:
                    data = fh.read()
                if data.startswith(b"\x1f\x8b"):
                    data = decompress(data)
                txt = data.decode('utf-8', errors='ignore')

                if is_unsupported_page(txt):
                    continue
                if is_archive_wrapper_page(txt):
                    continue

                ver = getversion(txt)
                if fn.find('bootstrap')>=0:
                    print("--- [%s] %s" % (ver, fn))
                    files = getworkers(txt)
                    if files:
                        print("\t" + "\n\t".join(files))
                    else:
                        print("??? no files in bootstrap")
                elif fn.find('serviceworker')>=0 or fn.find('stuff.js')>=0:
                    print("--- [%s] %s" % (ver, fn))
                    svc = decode_svc(txt)
                    if svc:
                        print("----->", svc.version, svc.releaseDate)
                        print("\t" + "\n\t".join(svc.hashedResources))
                        print("\t" + "\n\t".join(svc.unhashedResources))
                        print("\t" + "\n\t".join(svc.locales))
                        print("\t" + "\n\t".join(svc.styles))
                    else:
                        print("??? can't decode serviceworker")
                elif fn.find('runtime')>=0:
                    print("--- [%s] %s" % (ver, fn))
                    files = getruntime(txt)
                    if files:
                        print("\t" + "\n\t".join(files))
                    else:
                        print("??? no files in runtime")
                elif ver:
                    print("--- [%s] %s" % (ver, fn))
            except Exception as e:
                print("ERROR", e, fn)
                if args.debug:
                    raise

if __name__ == '__main__':
    main()
