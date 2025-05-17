import time
class Logger:
    """ 0: error
        1: warning
        2: message
        3: info
    """
    def __init__(self, filename):
        self.level = 2
        self.filename = filename

    def setLevel(self, level):
        self.level = level

    def log(self, data:dict)->None:
        level = data["level"]
        content = data["content"]
        timestamp = time.asctime()
        with open(self.filename, "at") as f:
            f.writelines(f"[{timestamp}] {level}: {content}")

    def message(self, message:dict):
        """Message must be a request["result"][0]["message"] type of dict"""
        chat_id = message.get("from", {}).get("id", "unknown")
        username = message.get("from", {}).get("username", "unknown")
        text = message.get("text", "")
        content = f"{chat_id} (@{username}) : {text}"
        data = {"level": "MESSAGE", "content": content}
        if self.level >= 3:
            self.log(data)
    
    def info(self, string):
        data = {"level": "INFO", "content": string}
        if self.level >= 2:
            self.log(data)

    def warn(self, string):
        data = {"level": "WARINING", "content": string}
        if self.level >= 1:
            self.log(data)

    def error(self, string):
        data = {"level": "ERROR", "content": string}
        if self.level >= 0:
            self.log(data)
