import os
import time
import random
from pyautogui import alert
from datetime import datetime
from json import (loads, dump)
from colorama import (Fore, Style)
from selenium.webdriver import Firefox
from inspect import (getfile, currentframe)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
        obrigatory_informations = ["youtube_playlist_link", "play_list_title", "spotify_songs_link"]
        for informations in obrigatory_informations:
            assert self.init_configs[informations] != "" or self.init_configs[informations] != '', \
                'As seguintes informações devem ser preenchidas: ["youtube_playlist_link", ' \
                '"play_list_title", "spotify_songs_link"]'

        # Webdriver
        self.browser = None
        if self.init_configs["browser"].capitalize().replace(" ", "") == "Firefox":
            profile = r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\{}".format(
                os.getenv('USERNAME'), self.init_configs["profile"])
            self.browser = "Firefox"
            self.profile = self.init_configs["profile"]
            self.driver = Firefox(firefox_profile=profile)
        else:
            self.driver = Firefox()
            self.browser = "Firefox"

        self.action_chains = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 50, poll_frequency=1)
        self.driver.set_window_size(self.init_configs["window_size_x"], self.init_configs["window_size_y"])
        self.driver.set_window_rect(self.init_configs["window_position_x"], self.init_configs["window_position_y"])

        # Urls
        self.urls = {
            "spotify_website": "https://open.spotify.com/",
            "sing_in_spotify": "https://accounts.spotify.com/login?continue=https%3A%2F%2Fopen.spotify.com%2F",
            "liked_songs_spotify": self.init_configs["spotify_songs_link"],
            "youtube": "https://www.youtube.com/",
            'youtube_playlist': self.init_configs["youtube_playlist_link"],
            'search_in_youtube': "https://www.youtube.com/results?search_query="
        }

        # User
        self.play_list_title = self.init_configs["play_list_title"]
        self.spotify_email = self.init_configs["spotify_email"]
        self.spotify_password = self.init_configs["spotify_password"]

        # Global variables
        self.youtube_songs_titles_and_times = []
        self.songs_for_add_in_youtube_playlist = []
        self.spotify_songs_titles_artists_and_times = []

    def Start(self):
        self.SingInSpotify()
        self.SaveLikedSoungs()
        self.SavePlayListSougs()
        self.Comparing()
        self.PutSongsInPlayList()

    def SingInSpotify(self):
        # Entrando no site do Spotify
        self.driver.get(self.urls["spotify_website"])

        # Esperando site carregar
        loc = (By.CSS_SELECTOR, 'div[class="q8AZzDc_1BumBHZg0tZb"]')
        self.wait.until(visibility_of_element_located(loc))

        # Vendo já se está logado
        is_logged = None
        try:
            loc = (By.CSS_SELECTOR, 'button[class="odcjv30UQnjaTv4sylc0"]')
            assert self.driver.find_element(*loc) is not None
            self.Print('Você já está logado', "GREEN")
            is_logged = True
        except NoSuchElementException:
            is_logged = False

        # Verificando se está tudo certo
        assert is_logged is not None

        # Caso não esteja logado logar
        if is_logged is False:
            self.Print("Tentando fazer login no Spotify", "BLUE")
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
        self.SaveInformations(self.locate_settings,
                              browser=self.browser, profile=self.profile,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              play_list_title=self.init_configs["play_list_title"],
                              spotify_songs_link=self.init_configs["spotify_songs_link"],
                              youtube_playlist_link=self.init_configs["youtube_playlist_link"],
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
        loc = (By.CSS_SELECTOR, 'span[class="Type__TypeElement-goli3j-0 cPwEdQ RANLXG3qKB61Bh33I0r2"]')
        self.wait.until(visibility_of_element_located(loc))

        # Obtendo quantidade de músicas
        self.Print("Obtendo quantidade de músicas", "BLUE")
        loc = (By.CSS_SELECTOR, 'span[class="Type__TypeElement-goli3j-0 cPwEdQ RANLXG3qKB61Bh33I0r2"]')
        songs_number = self.driver.find_element(*loc).text
        songs_number = songs_number.split(' ')[0]

        # Obtendo Títulos e durações das músicas
        spotify_songs_times = []
        spotify_songs_titles = []
        spotify_songs_artists = []
        while True:
            # Obtendo título das músicas
            loc = (By.CSS_SELECTOR,'div[class="Type__TypeElement-goli3j-0 gwYBEX t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line"]')
            for title in self.driver.find_elements(*loc):
                if not title in spotify_songs_titles:
                    spotify_songs_titles.append(title)

            # Obtendo título das músicas
            loc = (By.CSS_SELECTOR,
                   'div[class="Type__TypeElement-goli3j-0 gwYBEX t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line"]')
            for title in self.driver.find_elements(*loc):
                if not title in spotify_songs_titles:
                    spotify_songs_titles.append(title)

            # Obtendo autores das músicas
            loc = (By.CSS_SELECTOR,
                   'span[class="Type__TypeElement-goli3j-0 eDbSCl rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line"]')
            for artist in self.driver.find_elements(*loc):
                if not artist in spotify_songs_artists:
                    spotify_songs_artists.append(artist)

            # Obtendo tempo das músicas
            loc = (By.CSS_SELECTOR, 'div[class="Type__TypeElement-goli3j-0 eDbSCl Btg2qHSuepFGBG6X0yEN"]')
            for duraction in self.driver.find_elements(*loc):
                if not duraction in spotify_songs_times:
                    spotify_songs_times.append(duraction)
            self.Print("Quantidade de músicas obtidas: {} de {}".format(len(spotify_songs_titles), int(songs_number)), "MAGENTA")

            # Adicionando as informações obtidas em uma lista
            for title in enumerate(spotify_songs_titles):
                if title[0] + 1 > len(self.spotify_songs_titles_artists_and_times):
                    self.spotify_songs_titles_artists_and_times.append([title[1].text,
                                                                       spotify_songs_artists[title[0]].text,
                                                                       spotify_songs_times[title[0]].text])

            # Rolando a página para obter o restante das músicas
            if not int(songs_number) == len(spotify_songs_titles):
                time.sleep(random.randint(1, 3))
                # self.driver.execute_script("window.scrollTo(0, {})".format(random.randint(50, 100)))
                self.driver.find_element(By.CSS_SELECTOR, 'div[class="ShMHCGsT93epRGdxJp2w Ss6hr6HYpN4wjHJ9GHmi"]').send_keys(Keys.PAGE_DOWN)
                time.sleep(random.randint(1, 3))
            else:
                break

        # Salvando informações
        self.SaveInformations(self.locate_settings,
                              browser=self.browser, profile=self.profile,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              play_list_title=self.init_configs["play_list_title"],
                              spotify_songs_link=self.init_configs["spotify_songs_link"],
                              youtube_playlist_link=self.init_configs["youtube_playlist_link"],
                              )

        # Verificando se tudo está correto
        self.Print("A quantidade de músicas, titulos e artistas foram obtidos com sucesso", "GREEN")
        print(Fore.GREEN + "Título das músicas, tempos e artistas:" + Style.RESET_ALL,
              self.spotify_songs_titles_artists_and_times)

    def SavePlayListSougs(self):
        # Indo para a playlist de músicas no youtube
        self.driver.get(self.urls["youtube_playlist"])

        # Esperar página carregar
        loc = (By.CSS_SELECTOR, 'ytd-button-renderer[id="edit-button"]')
        self.wait.until(visibility_of_element_located(loc), "Sua conta provavelmente não é a propietária desta "
                                                             "play-list")

        # Delay
        time.sleep(1)

        # Obtendo quantidade de músicas
        try:
            loc = (By.CSS_SELECTOR, 'yt-formatted-string[class="style-scope ytd-playlist-sidebar-primary-info-renderer"] > '
                                    'span[class="style-scope yt-formatted-string"]')
            songs_number = self.driver.find_element(*loc).text
        except NoSuchElementException:
            songs_number = "1"

        # Caso tenha algum vídeo indisponível ocuto
        try:
            loc = (By.CSS_SELECTOR, 'ytd-alert-with-button-renderer[class="style-scope ytd-browse"]')
            assert self.driver.find_element(*loc) is not None
            self.Click('yt-icon-button[id="button"][class="dropdown-trigger style-scope ytd-menu-renderer"]')
            self.Click('ytd-menu-navigation-item-renderer[class="style-scope ytd-menu-popup-renderer iron-selected"]')
        except NoSuchElementException:
            pass

        songs_titles = []
        songs_times = []
        while True:
            # Vendo se está na página correta
            assert "playlist" in self.driver.current_url.split("/")[3], "Página incorreta"
            # Obtendo título das músicas
            loc = (By.CSS_SELECTOR, 'a[id="video-title"]')
            for title in self.driver.find_elements(*loc):
                if not title in songs_titles:
                    songs_titles.append(title)
            # Obtendo tempo das músicas
            loc = (By.CSS_SELECTOR, 'ytd-thumbnail-overlay-time-status-renderer[class="style-scope ytd-thumbnail"]')
            for duraction in self.driver.find_elements(*loc):
                if not duraction in songs_times:
                    songs_times.append(duraction)
            self.Print("Quantidade de músicas obtidas: {} de {}".format(len(songs_titles), int(songs_number)), "MAGENTA")
            if int(songs_number) == len(songs_titles) and int(songs_number) == len(songs_times):
                break
            else:
                time.sleep(random.randint(0, 2))
                self.driver.find_element(By.CSS_SELECTOR, 'html').send_keys(Keys.PAGE_DOWN)
                time.sleep(random.randint(0, 2))

        # Adicionando as informações obtidas em uma lista
        for title in enumerate(songs_titles):
            self.youtube_songs_titles_and_times.append([title[1].text, songs_times[title[0]].text])

        # Salvando informações
        self.SaveInformations(self.locate_settings,
                              browser=self.browser, profile=self.profile,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              play_list_title=self.init_configs["play_list_title"],
                              spotify_songs_link=self.init_configs["spotify_songs_link"],
                              youtube_playlist_link=self.init_configs["youtube_playlist_link"],
                              )

        # Verificando se tudo está correto
        self.Print("A quantidade de músicas e titulos foram obtidos com sucesso", "GREEN")
        print(Fore.GREEN + "Título das músicas e tempos:" + Style.RESET_ALL,
              self.youtube_songs_titles_and_times)

    def Comparing(self):
        # Comparando se os títulos e os tempos das músicas obtidas são semelhantes
        self.Print("Comparando se os títulos e os tempos das músicas obtidas são semelhantes", "BLUE")
        print("\n\n")
        songs_exist = []
        for songs in self.spotify_songs_titles_artists_and_times:
            for songs1 in self.youtube_songs_titles_and_times:
                print("Comparando", Fore.LIGHTMAGENTA_EX + '"{}"'.format(songs[0]) + Style.RESET_ALL, "com",
                      Fore.MAGENTA + '"{}"'.format(songs1[0]) + Style.RESET_ALL)
                if songs[0].lower() in songs1[0].lower():
                    if abs(int(songs[2].replace(':', '')) - int(songs1[1].replace(':', ''))) <= 5:
                        self.Print('"{}" já estáva na play-list do youtube!'.format(songs[0]), "YELLOW")
                        songs_exist.append(songs[0])
                        break

        # Obtendo as músicas que serão postas na play-list do youtube
        for songs in self.spotify_songs_titles_artists_and_times:
            print("Proucurando", Fore.LIGHTMAGENTA_EX + '"{}"'.format(songs[0]) + Style.RESET_ALL, "em",
                  Fore.MAGENTA + '"{}"'.format(songs_exist) + Style.RESET_ALL)
            if not songs[0] in songs_exist:
                self.songs_for_add_in_youtube_playlist.append([songs[0] + " " + songs[1], songs[2]])
                # self.songs_time_that_will_add_in_youtube_playlist.append(songs[2])
                self.Print('"{}" foi adicionada na play-list do youtube'.format([songs[0] + " " + songs[1], songs[2]]), "GREEN")

        # Adicionando-as em uma lista
        #self.songs_for_add_in_youtube_playlist = list(set(self.songs_for_add_in_youtube_playlist))
        self.Print("Músicas que serão adicionadas na play-list do youtube:", "MAGENTA")
        print(self.songs_for_add_in_youtube_playlist)
        print("\n\n")

        # Salvando informações
        self.SaveInformations(self.locate_settings,
                              browser=self.browser, profile=self.profile,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              play_list_title=self.init_configs["play_list_title"],
                              spotify_songs_link=self.init_configs["spotify_songs_link"],
                              youtube_playlist_link=self.init_configs["youtube_playlist_link"],
                              )

    def PutSongsInPlayList(self):
        self.Print("Tentando adicionar as músicas na play-list do youtube", "BlUE")
        added = 0
        for song in enumerate(self.songs_for_add_in_youtube_playlist):
            # Pesquisando a música que será adicionada
            self.driver.get(self.urls["search_in_youtube"] + song[1][0].replace(" ", "+"))

            # Esperando página carregar
            loc = (By.CSS_SELECTOR, 'div[id="title-wrapper"]')
            self.wait.until(visibility_of_element_located(loc))

            song_encontred = False
            for i in range(4):
                # Pengado titulo
                loc = (By.CSS_SELECTOR, 'div[id="title-wrapper"]')
                title = self.driver.find_elements(*loc)[i].text

                # Esperando página carregar
                loc = (By.CSS_SELECTOR, 'ytd-thumbnail-overlay-time-status-renderer[class="style-scope ytd-thumbnail"]')
                self.wait.until(visibility_of_element_located(loc))

                # Obtendo duração do vídeo
                loc = (By.CSS_SELECTOR, 'ytd-thumbnail-overlay-time-status-renderer[class="style-scope ytd-thumbnail"]')
                duraction = self.driver.find_elements(*loc)[i].text

                # Procurando semelhanças entre o título da música pesquisada com os títulos do resultado
                title_is_similar = False
                for song_names_part in song[1][0].split(" "):
                    if song_names_part.lower() in title.lower() and song_names_part != " ":
                        title_is_similar = True
                        break

                # Proucurando semelhanças entre as durações
                duraction_is_similar = False
                if title_is_similar:
                    if abs(int(duraction.replace(":", "")) - int(song[1][1].replace(":", ""))) <= 5:
                        self.Print("Música encontrada", "GREEN")
                        duraction_is_similar = True

                # Definindo se a música foi encontrada
                if title_is_similar and duraction_is_similar:
                    song_encontred = True

                # Caso o título e duração se encaixem nos requisitos, adicioná-lo na ply-list
                if song_encontred:
                    # Delay
                    time.sleep(random.randint(1, 2))

                    # Gerando um valor aleatório para descidir se irá clickar no título ou irá direto nos 3 pontinhos
                    value2 = random.randint(0, 100)
                    # Clickando nos 3 pontinhos
                    loc = (By.CSS_SELECTOR, 'div[id="title-wrapper"]')
                    self.action_chains.move_to_element_with_offset(self.driver.find_elements(*loc)[i],
                                                                   random.randint(1, 15),
                                                                   random.randint(1, 15)).perform()

                    # Delay
                    time.sleep(random.randint(1, 2))

                    loc = (By.CSS_SELECTOR, 'ytd-menu-renderer[class="style-scope ytd-video-renderer"] > yt-icon-button[class="dropdown-trigger style-scope ytd-menu-renderer"]')
                    self.action_chains.move_to_element_with_offset(self.driver.find_elements(*loc)[i],
                                                                   random.randint(1, 5),
                                                                   random.randint(1, 5)).click().perform()

                    # Delay
                    time.sleep(random.randint(1, 3))

                    # Clickando em salvar na play-list
                    loc = (By.CSS_SELECTOR, 'tp-yt-paper-item[class="style-scope ytd-menu-service-item-renderer"]')
                    self.action_chains.move_to_element(self.driver.find_elements(*loc)[2]).click().perform()
                    try:
                        # Delay
                        time.sleep(random.randint(1, 3))

                        # Clickando em salvar na play-list escolhida
                        self.Click('div[id="checkbox-label"] > yt-formatted-string[title="{}"]'.format(self.play_list_title))
                    except NoSuchElementException:
                        assert 1 + 1 == 3, "Provavelmente o título da play-list está incorreto"
                    self.Print('A música "{}" acaba de ser adicionada à play-list "{}"'.format(title, self.play_list_title), "MAGENTA")

                    # Clickando no x
                    if value2 >= 50:
                        self.Click('yt-icon-button[id="close-button"][class="style-scope ytd-add-to-playlist-renderer"]')
                    break

            if not song_encontred:
                self.Print('A música "{}" não foi encontrada', "RED")
            else:
                added += 1
                self.Print("Quantidade músicas adicionadas a playlist:{} de {}".format(added, len(self.songs_for_add_in_youtube_playlist)), "CYAN")

            time.sleep(random.randint(5, 10))

            # Salvando informações
            self.SaveInformations(self.locate_settings,
                                  browser=self.browser, profile=self.profile,
                                  window_size_x=self.driver.get_window_size()['width'],
                                  window_size_y=self.driver.get_window_size()['height'],
                                  window_position_x=self.driver.get_window_position()["x"],
                                  window_position_y=self.driver.get_window_position()["y"],
                                  play_list_title=self.init_configs["play_list_title"],
                                  spotify_songs_link=self.init_configs["spotify_songs_link"],
                                  youtube_playlist_link=self.init_configs["youtube_playlist_link"],
                                  )

    def Quit(self):
        # Salvando informações
        self.SaveInformations(self.locate_settings,
                              browser=self.browser, profile=self.profile,
                              window_size_x=self.driver.get_window_size()['width'],
                              window_size_y=self.driver.get_window_size()['height'],
                              window_position_x=self.driver.get_window_position()["x"],
                              window_position_y=self.driver.get_window_position()["y"],
                              play_list_title=self.init_configs["play_list_title"],
                              spotify_songs_link=self.init_configs["spotify_songs_link"],
                              youtube_playlist_link=self.init_configs["youtube_playlist_link"],
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
        time.sleep(random.random())
        locator = (By.CSS_SELECTOR, loc_by_css_locator)
        self.wait.until(element_to_be_clickable(locator))
        self.action_chains.move_to_element(self.driver.find_element(*locator)).click().perform()

    def Write(self, loc_by_css_locator: str, text: str):
        locator = (By.CSS_SELECTOR, loc_by_css_locator)
        self.wait.until(element_to_be_clickable(locator))
        self.driver.find_element(*locator).clear()
        for letra in text:
            self.driver.find_element(*locator).send_keys(letra)
            time.sleep(random.random() / random.randint(1, 2))

    def WaintElementIsPresent(self, loc_by_css_locator: str):
        loc = (By.CSS_SELECTOR, loc_by_css_locator)
        time_remaining = 20
        while True:
            try:
                assert self.driver.find_element(*loc) is not None
                return True
            except NoSuchElementException:
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

    def SaveInformations(self, locate_setting, browser="firefox", window_size_x=1200, window_size_y=1000, window_position_x=0, window_position_y=0,
                         youtube_playlist_link="", play_list_title="", spotify_songs_link="",
                         profile="", spotify_email="", spotify_password=""
                         ):
        if profile is None:
            folder = r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles".format(os.getenv('USERNAME'))
            for root, dirs, files in os.walk(folder):
                profile = r"{}\{}".format(folder, dirs[0])

        with open(locate_setting, "w") as setting:
            dump({
                "browser": browser,
                "window_size_x": window_size_x,
                "window_size_y": window_size_y,
                "window_position_x": window_position_x,
                "window_position_y": window_position_y,
                "profile": profile,
                "youtube_playlist_link": youtube_playlist_link,
                "spotify_songs_link": spotify_songs_link,
                "play_list_title": play_list_title,
                "spotify_email": spotify_email,
                "spotify_password": spotify_password,
            }, setting)


# _Init________________________________________________________________________________________________________________#


bot = Spotify()
bot.Start()


# _Finish______________________________________________________________________________________________________________#


bot.Quit()

