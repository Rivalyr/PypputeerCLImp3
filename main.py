"""
The thing with this script its i usualy use mp3 or flac but the quality normally with most common youtube downloaders
are poor. like 128kbps. so flew months ago i was using this page and i thought "i didnt know this page have 360kbps"
thrn i found pyppeteer as a selenium sustite. and this a good way to learn and apply the package.

page where u will download the songs: https://getn.topsandtees.space/

Rivalyr 22/01/2023 | 10:40pm
"""
from pyppeteer import launch
from bs4 import BeautifulSoup
import requests
import asyncio
import time
import os


async def main():
    """
    Browser sends a background chromium app, then create a new page. after that with 'goto' method it sends u to the
    page where u r gonna do everything a
    """
    global songname, descarga, corregido
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://getn.topsandtees.space/')

    # Ask for and input. try with some popular song like "Kanye West - Bound 2 Explicit"
    # then it will search for the most popural one

    nombre_cancion = input(str("¿What do u want on mp3 today?\nSongname or link from YT: "))
    inputprincipal = 'input[placeholder="Enter YouTube url or search phrase"]'
    await page.click(f'{inputprincipal}')
    await page.type(f'{inputprincipal}', nombre_cancion)

    # Sends the song name and wait until the page its ready

    await page.focus(f'{inputprincipal}')
    await page.keyboard.press('Enter')
    await page.keyboard.up('Enter')
    # i had to use asyncio bc i dont find another way aleast this didnt cause any problems
    await asyncio.sleep(2)

    # press the first download button and wait 2 seconds for let the api get the right link for the 360kbps
    await page.click('.search-item__download')
    await asyncio.sleep(2)

    # Get the page link, for using it after with bs4 to get the download api response
    htmldwn = page.url
    htmlbase = await page.content()
    soupbase = BeautifulSoup(htmlbase, 'html.parser')

    # Search for the name of the song, there is the same youtube name on the file
    element = soupbase.find("h1", class_="content__title")

    # First i had to create the songtitle and asigne some value bc i was getting a error.
    # then the conditional for another thing relate with default value. idk, package things
    if element is not None:
        songtitle = element.text
        songname = songtitle + '.mp3'
        print(f'Downloading {songtitle}\n')
        # > Kanye West - Bound 2(Explicit)

    # Creates the file and replace some characters in case of there are some. (windows reserved char. idk)
    # reserved windows characters and that. even change the "-" to "-" again just for practice pruporses
    nombre = songname
    char_i = ["\\", "/", "|", "-", ":", "*", "?", "\"", "<", ">"]

    for char in char_i:
        if char in nombre:
            corregido = nombre.replace(char, '-')
            print(corregido)
            break
        elif char != nombre:
            print('Changing song´s characters in the name for a compatible file name')
            # This only works in cmd. in other way it just get ignore (vscode cmd option make it work)
            os.system('cls')

    with open(str(corregido), "x") as file:
        pass
    time.sleep(2)
    await asyncio.sleep(3)

    # get the api link for download the file
    r = requests.get(f'{htmldwn}')
    await browser.close()
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    # The same thing above. idk why i have to use conditionals but aight
    download = soup.select_one('.btn_clck_spec')
    if download is not None:
        descarga = download.get('data-href')

    #   print(descarga) > https://pawanasita.com/get/2286589/xn8zQ28wdGS5JlA8LnQku29pYXD0PPcNp9YQ7XaESqM/mp3

    # Makes an api request for download the song
    time.sleep(2)
    r = requests.get(descarga)
    with open(corregido, "wb") as f:
        f.write(r.content)
    print()

    # this is for preview the progress around the page like clicks and another things happened doing the script
    # await page.screenshot({'path': 'example.png'})


# run script until it finish and download the file. this doesnt need a try - catch for errors, its a basic page
asyncio.get_event_loop().run_until_complete(main())

"""
its kinda simple script, if u need some explanation (i hope its clear) u can dm me on discord 
Rivalyr#3427

learning and coding with the lib start at 11:00 a.m - 7:40pm
Comments start at 10:48 p.m - 12:00pm
debug basic stuff 00:00 - 1:00am > 1:30pm to 2:40

Rivalyr 23/01/23 | 2:48
"""
