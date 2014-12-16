import os, subprocess
from gi.repository import Nautilus, GObject, GConf, Gtk, GLib
from gettext import gettext, locale, bindtextdomain, textdomain

ROOT_UID=0
WARNING_DISPLAYED_FILENAME='.nautilus-admin-warning-displayed'

class NautilusAdmin(Nautilus.MenuProvider, GObject.GObject):
	def __init__(self):
		self.client = GConf.Client.get_default()

	def get_file_items(self, window, files):
		if os.getuid() == ROOT_UID: # don't show when already running as root
			return
		if len(files) != 1:
			return
		file = files[0]
		if not file.is_directory() or file.get_uri_scheme() != 'file':
			return
		self._setup_gettext();
		item = Nautilus.MenuItem(name='NautilusAdmin::Nautilus',
		                         label=gettext('Open as Administrator'),
		                         tip=gettext('Open this folder as administrator'))
		item.connect('activate', self._nautilus_run, file)
		return (item, )

	def get_background_items(self, window, file):
		if os.getuid() == ROOT_UID: # don't show when already running as root
			return
		if not file.is_directory() or file.get_uri_scheme() != 'file':
			return
		self._setup_gettext();
		item = Nautilus.MenuItem(name='NautilusAdmin::Nautilus',
		                         label=gettext('Open as Administrator'),
		                         tip=gettext('Open this folder as administrator'))
		item.connect('activate', self._nautilus_run, file)
		return (item, )

	def _setup_gettext(self):
		locale.setlocale(locale.LC_ALL, '')
		bindtextdomain('nautilus-admin', '@CMAKE_INSTALL_PREFIX@/share/locale')
		textdomain('nautilus-admin')

	def _nautilus_run(self, menu, file):
		conf_dir = GLib.get_user_config_dir()
		conf_file = os.path.join(conf_dir, WARNING_DISPLAYED_FILENAME)
		if not os.path.exists(conf_file):
			dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
				                                Gtk.ButtonsType.OK_CANCEL,
				                                "Open folder as Administrator")
			msg = gettext('Running the File Manager as Administrator (<i>root</i> user) is <b>dangerous</b>!\n'
				          'Proceed only if you know what you are doing!')
			dialog.format_secondary_markup(msg)
			response = dialog.run()
			dialog.destroy()
			if response == Gtk.ResponseType.OK:
				if not os.path.isdir(conf_dir):
					os.makedirs(conf_dir)
				open(conf_file, 'w').close()
			else:
				return
			
		uri = file.get_uri()
		subprocess.Popen(['/usr/bin/pkexec', '/usr/bin/nautilus', '--no-desktop', uri])
