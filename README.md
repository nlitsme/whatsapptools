whatsapp tools
==============

This repository contains a collection of scripts i use to manage whatsapp chats from the commandline.

Most of these tools require root access to your android device.


decrypt12.py
============

Shows how to manually decrypt whatsapp backups


grabmsgs.py
===========

Downloads and decrypts new media files in all of your whatsapp chats.


wamsgs.py
=========

lists all messages in a whatsapp chat.

This tool is not really finished yet.



decodemsg.py
============

Decode the hex representation of a whatsapp protocol message.


get\_files\_from\_js.py
====================

Examines javascript files and extracts version information and file lists from them.

get\_proto\_from\_js.py
====================

Extracts protocol definitions from javascript files.


get\_web\_whatsapp.py
====================

Download most recent web.whatsapp.com files.

scan-assets.sh and dn-assets.sh
==============

Scripts used to populate the web.whatsapp.com directory in the wacode repository.

version-structure.py
====================

print out a diagram showing how whatsapp version numbers are organised.

makeapplinks.py
===============

Used to create the symlinks in the wacode repository.


waproxy.py
============

 * `domain\_srv.crt` `domain\_srv.key` are needed for the proxy.

To use: 
  * populate a directory with patched versions of whatsapp html and javascript files.

  * run this script, then in your browser connect to: https://localhost:8111/
  * link using the qr-code.
  * view message traffic in the javascript console.


Author
======

Willem Hengeveld <itsme@xs4all.nl>


