#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio
import mimetypes
entity = 'AudioTube_bot' #имя сессии - все равно какое
api_id = 1959
api_hash = '88b68d6da53fe68c1c3541bbefc'
phone =  '+79620181488'
client = TelegramClient(entity, api_id, api_hash, update_workers=None, spawn_read_thread=False)
client.connect()
if not client.is_user_authorized():
    # client.send_code_request(phone) #при первом запуске - раскомментить, после авторизации для избежания FloodWait советую закомментить
    client.sign_in(phone, input('Enter code: '))
client.start()
def main(argv):
    file_path = argv[1]
    file_name = argv[2]
    chat_id = argv[3]
    object_id = argv[4]
    bot_name = argv[5]
    duration = argv[6]
    mimetypes.add_type('audio/aac','.aac')
    mimetypes.add_type('audio/ogg','.ogg')
    msg = client.send_file(
                           str(bot_name),
                           file_path,
                           caption=str(chat_id + ':' + object_id + ':' + duration),
                           file_name=str(file_name),
                           use_cache=False,
                           part_size_kb=512,
                           attributes=[DocumentAttributeAudio(
                                                      int(duration),
                                                      voice=None,
                                                      title=file_name[:-4],
                                                      performer='')]
                           )
    client.disconnect()
    return 0

if __name__ == '__main__':
    import sys
    main(sys.argv[0:])