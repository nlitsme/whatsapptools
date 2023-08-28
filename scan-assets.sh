# discovering manifest files by enumerating all version nrs, 
cd wacode
for ((a=2300 ; a<2400 ; a++)); do
    for ((b=0 ; b<25 ; b++)); do
        f="web.whatsapp.com/assets-manifest-2.$a.$b.json"
        if [[ ! -e "$f" ]]; then
            get -H "User-Agent: Mozilla/5.0" -m HEAD "https://$f" | grep -q "^HTTP/1.1 200"  && wget -U "Mozilla/5.0" -x -nc "https://$f"
        fi
        f="web.whatsapp.com/binary-transparency-manifest-2.$a.$b.json"
        if [[ ! -e "$f" ]]; then
            get -H "User-Agent: Mozilla/5.0" -m HEAD "https://$f" | grep -q "^HTTP/1.1 200"  && wget -U "Mozilla/5.0" -x -nc "https://$f"
        fi

    done
done
exit 0
