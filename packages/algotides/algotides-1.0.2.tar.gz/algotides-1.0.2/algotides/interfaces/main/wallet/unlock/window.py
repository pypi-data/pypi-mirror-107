# Python
from functools import partial


# PySide2
from PySide2 import QtWidgets, QtCore, QtGui
# py-algorand-sdk
from algosdk.kmd import KMDClient
from algosdk.wallet import Wallet as AlgosdkWallet


# Tides
#   Miscellaneous
from algotides.interfaces.main.wallet.entities import Wallet
import algotides.threadpool as threadpool
#   Interfaces
from algotides.interfaces.main.wallet.unlock.ui_window import Ui_UnlockWallet


class UnlockWallet(QtWidgets.QDialog, Ui_UnlockWallet):
    def __init__(
            self,
            parent: QtWidgets.QWidget,
            wallet: Wallet,
            kmd_client: KMDClient):
        super().__init__(parent, QtCore.Qt.WindowCloseButtonHint)

        # Anti memory leak
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.wallet = wallet
        self.kmd_client = kmd_client
        self.return_value = None

        self.worker = None

        self.setupUi(self)

        self.widget.setVisible(False)

    def closeEvent(self, arg__1: QtGui.QCloseEvent):
        if self.worker:
            self.worker.signals.success.disconnect()
            self.worker.signals.error.disconnect()
        arg__1.accept()

    # We override accept of this class and don't use super().accept() inside.
    #  This is because we just treat this method as a slot connected to the OK button.
    #  Either super().accept() or super().reject() will be eventually called when the worker is done.
    def accept(self):
        self.lineEdit.setEnabled(False)
        self.widget.setVisible(True)
        self.buttonBox.setEnabled(False)

        self.worker = threadpool.start_worker(
            QtCore.QThreadPool.globalInstance(),
            # We have to use partial because for some reason the creation of an object is not considered a callable.
            #  I still have to look into this.
            # TODO: Look into this.
            partial(
                AlgosdkWallet,
                self.wallet.info["name"],
                self.lineEdit.text(),
                self.kmd_client
            ),
            self.unlock_success,
            self.unlock_failure
        )

    @QtCore.Slot(object)
    def unlock_success(self, result: object):
        self.return_value = result
        super().accept()

    @QtCore.Slot(Exception)
    def unlock_failure(self, error: Exception):
        QtWidgets.QMessageBox.critical(self, "Could not open wallet", str(error))
        self.return_value = None
        super().reject()
