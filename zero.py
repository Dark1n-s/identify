# ------------------------------------------Modules import-------------------------------------------#

import telebot
from telebot import types
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------Authorization--------------------------------------------------#

keys = ["TOKEN", "SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET"]
TOKEN = os.getenv(keys[0])
bot = telebot.TeleBot(TOKEN)
SPOTIPY_CLIENT_ID = os.getenv(keys[1])
SPOTIPY_CLIENT_SECRET = os.getenv(keys[2])
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))


# -------------------------------------------Main Code--------------------------------------------------#

def get_current_track():
    try:
        current_track = sp.current_playback()
        if current_track is not None and 'item' in current_track:
            track_name = current_track['item']['name']
            artists = ', '.join([artist['name'] for artist in current_track['item']['artists']])
            return f"Currently listening to 🎧 <b>{track_name} - {artists}</b>"
        else:
            return "No track currently playing."
    except Exception:
        return "Error getting current track."


# -------------------------------------------Bot Code--------------------------------------------------#

@bot.message_handler(commands=['song'])
def send_current_song(message):
    current_song = get_current_track()
    bot.send_message(message.chat.id, current_song, parse_mode='html')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton('Get Current Song🎧')
    markup.add(btn)
    bot.send_message(message.chat.id,
                     f"<b>Hi <i>{message.from_user.first_name}</i>! If you want to know what i`m 🎧 listening to, just type /song \nor click button below⬇️</b>",
                     parse_mode='html', reply_markup=markup)
    while True:
        time.sleep(30)
        current_song = get_current_track()
        bot.send_message(message.chat.id, current_song, parse_mode='html')


@bot.message_handler()
def send_song(message):
    if message.text == "Get Current Song🎧":
        current_song = get_current_track()
        bot.send_message(message.chat.id, current_song, parse_mode='html')


@bot.message_handler()
def auto_send(message):
    current_song = get_current_track()
    bot.send_message(message.chat.id, current_song, parse_mode='html')


bot.polling(none_stop=True)
