#!/usr/bin/python
import urllib.request, urllib.parse
from urllib.error import HTTPError
import json
import sys, os
from PIL import Image

HEADERS = [('Accept', '*/*'), ('User-Agent', 'MTG/ThermalPrinter/1.0')]
CACHEDIR = ".magic_cache"
IMG_SIZE = (504, 702)

def choose(catalog:dict)->str:
    for i, c in enumerate(catalog['data']):
        print(f"{i+1:>2}: {c}")
    choice = int(input("\nChoose card number from above: ")) - 1
    return catalog['data'][choice]

def card_search(name:str, is_bot=False)->str: # card name
    url = "https://api.scryfall.com/cards/autocomplete?q="
    name = urllib.parse.quote(name, safe='', encoding="utf-8")
    req = urllib.request.Request(url+name)
    for h in HEADERS:
        req.add_header(*h)
    with urllib.request.urlopen(req) as response:
        catalog = json.loads(response.read())
    if catalog['total_values'] == 0:
        if is_bot:
            return "nomatch"
        print("No cards found")
        exit(1)
    elif catalog['total_values'] == 1:
        return catalog['data'][0]
    else:
        if is_bot:
            return catalog["data"]
        return choose(catalog)

def card_fetch(name:str)->dict:
    url = "https://api.scryfall.com/cards/named?fuzzy="
    name = urllib.parse.quote(name, safe='', encoding="utf-8")
    req = urllib.request.Request(url+name)
    for h in HEADERS:
        req.add_header(*h)
    with urllib.request.urlopen(req) as response:
        try:
            card = json.loads(response.read())
        except HTTPError as e:
            print(e)
            exit(1)
    return card

def download_full(card:dict)->None:
    print(card)
    url = card['image_uris']['large']
    name = card['name']
    urllib.request.urlretrieve(url, os.path.join(CACHEDIR, name))

def image_to_bits(card_name:str)->list: # Actually, returns ImagingCore instance
    img = Image.open(os.path.join(CACHEDIR, card_name))
    img.thumbnail((IMG_SIZE[1], IMG_SIZE[1]))
    img = img.convert("1")
    return img.getdata()

def print_img(bits:list):
    with open("/dev/usb/lp0", "wb") as printer:
        printer.write(
                ("SIZE 80 mm,90 mm\r\n"
                 "GAP 0,0\r\n"
                 "CLS\r\n"
                 f"BITMAP 0,0,{IMG_SIZE[0]//8},{IMG_SIZE[1]},0,"
                 ).encode())
    
        for i in range(0, len(bits), 8):
            str_byte = "".join(["1" if b else "0" for b in bits[i:i+8]])
            byte = int(str_byte, 2).to_bytes(1, byteorder='little')
            printer.write(byte)
        printer.write("\r\nPRINT 1,1\r\n".encode())

def main():
    if len(sys.argv) >= 2:
        keyword = sys.argv[1]
    else:
        print("provide name")
        exit(1)
    if not os.path.exists(CACHEDIR):
        os.makedirs(CACHEDIR)
    card_name = card_search(keyword)
    if not os.path.exists(os.path.join(CACHEDIR, card_name)):
        card = card_fetch(card_name)
        download_full(card)
    bits = list(image_to_bits(card_name))
    print_img(bits)
    exit(0)

if __name__ == "__main__":
    main()
