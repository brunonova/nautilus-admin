import os, subprocess
from gi.repository import Nautilus, GObject, GConf, Gtk, GLib
from gettext import gettext, locale, bindtextdomain, textdomain

ROOT_UID = 0
WARNING_DISPLAYED_FILENAME = ".nautilus-admin-warning-displayed"

class NautilusAdmin(Nautilus.MenuProvider, GObject.GObject):
	"""Simple Nautilus extension that adds an 'Open as Administrator' item to
	the right-click menu, which opens the selected folder as root in Nautilus
	using 'pkexec'."""
	def __init__(self):
		pass

	def get_file_items(self, window, files):
		# Don't show when already running as root, or when more than 1 file is selected
		if os.geteuid() == ROOT_UID or len(files) != 1:
			return
		file = files[0]

		# file must be a local directory
		if not file.is_directory() or file.get_uri_scheme() != "file":
			return

		# Create the menu item
		self._setup_gettext();
		item = Nautilus.MenuItem(name="NautilusAdmin::Nautilus",
		                         label=gettext("Open as Administrator"),
		                         tip=gettext("Open this folder as administrator"))
		item.connect("activate", self._nautilus_run, file)
		return (item, )

	def get_background_items(self, window, file):
		# Don't show when already running as root
		if os.geteuid() == ROOT_UID:
			return

		# file must be a local directory
		if not file.is_directory() or file.get_uri_scheme() != "file":
			return

		# Create the menu item
		self._setup_gettext();
		item = Nautilus.MenuItem(name="NautilusAdmin::Nautilus",
		                         label=gettext("Open as Administrator"),
		                         tip=gettext("Open this folder as administrator"))
		item.connect("activate", self._nautilus_run, file)
		return (item, )

	def _nautilus_run(self, menu, file):
		"""'Open as Administrator' menu item callback."""
		# Show a warning dialog when first executed (by checking the file
		# WARNING_DISPLAYED_FILENAME in ~/.config)
		conf_dir = GLib.get_user_config_dir()
		conf_file = os.path.join(conf_dir, WARNING_DISPLAYED_FILENAME)
		if not os.path.exists(conf_file):
			dialog = Gtk.MessageDialog(None, 0, Gtk.MessageType.WARNING,
				                                Gtk.ButtonsType.OK_CANCEL,
				                                "Open folder as Administrator")
			msg = gettext("Running the File Manager as Administrator (<i>root</i> user) is <b>dangerous</b>!\n"
				          "Proceed only if you know what you are doing!")
			dialog.format_secondary_markup(msg)
			response = dialog.run()
			dialog.destroy()

			# Create WARNING_DISPLAYED_FILENAME to mark the dialog as displayed
			if response == Gtk.ResponseType.OK:
				try:
					if not os.path.isdir(conf_dir):
						os.makedirs(conf_dir)
					open(conf_file, "w").close() # create an empty file
				except:
					pass
			else:
				return

		# Open file in Nautilus as root
		uri = file.get_uri()
		subprocess.Popen(["/usr/bin/pkexec", "/usr/bin/nautilus", "--no-desktop", uri])

	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		locale.setlocale(locale.LC_ALL, "")
		bindtextdomain("nautilus-admin", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-admin")
