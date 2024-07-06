import os
from dotenv import load_dotenv
import base64
import json
from requests import post, get
import speech_recognition
import urllib.request
from PIL import Image
import io
import customtkinter

class spotify_api:
    def __init__(self):
        self.token = None

    def get_token(self):
        load_dotenv()
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        token_url = os.getenv("TOKEN_URL")
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(token_url, headers=headers, data=data)
        json_result = result.json()
        self.token = json_result["access_token"]
        return self.token

    def search_track(self, song_name):
        if not self.token:
            print("Token not available. Please fetch token first.")
            return None
        search_url = os.getenv("SEARCH_URL")
        headers = {"Authorization": "Bearer " + self.token}
        query = f"?q={song_name}&type=track&limit=1"
        query_url = search_url + query
        result = get(query_url, headers=headers)
        json_result = result.json()["tracks"]["items"]

        if not json_result:
            print("No songs found")
            return None

        spotify_song_uri = json_result[0]["uri"]  # Song uri
        image_link = json_result[0]["album"]["images"][0]["url"]  # Image uri

        return spotify_song_uri, image_link

class search_app:
    def __init__(self):
        self.root = customtkinter.CTk()
        self.root.geometry("800x500")
        
        frame = customtkinter.CTkFrame(master=self.root)
        frame.pack(expand=True, fill="both", anchor="center")
        
        label_title = customtkinter.CTkLabel(master=frame, text="Spotify Search App")
        label_title.pack(pady=10, padx=10)

        self.entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter a song")
        self.entry.pack(pady=10, padx=10)

        button1 = customtkinter.CTkButton(master=frame, text="Enter", command=self.button_click)
        button1.pack(pady=10, padx=10)

        button2 = customtkinter.CTkButton(master=frame, text="Voice Search", command=self.voice_search)
        button2.pack(pady=10, padx=10)

        self.spotify_api = spotify_api()
        self.recognizer = speech_recognition.Recognizer()

    def link_to_image(self, image_link):
        try:
            with urllib.request.urlopen(image_link) as response:
                raw_data = response.read()
            image = Image.open(io.BytesIO(raw_data))
            processed_image = customtkinter.CTkImage(image)
            return processed_image
        except urllib.error.URLError as e:
            print(f"Error fetching image: {e}")
            return None

    def button_click(self):
        song_name = self.entry.get()
        self.play_track(song_name)

    def voice_search(self):
        try:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = self.recognizer.listen(mic)

                text = self.recognizer.recognize_google(audio)
                self.play_track(text)

        except speech_recognition.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except speech_recognition.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def play_track(self, song_name):
        spotify_uri, image_link = self.spotify_api.search_track(song_name)
        if spotify_uri:
            os.system(f"start {spotify_uri}")  # Open the Spotify URI
            image = self.link_to_image(image_link)
            if image:
                # working
                label_image = customtkinter.CTkLabel(master=self.root, image=image)
                label_image.configure(width=640, height=640)
                label_image.pack()

    def main(self):
        self.spotify_api.get_token()
        self.root.mainloop()

if __name__ == "__main__":
    app = search_app()
    app.main()
