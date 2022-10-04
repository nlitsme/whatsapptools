#!/usr/bin/python3
import re
import zlib

"""
Extract the protobuf definitions from web.whatsapp.com javascript.

bootstrap_qr
    t.parse<name>MessageProto   

WAWebWorker
    (?:const|var) <var> = {};
    t.$<MessageName>Spec = <var>
     .internalSpec = {
             key: [id, flags, msgvar],
             ...
         };

web.whatsapp.com/index.aaf0305ab54c5ecb7a8e.worker.js
web.whatsapp.com/bootstrap_qr.97ab9fcca259a954924c.js



-- enum definition
const a = r(\d+)({ ( keyword: value, )+ }); t.enumname = a;


-- wrapper

    36142: (e, t, r) => {
        "use strict";
        Object.defineProperty(t, "__esModule", {
            value: !0
        }), (t.thename = )+void 0;
        var n = r(9599);               <--- reference other specs
        (
        const p = r(2134)({        <-- sometimes: n('qweqwe')
           ( name: value, )+
        });
        t.constname = p;
        |

        var c = Object.freeze({        <--- todo
            ERROR: 0,
            PENDING: 1,
            SERVER_ACK: 2,
            DELIVERY_ACK: 3,
            READ: 4,
            PLAYED: 5
        });
        t.WEB_MESSAGE_INFO_STATUS = c;

        )+
        (
        const h = {}
        t.MessageSpec = h;
        )+
        (
        t.internalDefaults = { key: c.VALNAME ... },   <-- todo
        |
        t.internalSpec = {  key: [...], ... },
        )+
    }

    -- sometimes the var is declared like this:
    #       const l = (0, u.default)({}, null);
    #       t.SyncdValueSpec = l;

-- sometimes vars are declared like this:
            var s = a(99454),
                i = {};
            t.FingerprintDataSpec = i;
            var r = {};

-- yet another enum definition:
        var v = function(e) {
            function t() {
                return (0, r.default)(this, t), (0, i.default)(this, (0, o.default)(t).apply(this, arguments))
            }
            return (0, c.default)(t, e), t
        }(d.default);
        t.PaymentInfo = v, v.CURRENCY = _, v.STATUS = g, v.TXNSTATUS = p;

      , d = function(e) {
            function t() {
                return (0, r.default)(this, t), (0, i.default)(this, (0, o.default)(t).apply(this, arguments))
            }
            return (0, c.default)(t, e), t
        }(u.default);
        t.MessageKey = d,

"""


class AssignVar:
    def __init__(self, txt, a, b):
        self.range = (a, b)
        self.txt = txt

        m = re.match(r'''
                (?:const\s|var\s|,\s*) ([a-zA-Z_0-9$]+) \s*=\s* (?:
                       \{\}
                       |
                       \(\d+,\s*\w.default\)\(\{\},\s*null\)
                   );\s*
                   ([a-zA-Z_0-9$]+)\.(\S+?)\s*=\s*\1
            ''', txt, flags=re.VERBOSE)
        if m:
            self.varname = m[1]
            self.rootvar = m[2]
            self.msgname = m[3]    #  includes 'Spec' suffix
            return
        raise Exception("can't parse var-assign")

    def __repr__(self): return "VAR %s\t%s\t%s" % (self.rootvar, self.varname, self.msgname)

def decodeflags(txt):
    """
    FLAGS.PACKED
    FLAGS.REPEATED
    FLAGS.REQUIRED
    TYPES.BOOL
    TYPES.BYTES
    TYPES.DOUBLE
    TYPES.ENUM  - has 3rd param
    TYPES.FIXED32
    TYPES.FIXED64
    TYPES.FLOAT
    TYPES.INT32
    TYPES.INT64
    TYPES.MESSAGE  - has 3rd param
    TYPES.SFIXED32
    TYPES.SFIXED64
    TYPES.STRING
    TYPES.UINT32
    TYPES.UINT64
    """

    return set(re.sub(r'^\w+\.', '', _) for _ in re.split(r'\s*\|\s*', txt))

class MessageProperty:
    def __init__(self, txt):
        self.txt = txt
        elems = re.split(r',\s*', txt)
        self.id = int(elems[0])
        self.flags = sorted(decodeflags(elems[1]))
        if len(elems) == 3:
            self.argument = elems[2]
        else:
            self.argument = None

        self.resolved = None
        
    def __repr__(self): return "%d:%s:%s" % (self.id, self.flags, self.resolved or self.argument)

class MessageSpec:
    def __init__(self, txt, a, b):
        self.range = (a, b)
        self.txt = txt
        m = re.match(r'''
                \b([a-zA-Z_0-9$]+)\.internalSpec \s*=\s* \{ ( (?: [^\[\]{}]+ \[ [^\[\]{}]+ \])+ ) ( [^\[\]{}]+ \{ [^\[\]{}]+ \[ [^\[\]{}]+ \]\})? \}
            ''', txt, flags=re.VERBOSE)
        if m:
            self.varname = m[1]
            propstext = m[2]
            self.oneofs = m[3]   # todo - decode this.
            self.props = { mm[1] : MessageProperty(mm[2]) for mm in re.finditer(r'''
                \b(\w+):\s*(?: 
                   \[(.*?)\]
                   |
                   \{\s*(\w+):\s*\[(.*?)\]\s*\}
                   )
            ''', propstext, flags=re.VERBOSE) if mm[2] }

            self.resolved = None

            return
        raise Exception("msgspec not matched")

    def __repr__(self): return "STRU: %s\t%s" % (self.resolved or self.varname, self.props)

class EnumSpec:
    def __init__(self, txt, a, b):
        self.range = (a, b)
        self.txt = txt
        m = re.match(r'''
                (?:const\s|var\s|,\s*) ([a-zA-Z_0-9$]+) \s*=\s* 
                     (?: \w\((?: \d+|"\w+" )\)
                        |
                        Object.freeze
                     )
                     \(\{([^{}]+)\}\);
                     \s*([a-zA-Z_0-9$]+)\.(\S+?) \s*=\s* \1
            ''', txt, flags=re.VERBOSE)
        if m:
            self.varname = m[1]
            self.consts = m[2]
            self.rootname = m[3]
            self.typename = m[4]
            return
        m = re.match(r'''
                (?:const\s|var\s|,\s*) ([a-zA-Z_0-9$]+) \s*=\s* function\(\w\)\s*\{
                  \s*function\s*\w\(\)\s*\{\s*return\s*\(0,\s*\w\.default\)\(this,\s*\w\),\s*\(0,\s*\w\.default\)\(this,\s*\(0,\s*\w\.default\)\(\w\)\.apply\(this,\s*arguments\)\)\s*\}\s*return\s*\(0,\s*\w\.default\)\(\w,\s*\w\),\s*\w
                \s*\}\(\w\.default\);
                \s*\w\.([a-zA-Z_0-9$]+) \s*=\s* \1 ((?: ,\s*\1\.\w+ \s*=\s* \w+)+)
            ''', txt, flags=re.VERBOSE)
        if m:
            self.varname = m[1]
            self.consts = m[3]
            self.rootname = "?"
            self.typename = m[2]
            return
        raise Exception("enumspec not matched")
    def __repr__(self): return "ENUM: %s\t%s\t%s\t%s" % (self.varname, self.rootname, self.typename, self.consts)


class Separator:
    def __init__(self, txt, a, b):
        self.range = (a, b)
        self.txt = txt
    def __repr__(self): return "Separator"

"""
todo:
       (const|var|,)?  name = ( {}  |  (0,x.default)({}, null)  )   [;,]

       name.name = name   [;,]

       name.internalSpec = { key:[...], ... }     -- msg

       name = n( num | "str" ) | Object.freeze({  key:val, ... })  -- enum

       internalDefaults
"""
patterns = [
    (AssignVar, re.compile(r'''
                (?:const\s|var\s|,\s*)  ([a-zA-Z_0-9$]+)  \s*=\s*  (?:
                    \{\}                                     #  var = {}
                    |
                    \(\d+,\s*\w.default\)\(\{\},\s*null\)    #  var = (0,x.default)({}, null)
                  );
                \s*
                [a-zA-Z_0-9$]+\.\S+?\s*=\s*\1(?=[,;])        # x.name = var
            ''', flags=re.VERBOSE)),
    (MessageSpec, re.compile(r'''
                \b[a-zA-Z_0-9$]+\.internalSpec \s*=\s* 
                    \{
                    (?: [^\[\]{}]+ \[ [^\[\]{}]+ \])+                     # key: "[" id, flags [, var] "]"
                    (?: [^\[\]{}]+ \{ [^\[\]{}]+ \[ [^\[\]{}]+ \]\} )?    # optional __oneofs__
                    \}
            ''', flags=re.VERBOSE)),
    (Separator, re.compile(r'''
                Object.defineProperty\(\w+,\s*"__esModule"
            ''', flags=re.VERBOSE)),
    (EnumSpec, re.compile(r'''
                (?:const\s|var\s|,\s*) ([a-zA-Z_0-9$]+) \s*=\s* 
                    (?:  \w\((?:\d+|"\w+")\) | Object.freeze)  \( \{[^{}]+\} \);   # ({ ..values.. })
                    \s*
                    [a-zA-Z_0-9$]+\.\S+? \s*=\s* \1(?=[,;])
            ''', flags=re.VERBOSE)),
    (EnumSpec, re.compile(r'''
                (?:const\s|var\s|,\s*) ([a-zA-Z_0-9$]+) \s*=\s* function\(\w\)\s*\{
                      \s*function\s*\w\(\)\s*\{
                         \s*return\s*\(0,\s*\w\.default\)\(this,\s*\w\),\s*\(0,\s*\w\.default\)\(this,\s*\(0,\s*\w\.default\)\(\w\)\.apply\(this,\s*arguments\)\)
                       \s*\}
                       \s*return\s*\(0,\s*\w\.default\)\(\w,\s*\w\), \s*\w
                    \s*\}\(\w\.default\);
                    \s*
                    \w\.[a-zA-Z_0-9$]+ \s*=\s* \1 (?: ,\s*\1\.\w+ \s*=\s* \w+ )+;
            ''', flags=re.VERBOSE)),
    ]
def extract_proto(txt):
    l = []
    for cls, r in patterns:
        for m in r.finditer(txt):
            l.append(cls(m[0], m.start(), m.end()))
    l = sorted(l, key=lambda x:x.range)

    scope = dict()
    for item in l:
        if isinstance(item, AssignVar):
            scope[item.varname] = item
        elif isinstance(item, EnumSpec):
            scope[item.varname] = item
        elif isinstance(item, Separator):
            scope = dict()
        elif isinstance(item, MessageSpec):
            for p in item.props.values():
                if p.argument:
                    v = scope.get(p.argument)
                    if v:
                        p.resolved = v.typename if isinstance(v, EnumSpec) else v.msgname
            v = scope.get(item.varname)
            if v:  # v should be a AssignVar
                if not isinstance(v, AssignVar):
                    print("PROBLEM: item %s found ref %s" % (item, v))
                else:
                    item.resolved = v.msgname
    print("\n".join(repr(_) for _ in l))

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

            print("==>", fn, "<==")
            extract_proto(txt)

        except Exception as e:
            print("ERROR", e, fn)
            if args.debug:
                raise

if __name__ == '__main__':
    main()
