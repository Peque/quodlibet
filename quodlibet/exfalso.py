#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright 2004-2005 Joe Wreschnig, Niklas Janlert
#           2012 Christoph Reiter
# <quod-libet-development@googlegroups.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import os

from quodlibet import app
from quodlibet import util
from quodlibet import const
from quodlibet import config
from quodlibet.senf import fsnative, argv


def main(argv):
    import quodlibet
    quodlibet.init()

    from quodlibet.qltk import add_signal_watch, Icons
    add_signal_watch(app.quit)

    opts = util.OptionParser(
        "Ex Falso", const.VERSION,
        _("an audio tag editor"), "[%s]" % _("directory"))

    argv.append(os.path.abspath(fsnative(u".")))
    opts, args = opts.parse(argv[1:])
    args[0] = os.path.realpath(args[0])

    config.init(os.path.join(quodlibet.get_user_dir(), "config"))

    app.name = "Ex Falso"
    app.id = "exfalso"
    quodlibet.set_application_info(Icons.EXFALSO, app.id, app.name)

    import quodlibet.library
    import quodlibet.player
    app.library = quodlibet.library.init()
    app.player = quodlibet.player.init_player("nullbe", app.librarian)
    from quodlibet.qltk.songlist import PlaylistModel
    app.player.setup(PlaylistModel(), None, 0)
    pm = quodlibet.init_plugins()
    pm.rescan()

    from quodlibet.qltk.exfalsowindow import ExFalsoWindow
    dir_ = args[0]
    app.window = ExFalsoWindow(app.library, dir_)
    app.window.init_plugins()

    from quodlibet.util.cover import CoverManager
    app.cover_manager = CoverManager()
    app.cover_manager.init_plugins()

    from quodlibet.qltk import session
    session.init("exfalso")

    quodlibet.enable_periodic_save(save_library=False)
    quodlibet.main(app.window)
    quodlibet.finish_first_session(app.id)
    config.save()

    util.print_d("Finished shutdown.")


if __name__ == "__main__":
    main(argv)
