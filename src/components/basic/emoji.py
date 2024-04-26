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
    
    def operate(self, operation: str, value: int):
        '''operation: feed, clean, heal'''
        if operation == "feed":
            self.status["hunger"] = max(0,min(100, self.status["hunger"] + value))
        elif operation == "clean":
            self.status["cleanliness"] = max(0,min(100, self.status["cleanliness"] + value))
        elif operation == "heal":
            self.status["health"] = max(0,min(100, self.status["health"] + value))
    
    def check_status(self)->str:
        '''
        Check the status of the pet
        
        It should be run in a loop/time interval to check the status of the pet
        '''
        # lost of hunger, health, cleanliness
        msg=""
        if self.status["cleanliness"] <= 0:
            self.set_emoji("dirty")
            msg="I'm dirty! Clean me!"
        else:
            self.operate("clean", -1)
        
        if self.status["hunger"] <= 0:
            self.set_emoji("sad")
            msg="I'm hungry! Feed me!"
        else:
            self.operate("feed", -1)


        if self.status["health"] <= 0:
            self.set_emoji("sick")
            msg="I'm sick! Heal me!"
        else:
            if self.status["hunger"] <= 0 or self.status["cleanliness"] <= 0:
                self.operate("heal", -1)
        return msg
    
class EmojiThread(QThread):
    emoji_status_updated, emoji_message_updated = Signal(str), Signal(str)
    hunger_updated, cleanliness_updated, health_updated = Signal(int), Signal(int), Signal(int)

    def __init__(self):
        super().__init__()
        self.emoji_obj=Emoji()

    def run(self):
        while True:
            # check status continuously
            msg=self.emoji_obj.check_status()
            # awake/sleepy
            current_time = datetime.datetime.now().time()
            if msg=="": # if everything is fine with the pet
                self.emoji_obj.operate("heal", 1)
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
