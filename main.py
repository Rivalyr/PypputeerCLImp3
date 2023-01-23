# https://getn.topsandtees.space/
from pyppeteer import launch 
import asyncio
import requests
from bs4 import BeautifulSoup

async def main():
    # Lanza el navegador
    # Espera a crear una nueva pagina
    # Va a este link GoTo = Pagina
    # Consigue el titulo de la pagina

    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://getn.topsandtees.space/')
    # titulo = await page.title() 
    # print(titulo)


    # Le da click a ese selector css
    # Escribe dentro del selector
    cancion = input(str("¿Qué cancion deseas descargar?\nTitulo de la cancion:"))
    inputprincipal = 'input[placeholder="Enter YouTube url or search phrase"]'
    await page.click(f'{inputprincipal}')
    await page.type(f'{inputprincipal}', cancion)

    # Me enfoco en un elemento para que la pulsacion de tecla no falle o eso entendi
    # Presiona y suelta la tecla  enter
    # me toca meterle el sleep con asyncio porque el waitFornavigation no sirve

    await page.focus(f'{inputprincipal}')
    await page.keyboard.press('Enter')
    await page.keyboard.up('Enter')
    
    await asyncio.sleep(2)


    # Le doy al boton de descarga a la maxima calidad 320kbps
    # analiza las entrasdas
    await page.click('.search-item__download')
    await asyncio.sleep(2)

    ## PARA CONSEGUIR EL PUTO LINK DE LA PAGINA SE USA VARIABLE. NO METODO CON AWAIT
    htmlDwn = page.url
    htmlbase= await page.content()
    soupbase = BeautifulSoup(htmlbase, 'html.parser')

    # Buscar el primer elemento "div" con el atributo "class" con el valor "mi-clase"
    element = soupbase.find("h1", class_="content__title")
    # Esto es para que en caso de que no lo encuentre, no me muestre el error ese raro
    # ESto es para conseguir el link para bajar la cancion 
    if element is not None:
        cosa = element.text
        songtitle = cosa + '.mp3'
        print(cosa) #> Kanye West - Bound 2 (Explicit)

    r = requests.get(f'{htmlDwn}')
    await browser.close()
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')  
    
    # De nuevo lo mismo, en caso de que lo encuentre, cambia su valor de none a lo que me devuelva
    download = soup.select_one('.btn_clck_spec')
    if download is not None:
        # Esto funciona con el "Attrs" o sin el. da igual
        descarga = download.get('data-href')
        # print(descarga) > https://pawanasita.com/get/2286589/xn8zQ28wdGS5JlA8LnQku29pYXD0PPcNp9YQ7XaESqM/mp3
        r = requests.get(f'{descarga}')

        print(r.status_code)
        
        with open(songtitle , 'wb') as f:
            f.write(r.content)

    # esto saca una screenshot, es como para saber que estoy viendo
    # await page.screenshot({'path': 'example.png'})
asyncio.get_event_loop().run_until_complete(main()) # corre el script hasta que se termine la funcion
