import os, subprocess
from gi.repository import Nautilus, GObject, GConf, Gtk, GLib
from gettext import gettext, locale, bindtextdomain, textdomain

ROOT_UID = 0

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
		                         tip=gettext("Open this folder with root privileges"))
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
		                         tip=gettext("Open this folder with root privileges"))
		item.connect("activate", self._nautilus_run, file)
		return (item, )

	def _nautilus_run(self, menu, file):
		"""'Open as Administrator' menu item callback."""
		uri = file.get_uri()
		subprocess.Popen(["/usr/bin/pkexec", "/usr/bin/nautilus", "--no-desktop", uri])

	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		locale.setlocale(locale.LC_ALL, "")
		bindtextdomain("nautilus-admin", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-admin")
