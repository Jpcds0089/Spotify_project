import time
import random
from colorama import (Fore, Style)
from selenium.webdriver.common.by import By
from selenium.webdriver import (Firefox, Chrome)
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable, presence_of_element_located, number_of_windows_to_be


# _Source______________________________________________________________________________________________________________#


class Spotify:
    def __init__(self):
        self.Print("\nIniciando configurações", "blue")
        # Scripts

        # Json sentings

        # Webdriver
        self.driver = Firefox()
        self.waint = WebDriverWait(self.driver, 10, poll_frequency=1)

        # Urls
        self.urls = {
            "sing_in_spotify": "https://accounts.spotify.com/login?continue=https%3A%2F%2Fopen.spotify.com%2F"
        }

        # User
        self.email = input("Escreva seu email ou usuário do Spotify aqui: ")
        self.password = input("Escreva sua senha do Spotify aqui: ")

    def Start(self):
        self.SingInSpotify()

    def SingInSpotify(self):
        # Entrando no site
        self.driver.get(self.urls["sing_in_spotify"])

        # Digitando o e-mail
        input_email = 'input[id="login-username"]'
        self.Click(input_email)
        self.Write(input_email, self.email)

        # Delay
        time.sleep(random.random() / random.randint(1, 3))
        
        # Digitando a senha
        input_password = 'input[id="login-password"]'
        self.Click(input_password)
        self.Write(input_password, self.password)

        # Clickando em entrar
        loc_login_button = 'button[id="login-button"]'
        self.Click(loc_login_button)

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

    def Print(self, text:str, color="RED" or "GREEN" or "BLUE" or "WHITE" or "BLACK" or "MAGENTA" or "CYAN" or "YELLOW"):
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

    @staticmethod
    def digite_como_uma_pessoa(frase, campo_input_unico):
        print("Digitando...")
        for letra in frase:
            campo_input_unico.send_keys(letra)
            time.sleep(random.randint(1, 5) / 30)


# _Init________________________________________________________________________________________________________________#


bot = Spotify()
bot.Start()
