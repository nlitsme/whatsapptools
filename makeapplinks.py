from collections import defaultdict
import re
import os
import json

def shortenname(fn):
    if m := re.match(r'(\S+)\.[0-9a-f]{20}(?:[0-9a-f]{12})?((?:\.worker)?\.js)$', fn):
        return m[1]+m[2]
    if m := re.match(r'(libsignal-protocol)-[0-9a-f]{7}(\.min\.js)', fn):
        return m[1]+m[2]
    return fn

def mklink(src, dst):
    basedir = os.path.dirname(dst)
    os.makedirs(basedir, exist_ok=True)

    if os.path.lexists(dst) and os.path.islink(dst):
        # only replace existing symlinks, so we don't accidentally overwrite
        # real files.
        os.unlink(dst)
    os.symlink(src, dst)

def make_links_for_manifest(amname, xref):
    btname = amname.replace("assets-", "binary-transparency-")
    with open(btname, "r") as fh:
        bt = json.load(fh)
    with open(amname, "r") as fh:
        a = json.load(fh)
    version = bt.get("version")

    # leaves is used to check consistency, after creating all links, the set should be empty.
    leaves = set(bt.get('leaves'))

    src_path = "../../web.whatsapp.com/"

    dst_short_path = os.path.join("shortnames", version)
    os.makedirs(dst_short_path, exist_ok=True)

    dst_full_path = os.path.join("fullnames", bt.get("version"))
    os.makedirs(dst_full_path, exist_ok=True)

    # start by linking the manifest files.
    
    for fn in (btname, amname):
        fn = os.path.basename(fn)
        xref[fn].add(version)
        mklink(os.path.join(src_path, fn), os.path.join(dst_short_path, fn) )
        mklink(os.path.join(src_path, fn), os.path.join(dst_full_path, fn) )

    for filename, filehash in a.items():
        if "0x"+filehash in leaves:
            leaves.remove("0x"+filehash)
        else:
            print(f"Note: manifest {version} inconsistency: hash of {filename} from assets is not in binary-transparency")
        xref[filename].add(version)

        if filename.startswith("inline-js-"):
            # these are the hashes of the <script> tags inside the toplevel index.html
            continue

        shortname = shortenname(filename)
        prefix = "../" if filename.find('/') > 0 else ""
        mklink(os.path.join(prefix + src_path, filename), os.path.join(dst_short_path, shortname)) 
        mklink(os.path.join(prefix + src_path, filename), os.path.join(dst_full_path, filename)) 

    if leaves:
        print("unhandled hashes in {version}:", leaves)


def main():
    xref = defaultdict(set)

    for ent in os.scandir("web.whatsapp.com"):
        if ent.name.startswith("assets-manifest"):
            make_links_for_manifest(os.path.join("web.whatsapp.com", ent.name), xref)

    for ent in os.scandir("web.whatsapp.com"):
        if ent.name not in xref:
            if ent.name.startswith("check-update?version"):
                continue
            if ent.name.find("?cache-bust=") > 0:
                continue
            print("?", ent.name)

if __name__=='__main__':
    main()
