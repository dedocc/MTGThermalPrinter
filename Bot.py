import json
import urllib.request, urllib.parse

class Bot:
    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"
        self.offset = self.getLatestID() + 1

    def apicall(self, command:str, params:str) -> bytes:
        """Unofficial method, to be used as a backend for any API call,
        should strictly expect already json-serialized data"""
        url = f"https://api.telegram.org/bot{self.token}/"
        headers = {"Content-Type": "application/json"}
        data = params.encode("utf-8")
        req = urllib.request.Request(url + command, data, headers)
        with urllib.request.urlopen(req) as request:
            return request.read()
    
    def getLatestID(self):
        """Unofficial method, wrapper for getting latest offset"""
        update = json.loads(self.getUpdates())
        if update["result"]:
            return update["result"][0]["update_id"]
        return 0

    def getUpdates(self, offset=0, limit=100,
                   timeout=0, allowed_updates:list[str]=[]) -> bytes:
        self.offset += 1
        params = json.dumps({k: v for k, v in locals().items() if k != "self"})
        return self.apicall("getUpdates", params)

    def getFile(self, file_id):
        params = json.dumps({k: v for k, v in locals().items() if k != "self"})
        return self.apicall("getFile", params)

    def sendMessage(self, chat_id, text, reply_markup=""):
        params = json.dumps({k: v for k, v in locals().items() if k != "self"})
        return self.apicall("sendMessage", params)
