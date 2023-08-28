# downloads all assets from web.whatsapp.com mentioned in assets-manifest files, and not yet present.
cd wacode
for f in web.whatsapp.com/assets-manifest-*.json ; do
    jq < "$f" | perl -nle 'if (/"(\S+)":/) { print($1); }'
done | grep -v "^inline-" | while read f; do
    if [[ ! -e "web.whatsapp.com/$f" ]]; then
        get -m HEAD "https://web.whatsapp.com/$f" | grep -q "^HTTP/1.1 200"  && echo  "https://web.whatsapp.com/$f"
    fi
done | x0  wget -U "Mozilla/5.0" -x -nc
