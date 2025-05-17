import json

class InlineKeyboardButton:
    def __init__(self, text:str, callback_data:str|object):
        self.text = text
        self.callback_data = callback_data
    
    def __json__(self):
        """Custom serializer for json module
           Either call json.dumps(mybutton.__json__()) or
           json.dumps(mybutton, default=lambda b: b.__json__())
        """
        return {"text": self.text, "callback_data": self.callback_data}

class InlineKeyboard:
    """Usage:
          mykeyboard = InlineKeyboard([[button1, button2], [button3, button4]...])
       To send, use bot.sendMessage(chat_id, msg, reply_markup=mykeyboard.dumps())
    """
    def __init__(self, button_list:list[list[InlineKeyboardButton]]):
        self.keyboard = {"inline_keyboard":
                            [ [json.dumps(x.__json__()) for x in y]
                            for y in button_list]
                         }
    
    def toList(self)->list:
        return self.keyboard["inline_keyboard"]

    def dumps(self):
        return json.dumps(self.keyboard)
