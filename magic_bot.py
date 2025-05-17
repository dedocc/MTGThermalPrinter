import json
import urllib.request, urllib.parse
from magic_fetch import *

TOKEN = "8064344990:AAFqHa0tnl9c2soX2Q-LNHfEigivyS5txKQ"
MASTER_CHAT = "103703303"

class Bot:
    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{token}/"

    def apicall(self, command, args):
        arguments = urllib.parse.urlencode([(arg, value) for arg, value in args if arg != "self"])
        req = urllib.request.Request(self.url + command + "?" + arguments)
        with urllib.request.urlopen(req) as request:
            return request.read()

    def getUpdates(self, offset=0, limit=100, timeout=0, allowed_updates:list[str]=[]):
        return self.apicall("getUpdates", locals().items())

    def getMessage(self):
        return self.getUpdates(offset=self.getLatestID() + 1, timeout=30)
    
    def getLatestID(self):
        update = json.loads(self.getUpdates())
        if update["result"]:
            return update["result"][0]["update_id"]
        return 0

    def sendMessage(self, chat_id, text, reply_markup=""):
        return self.apicall("sendMessage", locals().items())

def greet(bot):
    bot.sendMessage(MASTER_CHAT, "✅ Bot started")

def parse_msg(bot, msg):
    chat_id = msg["message"]["chat"]["id"]
    content = msg["message"].get("text", "none").split() # "none" is such an awful HACK
    if content[0][0] == '/':
        match content[0]:
            case "/start":
                start(bot, chat_id)
            case "/print":
                printCard(bot, chat_id, query=" ".join(content[1:]))

def parse_callback(bot, query:dict):
    chat_id = query["from"]["id"]
    cb = query["data"]
    match cb:
        case "searchcard":
            printCard(bot, chat_id)


def start(bot, chat_id):
    start_msg = "Clicca qui per iniziare"
    keyboard = {"inline_keyboard":[[{"text":"Cerca una carta", "callback_data":"searchcard"}]]}
    bot.sendMessage(chat_id, start_msg, reply_markup=json.dumps(keyboard))


def printCard(bot, chat_id, query=None):
    if not query:
        bot.sendMessage(chat_id, "Scrivi il nome della carta")
        query = json.loads(bot.getMessage())["result"][0]["message"].get("text")
    result = card_search(query, is_bot=True)
    if type(result) == str:
        #bot.sendMessage(chat_id, result)
        if result == "nomatch":
            bot.sendMessage(chat_id, "Nessuna carta trovata")
            return
        cardname = result
    else:
        # select routine
        msg = "Seleziona una di queste"
        keyboard = {"inline_keyboard":[[{"text":name, "callback_data":num}] for num, name in enumerate(result)]}
        keyboard["inline_keyboard"].append([{"text":"❌ Annulla", "callback_data":-1}])
        bot.sendMessage(chat_id, msg, reply_markup=json.dumps(keyboard))
        upd = json.loads(bot.getMessage())
        cn = int(upd["result"][0]["callback_query"]["data"])
        if cn == -1:
            bot.sendMessage(chat_id, "Annullato")
            return None
        #bot.sendMessage(chat_id, result[cn])
        cardname = result[cn]
    card = card_fetch(cardname)
    download_full(card)
    print_img(list(image_to_bits(cardname)))
    bot.sendMessage(chat_id, f"Stampo {cardname}")


def listen(bot):
    offset = bot.getLatestID() + 1
    try:
        while True:
            upd = json.loads(bot.getUpdates(offset=offset, timeout=30))
            print(json.dumps(upd, indent=1))
            if upd["result"]:
                if upd["result"][0].get("callback_query"):
                    parse_callback(bot, upd["result"][0]["callback_query"])
                elif upd["result"][0]["message"].get("text"):
                    parse_msg(bot, upd["result"][0])
                elif upd["result"][0]["message"].get("photo"):
                    pass
                offset = upd["result"][0]["update_id"] + 1
    except KeyboardInterrupt:
        exit(0)

def main():
    my_bot = Bot(TOKEN)
    #greet(my_bot)
    listen(my_bot)

main()
        
