# Common functions to manage the Magic Thermal Printer
# -  
import urllib.parse, urllib.request
from urllib.error import HTTPError
import json

HEADERS = [('Accept', '*/*'), ('User-Agent', 'MTG/ThermalPrinter/1.0')]

def card_search(name:str, typ=None, extras=False, var=False)->dict:
    name = urllib.parse.quote(name, safe='', encoding="utf-8")
    t = f"+t:{typ}" if typ else ""
    e = "&include_extras=true" if extras else ""
    v = "&include_variations=true" if var else "" 
    url = "https://api.scryfall.com/cards/search?q={}{}{}{}"
    req = urllib.request.Request(url.format(name, t, e, v))
    for h in HEADERS:
        req.add_header(*h)
    with urllib.request.urlopen(req) as response:
        try:
            catalog = json.loads(response.read())
        except HTTPError: # No card found
            return dict()
    return catalog["data"]

def random_card(typ="")->dict:
    """typ can be any card type, such as land, creature, instant, etc"""
    t = f"?q=t:{typ}" if typ else ""
    url = "https://api.scryfall.com/cards/random"
    req = urllib.request.Request(url + t)
    for h in HEADERS:
        req.add_header(*h)
    with urllib.request.urlopen(req) as response:
        try: # catch wrong "typ" values
            card = json.loads(response.read())
        except HTTPError:
            return dict()
    return card
