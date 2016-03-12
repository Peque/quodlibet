# -*- coding: utf-8 -*-
# Copyright 2005 Joe Wreschnig
#           2016 Nick Boultbee
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import mutagen.apev2

from quodlibet.formats._apev2 import APEv2File
from quodlibet.plugins.songshelpers import each_song, is_writable
from quodlibet.plugins.songsmenu import SongsMenuPlugin


def is_an_mp3(song):
    return song.get("~filename", "").lower().endswith(".mp3")


class APEv2toID3v2(SongsMenuPlugin):
    PLUGIN_ID = "APEv2 to ID3v2"
    PLUGIN_NAME = _("APEv2 to ID3v2")
    PLUGIN_DESC = _("Converts your APEv2 tags to ID3v2 tags. This will delete "
                    "the APEv2 tags after conversion.")

    plugin_handles = each_song(is_an_mp3, is_writable)

    def plugin_song(self, song):
        try:
            apesong = APEv2File(song["~filename"])
        except:
            return # File doesn't have an APEv2 tag
        song.update(apesong)
        mutagen.apev2.delete(song["~filename"])
        song._song.write()
