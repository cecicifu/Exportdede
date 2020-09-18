#!/usr/bin/python3
# coding: utf-8

import requests
import signal
import threading
import sys
import os
import pytesseract
from time import sleep
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

# GLOBAL VARS
base_url = "https://www.megadede.com"

pelis_favorites = "/pelis/favorites"
pelis_pending = "/pelis/pending"
pelis_seen = "/pelis/seen"

series_following = "/series/following"
series_favorites = "/series/favorites"
series_pending = "/series/pending"
series_seen = "/series/seen"


location = None
timeout = 2

s = requests.Session()
s.headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
}
# FREE SSL PROXIES https://www.sslproxies.org/
s.proxies = {
    "https://185.110.96.11:3128",
    "https://185.110.96.12:3128",
    "https://78.46.81.7:1080",
    "https://51.255.103.170:3129",
    "https://188.40.183.189:1080",
    "https://188.165.141.114:3129",
}


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def signal_handler(key, frame):
    print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
          "] Exiting...\n")
    exit(1)


signal.signal(signal.SIGINT, signal_handler)


def execute():
    try:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "] Ejecutando script..\n")

        option = webdriver.ChromeOptions()
        option.add_argument("-incognito")
        # option.add_argument("--headless")
        # option.add_argument("disable-gpu")

        browser = webdriver.Chrome(
            executable_path='chromedriver.exe', options=option)

        browser.get(base_url + "/login")

        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "] Necesitas iniciar sesión para que el script continue..\n")

        wait = WebDriverWait(browser, 60)

        login = wait.until(ec.visibility_of_element_located(
            (By.CLASS_NAME, "username")))

        ActionChains(browser).move_to_element(login).perform()

        if (login):
            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Has iniciado sesión correctamente!\n")
            browser.minimize_window()

            # Capturar pelis
            print(get_pelis_favorites(browser))
            print(get_pelis_pending(browser))
            print(get_pelis_seen(browser))

            # Capturar series
            print(get_series_following(browser))
            print(get_series_favorites(browser))
            print(get_series_pending(browser))
            print(get_series_seen(browser))

            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] Listas exportadas!\n")

        else:
            print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
                  "] No se ha iniciado sesion correctamente o ha ocurrido un error!\n")

        browser.quit()

    except requests.exceptions.Timeout:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "] Timeout exception\n")
    except requests.exceptions.TooManyRedirects:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "] Too many redirects exception\n")
    except Exception as e:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "]", str(e), "\n")


def get_pelis_favorites(browser):
    browser.get(base_url + pelis_favorites)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    peliculas = []
    for row in rows:
        peliculas.append(row.select_one("div.media-title").text)

    return peliculas


def get_pelis_pending(browser):
    browser.get(base_url + pelis_pending)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    peliculas = []
    for row in rows:
        peliculas.append(row.select_one("div.media-title").text)

    return peliculas


def get_pelis_seen(browser):
    browser.get(base_url + pelis_seen)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    peliculas = []
    for row in rows:
        peliculas.append(row.select_one("div.media-title").text)

    return peliculas


def get_series_following(browser):
    browser.get(base_url + series_following)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    series = []
    for row in rows:
        series.append(row.select_one("div.media-title").text)

    return series


def get_series_favorites(browser):
    browser.get(base_url + series_favorites)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    series = []
    for row in rows:
        series.append(row.select_one("div.media-title").text)

    return series


def get_series_pending(browser):
    browser.get(base_url + series_pending)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    series = []
    for row in rows:
        series.append(row.select_one("div.media-title").text)

    return series


def get_series_seen(browser):
    browser.get(base_url + series_seen)
    body = browser.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    content = BeautifulSoup(source, "html.parser")

    rows = content.select("div.media-container")

    series = []
    for row in rows:
        series.append(row.select_one("div.media-title").text)

    return series


if __name__ == "__main__":
    try:
        threading.Thread(target=execute).start()
    except Exception as e:
        print("\n" + bcolors.OKGREEN + "[" + bcolors.ENDC + bcolors.OKBLUE + "*" + bcolors.OKGREEN +
              "]", str(e), "\n")
