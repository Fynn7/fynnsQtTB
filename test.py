import ctypes
ctypes.windll.user32.MessageBoxW(0, "hello world",'title', 0)


from PySide6.QtWidgets import QLabel

label=QLabel()
label.setText("hello world")
# get label text
print(label.text())