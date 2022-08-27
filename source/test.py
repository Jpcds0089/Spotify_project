import os
from json import (loads, dump)
from json.decoder import JSONDecodeError
from selenium.webdriver import Firefox
from inspect import (getfile, currentframe)
from selenium.common.exceptions import NoSuchElementException


main_folder = os.path.dirname(os.path.abspath(getfile(currentframe())))[0:-7]
main_folders = {
    "settings": r"{}\data\settings".format(main_folder),
    "add_ons": r"{}\data\add_ons".format(main_folder),
    "temporary": r"{}\data\temporary".format(main_folder)
}
locate_settings = r"{}\settings.json".format(main_folders["settings"])
locate_settings1 = r"{}\spotify_songs.json".format(main_folders["temporary"])
init_configs = loads(open(locate_settings).read())
profile = r"C:\Users\{}\AppData\Roaming\Mozilla\Firefox\Profiles\{}".format(
    os.getenv('USERNAME'), init_configs["profile"])
#driver = Firefox(firefox_profile=profile)

""""
spotify_songs_titles_artists_and_times = [[1, 1, 1], [2, 2, 2], [3, 3, 3]]
with open(r"{}\spotify_songs.json".format(main_folders["temporary"]), "w") as setting:
    dump(spotify_songs_titles_artists_and_times, setting)
"""

# Salvando músicas em um aquivo temporário json
with open(r"{}\spotify_songs.json".format(main_folders["temporary"]), "w") as setting:
    dump(None, setting)

try:
    init_configs = loads(open(locate_settings1).read())
    print(init_configs)
    if init_configs is None:
        print("Simmm")
except JSONDecodeError:
    print(JSONDecodeError)