import urllib.request
import urllib.parse

import html.parser
import json
import os
import re
import datetime

"""
download all files for the current web.whatsapp.com site.
"""


def httpget(url):
    hdrs = {
            "User-Agent": "Mozilla/5.0 (Mac) Gecko/20100101 Firefox/76.0",
    }
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req) as response:
        text = response.read()
        return text.decode('utf-8')

def jsonget(url):
    return json.loads(httpget(url))

class IndexParser(html.parser.HTMLParser):
    def __init__(self, warnings):
        super().__init__()
        self.warnings = warnings
        self.stack = []

        self.files = []

    def handle_starttag(self, tag, attrs):
        if tag in ("meta", "input", "br", "link", "img", "hr"):
            return self.handle_startendtag(tag, attrs)
        self.stack.append(tag)

        d = dict(attrs)
        if tag == 'script':
            src = d.get('src')
            if src:
                self.files.append(src)

    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            for i, e in reversed(list(enumerate(self.stack))):
                if e==tag:
                    self.warnings.append("missing end tag for: %s closing %s" % ( self.stack[i+1:], self.stack[i:i+1]))
                    while len(self.stack)>i:
                        self.stack.pop()
                    return
            self.warnings.append("could not find start tag for: %s in %s" % (tag, self.stack))

    def handle_startendtag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'link':
            rel = d.get('rel')
            href = d.get('href')
            if href and rel in ('stylesheet', 'preload'):
                self.files.append(href.lstrip('/'))

    def handle_data(self, data):
        pass

def save(args, fn, html, unique=False):
    if type(html) == str:
        html = html.encode('utf-8')
    os.makedirs(os.path.join(args.basepath, "web.whatsapp.com", os.path.dirname(fn)), exist_ok=True)

    if unique:
        root, ext = os.path.splitext(fn)
        now = datetime.datetime.now()
        fn = f"{root}-{now:%Y%m%d-%H%M%S}{ext}"
    print("saving %d bytes to %s" % (len(html), fn))
    with open(os.path.join(args.basepath, "web.whatsapp.com", fn.lstrip('/')), "wb") as fh:
        fh.write(html)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='get updates to the web.whatsapp.')
    parser.add_argument('basepath', type=str, help="where to store the whatsapp files", default='.')
    args = parser.parse_args()


    indexhtml = httpget("https://web.whatsapp.com/")
    save(args, "index.html", indexhtml, unique=True)

    w = []
    parser = IndexParser(w)
    parser.feed(indexhtml)
    parser.close()
    if w:
        print("!", "\n! ".join(w))

    appversion = None
    runtimejs = None
    vendorbootstrapqrjs = None
    bootstrapqrjs = None
    for f in parser.files:
        content = httpget("https://web.whatsapp.com/" + f)
        save(args, f, content)
        if m := re.match(r'binary-transparency-manifest-(\S+)\.json', f):
            appversion = m[1]
        elif m := re.match(r'runtime-[0-9a-f]{20}\.js', f):
            runtimejs = content
        elif m := re.match(r'vendor1~bootstrap_qr\.[0-9a-f]{20}\.js', f):
            vendorbootstrapqrjs = content
        elif m := re.match(r'(?:bootstrap_qr|app)\.[0-9a-f]{20}\.js', f):
            bootstrapqrjs = content
    svcworkerjs = httpget("https://web.whatsapp.com/serviceworker.js")
    save(args, "serviceworker.js", svcworkerjs, unique=True)
    # -> version: "...", hashedResources: [...], unhashedResources: [...], l10n: { locales: { ... } }, releaseDate: \d+
    assetsjson = jsonget(f"https://web.whatsapp.com/assets-manifest-{appversion}.json")
    save(args, f"assets-manifest-{appversion}.json", json.dumps(assetsjson))
    for k, v in assetsjson.items():
        content = httpget("https://web.whatsapp.com/" + k)
        save(args, k, content)

    # runtime.js
    # e => (({ \d+:"\S+", ... }[e] || e) + "." + { \d+:"[0-9a-f]{20}", ... }[e] + "\.js")
    # e => ({ \d+:"\S+", ...  } [e] + "." + { \d+:"[0-9a-f]{20}", ...  } [e] + ".css")

    # bootstrapqr  new Worker(\w.\w + "...js")

    #https://web.whatsapp.com/status.json

    for p in ("darwin-store", "win32-store", "darwin", "win32", "web", "win32-beta", "darwin-beta"):
        j = jsonget(f"https://web.whatsapp.com/check-update?version=1.0&platform={p}")
        save(args, f"check-update?version=1.0&platform={p}", json.dumps(j))

    print()
    print("now run bash scan-assets.sh")
    print("then run bash dn-assets.sh")

if __name__ == '__main__':
    main()
