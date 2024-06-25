import customtkinter
from dotenv import load_dotenv
import os

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

    return root

def button_click():
    song_name = entry.get()

def get_token():
    load_dotenv()
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    auth_string = client_id +":"+client_secret
    auth_bytes = auth_string.encode("utf-8")
    

def main():
    root = build_gui()
    get_token()
    root.mainloop()

if __name__ == "__main__":
    main()