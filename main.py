import customtkinter
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import subprocess
import speech_recognition

def build_gui():
    width_height = "800x500"
    root = customtkinter.CTk()
    root.geometry(width_height)

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(expand=True, fill="both", anchor="center")

    label = customtkinter.CTkLabel(master=frame, text="Spotify Search App")
    label.pack(pady=10, padx=10)

    global entry
    entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter a song")
    entry.pack(pady=10, padx=10)

    button1 = customtkinter.CTkButton(master=frame, text="Enter", command=button_click)
    button1.pack(pady=10, padx=10)

    button2 = customtkinter.CTkButton(master=frame, text="Voice Search", command=button_click)
    button2.pack(pady=10, padx=10)

    return root

def start_app(command):
    try:
        if os.name == 'nt':  # For Windows
            os.system("spotify")
        elif os.name == 'posix':  # For Unix/Linux/MacOS
            subprocess.run(['echo', '-e', f'{command}\n'], check=True, shell=True)
        else:
            print("Unsupported OS")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

def button_click():
    song_name = entry.get()
    search_func(song_name)


def get_token():
    global token
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_string = client_id +":"+client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    token_url = os.getenv("TOKEN_URL")
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(token_url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

def search_func(song_name):
    search_url = os.getenv("SEARCH_URL")
    headers = {"Authorization": "Bearer "+token}
    query = f"?q={song_name}&type=track&limit=1"
    query_url = search_url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"][0]
    if len(json_result)==0:
        print("No songs found")
        return None
    spotify_song_uri = json_result["uri"]
    os.system(f"start {spotify_song_uri} /silent")

def voice_search():
    recognizer = speech_recognition.Recognizer()

def main():
    get_token()
    root = build_gui()
    root.mainloop()

if __name__ == "__main__":
    main()