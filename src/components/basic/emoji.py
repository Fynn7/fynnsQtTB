import datetime
from PySide6.QtCore import QThread, Signal

from baseWindow import BaseWindow


class Emoji:
    def __init__(self, emoji: str, status: dict[str, int]):
        self.status: dict = status
        self.emoji: str = emoji

    def operate(self, operation: str, value: int):
        '''operation: feed, clean, heal'''
        if operation == "feed":
            self.status["hunger"] = max(
                0, min(100, self.status["hunger"] + value))
        elif operation == "clean":
            self.status["cleanliness"] = max(
                0, min(100, self.status["cleanliness"] + value))
        elif operation == "heal":
            self.status["health"] = max(
                0, min(100, self.status["health"] + value))

    def check_status(self) -> str:
        '''
        Check the status of the pet

        It should be run in a loop/time interval to check the status of the pet
        '''
        # lost of hunger, health, cleanliness
        msg = ""
        if self.status["cleanliness"] <= 0:
            self.emoji = "🤢"
            msg = "I'm dirty! Clean me!"
        else:
            self.operate("clean", -1)

        if self.status["hunger"] <= 0:
            self.emoji = "😢"
            msg = "I'm hungry! Feed me!"
        else:
            self.operate("feed", -1)

        if self.status["health"] <= 0:
            self.emoji = "🤒"
            msg = "I'm sick! Heal me!"
        else:
            if self.status["hunger"] <= 0 or self.status["cleanliness"] <= 0:
                self.operate("heal", -1)
        return msg


class EmojiThread(QThread):
    # consider that the signals are grouply updated, so we can use a single signal for each group
    emoji_signals_updated = Signal(dict)
    message_updated = Signal(str)

    def __init__(self, emoji_data: dict):
        super().__init__()
        self.emoji_obj = Emoji(**emoji_data)

    def run(self, time_interval=10):
        while True:
            # check status continuously
            msg = self.emoji_obj.check_status()
            # awake/sleepy
            current_time = datetime.datetime.now().time()
            if msg == "":  # if everything is fine with the pet
                self.emoji_obj.operate("heal", 1)
                if current_time.hour >= 22 or current_time.hour < 6:
                    self.emoji_obj.emoji = "😴"
                    msg = "zzz..."
                else:
                    self.emoji_obj.emoji = "\ud83d\ude0a"
                    msg = "Good day!"

            # update signals
            self.emoji_signals_updated.emit({
                "emoji": self.emoji_obj.emoji,
                "status": self.emoji_obj.status
            })
            self.message_updated.emit(msg)

            self.msleep(1_000*time_interval)  # 1 seconds per update
