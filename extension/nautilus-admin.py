import os, subprocess
from gi.repository import Nautilus, GObject, GConf

#TODO: show a warning on first use
#TODO: localization

ROOT_UID=0

class NautilusAdmin(Nautilus.MenuProvider, GObject.GObject):
	def __init__(self):
		self.client = GConf.Client.get_default()

	def nautilus_run(self, menu, file):
		uri = file.get_uri()
		subprocess.Popen(['@CMAKE_INSTALL_PREFIX@/bin/nautilus-pkexec', uri])

	def get_file_items(self, window, files):
		if os.getuid() == ROOT_UID: # don't show when already running as root
			return
		if len(files) != 1:
			return
		file = files[0]
		if not file.is_directory() or file.get_uri_scheme() != 'file':
			return
		item = Nautilus.MenuItem(name='NautilusAdmin::Nautilus',
		                         label='Open as Administrator',
		                         tip='Open this folder as administrator')
		item.connect('activate', self.nautilus_run, file)
		return (item, )

	def get_background_items(self, window, file):
		if os.getuid() == ROOT_UID: # don't show when already running as root
			return
		if not file.is_directory() or file.get_uri_scheme() != 'file':
			return
		item = Nautilus.MenuItem(name='NautilusAdmin::Nautilus',
		                         label='Open as Administrator',
		                         tip='Open this folder as administrator')
		item.connect('activate', self.nautilus_run, file)
		return (item, )
