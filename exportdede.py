#!/usr/bin/python3
# coding: utf-8

import json
from time import sleep
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

base_url = "https://www.megadede.com"
timeout = 2

row_element = "div.media-container"
title_element = "div.media-title"

list_element = "div#your-listas > div.lista"
name_element = "div.content > h2"
description_element = "div.description"
author_element = "a.username"
followers_element = "span.number"
item_element = "div.media-container"
item_title_element = "div.media-title"


def execute():
    print("\n[*] Ejecutando herramienta..\n")

    sleep(timeout)

    option = webdriver.ChromeOptions()
    option.add_argument("-incognito")

    browser = webdriver.Chrome(
        executable_path='libs/chromedriver.exe', options=option)

    browser.get(base_url + "/login")

    print("\n[*] Abriendo navegador..\n")

    sleep(timeout)

    print("\n[*] Inicia sesión para continuar..\n")

    sleep(timeout)

    wait = WebDriverWait(browser, 60)

    login = wait.until(ec.visibility_of_element_located(
        (By.CLASS_NAME, "username")))

    ActionChains(browser).move_to_element(login).perform()

    if login:
        print("\n[*] Has iniciado sesión correctamente!\n")
        browser.minimize_window()

        sleep(timeout)

        print("\n[*] Mostrando listas..\n")

        sleep(timeout)

        listas = {
            "peliculas": {
                "peliculas_favorites": get_pelis_favorites(browser),
                "peliculas_pending": get_pelis_pending(browser),
                "peliculas_seen": get_pelis_seen(browser),
            },
            "series": {
                "series_following": get_series_following(browser),
                "series_favorites": get_series_favorites(browser),
                "series_pending": get_series_pending(browser),
                "series_seen": get_series_seen(browser),
            },
            "listas": get_listas(browser),
        }

        print(json.dumps(listas))

        print("\n[*] Exportando archivo JSON..\n")

        sleep(timeout)

        with open('lists.json', 'w') as outfile:
            json.dump(listas, outfile)

        print("\n[*] Exportando archivo CSV..\n")

        sleep(timeout)

        df = pd.read_json(r'lists.json')
        df.to_csv(r'lists.csv', index=None)

        print("\n[*] Se ha exportado satisfactoriamente!\n")

        sleep(timeout)

        print("\n[*] Finalizando herramienta..\n")

        sleep(timeout)

    else:
        print(
            "\n[*] No se ha iniciado sesion correctamente o ha ocurrido un error!\n")

        sleep(timeout)

        print("\n[*] Finalizando herramienta..\n")

    browser.quit()


def get_listas(browser):
    browser.get(base_url + "/listas")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(list_element)

    items = dict()
    for row in rows:
        d = dict()
        href = row.select_one("a")["href"]

        browser.get(base_url + href)
        body = browser.execute_script("return document.body")
        source = body.get_attribute('innerHTML')
        content = BeautifulSoup(source, "html.parser")

        d["url"] = href

        if content.select_one(name_element) is not None:
            d["nombre"] = content.select_one(name_element).text
        else:
            d["nombre"] = "null"

        if content.select_one(description_element) is not None:
            d["descripcion"] = content.select_one(description_element).text
        else:
            d["descripcion"] = "null"

        if content.select_one(author_element) is not None:
            d["autor"] = content.select_one(author_element).text.strip()
        else:
            d["autor"] = "null"

        if content.select_one(followers_element) is not None:
            d["seguidores"] = content.select_one(followers_element).text
        else:
            d["seguidores"] = "null"

        if content.select_one(item_element) is not None:
            sub_items = content.select(item_element)

            d["lista"] = []
            for sub_item in sub_items:
                d["lista"].append(sub_item.select_one(item_title_element).text)
        else:
            d["lista"] = "null"

        items[d.get("nombre")] = d

    return items


def get_pelis_favorites(browser):
    browser.get(base_url + "/pelis/favorites")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(row_element)

    items = []
    for row in rows:
        items.append(row.select_one(title_element).text)

    return items


def get_pelis_pending(browser):
    browser.get(base_url + "/pelis/pending")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(row_element)

    items = []
    for row in rows:
        items.append(row.select_one(title_element).text)

    return items


def get_pelis_seen(browser):
    browser.get(base_url + "/pelis/seen")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(row_element)

    items = []
    for row in rows:
        items.append(row.select_one(title_element).text)

    return items


def get_series_following(browser):
    browser.get(base_url + "/series/following")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(row_element)

    items = []
    for row in rows:
        items.append(row.select_one(title_element).text)

    return items


def get_series_favorites(browser):
    browser.get(base_url + "/series/favorites")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(row_element)

    items = []
    for row in rows:
        items.append(row.select_one(title_element).text)

    return items


def get_series_pending(browser):
    browser.get(base_url + "/series/pending")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(row_element)

    items = []
    for row in rows:
        items.append(row.select_one(title_element).text)

    return items


def get_series_seen(browser):
    browser.get(base_url + "/series/seen")
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select(row_element)

    items = []
    for row in rows:
        items.append(row.select_one(title_element).text)

    return items


if __name__ == "__main__":
    try:
        execute()
    except Exception as e:
        print("\n[*]", str(e), "\n")

        sleep(timeout)

        print("\n[*] Finalizando herramienta..\n")
