import os, urllib, subprocess
from gi.repository import Nautilus, GObject, GConf

#TODO: show a warning on first use
#TODO: localization

class NautilusAdmin(Nautilus.MenuProvider, GObject.GObject):
	def __init__(self):
		self.client = GConf.Client.get_default()

	def nautilus_run(self, menu, url):
		filename = urllib.unquote(url.get_uri()[7:])
		subprocess.Popen(["@CMAKE_INSTALL_PREFIX@/bin/nautilus-pkexec", filename])

	def get_file_items(self, window, files):
		if(len(files) == 1):
			file = files[0]
			if not file.is_directory() or file.get_uri_scheme() != 'file':
				return
			item = Nautilus.MenuItem(name='NautilusAdmin::Nautilus', label='Open as Root', tip='Open as Root user')
			item.connect('activate', self.nautilus_run, file)
			return (item, )

	def get_background_items(self, window, file):
		item = Nautilus.MenuItem(name='NautilusAdmin::Nautilus', label='Open as Root', tip='Open as Root user')
		item.connect('activate', self.nautilus_run, file)
		return (item, )
