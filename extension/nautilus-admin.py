# Copyright (c) 2015 Bruno Nova <brunomb.nova@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os, subprocess
from gi.repository import Nautilus, GObject
from gettext import gettext, locale, bindtextdomain, textdomain

ROOT_UID = 0
PKEXEC_PATH="@PKEXEC_PATH@"
NAUTILUS_PATH="@NAUTILUS_PATH@"
GEDIT_PATH="@GEDIT_PATH@"

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
		if file.get_uri_scheme() == "file": # must be a local file/directory
			if file.is_directory():
				if os.path.exists(NAUTILUS_PATH):
					items += [self._create_nautilus_item(file)]
			else:
				if os.path.exists(GEDIT_PATH):
					items += [self._create_gedit_item(file)]

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
			if os.path.exists(NAUTILUS_PATH):
				items += [self._create_nautilus_item(file)]

		return items


	def _setup_gettext(self):
		"""Initializes gettext to localize strings."""
		try: # prevent a possible exception
			locale.setlocale(locale.LC_ALL, "")
		except:
			pass
		bindtextdomain("nautilus-admin", "@CMAKE_INSTALL_PREFIX@/share/locale")
		textdomain("nautilus-admin")

	def _create_nautilus_item(self, file):
		"""Creates the 'Open as Administrator' menu item."""
		item = Nautilus.MenuItem(name="NautilusAdmin::Nautilus",
		                         label=gettext("Open as Administrator"),
		                         tip=gettext("Open this folder with root privileges"))
		item.connect("activate", self._nautilus_run, file)
		return item

	def _create_gedit_item(self, file):
		"""Creates the 'Edit as Administrator' menu item."""
		item = Nautilus.MenuItem(name="NautilusAdmin::Gedit",
		                         label=gettext("Edit as Administrator"),
		                         tip=gettext("Open this file in the text editor with root privileges"))
		item.connect("activate", self._gedit_run, file)
		return item


	def _nautilus_run(self, menu, file):
		"""'Open as Administrator' menu item callback."""
		uri = file.get_uri()
		subprocess.Popen([PKEXEC_PATH, NAUTILUS_PATH, "--no-desktop", uri])

	def _gedit_run(self, menu, file):
		"""'Edit as Administrator' menu item callback."""
		uri = file.get_uri()
		subprocess.Popen([PKEXEC_PATH, GEDIT_PATH, uri])
