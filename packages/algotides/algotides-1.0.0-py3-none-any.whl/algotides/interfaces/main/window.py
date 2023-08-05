"""
This file declares the Main class subclassed from QMainWindow.

Main class is the fundamental interface from which the program offers its functionality
"""


# Python
from functools import partial


# PySide2
from PySide2 import QtWidgets, QtGui, QtCore
# py-algorand-sdk
from algosdk.kmd import KMDClient
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient


# Tides
# The qt_resources_data does not appear anywhere in the actual code but I think it gets loaded into PySide2
#   runtime environment.
# We can reference this from every other module while still only importing it here. I know, weird...

#   Resources
from algotides.interfaces.qrc_graphics import qt_resource_data
#   Miscellaneous
import algotides.constants as constants
#   Interfaces
from algotides.interfaces.main.ui_window import Ui_MainWindow
from algotides.interfaces.transaction.window import TransactionWindow
from algotides.interfaces.main.wallet.frame import WalletsFrame
from algotides.interfaces.contacts.window import ContactsWindow
from algotides.interfaces.settings.window import SettingsWindow
from algotides.interfaces.about.window import InfoWindow, CreditsWindow
from algotides.interfaces.main.closing_window import ClosingWindow

# I need this code here just so my very smart IDE detects this module as used and doesn't remove it automagically.
assert qt_resource_data


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Algorand Wallet Manager main window.

    This window will host the menubar and the frames for wallets and addresses.
    """
    def __init__(self):
        super().__init__()

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # API for Algorand node KMD client
        self.kmd_client = None
        self.algod_client = None
        self.indexer_client = None

        self.setupUi(self)

        self.menuBar().setNativeMenuBar(False)

        self.setWindowIcon(QtGui.QIcon(":/icons/tides.ico"))

        # This has to be done here because Qt Creator doesn't allow action on the menuBar itself.
        self.menuAction_NewTransaction = self.menuBar().addAction("New transaction")
        self.menuAction_Contacts = self.menuBar().addAction("Contacts")
        self.menuAction_Settings = self.menuBar().addAction("Settings")
        self.menu_About = self.menuBar().addMenu("About")
        self.menuAction_Info = self.menu_About.addAction("Info")
        self.menuAction_Credits = self.menu_About.addAction("Credits")

        # Connections
        self.menuAction_NewTransaction.triggered.connect(
            self.exec_transaction
        )
        self.menuAction_Settings.triggered.connect(
            self.exec_settings
        )
        self.menuAction_Contacts.triggered.connect(
            partial(self.exec_dialog, ContactsWindow)
        )
        self.menuAction_Info.triggered.connect(
            partial(self.exec_dialog, InfoWindow)
        )
        self.menuAction_Credits.triggered.connect(
            partial(self.exec_dialog, CreditsWindow)
        )

        QtCore.QTimer.singleShot(0, self.restart)

    @QtCore.Slot()
    def exec_transaction(self):
        if self.algod_client:
            try:
                # TODO: This should happen in thread.
                self.algod_client.status()
            except Exception:
                QtWidgets.QMessageBox.critical(self, "algod settings", "Please check algod settings.\n"
                                                                       "Algod daemon could be offline.")
                return

            transaction_dialog = TransactionWindow(self, self.queuedWidget.widget(0))
            transaction_dialog.exec_()

    @QtCore.Slot()
    def exec_settings(self):
        settings_window = SettingsWindow(self)
        if settings_window.exec_() == QtWidgets.QDialog.Accepted:
            self.restart()

    def exec_dialog(self, dialog: QtWidgets.QDialog):
        """
        This method executes a QDialog window.
        """
        child_dialog = dialog(self)
        child_dialog.exec_()

    def restart(self):
        """
        This method restart the application from the point when it tries to connect to a node to display wallets.
        This method can also be used to do the first start.

        This is done by deleting any existing WalletFrame and creating a new one.
        This method also makes sure that new settings are refreshed into new rest endpoints.
        """
        # This will be enabled in the future when it can be called. (i.e.: there exists at least one wallet)
        self.menuAction_NewTransaction.setEnabled(False)

        if self.queuedWidget.count() >= 1:
            self.queuedWidget.clear_queue()

        endpoints = SettingsWindow.calculate_rest_endpoints()

        # TODO: Check that those settings actually point to an online daemon.
        if "kmd" in endpoints:
            self.kmd_client = KMDClient(
                endpoints["kmd"]["token"],
                endpoints["kmd"]["address"]
            )
        if "algod" in endpoints:
            self.algod_client = AlgodClient(
                endpoints["algod"]["token"],
                endpoints["algod"]["address"]
            )
        if "indexer" in endpoints:
            self.indexer_client = IndexerClient(
                endpoints["indexer"]["token"],
                endpoints["indexer"]["address"]
            )

        if self.kmd_client:
            try:
                self.kmd_client.versions()
            except Exception:
                QtWidgets.QMessageBox.critical(self, "kmd settings", "Please check kmd settings.\n"
                                                                     "Kmd daemon could be offline.")
            else:
                self.queuedWidget.add_widget(
                    WalletsFrame(self, self.kmd_client, self.algod_client, self.indexer_client)
                )
        else:
            QtWidgets.QMessageBox.critical(self, "kmd settings", "kmd settings not found.")

    def closeEvent(self, event: QtGui.QCloseEvent):
        """
        This overridden method gets called before actually destroying self.

        It's used to finalize some resources and then it passes the event up the chain to let PySide2 deal with it.
        """
        SettingsWindow.shut_down()
        ContactsWindow.shut_down()

        # We have no choice but to do it this way because i have no control over how much time a call through algosdk
        #  could take and it's not possible to dirty kill a QRunnable.
        if QtCore.QThreadPool.globalInstance().activeThreadCount() > 0:
            self.setVisible(False)
            self.exec_dialog(ClosingWindow)

        event.accept()

    @staticmethod
    def initialize():
        """
        This method does some preparation work such as creating folders and files if they are not present in
        the filesystem.
        """
        # Create user data folders
        constants.path_app_data.mkdir(exist_ok=True)

        SettingsWindow.initialize()
        ContactsWindow.initialize()
