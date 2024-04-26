import datetime
from PySide6.QtCore import QThread, Signal

class Emoji:
    def __init__(self):
        self.emoji = {
            "happy": "😊",
            "sad": "😢",
            "sleep": "😴",
            "dirty": "🤢",
            "sick": "🤒"
        }
        self.status={
            "hunger":5,
            "cleanliness":5,
            "health":5,
        }
        self.current_emoji = self.emoji["happy"]

    def set_emoji(self, emoji_name: str):
        if emoji_name in self.emoji.keys():
            self.current_emoji = self.emoji[emoji_name]
    
    def feed(self, restore_hunger: int = 100):
        self.status["hunger"] = min(100, self.status["hunger"] + restore_hunger)
        print("Yum! Hunger restored to", self.status["hunger"])

    def clean(self, restore_cleanliness: int = 100):
        self.status["cleanliness"] = min(100, self.status["cleanliness"] + restore_cleanliness)
        print("Cleaned up! Cleanliness restored to", self.status["cleanliness"])
    
    def heal(self, restore_health: int = 100):
        self.status["health"] = min(100, self.status["health"] + restore_health)
        print("Feeling better! Health restored to", self.status["health"])
    
class EmojiThread(QThread):
    emoji_status_updated, emoji_message_updated = Signal(str), Signal(str)
    hunger_updated, cleanliness_updated, health_updated = Signal(int), Signal(int), Signal(int)

    def __init__(self):
        super().__init__()
        self.emoji_obj=Emoji()

    def run(self):
        while True:
            # lost of hunger, health, cleanliness
            msg=""
            if self.emoji_obj.status["cleanliness"] <= 0:
                self.emoji_obj.set_emoji("dirty")
                msg="I'm dirty! Clean me!"
            else:
                self.emoji_obj.status["cleanliness"] -= 1
            
            if self.emoji_obj.status["hunger"] <= 0:
                self.emoji_obj.set_emoji("sad")
                msg="I'm hungry! Feed me!"
            else:
                self.emoji_obj.status["hunger"] -= 1


            if self.emoji_obj.status["health"] <= 0:
                self.emoji_obj.set_emoji("sick")
                msg="I'm sick! Heal me!"
            else:
                if self.emoji_obj.status["hunger"] <= 0 or self.emoji_obj.status["cleanliness"] <= 0:
                    self.emoji_obj.status["health"] -= 1

            # awake/sleepy
            current_time = datetime.datetime.now().time()
            if msg=="": # everything is fine with the pet
                self.emoji_obj.status["health"] += 1
                if current_time.hour >= 22 or current_time.hour < 6:
                    self.emoji_obj.set_emoji("sleep")
                    msg="zzz..."
                else:
                    self.emoji_obj.set_emoji("happy")
                    msg="Good day!"
            
            # update signals
            self.hunger_updated.emit(self.emoji_obj.status["hunger"])
            self.cleanliness_updated.emit(self.emoji_obj.status["cleanliness"])
            self.health_updated.emit(self.emoji_obj.status["health"])
            self.emoji_message_updated.emit(msg)
            self.emoji_status_updated.emit(self.emoji_obj.current_emoji)
            
            self.msleep(1_000) # 1 seconds per update
