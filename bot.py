import json
import random
from telebot import TeleBot
from telebot import types
from openai import OpenAI
import requests

api_key_telegram = "7075406704:AAF5wtkuN0vgUFEscI_oNbUWPIOgRSfQ_3Y"
api_key_openai = "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"
base_url = "https://frases.docapi.dev/frase/obter"

bot = TeleBot(api_key_telegram)
gpt = OpenAI(api_key=api_key_openai)

message_list = []

def send_message_to_gpt(message_receive, message_list=[]):
    message_list.append(
        {"role": "user", "content": message_receive}
    )

    response = gpt.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = message_list
    )

    print(response)
    #message_response = response["choices"][0]["message"]
    #message_list.append(message_response)

    #return message_response


@bot.message_handler(commands=["cry"])
def opcao1(message_receive):
    bot.send_message(message_receive.chat.id, "Não chore my friend.")

@bot.callback_query_handler(func=lambda call:True)
def callback_question(callback):
    if callback.message:

        options = {
            'cry': lambda : bot.send_message(callback.message.chat.id, "Não chore my friend."),
            'phrase': lambda : bot.send_message(callback.message.chat.id, get_phrase()),
            'complain': lambda : bot.send_message(callback.message.chat.id, "Se for chorar manda aúdio."),
            'question': lambda : bot.send_message(callback.message.chat.id, "Envie sua pergunta.")
        }

        options[callback.data]()

def get_phrase():
    response = requests.get(base_url)

    response_json = response.content.decode('utf-8')
    response_dict = json.loads(response_json)

    return response_dict['resposta'][0]['frase']

def response_by_gpt(message_receive):
    gpt_message_reponse = send_message_to_gpt(message_receive, message_list)
    bot.send_message(message_receive.chat.id, gpt_message_reponse)

def verify_is_question(message_receive):
    if "?" in message_receive.text:
        return True
    return False

@bot.message_handler(func=verify_is_question)
def call_gpt_reponse_question(message_receive):
    bot.send_message(message_receive.chat.id, "Respondo já já....")

@bot.message_handler(commands=["start"])
def response(message_receive):
    markup = types.InlineKeyboardMarkup(row_width=2)

    answer = types.InlineKeyboardButton("Pergunta❓", callback_data="question")
    complain = types.InlineKeyboardButton("Reclamar❗", callback_data="complain")
    cry = types.InlineKeyboardButton("Chorar 😭", callback_data="cry")
    phrase = types.InlineKeyboardButton("Frase Motivacional ✅", callback_data="phrase")

    markup.add(answer, complain, cry, phrase)

    bot.send_message(message_receive.chat.id, "O que deseja fazer? 🤺", reply_markup=markup)

bot.polling()