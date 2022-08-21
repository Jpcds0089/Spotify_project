import os
import time
import random
from pyautogui import alert
from datetime import datetime
from json import (loads, dump)
from colorama import (Fore, Style)
from inspect import (getfile, currentframe)
from selenium.webdriver.common.by import By
from selenium.webdriver import (Firefox, Chrome)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (element_to_be_clickable, presence_of_element_located,\
                                                            number_of_windows_to_be)


# _Source______________________________________________________________________________________________________________#


class Spotify:
    def __init__(self):
        self.Print("\nIniciando configurações", "blue")

        # Folders
        self.main_folder = os.path.dirname(os.path.abspath(getfile(currentframe())))[0:-7]
        self.main_folders = {"settings": r"{}\data\settings".format(self.main_folder)}

        # Json sentings
        self.locate_settings = r"{}\settings.json".format(self.main_folders["settings"])
        self.init_configs = loads(open(self.locate_settings).read())

        # Webdriver
        self.browser = None
        if "Firefox" in self.init_configs["browser"].capitalize():
            self.driver = Firefox()
            self.browser = "Firefox"
        elif "Chrome" in self.init_configs["browser"].capitalize():
            self.driver = Chrome()
            self.browser = "Chrome"
        else:
            self.driver = Firefox()
            self.browser = "Firefox"

        self.waint = WebDriverWait(self.driver, 10, poll_frequency=1)
        self.SaveInformations(self.locate_settings, browser=self.browser)
        self.driver.set_window_size(self.init_configs["window_size_x"], self.init_configs["window_size_y"])
        self.driver.set_window_rect(self.init_configs["window_position_x"], self.init_configs["window_position_y"])

        # Urls
        self.urls = {
            "sing_in_spotify": "https://accounts.spotify.com/login?continue=https%3A%2F%2Fopen.spotify.com%2F",
            "liked_songs_spotify": "https://open.spotify.com/collection/tracks"
         }

        # User
        self.email = ""
        self.password = ""

        # Global variables
        self.songs_number = None
        self.spotify_songs_titles = []
        self.spotify_songs_artists = []
        self.spotify_songs_titles_and_artists = []

    def Start(self):
        self.SingInSpotify()
        self.SaveLikedSoungs()

    def SingInSpotify(self):
        # Entrando no site
        self.driver.get(self.urls["sing_in_spotify"])

        # Digitando o e-mail
        input_email = 'input[id="login-username"]'
        self.Click(input_email)
        self.Write(input_email, self.email)

        # Delay
        time.sleep(random.random())

        # Digitando a senha
        input_password = 'input[id="login-password"]'
        self.Click(input_password)
        self.Write(input_password, self.password)

        # Delay
        time.sleep(random.random())

        # Clickando em entrar
        loc_login_button = 'button[id="login-button"]'
        self.Click(loc_login_button)

        # Salvando informações
        self.SaveInformations(self.locate_settings, browser=self.browser,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              )

        # Verificando se tudo está correto
        try:
            asserting = self.driver.find_element((By.CSS_SELECTOR, 'span[class="Message-sc-15vkh7g-0 jHItEP"]'))
        except:
            asserting = None
        assert asserting is None, "E-mail ou senha incorreto "

    def SaveLikedSoungs(self):
        # Delay
        time.sleep(random.randint(1, 2))

        # Indo para o site das músicas favoritas
        self.driver.get(self.urls["liked_songs_spotify"])

        # Verificando se tudo está correto
        assert str(self.driver.current_url).split()[-1] == "tracks", 'Na url está: "{}" ao invéz de "tracks"'.format(
            str(self.driver.current_url).split()[-1])

        # Obtendo quantidade de músicas
        loc = (By.CSS_SELECTOR, 'span[class="Type__TypeElement-goli3j-0 jsusuc VrRwdIZO0sRX1lsWxJBe"]')
        self.waint.until(element_to_be_clickable(loc))
        self.songs_number = self.driver.find_elements(*loc)[-1].text

        # Obtendo título das músicas
        loc = (By.CSS_SELECTOR,
               'div[class="Type__TypeElement-goli3j-0 gwYBEX t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line"]')
        self.spotify_songs_titles = self.driver.find_elements(*loc)

        # Verificando se tudo está correto
        assert int(self.songs_number) == len(self.spotify_songs_titles), \
            "O número de músicas não condiz com a quantidade de títulos obtidos"

        # Obtendo autores das músicas
        loc = (By.CSS_SELECTOR,
               'span[class="Type__TypeElement-goli3j-0 eDbSCl rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line"]')
        self.spotify_songs_artists = self.driver.find_elements(*loc)

        # Verificando se tudo está correto
        assert int(self.songs_number) == len(self.spotify_songs_artists), \
            "O número de músicas não condiz com a quantidade de artistas obtidos"

        for title in self.spotify_songs_titles:
            for artists in self.spotify_songs_artists:
                self.spotify_songs_titles_and_artists.append([title.text, artists.text])

        # Salvando informações
        self.SaveInformations(self.locate_settings, browser=self.browser,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              )

        # Verificando se tudo está correto
        print(self.spotify_songs_titles_and_artists)

    def Quit(self):
        # Salvando informações
        self.SaveInformations(self.locate_settings, browser=self.browser,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              )

        # Fechando o driver
        self.driver.quit()

        # Informando que a automação foi finalizada
        clock = str(datetime.now().time())[:8].split(':')
        if 5 < int(clock[0]) <= 11:
            alert(title='Altomação finalizada', text='A Altomação acaba de ser finalizada. Tenha um bom dia!')
        if 11 < int(clock[0]) <= 17:
            alert(title='Altomação finalizada', text='A Altomação acaba de ser finalizada. Tenha uma boa tarde!')
        if 17 < int(clock[0]) <= 23 or -1 < int(clock[0]) <= 5:
            alert(title='Altomação finalizada', text='A Altomação acaba de ser finalizada. Tenha uma boa noite!')

    def Click(self, loc_by_css_locator: str):
        time.sleep(random.random() / random.randint(2, 3))
        locator = (By.CSS_SELECTOR, loc_by_css_locator)
        self.waint.until(element_to_be_clickable(locator))
        self.driver.find_element(*locator).click()

    def Write(self, loc_by_css_locator: str, text: str):
        locator = (By.CSS_SELECTOR, loc_by_css_locator)
        self.waint.until(element_to_be_clickable(locator))
        self.driver.find_element(*locator).clear()
        for letra in text:
            self.driver.find_element(*locator).send_keys(letra)
            time.sleep(random.random() / random.randint(1, 3))

    def Print(self, text: str, color="RED" or "GREEN" or "BLUE" or "WHITE" or "BLACK" or "MAGENTA" or "CYAN" or "YELLOW"):
        color = color.upper()
        if color == "RED":
            print(Fore.RED + text + Style.RESET_ALL)
        elif color == "GREEN":
            print(Fore.GREEN + text + Style.RESET_ALL)
        elif color == "BLUE":
            print(Fore.BLUE + text + Style.RESET_ALL)
        elif color == "WHITE":
            print(Fore.WHITE + text + Style.RESET_ALL)
        elif color == "BLACK":
            print(Fore.BLACK + text + Style.RESET_ALL)
        elif color == "MAGENTA":
            print(Fore.MAGENTA + text + Style.RESET_ALL)
        elif color == "CYAN":
            print(Fore.CYAN + text + Style.RESET_ALL)
        elif color == "YELLOW":
            print(Fore.YELLOW + text + Style.RESET_ALL)

    def SaveInformations(self, locate_setting, browser="firefox", window_size_x=1200, window_size_y=1000,
                         window_position_x=0, window_position_y=0):
        with open(locate_setting, "w") as setting:
            dump({
                    "browser": browser,
                    "window_size_x": window_size_x,
                    "window_size_y": window_size_y,
                    "window_position_x": window_position_x,
                    "window_position_y": window_position_y,
                }, setting)


# _Init________________________________________________________________________________________________________________#


bot = Spotify()
bot.Start()


# _Finish______________________________________________________________________________________________________________#


# bot.Quit()
