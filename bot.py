import telebot
import logging
import pickle
import pandas as pd

# Set logger
telebot.logging.basicConfig(filename='bot.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = telebot.logger

# Const values
TOKEN = open('token', 'r')
TOKEN = str(TOKEN.readline()).replace('\n', '').replace('\r', '')

helpMessage = "Canais de informação oficias da prefeitura:\nInstagram: https://www.instagram.com/prefeiturasaocarlosoficial/\nCanal no telegram: https://t.me/prefsaocarlos\n\nInformações sobre o bot:\nBot não oficial para divulgação de dados sobre o COVID19 em São Carlos, São Paulo.\nÚltima atualização de dados: 15/04/2020\nOs dados usados aqui podem ser encontrados em: https://github.com/MetlHedd/datasets/tree/master/covid19/saocarlos\nPerfil para informar bugs, sugestões, etc: @essecaraderosa\n\n**Escolha uma das opções abaixo:**"

commandsHelp = {
    'ajuda': 'Mostra os comandos do bot',
    'casosatuais': 'Informações sobre os casos atuais',
    'graficos': 'Gráficos separados por categorias',
    'vdata': 'EM BREVE: Vê informações de acordo com uma data especifica'
}

plotsCallbacks = {
    'CV19-CSH': 'Casos hospitalizados',
    'CV19-CONF': 'Casos confirmados',
    'CV19-DESC': 'Cassos descartados',
    'CV19-MIDC': 'Casos que vieram à óbito (em investigação, descartados e confirmados)',
    'CV19-LET': 'Porcentagem de letalidade',
    'FLU-NOTISO': 'Casos com sintomas leves'
}

# Carrega os dados do último dia atualizado
ultimo_dia_atualizado = "None"

with open('dados-ultimodia.obj', 'rb') as ultimo_dia_file:
    ultimo_dia_atualizado = pickle.load(ultimo_dia_file)

    ultimo_dia_atualizado = "Data da atualização: {}\nCasos confirmados: {}\nCasos descartados: {}\nÓbitos confirmados: {}\nÓbitos descartados: {}\nTaxa de letalidade: {:f}%".format(ultimo_dia_atualizado['Data'], ultimo_dia_atualizado['CV19-CONF'], ultimo_dia_atualizado['CV19-DESC'], ultimo_dia_atualizado['CV19-MCONF'], ultimo_dia_atualizado['CV19-MDESC'], (ultimo_dia_atualizado['CV19-MCONF'] / (ultimo_dia_atualizado['CV19-CONF'] + ultimo_dia_atualizado['CV19-MCONF'])) * 100)

# Set bot initial configs
bot = telebot.TeleBot(TOKEN)
telebot.logger.setLevel(logging.DEBUG)

# Commands
@bot.callback_query_handler(func=lambda call: call.data == 'ajudaButton')
@bot.message_handler(commands=['start', 'help', 'ajuda'])
def send_help(m):
    chat_id = None

    if isinstance(m, telebot.types.Message):
        chat_id = m.chat.id
    else:
        chat_id = m.message.chat.id

    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for i in commandsHelp:
        markup.add(telebot.types.InlineKeyboardButton(commandsHelp[i], callback_data = i + 'Button'))
    
    logger.info(m)
    bot.send_message(chat_id, helpMessage, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'casosatuaisButton')
@bot.message_handler(commands=['casosatuais'])
def send_casos_atuais(m):
    chat_id = None

    if isinstance(m, telebot.types.Message):
        chat_id = m.chat.id
    else:
        chat_id = m.message.chat.id
    
    bot.send_message(chat_id, ultimo_dia_atualizado)

# Gráficos
@bot.message_handler(commands=['graficos'])
@bot.callback_query_handler(func=lambda call: call.data.startswith('graficosButton'))
def send_graficos(m):
    chat_id = None
    message_text = None

    if isinstance(m, telebot.types.Message):
        chat_id = m.chat.id
        message_text = m.text
    else:
        chat_id = m.message.chat.id
        message_text = m.data
    
    text_split = message_text.split(' ')

    logger.info(text_split)

    if isinstance(m, telebot.types.CallbackQuery) and len(text_split) > 1:
        grafico_escolhido = text_split[1]

        plotsImgs = {
            'CV19-CSH': open('plots/CV19-CSH.png', 'rb'),
            'CV19-CONF': open('plots/CV19-CONF.png', 'rb'),
            'CV19-DESC': open('plots/CV19-DESC.png', 'rb'),
            'CV19-MIDC': open('plots/CV19-MIDC.png', 'rb'),
            'CV19-LET': open('plots/CV19-LET.png', 'rb'),
            'FLU-NOTISO': open('plots/FLU-NOTISO.png', 'rb')
        }

        if grafico_escolhido in plotsImgs:
            bot.send_photo(chat_id, plotsImgs[grafico_escolhido])
    else:
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)

        for i in plotsCallbacks:
            markup.add(telebot.types.InlineKeyboardButton(plotsCallbacks[i], callback_data = 'graficosButton ' + i))
        
        bot.send_message(chat_id, 'Escolha algum dos gráficos abaixo para poder visualizar:', reply_markup=markup)
    

bot.polling()