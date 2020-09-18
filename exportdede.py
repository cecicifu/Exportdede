#!/usr/bin/python3
# coding: utf-8

import signal
import threading
import sys
import os
import json
from time import sleep

import pytesseract
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

try:
    from PIL import Image
except ImportError:
    import Image

base_url = "https://www.megadede.com"
timeout = 2

row_element = "div.media-container"
title_element = "div.media-title"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def exit_handler(key, frame):
    print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
          "] Exiting...\n")
    exit(1)


signal.signal(signal.SIGINT, exit_handler)


def execute():
    try:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "] Ejecutando herramienta..\n")

        sleep(timeout)

        option = webdriver.ChromeOptions()
        option.add_argument("-incognito")

        browser = webdriver.Chrome(
            executable_path='chromedriver.exe', options=option)

        browser.get(base_url + "/login")

        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "] Abriendo navegador.. inicia sesión para continuar.\n")

        sleep(timeout)

        wait = WebDriverWait(browser, 60)

        login = wait.until(ec.visibility_of_element_located(
            (By.CLASS_NAME, "username")))

        ActionChains(browser).move_to_element(login).perform()

        if (login):
            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Has iniciado sesión correctamente!\n")
            browser.minimize_window()

            sleep(timeout)

            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Mostrando listas..\n")

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
                }
            }

            print(json.dumps(listas))

            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Exportando archivo JSON..\n")

            sleep(timeout)

            with open('lists.json', 'w') as outfile:
                json.dump(listas, outfile)

            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Archivo exportado (lists.json)!\n")

            sleep(timeout)

            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Finalizando herramienta..\n")

            sleep(timeout)

        else:
            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] No se ha iniciado sesion correctamente o ha ocurrido un error!\n")

            sleep(timeout)

            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Finalizando herramienta..\n")

        browser.quit()

    except Exception as e:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "]", str(e), "\n")


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
        threading.Thread(target=execute).start()
    except Exception as e:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "]", str(e), "\n")

        sleep(timeout)

        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "] Finalizando herramienta..\n")
