# Copyright: ijgnd 
#            Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from PyQt5 import QtCore

from aqt.addons import AddonsDialog  
from anki.hooks import wrap
from aqt.qt import *



def after_init(self, addonsManager):
    #add filter bar
    self.filterbar = QLineEdit(self)
    self.filterbar.setPlaceholderText('type here to filter')
    self.form.verticalLayout_2.addWidget(self.filterbar)
    QtCore.QTimer.singleShot(0, self.filterbar.setFocus)
    self.filterbar.textChanged.connect(self.filterAddons) 
AddonsDialog.__init__ = wrap(AddonsDialog.__init__, after_init)


def filterAddons(self, text):
    terms = text.lower().split()

    addonList = self.form.addonList
    mgr = self.mgr

    self.addons = list(mgr.all_addon_meta())
    self.addons.sort(key=lambda a: a.human_name().lower())
    self.addons.sort(key=self.should_grey)

    selected = set(self.selectedAddons())
    addonList.clear()
    for addon in self.addons:
        name = self.name_for_addon_list(addon)
        item = QListWidgetItem(name, addonList)
        for i in terms:
            if i not in name.lower():
                item.setHidden(True)
                break
        if self.should_grey(addon):
            item.setForeground(Qt.gray)
        if addon.dir_name in selected:
            item.setSelected(True)
    addonList.repaint()   # in Anki 2.1.20 it's addonList.reset()
AddonsDialog.filterAddons = filterAddons
