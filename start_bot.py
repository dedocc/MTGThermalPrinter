try:
    from private import TOKEN
except ImportError:
    token = input("Paste Telegram bot API key: ")
    with open("private.py", "wt") as f:
        f.writelines(f"TOKEN = \"{token}\"")
    from private import TOKEN

from Bot import Bot

# Bot-usage functions
# Main listening cycle with branching

bot = Bot(TOKEN)

def listen(bot):
    pass
