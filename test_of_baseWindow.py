'''SAVE THIS FILE! FOR DEVELOPER to develope other subWindows

this is an 'instruction' file for developer to develope other subWindows
'''

from baseWindow import BaseWindow
from PyQt6 import QtWidgets

class TestWindow(BaseWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Window")
    
        self.addWidgetToLayout("QLabel",text="Hello World!")
        self.addWidgetToLayout("QPushButton",text="Push me!",clickedConn=self.testClick)
        self.addWidgetToLayout("QLineEdit",text="Type here!")
        # self.addWidgetToLayout("XXX",text="Type here!") # raised fatal error. TEST COMPLETED.
        
        self.addBasicMenus()
        # dont set close event (default true)
        self.hasCloseEvent=False


        # show a msg box
        self.showMessageBox("information","Hello World!")

        self.showMessageBox("warning","Hello World!")

        answer=self.showMessageBox("question","Choose!")
        if answer==QtWidgets.QMessageBox.StandardButton.Yes:
            print("User choosed Yes!")
        else:
            print("Use r choosed No!")

    def testClick(self):
        print("Clicked!".capitalize())

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    mainWindow = TestWindow()
    mainWindow.show()
    app.exec()