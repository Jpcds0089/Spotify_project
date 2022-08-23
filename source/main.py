import os
import time
import random
from pyautogui import alert
from datetime import datetime
from json import (loads, dump)
from colorama import (Fore, Style)
from inspect import (getfile, currentframe)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import (Firefox, Chrome)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, visibility_of_element_located


# _Source______________________________________________________________________________________________________________#


class Spotify:
    def __init__(self):
        self.Print("\nIniciando configurações", "blue")

        # Folders
        self.main_folder = os.path.dirname(os.path.abspath(getfile(currentframe())))[0:-7]
        self.main_folders = {
            "settings": r"{}\data\settings".format(self.main_folder),
            "add_ons": r"{}\data\add_ons".format(self.main_folder)
        }

        # Json sentings
        self.locate_settings = r"{}\settings.json".format(self.main_folders["settings"])
        self.init_configs = loads(open(self.locate_settings).read())

        # Webdriver
        self.browser = None
        if "Firefox" in self.init_configs["browser"].capitalize():
            self.browser = "Firefox"
            profile = r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\eravxhtl.default-release".format(os.getenv('USERNAME'))
            self.driver = Firefox(firefox_profile=profile)
        elif "Chrome" in self.init_configs["browser"].capitalize():
            self.browser = "Chrome"
            chrome_options = Options()
            chrome_options.add_argument("lang=pt-BR")
            #os.startfile('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\localhost"')
            chrome_options.add_experimental_option("debuggerAddress", "localhost:9222")
            self.driver = Chrome(options=chrome_options)
        else:
            self.driver = Firefox()
            self.browser = "Firefox"

        self.action_chains = ActionChains(self.driver)
        self.waint = WebDriverWait(self.driver, 15, poll_frequency=1)
        self.SaveInformations(self.locate_settings, browser=self.browser)
        self.driver.set_window_size(self.init_configs["window_size_x"], self.init_configs["window_size_y"])
        self.driver.set_window_rect(self.init_configs["window_position_x"], self.init_configs["window_position_y"])

        # Urls
        self.urls = {
            "spotify_website": "https://open.spotify.com/",
            "sing_in_spotify": "https://accounts.spotify.com/login?continue=https%3A%2F%2Fopen.spotify.com%2F",
            "liked_songs_spotify": "https://open.spotify.com/collection/tracks",
            "youtube": "https://www.youtube.com/",
            'youtube_playlist': "https://www.youtube.com/playlist?list=PLsQ7y6rmfgDgv332B8q6BVL7mvjL08mvN"
        }

        # User
        self.spotify_email = ""
        self.spotify_password = ""
        self.youtube_email = ""
        self.youtube_password = ""
        self.youtube_email_verification_code = ""

        # Global variables
        self.youtube_songs_titles_and_times = []
        self.spotify_songs_titles_artists_and_times = []

    def Start(self):
        ...
        # self.SingInSpotify()
        # self.SaveLikedSoungs()
        # self.SavePlayListSougs()
        # self.Comparing()

    def SingInSpotify(self):
        # Entrando no site do Spotify
        self.driver.get(self.urls["spotify_website"])

        # Esperando site carregar
        loc = (By.CSS_SELECTOR, 'a[class="logo WJsKJXEbycxxq8OcGHM1 active"]')
        self.waint.until(element_to_be_clickable(loc))

        # Vendo já se está logado
        is_logged = None
        try:
            loc = (By.CSS_SELECTOR, 'button[class="odcjv30UQnjaTv4sylc0"]')
            assert self.driver.find_element(*loc) is not None
            is_logged = True
        except NoSuchElementException:
            is_logged = False

        # Verificando se está tudo certo
        assert is_logged is not None

        # Caso não esteja logado logar
        if is_logged is False:
            # Entrando no site de login
            self.driver.get(self.urls["sing_in_spotify"])

            # Digitando o e-mail
            input_email = 'input[id="login-username"]'
            self.Click(input_email)
            self.Write(input_email, self.spotify_email)

            # Delay
            time.sleep(random.random())

            # Digitando a senha
            input_password = 'input[id="login-password"]'
            self.Click(input_password)
            self.Write(input_password, self.spotify_password)

            # Delay
            time.sleep(random.random())

            # Clickando em entrar
            loc_login_button = 'button[id="login-button"]'
            self.Click(loc_login_button)

            # Verificando se tudo está correto
            loggin_incorret = None
            try:
                loc = (By.CSS_SELECTOR, 'span[class="Message-sc-15vkh7g-0 jHItEP"]')
                assert self.driver.find_element(*loc) is not None
                loggin_incorret = True
            except NoSuchElementException:
                loggin_incorret = False

            # Verificando se está tudo certo
            assert loggin_incorret is False, "E-mail ou senha incorreto "
            self.Print("Login feito com sucesso", "GREEN")

        # Salvando informações
        self.SaveInformations(self.locate_settings, browser=self.browser,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              )

    def SaveLikedSoungs(self):
        # Delay
        time.sleep(random.randint(1, 2))

        # Indo para o site das músicas favoritas
        self.driver.get(self.urls["liked_songs_spotify"])
        # Verificando se tudo está correto
        assert str(self.driver.current_url).split("/")[-1] == "tracks", 'Na url está: "{}" ao invéz de "tracks"'.format(
            str(self.driver.current_url).split("/")[-1])

        # Esperando site carregar
        loc = (By.CSS_SELECTOR, 'a[class="t_yrXoUO3qGsJS4Y6iXX"]')
        self.waint.until(element_to_be_clickable(loc))

        # Obtendo quantidade de músicas
        loc = (By.CSS_SELECTOR, 'span[class="Type__TypeElement-goli3j-0 jsusuc VrRwdIZO0sRX1lsWxJBe"]')
        songs_number = self.driver.find_elements(*loc)[-1].text

        # Obtendo título das músicas
        loc = (By.CSS_SELECTOR,
               'div[class="Type__TypeElement-goli3j-0 gwYBEX t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line"]')
        spotify_songs_titles = self.driver.find_elements(*loc)
        # Verificando se tudo está correto
        assert int(songs_number) == len(spotify_songs_titles), \
            "O número de músicas não condiz com a quantidade de títulos obtidos"

        # Obtendo autores das músicas
        loc = (By.CSS_SELECTOR,
               'span[class="Type__TypeElement-goli3j-0 eDbSCl rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line"]')
        spotify_songs_artists = self.driver.find_elements(*loc)
        # Verificando se tudo está correto
        assert int(songs_number) == len(spotify_songs_artists), \
            "O número de músicas não condiz com a quantidade de artistas obtidos"

        # Obtendo tempo das músicas
        loc = (By.CSS_SELECTOR, 'div[class="Type__TypeElement-goli3j-0 eDbSCl Btg2qHSuepFGBG6X0yEN"]')
        spotify_songs_times = self.driver.find_elements(*loc)
        # Verificando se tudo está correto
        assert int(songs_number) == len(spotify_songs_times), \
            "O número de músicas não condiz com a quantidade de artistas obtidos"

        # Adicionando as informações obtidas em uma lista
        for title in enumerate(spotify_songs_titles):
            self.spotify_songs_titles_artists_and_times.append([title[1].text,
                                                                spotify_songs_artists[title[0]].text,
                                                                spotify_songs_times[title[0]].text])

        # Salvando informações
        self.SaveInformations(self.locate_settings, browser=self.browser,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              )

        # Verificando se tudo está correto
        self.Print("A quantidade de músicas, titulos e artistas foram obtidos com sucesso", "GREEN")
        print(Fore.GREEN + "Título das músicas, tempos e artistas:" + Style.RESET_ALL,
              self.spotify_songs_titles_artists_and_times)

    def SingInYoutube(self):
        # Indo para o site das músicas favoritas
        self.driver.get(self.urls["youtube"])

        # Esperando site carregar
        self.WaintElementIsPresent('ytd-topbar-logo-renderer[id="logo"]')

        # Vendo já se está logado
        is_logged = None
        try:
            loc = (By.CSS_SELECTOR, 'button[id="avatar-btn"]')
            assert self.driver.find_element(*loc) is not None
            is_logged = True
        except NoSuchElementException:
            is_logged = False

        # Verificando se está tudo certo
        assert is_logged is not None

        # Caso não esteja logado logar
        if is_logged is False:
            # Verificando se tudo está correto
            assert str(self.driver.current_url).split("/")[2] == "www.youtube.com", \
                'Na url está: "{}" ao invéz de "www.youtube.com"'.format(str(self.driver.current_url).split("/")[2])

            # Delay
            time.sleep(random.randint(1, 2))

            # Clickando no botão de fazer login
            self.Click('ytd-button-renderer[class="style-scope ytd-masthead style-suggestive size-small"]')

            # Esperando site carregar
            self.waint.until(element_to_be_clickable((By.CSS_SELECTOR, 'div[class="Xb9hP"]')))

            # Verificando se tudo está correto
            assert str(self.driver.current_url).split("/")[2] == "accounts.google.com", \
                'Na url está: "{}" ao invéz de "accounts.google.com"'.format(
                    str(self.driver.current_url).split("/")[-1])

            # Delay
            time.sleep(random.randint(1, 2))

            # Escrevendo o e-mail passado pelo ultilizador
            self.Write('input[id="identifierId"]', self.youtube_email)
            # Delay
            time.sleep(random.randint(1, 2))
            # Pressionando enter
            self.driver.find_element(By.CSS_SELECTOR, 'input[id="identifierId"]').send_keys(Keys.ENTER)

            # Escrevendo a senha passado pelo ultilizador
            self.Write('input[class="whsOnd zHQkBf"]', self.youtube_password)
            # Delay
            time.sleep(random.randint(1, 2))
            # Pressionando enter
            self.driver.find_element(By.CSS_SELECTOR, 'input[class="whsOnd zHQkBf"').send_keys(Keys.ENTER)

        #
        if self.youtube_email_verification_code is not None or self.youtube_email_verification_code != "":
            ...

    def SavePlayListSougs(self):
        # Indo para a playlist de músicas no youtube
        self.driver.get(self.urls["youtube_playlist"])

        # Esperar página carregar
        self.WaintElementIsPresent('ytd-button-renderer[id="edit-button"]')

        # Delay
        time.sleep(1)

        # Obtendo quantidade de músicas
        loc = (By.CSS_SELECTOR, 'yt-formatted-string[class="style-scope ytd-playlist-sidebar-primary-info-renderer"] > '
                                'span[class="style-scope yt-formatted-string"]')
        songs_number = self.driver.find_element(*loc).text

        # Obtendo título das músicas
        loc = (By.CSS_SELECTOR, 'a[id="video-title"]')
        songs_titles = self.driver.find_elements(*loc)
        # Verificando se tudo está correto
        assert int(songs_number) == len(songs_titles), \
            "O número de músicas não condiz com a quantidade de títulos obtidos"

        # Obtendo tempo das músicas
        loc = (By.CSS_SELECTOR, 'ytd-thumbnail-overlay-time-status-renderer[class="style-scope ytd-thumbnail"]')
        songs_times = self.driver.find_elements(*loc)
        # Verificando se tudo está correto
        assert int(songs_number) == len(songs_times), \
            "O número de músicas não condiz com a quantidade de artistas obtidos"

        # Adicionando as informações obtidas em uma lista
        for title in enumerate(songs_titles):
            self.youtube_songs_titles_and_times.append([title[1].text, songs_times[title[0]].text])

        # Salvando informações
        self.SaveInformations(self.locate_settings, browser=self.browser,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              )

        # Verificando se tudo está correto
        self.Print("A quantidade de músicas e titulos foram obtidos com sucesso", "GREEN")
        print(Fore.GREEN + "Título das músicas e tempos:" + Style.RESET_ALL,
              self.youtube_songs_titles_and_times)

    def Comparing(self):


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
        self.action_chains.move_to_element_with_offset(self.driver.find_element(*locator), random.randint(1, 10),
                                                       random.randint(1, 10)).click().perform()

    def Write(self, loc_by_css_locator: str, text: str):
        locator = (By.CSS_SELECTOR, loc_by_css_locator)
        self.waint.until(element_to_be_clickable(locator))
        self.driver.find_element(*locator).clear()
        for letra in text:
            self.driver.find_element(*locator).send_keys(letra)
            time.sleep(random.random() / random.randint(1, 3))

    def WaintElementIsPresent(self, loc_by_css_locator: str):
        loc = (By.CSS_SELECTOR, loc_by_css_locator)
        time_remaining = 20
        while True:
            if self.driver.find_element(*loc) is not None:
                return True
            else:
                time.sleep(0.5)
                time_remaining = -1
            assert time_remaining != 0, "TimeoutException"

    def Print(self, text: str,
              color="RED" or "GREEN" or "BLUE" or "WHITE" or "BLACK" or "MAGENTA" or "CYAN" or "YELLOW"):
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
self = bot

# _Finish______________________________________________________________________________________________________________#


# bot.Quit()
