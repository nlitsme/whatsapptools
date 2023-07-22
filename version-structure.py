from collections import defaultdict
import re
import os
import json

# analyze all known 2.x.y versions for web.whatsapp,
# print them in x/y grid to possibly spot a pattern to the way they are assigned.

def main():
    versions = set()
    for ent in os.scandir("web.whatsapp.com"):
        if ent.name.startswith("app.") or ent.name.startswith("bootstrap_qr."):
            with open(os.path.join("web.whatsapp.com", ent.name), "r") as fh:
                jstext = fh.read()
            v = ""
            if m := re.search(r'VERSION_BASE:"(\d\.\d+\.\d+)"', jstext):
                v = m[1]
            elif m := re.search(r'appVersion:"(\d\.\d+\.\d+)"', jstext):
                v = m[1]

            if m := re.match(r'2\.(\d+)\.(\d+)', v):
                versions.add((int(m[1]), int(m[2])))

        if ent.name.startswith("binary-transparency"):
            js = json.load(open(os.path.join("web.whatsapp.com", ent.name)))
            v = js.get("version")
            if m := re.match(r'2\.(\d+)\.(\d+)', v):
                versions.add((int(m[1]), int(m[2])))

    d = defaultdict(set)
    for a, b in versions:
        d[a].add(b)

    maxsub = max(subversion for minor, subversion in versions)
    prev = 0
    for k, v in sorted(d.items()):
        if int(k)-prev > 10:
            # add empty line when a lot of minor versions are skipped.
            print()
        l = "".join("%3d" % i if i in v else "  -" for i in range(maxsub+1))
        print("%s: %s" % (k, l))
        prev = int(k)

if __name__=='__main__':
    main()
