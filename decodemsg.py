from binascii import a2b_hex, b2a_hex
import re
import sys
sys.path += [ '/home/itsme/prj/pixel' ]
from protobuf import DataReader

# manually decode a whatsapp protocol message

def unhex(x): return a2b_hex(re.sub(r'\W+','', x))
def tohex(x): return b2a_hex(x).decode()

singleByte = [  # v5
None,                                   # 0x00 - LIST_EMPTY
None,                                   # 0x01
None,                                   # 0x02 - STREAM_END
"200",                                  # 0x03
"400",                                  # 0x04
"404",                                  # 0x05
"500",                                  # 0x06
"501",                                  # 0x07
"502",                                  # 0x08
"action",                               # 0x09
"add",                                  # 0x0a
"after",                                # 0x0b
"archive",                              # 0x0c
"author",                               # 0x0d
"available",                            # 0x0e
"battery",                              # 0x0f
"before",                               # 0x10
"body",                                 # 0x11
"broadcast",                            # 0x12
"chat",                                 # 0x13
"clear",                                # 0x14
"code",                                 # 0x15
"composing",                            # 0x16
"contacts",                             # 0x17
"count",                                # 0x18
"create",                               # 0x19
"debug",                                # 0x1a
"delete",                               # 0x1b
"demote",                               # 0x1c
"duplicate",                            # 0x1d
"encoding",                             # 0x1e
"error",                                # 0x1f
"false",                                # 0x20
"filehash",                             # 0x21
"from",                                 # 0x22
"g.us",                                 # 0x23
"group",                                # 0x24
"groups_v2",                            # 0x25
"height",                               # 0x26
"id",                                   # 0x27
"image",                                # 0x28
"in",                                   # 0x29
"index",                                # 0x2a
"invis",                                # 0x2b
"item",                                 # 0x2c
"jid",                                  # 0x2d
"kind",                                 # 0x2e
"last",                                 # 0x2f
"leave",                                # 0x30
"live",                                 # 0x31
"log",                                  # 0x32
"media",                                # 0x33
"message",                              # 0x34
"mimetype",                             # 0x35
"missing",                              # 0x36
"modify",                               # 0x37
"name",                                 # 0x38
"notification",                         # 0x39
"notify",                               # 0x3a
"out",                                  # 0x3b
"owner",                                # 0x3c
"participant",                          # 0x3d
"paused",                               # 0x3e
"picture",                              # 0x3f
"played",                               # 0x40
"presence",                             # 0x41
"preview",                              # 0x42
"promote",                              # 0x43
"query",                                # 0x44
"raw",                                  # 0x45
"read",                                 # 0x46
"receipt",                              # 0x47
"received",                             # 0x48
"recipient",                            # 0x49
"recording",                            # 0x4a
"relay",                                # 0x4b
"remove",                               # 0x4c
"response",                             # 0x4d
"resume",                               # 0x4e
"retry",                                # 0x4f
"s.whatsapp.net",                       # 0x50
"seconds",                              # 0x51
"set",                                  # 0x52
"size",                                 # 0x53
"status",                               # 0x54
"subject",                              # 0x55
"subscribe",                            # 0x56
"t",                                    # 0x57
"text",                                 # 0x58
"to",                                   # 0x59
"true",                                 # 0x5a
"type",                                 # 0x5b
"unarchive",                            # 0x5c
"unavailable",                          # 0x5d
"url",                                  # 0x5e
"user",                                 # 0x5f
"value",                                # 0x60
"web",                                  # 0x61
"width",                                # 0x62
"mute",                                 # 0x63
"read_only",                            # 0x64
"admin",                                # 0x65
"creator",                              # 0x66
"short",                                # 0x67
"update",                               # 0x68
"powersave",                            # 0x69
"checksum",                             # 0x6a
"epoch",                                # 0x6b
"block",                                # 0x6c
"previous",                             # 0x6d
"409",                                  # 0x6e
"replaced",                             # 0x6f
"reason",                               # 0x70
"spam",                                 # 0x71
"modify_tag",                           # 0x72
"message_info",                         # 0x73
"delivery",                             # 0x74
"emoji",                                # 0x75
"title",                                # 0x76
"description",                          # 0x77
"canonical-url",                        # 0x78
"matched-text",                         # 0x79
"star",                                 # 0x7a
"unstar",                               # 0x7b
"media_key",                            # 0x7c
"filename",                             # 0x7d
"identity",                             # 0x7e
"unread",                               # 0x7f
"page",                                 # 0x80
"page_count",                           # 0x81
"search",                               # 0x82
"media_message",                        # 0x83
"security",                             # 0x84
"call_log",                             # 0x85
"profile",                              # 0x86
"ciphertext",                           # 0x87  v6
"invite",                               # 0x88  v6
"gif",                                  # 0x89  v7
"vcard",                                # 0x8a  v7
"frequent",                             # 0x8b  v7
"privacy",                              # 0x8c  v8
"blacklist",                            # 0x8d  v8
"whitelist",                            # 0x8e  v8
"verify",                               # 0x8f  v8
"location",                             # 0x90  v9
"document",                             # 0x91  v9
"elapsed",                              # 0x92  v9
"revoke_invite",                        # 0x93  v9
"expiration",                           # 0x94  v9
"unsubscribe",                          # 0x95  v9
"disable",                              # 0x96  v9
"vname",                                # 0x97  v10
"old_jid",                              # 0x98  v10
"new_jid",                              # 0x99  v10
"announcement",                         # 0x9a  v10
"locked",                               # 0x9b  v10
"prop",                                 # 0x9c  v10
"label",                                # 0x9d  v10
"color",                                # 0x9e  v10
"call",                                 # 0x9f  v10
"offer",                                # 0xa0  v10
"call-id",                              # 0xa1  v10
"quick_reply",                          # 0xa2  v11
"sticker",                              # 0xa3  v11
"pay_t",                                # 0xa4  v11
"accept",                               # 0xa5  v11
"reject",                               # 0xa6  v11
"sticker_pack",                         # 0xa7  v11
"invalid",                              # 0xa8  v11
"canceled",                             # 0xa9  v11
"missed",                               # 0xaa  v11
"connected",                            # 0xab  v11
"result",                               # 0xac  v11
"audio",                                # 0xad  v11
"video",                                # 0xae  v11
"recent",                               # 0xaf  v11
]


SingleByteTokens = [
    "",                               # 0x00
    "xmlstreamstart",                 # 0x01
    "xmlstreamend",                   # 0x02
    "s.whatsapp.net",                 # 0x03
    "type",                           # 0x04
    "participant",                    # 0x05
    "from",                           # 0x06
    "receipt",                        # 0x07
    "id",                             # 0x08
    "broadcast",                      # 0x09
    "status",                         # 0x0a
    "message",                        # 0x0b
    "notification",                   # 0x0c
    "notify",                         # 0x0d
    "to",                             # 0x0e
    "jid",                            # 0x0f
    "user",                           # 0x10
    "class",                          # 0x11
    "offline",                        # 0x12
    "g.us",                           # 0x13
    "result",                         # 0x14
    "mediatype",                      # 0x15
    "enc",                            # 0x16
    "skmsg",                          # 0x17
    "off_cnt",                        # 0x18
    "xmlns",                          # 0x19
    "presence",                       # 0x1a
    "participants",                   # 0x1b
    "ack",                            # 0x1c
    "t",                              # 0x1d
    "iq",                             # 0x1e
    "device_hash",                    # 0x1f
    "read",                           # 0x20
    "value",                          # 0x21
    "media",                          # 0x22
    "picture",                        # 0x23
    "chatstate",                      # 0x24
    "unavailable",                    # 0x25
    "text",                           # 0x26
    "urn:xmpp:whatsapp:push",         # 0x27
    "devices",                        # 0x28
    "verified_name",                  # 0x29
    "contact",                        # 0x2a
    "composing",                      # 0x2b
    "edge_routing",                   # 0x2c
    "routing_info",                   # 0x2d
    "item",                           # 0x2e
    "image",                          # 0x2f
    "verified_level",                 # 0x30
    "get",                            # 0x31
    "fallback_hostname",              # 0x32
    "2",                              # 0x33
    "media_conn",                     # 0x34
    "1",                              # 0x35
    "v",                              # 0x36
    "handshake",                      # 0x37
    "fallback_class",                 # 0x38
    "count",                          # 0x39
    "config",                         # 0x3a
    "offline_preview",                # 0x3b
    "download_buckets",               # 0x3c
    "w:profile:picture",              # 0x3d
    "set",                            # 0x3e
    "creation",                       # 0x3f
    "location",                       # 0x40
    "fallback_ip4",                   # 0x41
    "msg",                            # 0x42
    "urn:xmpp:ping",                  # 0x43
    "fallback_ip6",                   # 0x44
    "call-creator",                   # 0x45
    "relaylatency",                   # 0x46
    "success",                        # 0x47
    "subscribe",                      # 0x48
    "video",                          # 0x49
    "business_hours_config",          # 0x4a
    "platform",                       # 0x4b
    "hostname",                       # 0x4c
    "version",                        # 0x4d
    "unknown",                        # 0x4e
    "0",                              # 0x4f
    "ping",                           # 0x50
    "hash",                           # 0x51
    "edit",                           # 0x52
    "subject",                        # 0x53
    "max_buckets",                    # 0x54
    "download",                       # 0x55
    "delivery",                       # 0x56
    "props",                          # 0x57
    "sticker",                        # 0x58
    "name",                           # 0x59
    "last",                           # 0x5a
    "contacts",                       # 0x5b
    "business",                       # 0x5c
    "primary",                        # 0x5d
    "preview",                        # 0x5e
    "w:p",                            # 0x5f
    "pkmsg",                          # 0x60
    "call-id",                        # 0x61
    "retry",                          # 0x62
    "prop",                           # 0x63
    "call",                           # 0x64
    "auth_ttl",                       # 0x65
    "available",                      # 0x66
    "relay_id",                       # 0x67
    "last_id",                        # 0x68
    "day_of_week",                    # 0x69
    "w",                              # 0x6a
    "host",                           # 0x6b
    "seen",                           # 0x6c
    "bits",                           # 0x6d
    "list",                           # 0x6e
    "atn",                            # 0x6f
    "upload",                         # 0x70
    "is_new",                         # 0x71
    "w:stats",                        # 0x72
    "key",                            # 0x73
    "paused",                         # 0x74
    "specific_hours",                 # 0x75
    "multicast",                      # 0x76
    "stream:error",                   # 0x77
    "mmg.whatsapp.net",               # 0x78
    "code",                           # 0x79
    "deny",                           # 0x7a
    "played",                         # 0x7b
    "profile",                        # 0x7c
    "fna",                            # 0x7d
    "device-list",                    # 0x7e
    "close_time",                     # 0x7f
    "latency",                        # 0x80
    "gcm",                            # 0x81
    "pop",                            # 0x82
    "audio",                          # 0x83
    "26",                             # 0x84
    "w:web",                          # 0x85
    "open_time",                      # 0x86
    "error",                          # 0x87
    "auth",                           # 0x88
    "ip4",                            # 0x89
    "update",                         # 0x8a
    "profile_options",                # 0x8b
    "config_value",                   # 0x8c
    "category",                       # 0x8d
    "catalog_not_created",            # 0x8e
    "00",                             # 0x8f
    "config_code",                    # 0x90
    "mode",                           # 0x91
    "catalog_status",                 # 0x92
    "ip6",                            # 0x93
    "blocklist",                      # 0x94
    "registration",                   # 0x95
    "7",                              # 0x96
    "web",                            # 0x97
    "fail",                           # 0x98
    "w:m",                            # 0x99
    "cart_enabled",                   # 0x9a
    "ttl",                            # 0x9b
    "gif",                            # 0x9c
    "300",                            # 0x9d
    "device_orientation",             # 0x9e
    "identity",                       # 0x9f
    "query",                          # 0xa0
    "401",                            # 0xa1
    "media-gig2-1.cdn.whatsapp.net",  # 0xa2
    "in",                             # 0xa3
    "3",                              # 0xa4
    "te2",                            # 0xa5
    "add",                            # 0xa6
    "fallback",                       # 0xa7
    "categories",                     # 0xa8
    "ptt",                            # 0xa9
    "encrypt",                        # 0xaa
    "notice",                         # 0xab
    "thumbnail-document",             # 0xac
    "item-not-found",                 # 0xad
    "12",                             # 0xae
    "thumbnail-image",                # 0xaf
    "stage",                          # 0xb0
    "thumbnail-link",                 # 0xb1
    "usync",                          # 0xb2
    "out",                            # 0xb3
    "thumbnail-video",                # 0xb4
    "8",                              # 0xb5
    "01",                             # 0xb6
    "context",                        # 0xb7
    "sidelist",                       # 0xb8
    "thumbnail-gif",                  # 0xb9
    "terminate",                      # 0xba
    "not-authorized",                 # 0xbb
    "orientation",                    # 0xbc
    "dhash",                          # 0xbd
    "capability",                     # 0xbe
    "side_list",                      # 0xbf
    "md-app-state",                   # 0xc0
    "description",                    # 0xc1
    "serial",                         # 0xc2
    "readreceipts",                   # 0xc3
    "te",                             # 0xc4
    "business_hours",                 # 0xc5
    "md-msg-hist",                    # 0xc6
    "tag",                            # 0xc7
    "attribute_padding",              # 0xc8
    "document",                       # 0xc9
    "open_24h",                       # 0xca
    "delete",                         # 0xcb
    "expiration",                     # 0xcc
    "active",                         # 0xcd
    "prev_v_id",                      # 0xce
    "true",                           # 0xcf
    "passive",                        # 0xd0
    "index",                          # 0xd1
    "4",                              # 0xd2
    "conflict",                       # 0xd3
    "remove",                         # 0xd4
    "w:gp2",                          # 0xd5
    "config_expo_key",                # 0xd6
    "screen_height",                  # 0xd7
    "replaced",                       # 0xd8
    "02",                             # 0xd9
    "screen_width",                   # 0xda
    "uploadfieldstat",                # 0xdb
    "2:47DEQpj8",                     # 0xdc
    "media-bog1-1.cdn.whatsapp.net",  # 0xdd
    "encopt",                         # 0xde
    "url",                            # 0xdf
    "catalog_exists",                 # 0xe0
    "keygen",                         # 0xe1
    "rate",                           # 0xe2
    "offer",                          # 0xe3
    "opus",                           # 0xe4
    "media-mia3-1.cdn.whatsapp.net",  # 0xe5
    "privacy",                        # 0xe6
    "media-mia3-2.cdn.whatsapp.net",  # 0xe7
    "signature",                      # 0xe8
    "preaccept",                      # 0xe9
    "token_id",                       # 0xea
    "media-eze1-1.cdn.whatsapp.net",  # 0xeb
]
DoubleByteTokens = [ [
    "media-for1-1.cdn.whatsapp.net",                 # 0:0x00
    "relay",                                         # 0:0x01
    "media-gru2-2.cdn.whatsapp.net",                 # 0:0x02
    "uncompressed",                                  # 0:0x03
    "medium",                                        # 0:0x04
    "voip_settings",                                 # 0:0x05
    "device",                                        # 0:0x06
    "reason",                                        # 0:0x07
    "media-lim1-1.cdn.whatsapp.net",                 # 0:0x08
    "media-qro1-2.cdn.whatsapp.net",                 # 0:0x09
    "media-gru1-2.cdn.whatsapp.net",                 # 0:0x0a
    "action",                                        # 0:0x0b
    "features",                                      # 0:0x0c
    "media-gru2-1.cdn.whatsapp.net",                 # 0:0x0d
    "media-gru1-1.cdn.whatsapp.net",                 # 0:0x0e
    "media-otp1-1.cdn.whatsapp.net",                 # 0:0x0f
    "kyc-id",                                        # 0:0x10
    "priority",                                      # 0:0x11
    "phash",                                         # 0:0x12
    "mute",                                          # 0:0x13
    "token",                                         # 0:0x14
    "100",                                           # 0:0x15
    "media-qro1-1.cdn.whatsapp.net",                 # 0:0x16
    "none",                                          # 0:0x17
    "media-mrs2-2.cdn.whatsapp.net",                 # 0:0x18
    "sign_credential",                               # 0:0x19
    "03",                                            # 0:0x1a
    "media-mrs2-1.cdn.whatsapp.net",                 # 0:0x1b
    "protocol",                                      # 0:0x1c
    "timezone",                                      # 0:0x1d
    "transport",                                     # 0:0x1e
    "eph_setting",                                   # 0:0x1f
    "1080",                                          # 0:0x20
    "original_dimensions",                           # 0:0x21
    "media-frx5-1.cdn.whatsapp.net",                 # 0:0x22
    "background",                                    # 0:0x23
    "disable",                                       # 0:0x24
    "original_image_url",                            # 0:0x25
    "5",                                             # 0:0x26
    "transaction-id",                                # 0:0x27
    "direct_path",                                   # 0:0x28
    "103",                                           # 0:0x29
    "appointment_only",                              # 0:0x2a
    "request_image_url",                             # 0:0x2b
    "peer_pid",                                      # 0:0x2c
    "address",                                       # 0:0x2d
    "105",                                           # 0:0x2e
    "104",                                           # 0:0x2f
    "102",                                           # 0:0x30
    "media-cdt1-1.cdn.whatsapp.net",                 # 0:0x31
    "101",                                           # 0:0x32
    "109",                                           # 0:0x33
    "110",                                           # 0:0x34
    "106",                                           # 0:0x35
    "background_location",                           # 0:0x36
    "v_id",                                          # 0:0x37
    "sync",                                          # 0:0x38
    "status-old",                                    # 0:0x39
    "111",                                           # 0:0x3a
    "107",                                           # 0:0x3b
    "ppic",                                          # 0:0x3c
    "media-scl2-1.cdn.whatsapp.net",                 # 0:0x3d
    "business_profile",                              # 0:0x3e
    "108",                                           # 0:0x3f
    "invite",                                        # 0:0x40
    "04",                                            # 0:0x41
    "audio_duration",                                # 0:0x42
    "media-mct1-1.cdn.whatsapp.net",                 # 0:0x43
    "media-cdg2-1.cdn.whatsapp.net",                 # 0:0x44
    "media-los2-1.cdn.whatsapp.net",                 # 0:0x45
    "invis",                                         # 0:0x46
    "net",                                           # 0:0x47
    "voip_payload_type",                             # 0:0x48
    "status-revoke-delay",                           # 0:0x49
    "404",                                           # 0:0x4a
    "state",                                         # 0:0x4b
    "use_correct_order_for_hmac_sha1",               # 0:0x4c
    "ver",                                           # 0:0x4d
    "media-mad1-1.cdn.whatsapp.net",                 # 0:0x4e
    "order",                                         # 0:0x4f
    "540",                                           # 0:0x50
    "skey",                                          # 0:0x51
    "blinded_credential",                            # 0:0x52
    "android",                                       # 0:0x53
    "contact_remove",                                # 0:0x54
    "enable_downlink_relay_latency_only",            # 0:0x55
    "duration",                                      # 0:0x56
    "enable_vid_one_way_codec_nego",                 # 0:0x57
    "6",                                             # 0:0x58
    "media-sof1-1.cdn.whatsapp.net",                 # 0:0x59
    "accept",                                        # 0:0x5a
    "all",                                           # 0:0x5b
    "signed_credential",                             # 0:0x5c
    "media-atl3-1.cdn.whatsapp.net",                 # 0:0x5d
    "media-lhr8-1.cdn.whatsapp.net",                 # 0:0x5e
    "website",                                       # 0:0x5f
    "05",                                            # 0:0x60
    "latitude",                                      # 0:0x61
    "media-dfw5-1.cdn.whatsapp.net",                 # 0:0x62
    "forbidden",                                     # 0:0x63
    "enable_audio_piggyback_network_mtu_fix",        # 0:0x64
    "media-dfw5-2.cdn.whatsapp.net",                 # 0:0x65
    "note.m4r",                                      # 0:0x66
    "media-atl3-2.cdn.whatsapp.net",                 # 0:0x67
    "jb_nack_discard_count_fix",                     # 0:0x68
    "longitude",                                     # 0:0x69
    "Opening.m4r",                                   # 0:0x6a
    "media-arn2-1.cdn.whatsapp.net",                 # 0:0x6b
    "email",                                         # 0:0x6c
    "timestamp",                                     # 0:0x6d
    "admin",                                         # 0:0x6e
    "media-pmo1-1.cdn.whatsapp.net",                 # 0:0x6f
    "America/Sao_Paulo",                             # 0:0x70
    "contact_add",                                   # 0:0x71
    "media-sin6-1.cdn.whatsapp.net",                 # 0:0x72
    "interactive",                                   # 0:0x73
    "8000",                                          # 0:0x74
    "acs_public_key",                                # 0:0x75
    "sigquit_anr_detector_release_rollover_percent", # 0:0x76
    "media.fmed1-2.fna.whatsapp.net",                # 0:0x77
    "groupadd",                                      # 0:0x78
    "enabled_for_video_upgrade",                     # 0:0x79
    "latency_update_threshold",                      # 0:0x7a
    "media-frt3-2.cdn.whatsapp.net",                 # 0:0x7b
    "calls_row_constraint_layout",                   # 0:0x7c
    "media.fgbb2-1.fna.whatsapp.net",                # 0:0x7d
    "mms4_media_retry_notification_encryption_enabled",#0:0x7e
    "timeout",                                       # 0:0x7f
    "media-sin6-3.cdn.whatsapp.net",                 # 0:0x80
    "audio_nack_jitter_multiplier",                  # 0:0x81
    "jb_discard_count_adjust_pct_rc",                # 0:0x82
    "audio_reserve_bps",                             # 0:0x83
    "delta",                                         # 0:0x84
    "account_sync",                                  # 0:0x85
    "default",                                       # 0:0x86
    "media.fjed4-6.fna.whatsapp.net",                # 0:0x87
    "06",                                            # 0:0x88
    "lock_video_orientation",                        # 0:0x89
    "media-frt3-1.cdn.whatsapp.net",                 # 0:0x8a
    "w:g2",                                          # 0:0x8b
    "media-sin6-2.cdn.whatsapp.net",                 # 0:0x8c
    "audio_nack_algo_mask",                          # 0:0x8d
    "media.fgbb2-2.fna.whatsapp.net",                # 0:0x8e
    "media.fmed1-1.fna.whatsapp.net",                # 0:0x8f
    "cond_range_target_bitrate",                     # 0:0x90
    "mms4_server_error_receipt_encryption_enabled",  # 0:0x91
    "vid_rc_dyn",                                    # 0:0x92
    "fri",                                           # 0:0x93
    "cart_v1_1_order_message_changes_enabled",       # 0:0x94
    "reg_push",                                      # 0:0x95
    "jb_hist_deposit_value",                         # 0:0x96
    "privatestats",                                  # 0:0x97
    "media.fist7-2.fna.whatsapp.net",                # 0:0x98
    "thu",                                           # 0:0x99
    "jb_discard_count_adjust_pct",                   # 0:0x9a
    "mon",                                           # 0:0x9b
    "group_call_video_maximization_enabled",         # 0:0x9c
    "mms_cat_v1_forward_hot_override_enabled",       # 0:0x9d
    "audio_nack_new_rtt",                            # 0:0x9e
    "media.fsub2-3.fna.whatsapp.net",                # 0:0x9f
    "media_upload_aggressive_retry_exponential_backoff_enabled", # 0:0xa0
    "tue",                                           # 0:0xa1
    "wed",                                           # 0:0xa2
    "media.fruh4-2.fna.whatsapp.net",                # 0:0xa3
    "audio_nack_max_seq_req",                        # 0:0xa4
    "max_rtp_audio_packet_resends",                  # 0:0xa5
    "jb_hist_max_cdf_value",                         # 0:0xa6
    "07",                                            # 0:0xa7
    "audio_nack_max_jb_delay",                       # 0:0xa8
    "mms_forward_partially_downloaded_video",        # 0:0xa9
    "media-lcy1-1.cdn.whatsapp.net",                 # 0:0xaa
    "resume",                                        # 0:0xab
    "jb_inband_fec_aware",                           # 0:0xac
    "new_commerce_entry_point_enabled",              # 0:0xad
    "480",                                           # 0:0xae
    "payments_upi_generate_qr_amount_limit",         # 0:0xaf
    "sigquit_anr_detector_rollover_percent",         # 0:0xb0
    "media.fsdu2-1.fna.whatsapp.net",                # 0:0xb1
    "fbns",                                          # 0:0xb2
    "aud_pkt_reorder_pct",                           # 0:0xb3
    "dec",                                           # 0:0xb4
    "stop_probing_before_accept_send",               # 0:0xb5
    "media_upload_max_aggressive_retries",           # 0:0xb6
    "edit_business_profile_new_mode_enabled",        # 0:0xb7
    "media.fhex4-1.fna.whatsapp.net",                # 0:0xb8
    "media.fjed4-3.fna.whatsapp.net",                # 0:0xb9
    "sigquit_anr_detector_64bit_rollover_percent",   # 0:0xba
    "cond_range_ema_jb_last_delay",                  # 0:0xbb
    "watls_enable_early_data_http_get",              # 0:0xbc
    "media.fsdu2-2.fna.whatsapp.net",                # 0:0xbd
    "message_qr_disambiguation_enabled",             # 0:0xbe
    "media-mxp1-1.cdn.whatsapp.net",                 # 0:0xbf
    "sat",                                           # 0:0xc0
    "vertical",                                      # 0:0xc1
    "media.fruh4-5.fna.whatsapp.net",                # 0:0xc2
    "200",                                           # 0:0xc3
    "media-sof1-2.cdn.whatsapp.net",                 # 0:0xc4
    "-1",                                            # 0:0xc5
    "height",                                        # 0:0xc6
    "product_catalog_hide_show_items_enabled",       # 0:0xc7
    "deep_copy_frm_last",                            # 0:0xc8
    "tsoffline",                                     # 0:0xc9
    "vp8/h.264",                                     # 0:0xca
    "media.fgye5-3.fna.whatsapp.net",                # 0:0xcb
    "media.ftuc1-2.fna.whatsapp.net",                # 0:0xcc
    "smb_upsell_chat_banner_enabled",                # 0:0xcd
    "canonical",                                     # 0:0xce
    "08",                                            # 0:0xcf
    "9",                                             # 0:0xd0
    ".",                                             # 0:0xd1
    "media.fgyd4-4.fna.whatsapp.net",                # 0:0xd2
    "media.fsti4-1.fna.whatsapp.net",                # 0:0xd3
    "mms_vcache_aggregation_enabled",                # 0:0xd4
    "mms_hot_content_timespan_in_seconds",           # 0:0xd5
    "nse_ver",                                       # 0:0xd6
    "rte",                                           # 0:0xd7
    "third_party_sticker_web_sync",                  # 0:0xd8
    "cond_range_target_total_bitrate",               # 0:0xd9
    "media_upload_aggressive_retry_enabled",         # 0:0xda
    "instrument_spam_report_enabled",                # 0:0xdb
    "disable_reconnect_tone",                        # 0:0xdc
    "move_media_folder_from_sister_app",             # 0:0xdd
    "one_tap_calling_in_group_chat_size",            # 0:0xde
    "10",                                            # 0:0xdf
    "storage_mgmt_banner_threshold_mb",              # 0:0xe0
    "enable_backup_passive_mode",                    # 0:0xe1
    "sharechat_inline_player_enabled",               # 0:0xe2
    "media.fcnq2-1.fna.whatsapp.net",                # 0:0xe3
    "media.fhex4-2.fna.whatsapp.net",                # 0:0xe4
    "media.fist6-3.fna.whatsapp.net",                # 0:0xe5
    "ephemeral_drop_column_stage",                   # 0:0xe6
    "reconnecting_after_network_change_threshold_ms",# 0:0xe7
    "media-lhr8-2.cdn.whatsapp.net",                 # 0:0xe8
    "cond_jb_last_delay_ema_alpha",                  # 0:0xe9
    "entry_point_block_logging_enabled",             # 0:0xea
    "critical_event_upload_log_config",              # 0:0xeb
    "respect_initial_bitrate_estimate",              # 0:0xec
    "smaller_image_thumbs_status_enabled",           # 0:0xed
    "media.fbtz1-4.fna.whatsapp.net",                # 0:0xee
    "media.fjed4-1.fna.whatsapp.net",                # 0:0xef
    "width",                                         # 0:0xf0
    "720",                                           # 0:0xf1
    "enable_frame_dropper",                          # 0:0xf2
    "enable_one_side_mode",                          # 0:0xf3
    "urn:xmpp:whatsapp:dirty",                       # 0:0xf4
    "new_sticker_animation_behavior_v2",             # 0:0xf5
    "media.flim3-2.fna.whatsapp.net",                # 0:0xf6
    "media.fuio6-2.fna.whatsapp.net",                # 0:0xf7
    "skip_forced_signaling",                         # 0:0xf8
    "dleq_proof",                                    # 0:0xf9
    "status_video_max_bitrate",                      # 0:0xfa
    "lazy_send_probing_req",                         # 0:0xfb
    "enhanced_storage_management",                   # 0:0xfc
    "android_privatestats_endpoint_dit_enabled",     # 0:0xfd
    "media.fscl13-2.fna.whatsapp.net",               # 0:0xfe
    "video_duration",                                # 0:0xff
],
[
    "group_call_discoverability_enabled",            # 1:0x00
    "media.faep9-2.fna.whatsapp.net",                # 1:0x01
    "msgr",                                          # 1:0x02
    "bloks_loggedin_access_app_id",                  # 1:0x03
    "db_status_migration_step",                      # 1:0x04
    "watls_prefer_ip6",                              # 1:0x05
    "jabber:iq:privacy",                             # 1:0x06
    "68",                                            # 1:0x07
    "media.fsaw1-11.fna.whatsapp.net",               # 1:0x08
    "mms4_media_conn_persist_enabled",               # 1:0x09
    "animated_stickers_thread_clean_up",             # 1:0x0a
    "media.fcgk3-2.fna.whatsapp.net",                # 1:0x0b
    "media.fcgk4-6.fna.whatsapp.net",                # 1:0x0c
    "media.fgye5-2.fna.whatsapp.net",                # 1:0x0d
    "media.flpb1-1.fna.whatsapp.net",                # 1:0x0e
    "media.fsub2-1.fna.whatsapp.net",                # 1:0x0f
    "media.fuio6-3.fna.whatsapp.net",                # 1:0x10
    "not-allowed",                                   # 1:0x11
    "partial_pjpeg_bw_threshold",                    # 1:0x12
    "cap_estimated_bitrate",                         # 1:0x13
    "mms_chatd_resume_check_over_thrift",            # 1:0x14
    "smb_upsell_business_profile_enabled",           # 1:0x15
    "product_catalog_webclient",                     # 1:0x16
    "groups",                                        # 1:0x17
    "sigquit_anr_detector_release_updated_rollout",  # 1:0x18
    "syncd_key_rotation_enabled",                    # 1:0x19
    "media.fdmm2-1.fna.whatsapp.net",                # 1:0x1a
    "media-hou1-1.cdn.whatsapp.net",                 # 1:0x1b
    "remove_old_chat_notifications",                 # 1:0x1c
    "smb_biztools_deeplink_enabled",                 # 1:0x1d
    "use_downloadable_filters_int",                  # 1:0x1e
    "group_qr_codes_enabled",                        # 1:0x1f
    "max_receipt_processing_time",                   # 1:0x20
    "optimistic_image_processing_enabled",           # 1:0x21
    "smaller_video_thumbs_status_enabled",           # 1:0x22
    "watls_early_data",                              # 1:0x23
    "reconnecting_before_relay_failover_threshold_ms",#1:0x24
    "cond_range_packet_loss_pct",                    # 1:0x25
    "groups_privacy_blacklist",                      # 1:0x26
    "status-revoke-drop",                            # 1:0x27
    "stickers_animated_thumbnail_download",          # 1:0x28
    "dedupe_transcode_shared_images",                # 1:0x29
    "dedupe_transcode_shared_videos",                # 1:0x2a
    "media.fcnq2-2.fna.whatsapp.net",                # 1:0x2b
    "media.fgyd4-1.fna.whatsapp.net",                # 1:0x2c
    "media.fist7-1.fna.whatsapp.net",                # 1:0x2d
    "media.flim3-3.fna.whatsapp.net",                # 1:0x2e
    "add_contact_by_qr_enabled",                     # 1:0x2f
    "https:#faq.whatsapp.com/payments",              # 1:0x30
    "multicast_limit_global",                        # 1:0x31
    "sticker_notification_preview",                  # 1:0x32
    "smb_better_catalog_list_adapters_enabled",      # 1:0x33
    "bloks_use_minscript_android",                   # 1:0x34
    "pen_smoothing_enabled",                         # 1:0x35
    "media.fcgk4-5.fna.whatsapp.net",                # 1:0x36
    "media.fevn1-3.fna.whatsapp.net",                # 1:0x37
    "media.fpoj7-1.fna.whatsapp.net",                # 1:0x38
    "media-arn2-2.cdn.whatsapp.net",                 # 1:0x39
    "reconnecting_before_network_change_threshold_ms",#1:0x3a
    "android_media_use_fresco_for_gifs",             # 1:0x3b
    "cond_in_congestion",                            # 1:0x3c
    "status_image_max_edge",                         # 1:0x3d
    "sticker_search_enabled",                        # 1:0x3e
    "starred_stickers_web_sync",                     # 1:0x3f
    "db_blank_me_jid_migration_step",                # 1:0x40
    "media.fist6-2.fna.whatsapp.net",                # 1:0x41
    "media.ftuc1-1.fna.whatsapp.net",                # 1:0x42
    "09",                                            # 1:0x43
    "anr_fast_logs_upload_rollout",                  # 1:0x44
    "camera_core_integration_enabled",               # 1:0x45
    "11",                                            # 1:0x46
    "third_party_sticker_caching",                   # 1:0x47
    "thread_dump_contact_support",                   # 1:0x48
    "wam_privatestats_enabled",                      # 1:0x49
    "vcard_as_document_size_kb",                     # 1:0x4a
    "maxfpp",                                        # 1:0x4b
    "fbip",                                          # 1:0x4c
    "ephemeral_allow_group_members",                 # 1:0x4d
    "media-bom1-2.cdn.whatsapp.net",                 # 1:0x4e
    "media-xsp1-1.cdn.whatsapp.net",                 # 1:0x4f
    "disable_prewarm",                               # 1:0x50
    "frequently_forwarded_max",                      # 1:0x51
    "media.fbtz1-5.fna.whatsapp.net",                # 1:0x52
    "media.fevn7-1.fna.whatsapp.net",                # 1:0x53
    "media.fgyd4-2.fna.whatsapp.net",                # 1:0x54
    "sticker_tray_animation_fully_visible_items",    # 1:0x55
    "green_alert_banner_duration",                   # 1:0x56
    "reconnecting_after_p2p_failover_threshold_ms",  # 1:0x57
    "connected",                                     # 1:0x58
    "share_biz_vcard_enabled",                       # 1:0x59
    "stickers_animation",                            # 1:0x5a
    "0a",                                            # 1:0x5b
    "1200",                                          # 1:0x5c
    "WhatsApp",                                      # 1:0x5d
    "group_description_length",                      # 1:0x5e
    "p_v_id",                                        # 1:0x5f
    "payments_upi_intent_transaction_limit",         # 1:0x60
    "frequently_forwarded_messages",                 # 1:0x61
    "media-xsp1-2.cdn.whatsapp.net",                 # 1:0x62
    "media.faep8-1.fna.whatsapp.net",                # 1:0x63
    "media.faep8-2.fna.whatsapp.net",                # 1:0x64
    "media.faep9-1.fna.whatsapp.net",                # 1:0x65
    "media.fdmm2-2.fna.whatsapp.net",                # 1:0x66
    "media.fgzt3-1.fna.whatsapp.net",                # 1:0x67
    "media.flim4-2.fna.whatsapp.net",                # 1:0x68
    "media.frao1-1.fna.whatsapp.net",                # 1:0x69
    "media.fscl9-2.fna.whatsapp.net",                # 1:0x6a
    "media.fsub2-2.fna.whatsapp.net",                # 1:0x6b
    "superadmin",                                    # 1:0x6c
    "media.fbog10-1.fna.whatsapp.net",               # 1:0x6d
    "media.fcgh28-1.fna.whatsapp.net",               # 1:0x6e
    "media.fjdo10-1.fna.whatsapp.net",               # 1:0x6f
    "third_party_animated_sticker_import",           # 1:0x70
    "delay_fec",                                     # 1:0x71
    "attachment_picker_refresh",                     # 1:0x72
    "android_linked_devices_re_auth_enabled",        # 1:0x73
    "rc_dyn",                                        # 1:0x74
    "green_alert_block_jitter",                      # 1:0x75
    "add_contact_logging_enabled",                   # 1:0x76
    "biz_message_logging_enabled",                   # 1:0x77
    "conversation_media_preview_v2",                 # 1:0x78
    "media-jnb1-1.cdn.whatsapp.net",                 # 1:0x79
    "ab_key",                                        # 1:0x7a
    "media.fcgk4-2.fna.whatsapp.net",                # 1:0x7b
    "media.fevn1-1.fna.whatsapp.net",                # 1:0x7c
    "media.fist6-1.fna.whatsapp.net",                # 1:0x7d
    "media.fruh4-4.fna.whatsapp.net",                # 1:0x7e
    "media.fsti4-2.fna.whatsapp.net",                # 1:0x7f
    "mms_vcard_autodownload_size_kb",                # 1:0x80
    "watls_enabled",                                 # 1:0x81
    "notif_ch_override_off",                         # 1:0x82
    "media.fsaw1-14.fna.whatsapp.net",               # 1:0x83
    "media.fscl13-1.fna.whatsapp.net",               # 1:0x84
    "db_group_participant_migration_step",           # 1:0x85
    "1020",                                          # 1:0x86
    "cond_range_sterm_rtt",                          # 1:0x87
    "invites_logging_enabled",                       # 1:0x88
    "triggered_block_enabled",                       # 1:0x89
    "group_call_max_participants",                   # 1:0x8a
    "media-iad3-1.cdn.whatsapp.net",                 # 1:0x8b
    "product_catalog_open_deeplink",                 # 1:0x8c
    "shops_required_tos_version",                    # 1:0x8d
    "image_max_kbytes",                              # 1:0x8e
    "cond_low_quality_vid_mode",                     # 1:0x8f
    "db_receipt_migration_step",                     # 1:0x90
    "jb_early_prob_hist_shrink",                     # 1:0x91
    "media.fdmm2-3.fna.whatsapp.net",                # 1:0x92
    "media.fdmm2-4.fna.whatsapp.net",                # 1:0x93
    "media.fruh4-1.fna.whatsapp.net",                # 1:0x94
    "media.fsaw2-2.fna.whatsapp.net",                # 1:0x95
    "remove_geolocation_videos",                     # 1:0x96
    "new_animation_behavior",                        # 1:0x97
    "fieldstats_beacon_chance",                      # 1:0x98
    "403",                                           # 1:0x99
    "authkey_reset_on_ban",                          # 1:0x9a
    "continuous_ptt_playback",                       # 1:0x9b
    "reconnecting_after_relay_failover_threshold_ms",# 1:0x9c
    "false",                                         # 1:0x9d
    "group",                                         # 1:0x9e
    "sun",                                           # 1:0x9f
    "conversation_swipe_to_reply",                   # 1:0xa0
    "ephemeral_messages_setting",                    # 1:0xa1
    "smaller_video_thumbs_enabled",                  # 1:0xa2
    "md_device_sync_enabled",                        # 1:0xa3
    "bloks_shops_pdp_url_regex",                     # 1:0xa4
    "lasso_integration_enabled",                     # 1:0xa5
    "media-bom1-1.cdn.whatsapp.net",                 # 1:0xa6
    "new_backup_format_enabled",                     # 1:0xa7
    "256",                                           # 1:0xa8
    "media.faep6-1.fna.whatsapp.net",                # 1:0xa9
    "media.fasr1-1.fna.whatsapp.net",                # 1:0xaa
    "media.fbtz1-7.fna.whatsapp.net",                # 1:0xab
    "media.fesb4-1.fna.whatsapp.net",                # 1:0xac
    "media.fjdo1-2.fna.whatsapp.net",                # 1:0xad
    "media.frba2-1.fna.whatsapp.net",                # 1:0xae
    "watls_no_dns",                                  # 1:0xaf
    "600",                                           # 1:0xb0
    "db_broadcast_me_jid_migration_step",            # 1:0xb1
    "new_wam_runtime_enabled",                       # 1:0xb2
    "group_update",                                  # 1:0xb3
    "enhanced_block_enabled",                        # 1:0xb4
    "sync_wifi_threshold_kb",                        # 1:0xb5
    "mms_download_nc_cat",                           # 1:0xb6
    "bloks_minification_enabled",                    # 1:0xb7
    "ephemeral_messages_enabled",                    # 1:0xb8
    "reject",                                        # 1:0xb9
    "voip_outgoing_xml_signaling",                   # 1:0xba
    "creator",                                       # 1:0xbb
    "dl_bw",                                         # 1:0xbc
    "payments_request_messages",                     # 1:0xbd
    "target_bitrate",                                # 1:0xbe
    "bloks_rendercore_enabled",                      # 1:0xbf
    "media-hbe1-1.cdn.whatsapp.net",                 # 1:0xc0
    "media-hel3-1.cdn.whatsapp.net",                 # 1:0xc1
    "media-kut2-2.cdn.whatsapp.net",                 # 1:0xc2
    "media-lax3-1.cdn.whatsapp.net",                 # 1:0xc3
    "media-lax3-2.cdn.whatsapp.net",                 # 1:0xc4
    "sticker_pack_deeplink_enabled",                 # 1:0xc5
    "hq_image_bw_threshold",                         # 1:0xc6
    "status_info",                                   # 1:0xc7
    "voip",                                          # 1:0xc8
    "dedupe_transcode_videos",                       # 1:0xc9
    "grp_uii_cleanup",                               # 1:0xca
    "linked_device_max_count",                       # 1:0xcb
    "media.flim1-1.fna.whatsapp.net",                # 1:0xcc
    "media.fsaw2-1.fna.whatsapp.net",                # 1:0xcd
    "reconnecting_after_call_active_threshold_ms",   # 1:0xce
    "1140",                                          # 1:0xcf
    "catalog_pdp_new_design",                        # 1:0xd0
    "media.fbtz1-10.fna.whatsapp.net",               # 1:0xd1
    "media.fsaw1-15.fna.whatsapp.net",               # 1:0xd2
    "0b",                                            # 1:0xd3
    "consumer_rc_provider",                          # 1:0xd4
    "mms_async_fast_forward_ttl",                    # 1:0xd5
    "jb_eff_size_fix",                               # 1:0xd6
    "voip_incoming_xml_signaling",                   # 1:0xd7
    "media_provider_share_by_uuid",                  # 1:0xd8
    "suspicious_links",                              # 1:0xd9
    "dedupe_transcode_images",                       # 1:0xda
    "green_alert_modal_start",                       # 1:0xdb
    "media-cgk1-1.cdn.whatsapp.net",                 # 1:0xdc
    "media-lga3-1.cdn.whatsapp.net",                 # 1:0xdd
    "template_doc_mime_types",                       # 1:0xde
    "important_messages",                            # 1:0xdf
    "user_add",                                      # 1:0xe0
    "vcard_max_size_kb",                             # 1:0xe1
    "media.fada2-1.fna.whatsapp.net",                # 1:0xe2
    "media.fbog2-5.fna.whatsapp.net",                # 1:0xe3
    "media.fbtz1-3.fna.whatsapp.net",                # 1:0xe4
    "media.fcgk3-1.fna.whatsapp.net",                # 1:0xe5
    "media.fcgk7-1.fna.whatsapp.net",                # 1:0xe6
    "media.flim1-3.fna.whatsapp.net",                # 1:0xe7
    "media.fscl9-1.fna.whatsapp.net",                # 1:0xe8
    "ctwa_context_enterprise_enabled",               # 1:0xe9
    "media.fsaw1-13.fna.whatsapp.net",               # 1:0xea
    "media.fuio11-2.fna.whatsapp.net",               # 1:0xeb
    "status_collapse_muted",                         # 1:0xec
    "db_migration_level_force",                      # 1:0xed
    "recent_stickers_web_sync",                      # 1:0xee
    "bloks_session_state",                           # 1:0xef
    "bloks_shops_enabled",                           # 1:0xf0
    "green_alert_setting_deep_links_enabled",        # 1:0xf1
    "restrict_groups",                               # 1:0xf2
    "battery",                                       # 1:0xf3
    "green_alert_block_start",                       # 1:0xf4
    "refresh",                                       # 1:0xf5
    "ctwa_context_enabled",                          # 1:0xf6
    "md_messaging_enabled",                          # 1:0xf7
    "status_image_quality",                          # 1:0xf8
    "md_blocklist_v2_server",                        # 1:0xf9
    "media-del1-1.cdn.whatsapp.net",                 # 1:0xfa
    "13",                                            # 1:0xfb
    "userrate",                                      # 1:0xfc
    "a_v_id",                                        # 1:0xfd
    "cond_rtt_ema_alpha",                            # 1:0xfe
    "invalid",                                       # 1:0xff
],
[
    "media.fada1-1.fna.whatsapp.net",                # 2:0x00
    "media.fadb3-2.fna.whatsapp.net",                # 2:0x01
    "media.fbhz2-1.fna.whatsapp.net",                # 2:0x02
    "media.fcor2-1.fna.whatsapp.net",                # 2:0x03
    "media.fjed4-2.fna.whatsapp.net",                # 2:0x04
    "media.flhe4-1.fna.whatsapp.net",                # 2:0x05
    "media.frak1-2.fna.whatsapp.net",                # 2:0x06
    "media.fsub6-3.fna.whatsapp.net",                # 2:0x07
    "media.fsub6-7.fna.whatsapp.net",                # 2:0x08
    "media.fvvi1-1.fna.whatsapp.net",                # 2:0x09
    "search_v5_eligible",                            # 2:0x0a
    "wam_real_time_enabled",                         # 2:0x0b
    "report_disk_event",                             # 2:0x0c
    "max_tx_rott_based_bitrate",                     # 2:0x0d
    "product",                                       # 2:0x0e
    "media.fjdo10-2.fna.whatsapp.net",               # 2:0x0f
    "video_frame_crc_sample_interval",               # 2:0x10
    "media_max_autodownload",                        # 2:0x11
    "15",                                            # 2:0x12
    "h.264",                                         # 2:0x13
    "wam_privatestats_buffer_count",                 # 2:0x14
    "md_phash_v2_enabled",                           # 2:0x15
    "account_transfer_enabled",                      # 2:0x16
    "business_product_catalog",                      # 2:0x17
    "enable_non_dyn_codec_param_fix",                # 2:0x18
    "is_user_under_epd_jurisdiction",                # 2:0x19
    "media.fbog2-4.fna.whatsapp.net",                # 2:0x1a
    "media.fbtz1-2.fna.whatsapp.net",                # 2:0x1b
    "media.fcfc1-1.fna.whatsapp.net",                # 2:0x1c
    "media.fjed4-5.fna.whatsapp.net",                # 2:0x1d
    "media.flhe4-2.fna.whatsapp.net",                # 2:0x1e
    "media.flim1-2.fna.whatsapp.net",                # 2:0x1f
    "media.flos5-1.fna.whatsapp.net",                # 2:0x20
    "android_key_store_auth_ver",                    # 2:0x21
    "010",                                           # 2:0x22
    "anr_process_monitor",                           # 2:0x23
    "delete_old_auth_key",                           # 2:0x24
    "media.fcor10-3.fna.whatsapp.net",               # 2:0x25
    "storage_usage_enabled",                         # 2:0x26
    "android_camera2_support_level",                 # 2:0x27
    "dirty",                                         # 2:0x28
    "consumer_content_provider",                     # 2:0x29
    "status_video_max_duration",                     # 2:0x2a
    "0c",                                            # 2:0x2b
    "bloks_cache_enabled",                           # 2:0x2c
    "media.fadb2-2.fna.whatsapp.net",                # 2:0x2d
    "media.fbko1-1.fna.whatsapp.net",                # 2:0x2e
    "media.fbtz1-9.fna.whatsapp.net",                # 2:0x2f
    "media.fcgk4-4.fna.whatsapp.net",                # 2:0x30
    "media.fesb4-2.fna.whatsapp.net",                # 2:0x31
    "media.fevn1-2.fna.whatsapp.net",                # 2:0x32
    "media.fist2-4.fna.whatsapp.net",                # 2:0x33
    "media.fjdo1-1.fna.whatsapp.net",                # 2:0x34
    "media.fruh4-6.fna.whatsapp.net",                # 2:0x35
    "media.fsrg5-1.fna.whatsapp.net",                # 2:0x36
    "media.fsub6-6.fna.whatsapp.net",                # 2:0x37
    "minfpp",                                        # 2:0x38
    "5000",                                          # 2:0x39
    "locales",                                       # 2:0x3a
    "video_max_bitrate",                             # 2:0x3b
    "use_new_auth_key",                              # 2:0x3c
    "bloks_http_enabled",                            # 2:0x3d
    "heartbeat_interval",                            # 2:0x3e
    "media.fbog11-1.fna.whatsapp.net",               # 2:0x3f
    "ephemeral_group_query_ts",                      # 2:0x40
    "fec_nack",                                      # 2:0x41
    "search_in_storage_usage",                       # 2:0x42
    "c",                                             # 2:0x43
    "media-amt2-1.cdn.whatsapp.net",                 # 2:0x44
    "linked_devices_ui_enabled",                     # 2:0x45
    "14",                                            # 2:0x46
    "async_data_load_on_startup",                    # 2:0x47
    "voip_incoming_xml_ack",                         # 2:0x48
    "16",                                            # 2:0x49
    "db_migration_step",                             # 2:0x4a
    "init_bwe",                                      # 2:0x4b
    "max_participants",                              # 2:0x4c
    "wam_buffer_count",                              # 2:0x4d
    "media.fada2-2.fna.whatsapp.net",                # 2:0x4e
    "media.fadb3-1.fna.whatsapp.net",                # 2:0x4f
    "media.fcor2-2.fna.whatsapp.net",                # 2:0x50
    "media.fdiy1-2.fna.whatsapp.net",                # 2:0x51
    "media.frba3-2.fna.whatsapp.net",                # 2:0x52
    "media.fsaw2-3.fna.whatsapp.net",                # 2:0x53
    "1280",                                          # 2:0x54
    "status_grid_enabled",                           # 2:0x55
    "w:biz",                                         # 2:0x56
    "product_catalog_deeplink",                      # 2:0x57
    "media.fgye10-2.fna.whatsapp.net",               # 2:0x58
    "media.fuio11-1.fna.whatsapp.net",               # 2:0x59
    "optimistic_upload",                             # 2:0x5a
    "work_manager_init",                             # 2:0x5b
    "lc",                                            # 2:0x5c
    "catalog_message",                               # 2:0x5d
    "cond_net_medium",                               # 2:0x5e
    "enable_periodical_aud_rr_processing",           # 2:0x5f
    "cond_range_ema_rtt",                            # 2:0x60
    "media-tir2-1.cdn.whatsapp.net",                 # 2:0x61
    "frame_ms",                                      # 2:0x62
    "group_invite_sending",                          # 2:0x63
    "payments_web_enabled",                          # 2:0x64
    "wallpapers_v2",                                 # 2:0x65
    "0d",                                            # 2:0x66
    "browser",                                       # 2:0x67
    "hq_image_max_edge",                             # 2:0x68
    "image_edit_zoom",                               # 2:0x69
    "linked_devices_re_auth_enabled",                # 2:0x6a
    "media.faly3-2.fna.whatsapp.net",                # 2:0x6b
    "media.fdoh5-3.fna.whatsapp.net",                # 2:0x6c
    "media.fesb3-1.fna.whatsapp.net",                # 2:0x6d
    "media.fknu1-1.fna.whatsapp.net",                # 2:0x6e
    "media.fmex3-1.fna.whatsapp.net",                # 2:0x6f
    "media.fruh4-3.fna.whatsapp.net",                # 2:0x70
    "255",                                           # 2:0x71
    "web_upgrade_to_md_modal",                       # 2:0x72
    "audio_piggyback_timeout_msec",                  # 2:0x73
    "enable_audio_oob_fec_feature",                  # 2:0x74
    "from_ip",                                       # 2:0x75
    "image_max_edge",                                # 2:0x76
    "message_qr_enabled",                            # 2:0x77
    "powersave",                                     # 2:0x78
    "receipt_pre_acking",                            # 2:0x79
    "video_max_edge",                                # 2:0x7a
    "full",                                          # 2:0x7b
    "011",                                           # 2:0x7c
    "012",                                           # 2:0x7d
    "enable_audio_oob_fec_for_sender",               # 2:0x7e
    "md_voip_enabled",                               # 2:0x7f
    "enable_privatestats",                           # 2:0x80
    "max_fec_ratio",                                 # 2:0x81
    "payments_cs_faq_url",                           # 2:0x82
    "media-xsp1-3.cdn.whatsapp.net",                 # 2:0x83
    "hq_image_quality",                              # 2:0x84
    "media.fasr1-2.fna.whatsapp.net",                # 2:0x85
    "media.fbog3-1.fna.whatsapp.net",                # 2:0x86
    "media.ffjr1-6.fna.whatsapp.net",                # 2:0x87
    "media.fist2-3.fna.whatsapp.net",                # 2:0x88
    "media.flim4-3.fna.whatsapp.net",                # 2:0x89
    "media.fpbc2-4.fna.whatsapp.net",                # 2:0x8a
    "media.fpku1-1.fna.whatsapp.net",                # 2:0x8b
    "media.frba1-1.fna.whatsapp.net",                # 2:0x8c
    "media.fudi1-1.fna.whatsapp.net",                # 2:0x8d
    "media.fvvi1-2.fna.whatsapp.net",                # 2:0x8e
    "gcm_fg_service",                                # 2:0x8f
    "enable_dec_ltr_size_check",                     # 2:0x90
    "clear",                                         # 2:0x91
    "lg",                                            # 2:0x92
    "media.fgru11-1.fna.whatsapp.net",               # 2:0x93
    "18",                                            # 2:0x94
    "media-lga3-2.cdn.whatsapp.net",                 # 2:0x95
    "pkey",                                          # 2:0x96
    "0e",                                            # 2:0x97
    "max_subject",                                   # 2:0x98
    "cond_range_lterm_rtt",                          # 2:0x99
    "announcement_groups",                           # 2:0x9a
    "biz_profile_options",                           # 2:0x9b
    "s_t",                                           # 2:0x9c
    "media.fabv2-1.fna.whatsapp.net",                # 2:0x9d
    "media.fcai3-1.fna.whatsapp.net",                # 2:0x9e
    "media.fcgh1-1.fna.whatsapp.net",                # 2:0x9f
    "media.fctg1-4.fna.whatsapp.net",                # 2:0xa0
    "media.fdiy1-1.fna.whatsapp.net",                # 2:0xa1
    "media.fisb4-1.fna.whatsapp.net",                # 2:0xa2
    "media.fpku1-2.fna.whatsapp.net",                # 2:0xa3
    "media.fros9-1.fna.whatsapp.net",                # 2:0xa4
    "status_v3_text",                                # 2:0xa5
    "usync_sidelist",                                # 2:0xa6
    "17",                                            # 2:0xa7
    "announcement",                                  # 2:0xa8
    "...",                                           # 2:0xa9
    "md_group_notification",                         # 2:0xaa
    "0f",                                            # 2:0xab
    "animated_pack_in_store",                        # 2:0xac
    "013",                                           # 2:0xad
    "America/Mexico_City",                           # 2:0xae
    "1260",                                          # 2:0xaf
    "media-ams4-1.cdn.whatsapp.net",                 # 2:0xb0
    "media-cgk1-2.cdn.whatsapp.net",                 # 2:0xb1
    "media-cpt1-1.cdn.whatsapp.net",                 # 2:0xb2
    "media-maa2-1.cdn.whatsapp.net",                 # 2:0xb3
    "media.fgye10-1.fna.whatsapp.net",               # 2:0xb4
    "e",                                             # 2:0xb5
    "catalog_cart",                                  # 2:0xb6
    "hfm_string_changes",                            # 2:0xb7
    "init_bitrate",                                  # 2:0xb8
    "packless_hsm",                                  # 2:0xb9
    "group_info",                                    # 2:0xba
    "America/Belem",                                 # 2:0xbb
    "50",                                            # 2:0xbc
    "960",                                           # 2:0xbd
    "cond_range_bwe",                                # 2:0xbe
    "decode",                                        # 2:0xbf
    "encode",                                        # 2:0xc0
    "media.fada1-8.fna.whatsapp.net",                # 2:0xc1
    "media.fadb1-2.fna.whatsapp.net",                # 2:0xc2
    "media.fasu6-1.fna.whatsapp.net",                # 2:0xc3
    "media.fbog4-1.fna.whatsapp.net",                # 2:0xc4
    "media.fcgk9-2.fna.whatsapp.net",                # 2:0xc5
    "media.fdoh5-2.fna.whatsapp.net",                # 2:0xc6
    "media.ffjr1-2.fna.whatsapp.net",                # 2:0xc7
    "media.fgua1-1.fna.whatsapp.net",                # 2:0xc8
    "media.fgye1-1.fna.whatsapp.net",                # 2:0xc9
    "media.fist1-4.fna.whatsapp.net",                # 2:0xca
    "media.fpbc2-2.fna.whatsapp.net",                # 2:0xcb
    "media.fres2-1.fna.whatsapp.net",                # 2:0xcc
    "media.fsdq1-2.fna.whatsapp.net",                # 2:0xcd
    "media.fsub6-5.fna.whatsapp.net",                # 2:0xce
    "profilo_enabled",                               # 2:0xcf
    "template_hsm",                                  # 2:0xd0
    "use_disorder_prefetching_timer",                # 2:0xd1
    "video_codec_priority",                          # 2:0xd2
    "vpx_max_qp",                                    # 2:0xd3
    "ptt_reduce_recording_delay",                    # 2:0xd4
    "25",                                            # 2:0xd5
    "iphone",                                        # 2:0xd6
    "Windows",                                       # 2:0xd7
    "s_o",                                           # 2:0xd8
    "Africa/Lagos",                                  # 2:0xd9
    "abt",                                           # 2:0xda
    "media-kut2-1.cdn.whatsapp.net",                 # 2:0xdb
    "media-mba1-1.cdn.whatsapp.net",                 # 2:0xdc
    "media-mxp1-2.cdn.whatsapp.net",                 # 2:0xdd
    "md_blocklist_v2",                               # 2:0xde
    "url_text",                                      # 2:0xdf
    "enable_short_offset",                           # 2:0xe0
    "group_join_permissions",                        # 2:0xe1
    "enable_audio_piggyback_feature",                # 2:0xe2
    "image_quality",                                 # 2:0xe3
    "media.fcgk7-2.fna.whatsapp.net",                # 2:0xe4
    "media.fcgk8-2.fna.whatsapp.net",                # 2:0xe5
    "media.fclo7-1.fna.whatsapp.net",                # 2:0xe6
    "media.fcmn1-1.fna.whatsapp.net",                # 2:0xe7
    "media.feoh1-1.fna.whatsapp.net",                # 2:0xe8
    "media.fgyd4-3.fna.whatsapp.net",                # 2:0xe9
    "media.fjed4-4.fna.whatsapp.net",                # 2:0xea
    "media.flim1-4.fna.whatsapp.net",                # 2:0xeb
    "media.flim2-4.fna.whatsapp.net",                # 2:0xec
    "media.fplu6-1.fna.whatsapp.net",                # 2:0xed
    "media.frak1-1.fna.whatsapp.net",                # 2:0xee
    "media.fsdq1-1.fna.whatsapp.net",                # 2:0xef
    "to_ip",                                         # 2:0xf0
    "015",                                           # 2:0xf1
    "vp8",                                           # 2:0xf2
    "19",                                            # 2:0xf3
    "21",                                            # 2:0xf4
    "1320",                                          # 2:0xf5
    "auth_key_ver",                                  # 2:0xf6
    "message_processing_dedup",                      # 2:0xf7
    "server-error",                                  # 2:0xf8
    "wap4_enabled",                                  # 2:0xf9
    "420",                                           # 2:0xfa
    "014",                                           # 2:0xfb
    "cond_range_rtt",                                # 2:0xfc
    "ptt_fast_lock_enabled",                         # 2:0xfd
    "media-ort2-1.cdn.whatsapp.net",                 # 2:0xfe
    "fwd_ui_start_ts",                               # 2:0xff
],
[
    "contact_blacklist",                             # 3:0x00
    "Asia/Jakarta",                                  # 3:0x01
    "media.fepa10-1.fna.whatsapp.net",               # 3:0x02
    "media.fmex10-3.fna.whatsapp.net",               # 3:0x03
    "disorder_prefetching_start_when_empty",         # 3:0x04
    "America/Bogota",                                # 3:0x05
    "use_local_probing_rx_bitrate",                  # 3:0x06
    "America/Argentina/Buenos_Aires",                # 3:0x07
    "cross_post",                                    # 3:0x08
    "media.fabb1-1.fna.whatsapp.net",                # 3:0x09
    "media.fbog4-2.fna.whatsapp.net",                # 3:0x0a
    "media.fcgk9-1.fna.whatsapp.net",                # 3:0x0b
    "media.fcmn2-1.fna.whatsapp.net",                # 3:0x0c
    "media.fdel3-1.fna.whatsapp.net",                # 3:0x0d
    "media.ffjr1-1.fna.whatsapp.net",                # 3:0x0e
    "media.fgdl5-1.fna.whatsapp.net",                # 3:0x0f
    "media.flpb1-2.fna.whatsapp.net",                # 3:0x10
    "media.fmex2-1.fna.whatsapp.net",                # 3:0x11
    "media.frba2-2.fna.whatsapp.net",                # 3:0x12
    "media.fros2-2.fna.whatsapp.net",                # 3:0x13
    "media.fruh2-1.fna.whatsapp.net",                # 3:0x14
    "media.fybz2-2.fna.whatsapp.net",                # 3:0x15
    "options",                                       # 3:0x16
    "20",                                            # 3:0x17
    "a",                                             # 3:0x18
    "017",                                           # 3:0x19
    "018",                                           # 3:0x1a
    "mute_always",                                   # 3:0x1b
    "user_notice",                                   # 3:0x1c
    "Asia/Kolkata",                                  # 3:0x1d
    "gif_provider",                                  # 3:0x1e
    "locked",                                        # 3:0x1f
    "media-gua1-1.cdn.whatsapp.net",                 # 3:0x20
    "piggyback_exclude_force_flush",                 # 3:0x21
    "24",                                            # 3:0x22
    "media.frec39-1.fna.whatsapp.net",               # 3:0x23
    "user_remove",                                   # 3:0x24
    "file_max_size",                                 # 3:0x25
    "cond_packet_loss_pct_ema_alpha",                # 3:0x26
    "media.facc1-1.fna.whatsapp.net",                # 3:0x27
    "media.fadb2-1.fna.whatsapp.net",                # 3:0x28
    "media.faly3-1.fna.whatsapp.net",                # 3:0x29
    "media.fbdo6-2.fna.whatsapp.net",                # 3:0x2a
    "media.fcmn2-2.fna.whatsapp.net",                # 3:0x2b
    "media.fctg1-3.fna.whatsapp.net",                # 3:0x2c
    "media.ffez1-2.fna.whatsapp.net",                # 3:0x2d
    "media.fist1-3.fna.whatsapp.net",                # 3:0x2e
    "media.fist2-2.fna.whatsapp.net",                # 3:0x2f
    "media.flim2-2.fna.whatsapp.net",                # 3:0x30
    "media.fmct2-3.fna.whatsapp.net",                # 3:0x31
    "media.fpei3-1.fna.whatsapp.net",                # 3:0x32
    "media.frba3-1.fna.whatsapp.net",                # 3:0x33
    "media.fsdu8-2.fna.whatsapp.net",                # 3:0x34
    "media.fstu2-1.fna.whatsapp.net",                # 3:0x35
    "media_type",                                    # 3:0x36
    "receipt_agg",                                   # 3:0x37
    "016",                                           # 3:0x38
    "enable_pli_for_crc_mismatch",                   # 3:0x39
    "live",                                          # 3:0x3a
    "enc_rekey",                                     # 3:0x3b
    "frskmsg",                                       # 3:0x3c
    "d",                                             # 3:0x3d
    "media.fdel11-2.fna.whatsapp.net",               # 3:0x3e
    "proto",                                         # 3:0x3f
    "2250",                                          # 3:0x40
    "audio_piggyback_enable_cache",                  # 3:0x41
    "skip_nack_if_ltrp_sent",                        # 3:0x42
    "mark_dtx_jb_frames",                            # 3:0x43
    "web_service_delay",                             # 3:0x44
    "7282",                                          # 3:0x45
    "catalog_send_all",                              # 3:0x46
    "outgoing",                                      # 3:0x47
    "360",                                           # 3:0x48
    "30",                                            # 3:0x49
    "LIMITED",                                       # 3:0x4a
    "019",                                           # 3:0x4b
    "audio_picker",                                  # 3:0x4c
    "bpv2_phase",                                    # 3:0x4d
    "media.fada1-7.fna.whatsapp.net",                # 3:0x4e
    "media.faep7-1.fna.whatsapp.net",                # 3:0x4f
    "media.fbko1-2.fna.whatsapp.net",                # 3:0x50
    "media.fbni1-2.fna.whatsapp.net",                # 3:0x51
    "media.fbtz1-1.fna.whatsapp.net",                # 3:0x52
    "media.fbtz1-8.fna.whatsapp.net",                # 3:0x53
    "media.fcjs3-1.fna.whatsapp.net",                # 3:0x54
    "media.fesb3-2.fna.whatsapp.net",                # 3:0x55
    "media.fgdl5-4.fna.whatsapp.net",                # 3:0x56
    "media.fist2-1.fna.whatsapp.net",                # 3:0x57
    "media.flhe2-2.fna.whatsapp.net",                # 3:0x58
    "media.flim2-1.fna.whatsapp.net",                # 3:0x59
    "media.fmex1-1.fna.whatsapp.net",                # 3:0x5a
    "media.fpat3-2.fna.whatsapp.net",                # 3:0x5b
    "media.fpat3-3.fna.whatsapp.net",                # 3:0x5c
    "media.fros2-1.fna.whatsapp.net",                # 3:0x5d
    "media.fsdu8-1.fna.whatsapp.net",                # 3:0x5e
    "media.fsub3-2.fna.whatsapp.net",                # 3:0x5f
    "payments_chat_plugin",                          # 3:0x60
    "cond_congestion_no_rtcp_thr",                   # 3:0x61
    "green_alert",                                   # 3:0x62
    "not-a-biz",                                     # 3:0x63
    "..",                                            # 3:0x64
    "shops_pdp_urls_config",                         # 3:0x65
    "source",                                        # 3:0x66
    "media-dus1-1.cdn.whatsapp.net",                 # 3:0x67
    "mute_video",                                    # 3:0x68
    "01b",                                           # 3:0x69
    "currency",                                      # 3:0x6a
    "max_keys",                                      # 3:0x6b
    "resume_check",                                  # 3:0x6c
    "contact_array",                                 # 3:0x6d
    "qr_scanning",                                   # 3:0x6e
    "23",                                            # 3:0x6f
    "b",                                             # 3:0x70
    "media.fbfh15-1.fna.whatsapp.net",               # 3:0x71
    "media.flim22-1.fna.whatsapp.net",               # 3:0x72
    "media.fsdu11-1.fna.whatsapp.net",               # 3:0x73
    "media.fsdu15-1.fna.whatsapp.net",               # 3:0x74
    "Chrome",                                        # 3:0x75
    "fts_version",                                   # 3:0x76
    "60",                                            # 3:0x77
    "media.fada1-6.fna.whatsapp.net",                # 3:0x78
    "media.faep4-2.fna.whatsapp.net",                # 3:0x79
    "media.fbaq5-1.fna.whatsapp.net",                # 3:0x7a
    "media.fbni1-1.fna.whatsapp.net",                # 3:0x7b
    "media.fcai3-2.fna.whatsapp.net",                # 3:0x7c
    "media.fdel3-2.fna.whatsapp.net",                # 3:0x7d
    "media.fdmm3-2.fna.whatsapp.net",                # 3:0x7e
    "media.fhex3-1.fna.whatsapp.net",                # 3:0x7f
    "media.fisb4-2.fna.whatsapp.net",                # 3:0x80
    "media.fkhi5-2.fna.whatsapp.net",                # 3:0x81
    "media.flos2-1.fna.whatsapp.net",                # 3:0x82
    "media.fmct2-1.fna.whatsapp.net",                # 3:0x83
    "media.fntr7-1.fna.whatsapp.net",                # 3:0x84
    "media.frak3-1.fna.whatsapp.net",                # 3:0x85
    "media.fruh5-2.fna.whatsapp.net",                # 3:0x86
    "media.fsub6-1.fna.whatsapp.net",                # 3:0x87
    "media.fuab1-2.fna.whatsapp.net",                # 3:0x88
    "media.fuio1-1.fna.whatsapp.net",                # 3:0x89
    "media.fver1-1.fna.whatsapp.net",                # 3:0x8a
    "media.fymy1-1.fna.whatsapp.net",                # 3:0x8b
    "product_catalog",                               # 3:0x8c
    "1380",                                          # 3:0x8d
    "audio_oob_fec_max_pkts",                        # 3:0x8e
    "22",                                            # 3:0x8f
    "254",                                           # 3:0x90
    "media-ort2-2.cdn.whatsapp.net",                 # 3:0x91
    "media-sjc3-1.cdn.whatsapp.net",                 # 3:0x92
    "1600",                                          # 3:0x93
    "01a",                                           # 3:0x94
    "01c",                                           # 3:0x95
    "405",                                           # 3:0x96
    "key_frame_interval",                            # 3:0x97
    "body",                                          # 3:0x98
    "media.fcgh20-1.fna.whatsapp.net",               # 3:0x99
    "media.fesb10-2.fna.whatsapp.net",               # 3:0x9a
    "125",                                           # 3:0x9b
    "2000",                                          # 3:0x9c
    "media.fbsb1-1.fna.whatsapp.net",                # 3:0x9d
    "media.fcmn3-2.fna.whatsapp.net",                # 3:0x9e
    "media.fcpq1-1.fna.whatsapp.net",                # 3:0x9f
    "media.fdel1-2.fna.whatsapp.net",                # 3:0xa0
    "media.ffor2-1.fna.whatsapp.net",                # 3:0xa1
    "media.fgdl1-4.fna.whatsapp.net",                # 3:0xa2
    "media.fhex2-1.fna.whatsapp.net",                # 3:0xa3
    "media.fist1-2.fna.whatsapp.net",                # 3:0xa4
    "media.fjed5-2.fna.whatsapp.net",                # 3:0xa5
    "media.flim6-4.fna.whatsapp.net",                # 3:0xa6
    "media.flos2-2.fna.whatsapp.net",                # 3:0xa7
    "media.fntr6-2.fna.whatsapp.net",                # 3:0xa8
    "media.fpku3-2.fna.whatsapp.net",                # 3:0xa9
    "media.fros8-1.fna.whatsapp.net",                # 3:0xaa
    "media.fymy1-2.fna.whatsapp.net",                # 3:0xab
    "ul_bw",                                         # 3:0xac
    "ltrp_qp_offset",                                # 3:0xad
    "request",                                       # 3:0xae
    "nack",                                          # 3:0xaf
    "dtx_delay_state_reset",                         # 3:0xb0
    "timeoffline",                                   # 3:0xb1
    "28",                                            # 3:0xb2
    "01f",                                           # 3:0xb3
    "32",                                            # 3:0xb4
    "enable_ltr_pool",                               # 3:0xb5
    "wa_msys_crypto",                                # 3:0xb6
    "01d",                                           # 3:0xb7
    "58",                                            # 3:0xb8
    "dtx_freeze_hg_update",                          # 3:0xb9
    "nack_if_rpsi_throttled",                        # 3:0xba
    "253",                                           # 3:0xbb
    "840",                                           # 3:0xbc
    "media.famd15-1.fna.whatsapp.net",               # 3:0xbd
    "media.fbog17-2.fna.whatsapp.net",               # 3:0xbe
    "media.fcai19-2.fna.whatsapp.net",               # 3:0xbf
    "media.fcai21-4.fna.whatsapp.net",               # 3:0xc0
    "media.fesb10-4.fna.whatsapp.net",               # 3:0xc1
    "media.fesb10-5.fna.whatsapp.net",               # 3:0xc2
    "media.fmaa12-1.fna.whatsapp.net",               # 3:0xc3
    "media.fmex11-3.fna.whatsapp.net",               # 3:0xc4
    "media.fpoa33-1.fna.whatsapp.net",               # 3:0xc5
    "1050",                                          # 3:0xc6
    "021",                                           # 3:0xc7
    "clean",                                         # 3:0xc8
    "cond_range_ema_packet_loss_pct",                # 3:0xc9
    "media.fadb6-5.fna.whatsapp.net",                # 3:0xca
    "media.faqp4-1.fna.whatsapp.net",                # 3:0xcb
    "media.fbaq3-1.fna.whatsapp.net",                # 3:0xcc
    "media.fbel2-1.fna.whatsapp.net",                # 3:0xcd
    "media.fblr4-2.fna.whatsapp.net",                # 3:0xce
    "media.fclo8-1.fna.whatsapp.net",                # 3:0xcf
    "media.fcoo1-2.fna.whatsapp.net",                # 3:0xd0
    "media.ffjr1-4.fna.whatsapp.net",                # 3:0xd1
    "media.ffor9-1.fna.whatsapp.net",                # 3:0xd2
    "media.fisb3-1.fna.whatsapp.net",                # 3:0xd3
    "media.fkhi2-2.fna.whatsapp.net",                # 3:0xd4
    "media.fkhi4-1.fna.whatsapp.net",                # 3:0xd5
    "media.fpbc1-2.fna.whatsapp.net",                # 3:0xd6
    "media.fruh2-2.fna.whatsapp.net",                # 3:0xd7
    "media.fruh5-1.fna.whatsapp.net",                # 3:0xd8
    "media.fsub3-1.fna.whatsapp.net",                # 3:0xd9
    "payments_transaction_limit",                    # 3:0xda
    "252",                                           # 3:0xdb
    "27",                                            # 3:0xdc
    "29",                                            # 3:0xdd
    "tintagel",                                      # 3:0xde
    "01e",                                           # 3:0xdf
    "237",                                           # 3:0xe0
    "780",                                           # 3:0xe1
    "callee_updated_payload",                        # 3:0xe2
    "020",                                           # 3:0xe3
    "257",                                           # 3:0xe4
    "price",                                         # 3:0xe5
    "025",                                           # 3:0xe6
    "239",                                           # 3:0xe7
    "payments_cs_phone_number",                      # 3:0xe8
    "mediaretry",                                    # 3:0xe9
    "w:auth:backup:token",                           # 3:0xea
    "Glass.caf",                                     # 3:0xeb
    "max_bitrate",                                   # 3:0xec
    "240",                                           # 3:0xed
    "251",                                           # 3:0xee
    "660",                                           # 3:0xef
    "media.fbog16-1.fna.whatsapp.net",               # 3:0xf0
    "media.fcgh21-1.fna.whatsapp.net",               # 3:0xf1
    "media.fkul19-2.fna.whatsapp.net",               # 3:0xf2
    "media.flim21-2.fna.whatsapp.net",               # 3:0xf3
    "media.fmex10-4.fna.whatsapp.net",               # 3:0xf4
    "64",                                            # 3:0xf5
    "33",                                            # 3:0xf6
    "34",                                            # 3:0xf7
    "35",                                            # 3:0xf8
    "interruption",                                  # 3:0xf9
    "media.fabv3-1.fna.whatsapp.net",                # 3:0xfa
    "media.fadb6-1.fna.whatsapp.net",                # 3:0xfb
    "media.fagr1-1.fna.whatsapp.net",                # 3:0xfc
    "media.famd1-1.fna.whatsapp.net",                # 3:0xfd
    "media.famm6-1.fna.whatsapp.net",                # 3:0xfe
    "media.faqp2-3.fna.whatsapp.net",                # 3:0xff
]
]

DICTIONARY0 = 0xec
DICTIONARY1 = 0xed
DICTIONARY2 = 0xee
DICTIONARY3 = 0xef
# f0 - f5 : unused
FBJID       = 0xf6  # string, int16, string
ADJID       = 0xf7  # byte, byte, string
LIST8       = 0xf8  # listsize:int8,  [ ... ]
LIST16      = 0xf9  # listsize:int16, [ ... ]
JIDPAIR     = 0xfa  # opt-string, string
HEX8        = 0xfb
BINARY8     = 0xfc  # bytesize:int8,   "..."
BINARY20    = 0xfd  # bytesize
BINARY32    = 0xfe  # bytesize:int32,   "..."
NIBBLE8     = 0xff


def decode(data):
    class AgentDeviceJid:
        def __init__(self):
            self.agent = None
            self.device = None
            self.user = None
        def add(self, x):
            if self.user is None:
                self.user = x
            else:
                raise Exception("full")
        def full(self): return self.user is not None
        def __repr__(self): return f"ADJID<{self.agent};{self.device};{self.user}>"
    class JidPair:
        def __init__(self):
            self.user = None
            self.server = None
        def add(self, x):
            if self.user is None:
                self.user = x
            elif self.server is None:
                self.server = x
            else:
                raise Exception("full")
        def full(self): return self.server is not None
        def __repr__(self): return f"JID<{self.user};{self.server}>"
    class FacebookJid:
        def __init__(self):
            self.fbid = None
            self.device = None
            self.wadomain = None
        def add(self, x):
            if self.fbid is None:
                self.fbid = x
            elif self.device is None:
                self.device = x
            elif self.wadomain is None:
                self.wadomain = x
            else:
                raise Exception("full")
        def full(self): return self.wadomain is not None
        def __repr__(self): return f"FBID<{self.fbid};{self.num};{self.wadomain}>"
    class String:
        # this escapes [] in binary strings, so [] stay balanced in the output.
        def __init__(self, data):
            self.data = data
        #ef add(self, x):
        #   raise Exception("full")
        #ef full(self): return True
        def __repr__(self): return re.sub(r'[\[\]]', lambda m:"\\x%02x" % ord(m[0]), str(self.data))
    class List:
        def __init__(self, n):
            self.n = n
            self.l = []
        def add(self, x):
            if not self.full():
                self.l.append(x)
            else:
                raise Exception("full")
        def full(self): return self.n == len(self.l)
        def __repr__(self): return "[" + ",".join(repr(_) for _ in self.l) + "]"

    def decodeHex(data):
        # 0-9 a-f
        return tohex(data)
    def decodeNibble(data):
        # 0-9 - . x x x \0 
        return tohex(data).replace('a', '-').replace('b', '.')
    stack = []
    r = DataReader(data)
    while not r.eof():
        b = r.readbyte()
        if DICTIONARY0 <= b <= DICTIONARY3:
            n = r.readbyte()
            item = DoubleByteTokens[b-DICTIONARY0][n]
        elif b == FBJID:
            item = FacebookJid()
        elif b == ADJID:
            item = AgentDeviceJid()
            item.agent = r.readbyte()
            item.device = r.readbyte()
        elif b == LIST8:
            n = r.readbyte()
            item = List(n)
        elif b == LIST16:
            n = r.read16le()
            item = List(n)
        elif b == JIDPAIR:
            item = JidPair()
        elif b == HEX8:
            n = r.readbyte()
            item = decodeHex(r.read(n&127))
            if n&128:
                item = item[:-1]
        elif b == BINARY8:
            n = r.readbyte()
            item = String(r.read(n))
        elif b == BINARY20:
            n = r.read24be()
            item = String(r.read(n))
        elif b == BINARY32:
            n = r.read32le()
            item = String(r.read(n))
        elif b == NIBBLE8:
            n = r.readbyte()
            item = decodeNibble(r.read(n&127))
            if n&128:
                item = item[:-1]
        elif b < len(SingleByteTokens):
            item = SingleByteTokens[b]
        else:
            raise Exception("invalid token")

        if not stack:
            stack.append(item)
        else:
            stack[-1].add(item)

        # special case: FBJID
        if isinstance(stack[-1], FacebookJid) and stack[-1].needsint():
            stack[-1].add(r.read16le())

        if hasattr(item, 'full'):
            stack.append(item)
        else:
            while len(stack)>1 and stack[-1].full():
                stack.pop()
    if not stack:
        raise Exception("empty stack")
    if len(stack)>1:
        raise Exception("too many items")
    if not stack[0].full():
        print("WARN: not complete")
    return stack.pop()

# todo:
#   nodes are encoded like this:
#   tag, attrs:(key, value...), content[optional]

def main():
    import sys
    for line in sys.stdin:
        if m := re.match(r'^(\W+)(\w.*)', line):
            print(m[1], decode(unhex(m[2])))
        elif m := re.match(r'^([0-9a-f ]+)\s*$', line):
            print("=", decode(unhex(m[1])))
        else:
            print("?", line.rstrip("\n"))
if __name__=='__main__':
    main()
