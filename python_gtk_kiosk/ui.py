"""
App main UI module.
"""

from logging import getLogger

from pkg_resources import resource_filename


log = getLogger(__name__)


class AppUI:

    def __init__(self, kiosk):

        # Load font directory first so they are ready when the UI and CSS
        # provider are loaded
        self._load_fonts()

        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, GLib, Gdk

        self._mainloop = GLib.MainLoop()

        # Build GUI from Glade file
        self._builder = Gtk.Builder()
        self._builder.add_from_file(
            resource_filename(__package__, 'data/ui.glade')
        )

        # Setup style provider to use CSS
        style_provider = Gtk.CssProvider()
        style_provider.load_from_path(
            resource_filename(__package__, 'data/assets/style.css')
        )
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Get objects
        def go(identifier):
            widget = self._builder.get_object(identifier)
            if widget is None:
                raise ValueError('Widget "{}" not found'.format(identifier))

            return widget

        self._window = go('window')

        # UI elements
        self._dialog = go('my_dialog')

        # Connect signals
        self._builder.connect_signals(self)

        # Configure interface
        self._window.connect('destroy', self._mainloop.quit)

        # Set fullscreen or windowed
        if kiosk:
            screen = Gdk.Screen.get_default()
            self._window.set_size_request(
                screen.get_width(), screen.get_height()
            )
        else:
            # Default development size
            self._window.set_default_size(800, 480)

        # Everything is ready
        self._window.show()

    def _load_fonts(self):
        from ctypes import cdll, c_int, c_void_p, c_char_p

        self._fontconfig = cdll.LoadLibrary('libfontconfig.so.1')

        config = self._fontconfig.FcConfigReference(
            self._fontconfig.FcConfigGetCurrent()
        )

        self._fontconfig.FcConfigAppFontAddDir.restype = c_int
        self._fontconfig.FcConfigAppFontAddDir.argtypes = (c_void_p, c_char_p)

        # By adding assets/fonts we make sure that in the CSS file we can use
        # any of the fonts included in that dir
        fontdir = resource_filename(__package__, 'data/assets/fonts')
        self._fontconfig.FcConfigAppFontAddDir(config, fontdir.encode())

    def _show_dialog_cb(self, widget, data=None):
        self._dialog.show()

    def _close_dialog_cb(self, widget, data=None):
        self._dialog.hide()

    def start(self):
        try:
            self._mainloop.run()
        except KeyboardInterrupt:
            log.info('Ctrl+C hit, quitting ...')
            self.stop()

    def stop(self):
        self._mainloop.quit()


__all__ = [
    'AppUI',
]
