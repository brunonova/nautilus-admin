import os, subprocess
from gi.repository import Nautilus, GObject, GConf, Gtk, GLib
from gettext import gettext, locale, bindtextdomain, textdomain

ROOT_UID = 0

class NautilusAdmin(Nautilus.MenuProvider, GObject.GObject):
	"""Simple Nautilus extension that adds some administrative (root) actions to
	the right-click menu, using 'pkexec' to authenticate the administrator."""
	def __init__(self):
		pass

	def get_file_items(self, window, files):
		"""Returns the menu items to display when one or more files/folders are
		selected."""
		# Don't show when already running as root, or when more than 1 file is selected
		if os.geteuid() == ROOT_UID or len(files) != 1:
			return
		file = files[0]

		# Add the menu items
		items = []
		self._setup_gettext();
		if file.is_directory() and file.get_uri_scheme() == "file":
			items += [self._create_nautilus_item(file)]

		return items

	def get_background_items(self, window, file):
		"""Returns the menu items to display when no file/folder is selected
		(i.e. when right-clicking the background)."""
		# Don't show when already running as root
		if os.geteuid() == ROOT_UID:
			return

		# Add the menu items
		items = []
		self._setup_gettext();
		if file.is_directory() and file.get_uri_scheme() == "file":
			items += [self._create_nautilus_item(file)]

		return items


	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		locale.setlocale(locale.LC_ALL, "")
		bindtextdomain("nautilus-admin", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-admin")

	def _create_nautilus_item(self, file):
		"""Creates the 'Open as Administrator' menu item."""
		item = Nautilus.MenuItem(name="NautilusAdmin::Nautilus",
		                         label=gettext("Open as Administrator"),
		                         tip=gettext("Open this folder with root privileges"))
		item.connect("activate", self._nautilus_run, file)
		return item


	def _nautilus_run(self, menu, file):
		"""'Open as Administrator' menu item callback."""
		uri = file.get_uri()
		subprocess.Popen(["/usr/bin/pkexec", "/usr/bin/nautilus", "--no-desktop", uri])
