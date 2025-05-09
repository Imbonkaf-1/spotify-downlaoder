import requests
import json
import os
from dotenv import load_dotenv

#Function gets the access token to be used in requests
def get_access_token():

    #Client id and secrets and the refresh token in the .env file
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    refresh_token = os.getenv("REFRESH_TOKEN")

    #the spotify urls to authorize and get the token 
    auth_url = "https://accounts.spotify.com/authorize"
    url = "https://accounts.spotify.com/api/token"

    #the params for the token request
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    #Gets a token as a response and returns to be used 
    response = requests.post(url, data=data, headers=headers)
    token = response.json()
    token = token.get("access_token")
    return token

#Simple search using spotifys API
def Search():

    #the token from the previous function and the search api
    access = get_access_token()
    url = "https://api.spotify.com/v1/search"

    name = []
    artist = []
    track = []

    query = input("Enter song name: ")

    #params to push to the search api
    query = {
        "q": query,
        "type": "track"
    }

    headers = {
        "Authorization": f"Bearer {access}"
    }

    #Gets a json file of the first 20 results 
    response = (requests.get(url, headers=headers, params=query)).json()
    items = response.get("tracks", {}).get("items", {})

    index = 0

    #Finds and seperates the track names, artists and urls
    for item in items:

        name.append(item.get("name"))
        artist.append(item.get("artists")[0].get("name"))
        track.append(item.get("external_urls"))

        print(f"{index + 1}: {name[index]} - {artist[index]}")

        index = index + 1

    #To ask the user what song they want to download form the list
    while True:
        choice = input("Song? (1-20): ")

        try:
            choice = int(choice)
            if(choice - 1 >= 0 and choice - 1 < 20):
                break
            else:
                continue
        except:
            print("NOT A NUMBER!!!")
            continue

    #Chooses the track from the list of 20 based on the users choice    
    track = track[choice - 1].get("spotify")
    name = name[choice - 1]
    artist = artist[choice - 1]

    return track, name

#Downloads the song
def DownloadSong(track, name):

    #Takes the URL from the prev function and pushes it to the fabdl api
    url = track
    response = (requests.get(f"https://api.fabdl.com/spotify/get?url={url}")).json()

    #Gets the id and gid from the prev json response
    track_id = response["result"]["id"]
    gid = response["result"]["gid"]

    #Sends a request to the fabdl download api with the id and gid 
    download_link = (requests.get(f"https://api.fabdl.com/spotify/mp3-convert-task/{gid}/{track_id}")).json()
    status = download_link["result"]["status"]
    
    #checks if the download link exists 
    if status != 3:
        print("No download link found")
        print("P.s if you cant find it try the other ones with the same name (gotta fix that teehee :3)")
    else: 
        #pushes a request using the download link frmo fabdl from the prev request
        download_link = download_link["result"]["download_url"]
        download_link = f"https://api.fabdl.com{download_link}"

        download = requests.get(download_link)

        #creates a mp3 file 
        file = open(f"{name}.mp3", "wb")
        file.write(download.content)
        file.close()


access = get_access_token

track, name = Search()

DownloadSong(track, name)

    












