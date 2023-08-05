"""
This file contains AddressFrame which is a QFrame displayed as a result of an opened wallet.
"""


# Python
from functools import partial
from sys import stderr


# PySide2
from PySide2 import QtWidgets, QtCore, QtGui
# py-algorand-sdk
from algosdk.v2client.algod import AlgodClient
from algosdk.mnemonic import from_private_key, to_private_key


# Tides
#   Miscellaneous
from algotides.interfaces.main.wallet.entities import Wallet
#   Interfaces
from algotides.interfaces.main.address.ui_frame import Ui_AddressFrame
from algotides.interfaces.main.address.balance.window import BalanceWindow


class AddressFrame(QtWidgets.QFrame, Ui_AddressFrame):
    def __init__(
            self,
            parent: QtWidgets.QWidget,
            wallet: Wallet,
            algod_client: AlgodClient):
        super().__init__(parent)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet
        self.algod_client = algod_client

        self.setupUi(self)

        # Connections
        #   listWidget
        self.listWidget.itemDoubleClicked.connect(self.show_balance)
        self.listWidget.customContextMenuRequested.connect(self.show_context_menu)

        #   pushButtons
        self.pushButton_Return.clicked.connect(self.close)
        self.pushButton_Balance.clicked.connect(self.show_balance)
        self.pushButton_New.clicked.connect(self.new_address)
        self.pushButton_Forget.clicked.connect(self.forget_address)
        self.pushButton_Import.clicked.connect(self.import_address)
        self.pushButton_Export.clicked.connect(self.export_address)

        QtCore.QTimer.singleShot(0, self.setup_logic)

    def setup_logic(self):
        self.listWidget.clear()

        # We load the addresses in a non threaded way for now. It's reasonable because if we are at this point we know
        #  there is a working kmd server online.
        addresses = self.wallet.algo_wallet.list_keys()

        for address in addresses:
            self.listWidget.addItem(address)

        if len(addresses) >= 1:
            self.listWidget.setCurrentRow(0)

            for widget in [self.pushButton_Balance, self.pushButton_Forget, self.pushButton_Export]:
                widget.setEnabled(True)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        key = event.key()
        if key == int(QtCore.Qt.Key_Return):
            if self.listWidget.hasFocus():
                self.show_balance()
        elif key == int(QtCore.Qt.Key_Escape):
            self.close()

    @QtCore.Slot()
    def show_balance(self, item: QtWidgets.QListWidgetItem = None):
        if not item:
            item = self.listWidget.currentItem()

        if not self.algod_client:
            QtWidgets.QMessageBox.critical(self, "algod settings", "Please check algod settings.")
            return

        try:
            account_info = self.algod_client.account_info(item.text())
        except Exception as e:
            if __debug__:
                print(type(e), str(e), file=stderr)
            QtWidgets.QMessageBox.critical(self, "Could not load balance", str(e))
        else:
            dialog = BalanceWindow(self, account_info)
            dialog.exec_()

    @QtCore.Slot()
    def new_address(self):
        try:
            self.wallet.algo_wallet.generate_key()
        except Exception as e:
            if __debug__:
                print(type(e), str(e), file=stderr)
            QtWidgets.QMessageBox.critical(self, "Could not generate new address", str(e))
        else:
            self.setup_logic()

    @QtCore.Slot()
    def forget_address(self):
        item = self.listWidget.currentItem()

        if QtWidgets.QMessageBox.question(
            self, "Forget address from KMD",
            "Are you sure you want to forget this address?",
            QtWidgets.QMessageBox.StandardButton.Yes,
            QtWidgets.QMessageBox.StandardButton.No
        ) != QtWidgets.QDialogButtonBox.StandardButton.Yes:
            return

        try:
            self.wallet.algo_wallet.delete_key(item.text())
        except Exception as e:
            if __debug__:
                print(type(e), str(e), file=stderr)
            QtWidgets.QMessageBox.critical(self, "Could not forget address", str(e))
        else:
            self.setup_logic()

    @QtCore.Slot()
    def import_address(self):
        if QtWidgets.QMessageBox.question(
                self, "Importing address",
                "Please keep in mind that, when recovering a wallet in the future, only the addresses derived from "
                "the Master Derivation Key are restored.\n\n"
                "Importing an address inside a wallet is not the same as deriving it from the wallet.\n\n"
                "Would you like to continue?"
        ) != QtWidgets.QMessageBox.StandardButton.Yes:
            return

        new_address = QtWidgets.QInputDialog.getMultiLineText(
            self, "Importing address",
            "Please fill in with the address mnemonic private key"
        )
        if new_address[1]:
            try:
                self.wallet.algo_wallet.import_key(to_private_key(new_address[0]))
            except Exception as e:
                if __debug__:
                    print(type(e), str(e), file=stderr)
                QtWidgets.QMessageBox.critical(self, "Could not import address", str(e))
            else:
                self.setup_logic()

    @QtCore.Slot()
    def export_address(self):
        item = self.listWidget.currentItem()

        try:
            private_key = self.wallet.algo_wallet.export_key(item.text())
        except Exception as e:
            if __debug__:
                print(type(e), str(e), file=stderr)
            QtWidgets.QMessageBox.critical(self, "Could not export address", str(e))
        else:
            QtGui.QGuiApplication.clipboard().setText(from_private_key(private_key))
            QtWidgets.QMessageBox.information(self, "Success", "Private key copied into clipboard")

    @QtCore.Slot(QtCore.QPoint)
    def show_context_menu(self, pos: QtCore.QPoint):
        item = self.listWidget.itemAt(pos)
        if item:
            menu = QtWidgets.QMenu(self)

            menu.addAction("Copy to clipboard", partial(QtGui.QGuiApplication.clipboard().setText, item.text()))

            global_pos = self.listWidget.mapToGlobal(pos)
            menu.exec_(global_pos)

            menu.deleteLater()
