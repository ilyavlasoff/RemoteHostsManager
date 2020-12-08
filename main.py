from controllers import MainWindowController
from PyQt5 import QtWidgets
import sys
import asyncio
import quamash

qapp = QtWidgets.QApplication(sys.argv)
loop = quamash.QEventLoop(qapp)
asyncio.set_event_loop(loop)
with loop:
    application = MainWindowController.MainWindowController()
    application.show()
    loop.run_forever()
    sys.exit(loop.stop())
#sys.exit(qapp.exec())