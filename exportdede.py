#!/usr/bin/python3
# coding: utf-8

import json
import sys
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import *

base_url = "https://www.megadede.com"
timeout = 2


def execute():
    print("\n[*] Ejecutando..")

    sleep(timeout)

    browser = None

    try:
        if sys.argv[1] == "--firefox":
            browser = webdriver.Firefox(
                executable_path='libs/firefoxdriver.exe')
        elif sys.argv[1] == "--chrome":
            browser = webdriver.Chrome(
                executable_path='libs/chromedriver.exe')
        else:
            print("\n[*] Uso: py exportdede.py [--chrome|--firefox]")

            exit(0)

        browser.get(base_url + "/login")

        print("\n[*] Inicia sesión para continuar..")

        wait = WebDriverWait(browser, 300)

        login = wait.until(ec.visibility_of_element_located(
            (By.CLASS_NAME, "username")))

        ActionChains(browser).move_to_element(login).perform()

        if login:
            print("\n[*] Has iniciado sesión correctamente")
            browser.minimize_window()

            sleep(timeout)

            print("\n[*] Exportando archivo JSON..")

            sleep(timeout)

            data = {
                "peliculas": {
                    "peliculas_favoritas": get_pelis_favoritas(browser),
                    "peliculas_pendientes": get_pelis_pendientes(browser),
                    "peliculas_vistas": get_pelis_vistas(browser),
                },
                "series": {
                    "series_siguiendo": get_series_siguiendo(browser),
                    "series_favoritas": get_series_favoritas(browser),
                    "series_pendientes": get_series_pendientes(browser),
                    "series_vistas": get_series_vistas(browser),
                },
                "listas": get_listas(browser),
            }

            with open('lists.json', 'w') as outfile:
                json.dump(data, outfile)

            print("\n[*] Se ha exportado correctamente")

            sleep(timeout)

            browser.quit()

    except TimeoutException:
        print("\n[*] Se ha agotado el tiempo de espera")

        browser.quit()

    except WebDriverException:
        print("\n[*] Ejecución detenida")

    except IndexError:
        print("\n[*] Uso: py exportdede.py [--chrome|--firefox]")


def get_listas(browser):
    browser.get(base_url + "/listas")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div#your-listas > div.lista")

    items = dict()
    for row in rows:
        d = dict()
        href = row.select_one("a")["href"]

        browser.get(base_url + href)
        body = browser.execute_script("return document.body")
        source = body.get_attribute('innerHTML')
        content = BeautifulSoup(source, "html.parser")

        d["url"] = base_url + href

        if content.select_one("div.content > h2") is not None:
            d["nombre"] = content.select_one("div.content > h2").text
        else:
            d["nombre"] = None

        if content.select_one("div.description") is not None:
            d["descripcion"] = content.select_one("div.description").text
        else:
            d["descripcion"] = None

        if content.select_one("a.username") is not None:
            d["autor"] = content.select_one("a.username").text.strip()
        else:
            d["autor"] = None

        if content.select_one("span.number") is not None:
            d["seguidores"] = content.select_one("span.number").text
        else:
            d["seguidores"] = None

        if content.select_one("div.media-container") is not None:
            sub_items = content.select("div.media-container")

            d["lista"] = dict()
            for sub_item in sub_items:
                item = get_item_info(browser, sub_item)
                d["lista"][item.get("url")] = item
        else:
            d["lista"] = None

        items[d.get("nombre")] = d

    return items


def get_pelis_favoritas(browser):
    browser.get(base_url + "/pelis/favorites")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    items = dict()
    for row in rows:
        item = get_item_info(browser, row)
        items[item.get("url")] = item

    return items


def get_pelis_pendientes(browser):
    browser.get(base_url + "/pelis/pending")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    items = dict()
    for row in rows:
        item = get_item_info(browser, row)
        items[item.get("url")] = item

    return items


def get_pelis_vistas(browser):
    browser.get(base_url + "/pelis/seen")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    items = dict()
    for row in rows:
        item = get_item_info(browser, row)
        items[item.get("url")] = item

    return items


def get_series_siguiendo(browser):
    browser.get(base_url + "/series/following")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    items = dict()
    for row in rows:
        item = get_item_info(browser, row)
        items[item.get("url")] = item

    return items


def get_series_favoritas(browser):
    browser.get(base_url + "/series/favorites")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    items = dict()
    for row in rows:
        item = get_item_info(browser, row)
        items[item.get("url")] = item

    return items


def get_series_pendientes(browser):
    browser.get(base_url + "/series/pending")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    items = dict()
    for row in rows:
        item = get_item_info(browser, row)
        items[item.get("url")] = item

    return items


def get_series_vistas(browser):
    browser.get(base_url + "/series/seen")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    items = dict()
    for row in rows:
        item = get_item_info(browser, row)
        items[item.get("url")] = item

    return items


def get_item_info(browser, row):
    d = dict()

    d["nombre"] = row.select_one("div.media-title").text
    d["url"] = row.select_one("a[data-container='body']")["href"]

    browser.get(d.get("url"))
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    if content.select_one("div.external-links-container") is not None:
        d["imdb_id"] = content.select_one(
            "div.external-links-container > ul > li > a")["href"].split("/")[4]
        d["imdb_url"] = content.select_one(
            "div.external-links-container > ul > li > a")["href"]
    else:
        d["imdb_id"] = None
        d["imdb_url"] = None

    return d


if __name__ == "__main__":
    try:
        execute()

    except Exception as e:
        print("\n[*]", str(e))

    except KeyboardInterrupt:
        print("\n[*] Ejecución detenida")
