import requests
from spotify import token, playlist
from selenium import webdriver


# This function gets the json data from spotify
def get_json(key):
    query = "https://api.spotify.com/v1/playlists/{}/tracks?fields=items(track(name,artists(name)))".format(key)
    response = requests.get(
        query,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token),
        }
    )
    return response.json()


# This function turns the json data into a usable list
def format_into_list(data):
    bl = True
    track_list = []
    i = 0
    while bl:
        try:
            artist = data['items'][i]['track']['artists'][0]["name"]
            track = data['items'][i]['track']['name']
            track_list.append(track + " " + artist)
        except:
            bl = False
        i = i + 1
    return track_list


# This function will use the above list and generate a list of lists with karaoke codes
def get_karaoke_list(track_info_list):
    driver = webdriver.Firefox()
    success_list = ["Karaoke Codes:"]
    fail_list = ["", "Failed to find:"]
    for track_info in track_info_list:
        driver.get("https://www.clubdam.com/karaokesearch/?keyword={}".format(track_info))
        try:
            driver.implicitly_wait(3)
            url = driver.find_element_by_css_selector("div.song-name>a").get_attribute('href')
            code = url[-7:]
            song_name = driver.find_element_by_css_selector("div.song-name>a").text
            artist_name = driver.find_element_by_css_selector("div.artist-name>a").text
            success_list.append([song_name, artist_name, code])
        except:
            fail_list.append(track_info)
    return success_list + fail_list


# This function will take the above list of lists and return a coherent string
def stringify_results(karaoke_list):
    string_list = []
    for items in karaoke_list:
        if type(items) is list:
            string_list.append(items[0] + ", " + items[1] + ": " + items[2])
        else:
            string_list.append(items)
    return string_list


# This will be the final function that integrates all other functions
def print_playlist_items():
    json_data = get_json(playlist)
    json_list = (format_into_list(json_data))
    karaoke_list = get_karaoke_list(json_list)
    return stringify_results(karaoke_list)


final = "\n".join(print_playlist_items())


newFile = open("list.txt", "w")
newFile.write(final)
