import datetime
from PySide6.QtCore import QThread, Signal

class Emoji:
    def __init__(self):
        self.emoji = {
            "happy": "😊",
            "sad": "😢",
            "sleep": "😴"
        }
        self.current_emoji = self.emoji["happy"]

    def set_emoji(self, emoji_name: str):
        # Set the current emoji based on the given emoji name
        if emoji_name in self.emoji.keys():
            self.current_emoji = self.emoji[emoji_name]
    
class EmojiThread(QThread):
    emoji_obj=Emoji()
    emoji_status_updated = Signal(str)
    emoji_message_updated = Signal(str)

    def run(self):
        while True:
            # Perform your emoji status update logic here
            current_time = datetime.datetime.now().time()
            if current_time.hour >= 22 or current_time.hour < 6:
                self.emoji_obj.set_emoji("sleep")
                self.emoji_message_updated.emit("zzz... I'm sleeping... zzz...") 
            else:
                self.emoji_obj.set_emoji("happy")
                self.emoji_message_updated.emit("Hey there! What a nice day!")
            self.emoji_status_updated.emit(self.emoji_obj.current_emoji)
            
            self.msleep(10_000) # 10 seconds per update
