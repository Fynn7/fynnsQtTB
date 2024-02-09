# This File is no more useful since I don't use QCreator to build the whole project.
####################################################################################
QT = core gui widgets


SOURCES += \
    src/components/tools/mlToolBox.py \
    src/components/tools/pomodoroTimer.py \
    src/components/games/dice/dice.py \
    src/components/games/poker/poker.py \
    src/baseWindow.py \
    src/main.py

RESOURCES += \
    resource/settings.qrc

VENV_FOLDER = venv

python.commands = $$VENV_FOLDER/Scripts/python.exe

python.input = main.py

TARGET = fynnsQtTB
TEMPLATE = app
