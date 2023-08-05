#
# Copyright 2018 Martin Owens <doctormo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#
"""Gtk 3+ Inkscape 1.0 Extensions Manager GUI."""

import os
import sys
import webbrowser

from gtkme import Window, ChildWindow, TreeView, asyncme
from gtkme.pixmap import PixmapManager
from gtkme.main import Gtk

from ..utils import DATA_DIR, INKSCAPE_PROFILE
from ..remote import RemoteArchive
from .. import __state__

def tag(name, color='#EFEFEF', fgcolor='#333333'):
    return f'<span size=\'small\' font_family=\'monospace\' style=\'italic\' background=\'{color}\' foreground=\'{fgcolor}\'> {name} </span> '

class LocalTreeView(TreeView):
    """A List of locally installed packages"""
    def __init__(self, target, widget, *args, **kwargs):
        self._target = target
        self._pixmaps = kwargs['pixmaps']
        self._version = kwargs.pop('version', None)

        style = widget.get_style_context()
        self._fg_color = style.get_color(Gtk.StateFlags.NORMAL)
        #self._bg_color = style.get_property('background-color', Gtk.StateFlags.NORMAL)

        super().__init__(widget, *args, **kwargs)

    def get_name(self, item):
        #color = self._style.get_property('color', Gtk.StateFlags.NORMAL)
        return f"<big><b>{item.name}</b></big>\n<i>{item.summary}</i>"

    def get_icon(self, item):
        try:
            return self._pixmaps.get(item.get_icon(), '')
        except Exception:
            return ''

    def ViewColumn(self, *args, **kwargs):
        """Over-ride the default colors, as they are often wrong"""
        col = super().ViewColumn(*args, **kwargs)
        col._text_renderer.set_property("foreground-rgba", self._fg_color)
        # This is detected as black for remote treeview, we're not sure why
        #col._text_renderer.set_property("background-rgba", self._bg_color)
        return col

    def setup(self, *args, **kwargs):
        """Setup the treeview with one or many columns manually"""
        def get_version(item):
            if item.version:
                return f"<i>{item.version}</i>"

        col = self.ViewColumn('Extensions Package', expand=True,\
            text=self.get_name, template=None,\
            icon=self.get_icon,
            pad=0, size=None)

        col._icon_renderer.set_property('ypad', 2) # pylint: disable=protected-access
        col._text_renderer.set_property('xpad', 8) # pylint: disable=protected-access

        self.ViewColumn('Version', expand=False, text=get_version, template=None, pad=6)
        self.ViewColumn('Author', expand=False, text='author', pad=6)

        if self._target.version_specific:
            self.ViewColumn('Inkscape', expand=False, text='target', pad=6)

        self.ViewSort(data=lambda item: item.name, ascending=True, contains='name')

class RemoteTreeView(LocalTreeView):
    """A List of remote packages for installation"""
    def get_installed(self, item):
        if item.installed is None:
            item.set_installed(False)
            for installed_item in self._target.list_installed():
                if item.ident == installed_item.ident:
                    item.set_installed(True)
        return bool(item.installed)

    def setup(self, *args, **kwargs):
        def get_star(item):
            star = 'star-none.svg'
            if item.stars > 10:
                star = 'star-lots.svg'
            elif item.stars > 1:
                star = 'star-some.svg'
            return self._pixmaps.get(star)

        def get_sort(item):
            if not item.verified:
                return -100 + item.stars
            if self._version not in item.targets:
                return -20 + item.stars
            return item.stars + (1000 * int(item.recommended))

        super().setup(*args, **kwargs)
        self.ViewColumn('Stars', expand=True, text='stars', pad=0, size=16, icon=get_star)
        self.ViewSort(data=get_sort, ascending=True)

    def get_name(self, item):
        summary = item.summary
        if self.get_installed(item):
            summary = tag("Installed", "#37943e", "white") + summary.strip()
        elif not item.verified:
            summary = tag("Unverified", "#CB0000", "white") + summary.strip()
        elif self._version not in item.targets:
            targets = item.targets or ['No Inkscape Versions']
            summary = ''.join([tag(t, "#00CB00", "white") for t in targets])\
                + summary.strip()
        else:
            summary = tag("Verified", "#37943e", "white") \
                + tag(self._version, "#37943e", "white") \
                + summary.strip()

        return f"<big><b>{item.name}</b></big>\n<i>{summary}</i>\n" + \
            ''.join(tag(t) for t in item.tags)

class ExtensionManagerWindow(Window):
    name = 'gui'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = self.gapp.opt.target
        self._version = self.gapp.opt.version

        self.pixmaps = PixmapManager('pixmaps', pixmap_dir=DATA_DIR, size=48, load_size=(96,96))
        self.searching = self.widget('dl-searching')
        self.searchbox = self.searching.get_parent()
        self.searchbox.remove(self.searching)

        self.local = LocalTreeView(
            self.target,
            self.widget('local_extensions'),
            version=self._version,
            pixmaps=self.pixmaps,
            selected=self.select_local)

        self.remote = RemoteTreeView(
            self.target,
            self.widget('remote_extensions'),
            version=self._version,
            pixmaps=self.pixmaps,
            selected=self.select_remote)

        self.widget('loading').start()
        self.window.show_all()
        self.window.present()
        #self.window.set_keep_above(True)

        self.refresh_local()
        self.widget('remote_install').set_sensitive(False)
        self.widget('remote_info').set_sensitive(False)
        self.widget('local_install').set_sensitive(True)
        self.window.set_title(self.target.label + f" ({self._version}) - {__state__}")

        if not self.target.is_search:
            self.widget('remote_getlist').show()
            self.widget('dl-search').hide()
        else:
            self.widget('dl-search').show()
            self.widget('remote_getlist').hide()
        self.widget('no_results').hide()

        # Get a tasting of items from the server
        self._remote_search(None)

    def remote_getlist(self, widget):
        self._remote_search('')

    @asyncme.run_or_none
    def refresh_local(self):
        """Searches for locally installed extensions and adds them"""
        self.local.clear()
        self.widget('local_uninstall').set_sensitive(False)
        self.widget('local_information').set_sensitive(False)

        all_packages = []
        for item in self.target.list_installed(cached=False):
            self.local.add_item([item])
        self.widget('loading').stop()

    def select_local(self, item):
        """Select an installed extension"""
        self.widget('local_uninstall').set_sensitive(item.is_uninstallable())
        self.widget('local_information').set_sensitive(bool(item))

    def local_information(self, widget):
        """Show the more information window"""
        if self.local.selected:
            self.load_window('info', pixmaps=self.pixmaps, item=self.local.selected)

    def local_uninstall(self, widget):
        """Uninstall selected extection package"""
        item = self.local.selected
        if item.is_uninstallable():
            if item.uninstall():
                self.local.remove_item(item)
                self.remote.refresh()

    def change_remote_all(self, widget, unk):
        """When the source switch button is clicked"""
        self.remote_search(self.widget('dl-search'))

    def remote_search(self, widget):
        """Remote search activation"""
        query = widget.get_text()
        if len(query) > 2:
            self._remote_search(query)

    def _remote_search(self, query):
        filtered = False #self.widget('remote_target').get_active()
        self.remote.clear()
        self.widget('no_results').hide()
        self.widget('results_found').show()
        self.widget('remote_install').set_sensitive(False)
        self.widget('remote_info').set_sensitive(False)
        self.widget('dl-search').set_sensitive(False)
        self.searchbox.add(self.searching)
        self.widget('dl-searching').start()
        self.async_search(query, filtered)

    def remote_info(self, widget):
        """Show the remote information"""
        if self.remote.selected and self.remote.selected.link:
            webbrowser.open(self.remote.selected.link)

    @asyncme.run_or_none
    def async_search(self, query, filtered):
        """Asyncronous searching in PyPI"""
        for package in self.target.search(query, filtered):
            self.add_search_result(package)
        self.search_finished()

    @asyncme.mainloop_only
    def add_search_result(self, package):
        """Adding things to Gtk must be done in mainloop"""
        self.remote.add_item([package])

    @asyncme.mainloop_only
    def search_finished(self):
        """After everything, finish the search"""
        self.searchbox.remove(self.searching)
        self.widget('dl-search').set_sensitive(True)
        self.replace(self.searching, self.remote)
        if not self.remote._model.iter_n_children():
            self.widget('no_results').show()
            self.widget('results_found').hide()

    def select_remote(self, item):
        """Select an installed extension"""
        # Do we have a place to install packages to?
        active = self.remote.selected \
            and self.remote.selected.is_installable(self._version) \
            and not self.remote.selected.installed
        self.widget('remote_install').set_sensitive(active)
        if self.remote.selected.link:
            self.widget('remote_info').set_sensitive(True)

    def remote_install(self, widget):
        """Install a remote package"""
        self.widget('remote_install').set_sensitive(False)
        item = self.remote.selected
        try:
            item.install()
        except Exception as err:
            self.dialog(str(err))
            return
        self.remote.refresh()
        self.refresh_local()
        self.widget('main_notebook').set_current_page(0)

    def local_install(self, widget):
        """Install from a local filename"""
        dialog = Gtk.FileChooserDialog(
            title="Please choose a package file", transient_for=self.window,
            action=Gtk.FileChooserAction.OPEN)

        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK)

        filter_py = Gtk.FileFilter()
        filter_py.set_name("Packages")
        filter_py.add_mime_type("application/x-compressed-tar")
        filter_py.add_mime_type("application/zip")
        dialog.add_filter(filter_py)

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Python Wheel")
        filter_text.add_mime_type("application/zip")
        filter_text.add_pattern("*.whl")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.target._install(dialog.get_filename(), {})
            self.refresh_local()

        dialog.destroy()

    def update_all(self, widget=None):
        """Update the extensions manager, and everything else"""
        pass

    def dialog(self, msg):
        self.widget('dialog_msg').set_label(msg)
        self.widget('dialog').set_transient_for(self.window)
        self.widget('dialog').show_all()

    def close_dialog(self, widget):
        self.widget('dialog_msg').set_label('')
        self.widget('dialog').hide()

