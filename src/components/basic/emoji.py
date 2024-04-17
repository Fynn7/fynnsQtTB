import time
import datetime
import threading

class Emoji:
    '''
    TODO: Setup a Thread to run this class and update the status of emoji
    
    e.g.: get time, if nighttime, change emoji to sleep
    '''
    def __init__(self):
        self.emoji = {
            "happy": "😊",
            "sad": "😢",
            "sleep": "😴"
        }
        self.current_emoji = self.emoji["happy"]

        self.thread = threading.Thread(target=self.update_emoji_status)
        self.thread.start()
    def update_emoji_status(self):
        while True:
            # Perform your emoji status update logic here
            current_time = datetime.datetime.now().time()
            if current_time.hour >= 22 or current_time.hour < 6:
                self.set_emoji("sleep")
            else:
                self.set_emoji("happy")
            time.sleep(1)  # Update emoji status every minute

    def set_emoji(self, emoji_name: str):
        # Set the current emoji based on the given emoji name
        if emoji_name in self.emoji.keys():
            self.current_emoji = self.emoji[emoji_name]
        # send a signal to main.py and update gui
        # TODO: Implement signal to update the emoji in the GUI

    def eat(self, food: str) -> str:
        return f"Yum! I like {food}!"

    def clean(self) -> str:
        return "I'm clean now!"

    def talk(self, msg: str) -> str:
        return msg
