"""
This main function will initialize PySide2 & Main and manage the starting of the program.
"""

# Python
import locale
import sys

# PySide2
from PySide2 import QtWidgets


# TODO Maybe look into Qt model/view because management of contacts, wallets and addresses is getting out of hand
#   especially in TransactionWindow.
# TODO make so that every operation that calls py-algorand-sdk happen on a thread
#   and the application displays the loading icon.
def main():
    locale.setlocale(locale.LC_ALL, '')
    # Manager of all things regarding a widget-based Qt5 app.
    #  Eg.: mainloop, events, initialization, finalization, ...
    app = QtWidgets.QApplication([])

    # This import has to be done here because there are several static resources inside this package which
    #  will be loaded during the import of the package itself. So because most misc are PySide2 objects
    #  QApplication needs to be running to perform all task needed.
    from algotides.interfaces.main.window import MainWindow

    MainWindow.initialize()

    main_window = MainWindow()
    main_window.show()

    # Enter main loop.
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
