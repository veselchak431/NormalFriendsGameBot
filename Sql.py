import os
import urllib.parse as urlparse
from os import remove
from random import randint

import psycopg2
import telebot
import yadisk
from flask import Flask, request

import test
import testbiometry
from wanted_person_image import create_foto_of_wanted

from PIL import Image, ImageDraw, ImageFont


print("start on version 1.2.0")

TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)


def init_DB(connect):
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Players(
       Id INT PRIMARY KEY,
       Name TEXT,
       Height Text,
       InterestingFact TEXT,
       LookFact TEXT,
       RandomFacts TEXT,
       BiometryEncoding TEXT
       );""")
    connect.commit()


class player:
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.height = ''
        self.biometry = ''
        self.zadiak = ''
        self.facts = []
        self.comingPartners = []
        self.get_biometry = "onReg"
        self.busy = True
        self.BiometryBusy = False

    def get_fact(self):
        return self.facts[randint(0, len(self.facts) - 1)]

    def IsInTwo(self):
        for two in TwoOfPeples:
            if two[0] == self or two[1] == self:
                return True
        return False

    def __repr__(self):
        return self.name


Peoples = []
TwoOfPeples = []

startGame = telebot.types.InlineKeyboardMarkup()
startGame.add(telebot.types.InlineKeyboardButton(text="Погнали!", callback_data="Resume"))


def getPepleFromMessage(message):
    for people in Peoples:
        if people.id == message.from_user.id:
            return people


def getTwoPepleFromMessage(message):
    for Two in TwoOfPeples:
        if Two[0].id == message.from_user.id or Two[1].id == message.from_user.id:
            return Two[0], Two[1]


class OnBiometry(telebot.custom_filters.SimpleCustomFilter):
    key = 'CHECK_BIM'

    @staticmethod
    def check(message):
        try:
            return getPepleFromMessage(message).get_biometry

        except:
            pass


class BusyPleers(telebot.custom_filters.SimpleCustomFilter):
    key = 'CHECK_BUSY'

    @staticmethod
    def check(message):
        try:
            return getPepleFromMessage(message).BiometryBusy
        except:
            pass


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(chat_id=message.from_user.id, text="отвеченно")
    #src = open('foto.jpg', "rb")
    #bot.send_photo(chat_id=message.from_user.id, photo=src)
    #src.close()

    create_foto_of_wanted("123", str("это обычный неработающий тест"))
    wanted = open('wanted.jpg', "rb")

    bot.send_photo(chat_id=message.from_user.id, photo=wanted)
    wanted.close()
    remove('wanted.jpg')
    #src = 'wanted.jpg'
    #print("файл существует wanted", os.path.exists(src))
    #if os.path.exists(src):
    #    remove(src)


    #wanted = open(src, "rb")
    #print("файл wanted cоздан", os.path.exists(src))
    #bot.send_photo(chat_id=message.from_user.id, photo=wanted)
    #wanted.close()
    #remove(src)
    #print("файл отправлен")
    #bot.send_photo(chat_id=message.from_user.id, photo=create_foto_of_wanted("123", str("это обычный неработающий тест")))


@bot.message_handler(commands=['start'])
def start(message):
    print("new player connect Player ID: ", message.from_user.id)
    People_id = message.from_user.id

    cursor.execute("SELECT * FROM Players WHERE Id = {}".format(str(People_id)))
    data = cursor.fetchall()

    if data != []:

        if data[0].count(None) != 0:  # Need for change to 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            cursor.execute("DELETE FROM Players WHERE Id = {}".format(str(People_id)))
            cursor.execute("INSERT INTO Players(Id) VALUES({});".format(str(People_id)))
            connect.commit()
            Peoples.append(player(People_id))
            msg = bot.send_message(message.from_user.id, """\
            Как тебя зовут?
            """)
            bot.register_next_step_handler(msg, get_name)

    if data == []:

        cursor.execute("INSERT INTO Players(Id) VALUES({});".format(People_id))
        connect.commit()
        Peoples.append(player(People_id))
        msg = bot.send_message(message.from_user.id, """\
        Как тебя зовут?
        """)
        bot.register_next_step_handler(msg, get_name)
    else:
        cursor.execute("SELECT Name FROM Players WHERE Id = {}".format(str(People_id)))
        Name = cursor.fetchall()[0][0]
        try:
            msg = bot.send_message(message.from_user.id, "Ты " + Name + " ? (Да/Нет)")
            bot.register_next_step_handler(msg, Hueta)
        except:
            pass


def Hueta(message):
    if (message.text).lower() == "да":

        global cursor
        Peoples.append(player(message.from_user.id))
        pl = getPepleFromMessage(message)
        cursor.execute("SELECT * FROM Players WHERE Id = {}".format(str(pl.id)))
        data = cursor.fetchone()
        pl.name = data[1]
        pl.height = data[2]
        for i in range(3, 6):
            pl.facts.append(data[i])
        pl.biometry = test.ReturnEncodingsFromSQL(data[6])
        pl.get_biometry = False

        print('Player with name: {} and ID: {} is ready'.format(pl, pl.id))

        bot.send_message(chat_id=message.from_user.id, text="""\
                понятно, скоро начнем
                """, reply_markup=startGame)

    elif (message.text).lower() == "нет":

        cursor.execute("DELETE FROM Players WHERE Id = {}".format(str(message.from_user.id)))
        connect.commit()
        cursor.execute("INSERT INTO Players(Id) VALUES({});".format(str(message.from_user.id)))
        connect.commit()
        Peoples.append(player(message.from_user.id))
        msg = bot.send_message(message.from_user.id, """\
                Как тебя зовут?
                """)
        bot.register_next_step_handler(msg, get_name)
    else:
        bot.send_message(message.from_user.id, "Что-то не понял, попробуй заново(/start)")


def get_name(message):
    pl = getPepleFromMessage(message)
    pl.name = message.text
    cursor.execute("UPDATE Players SET Name = '{}' WHERE Id = {};".format(message.text, str(message.from_user.id)))
    connect.commit()
    msg = bot.send_message(message.from_user.id, "Какого ты роста?")
    bot.register_next_step_handler(msg, get_height)


def get_height(message):
    pl = getPepleFromMessage(message)
    pl.height = message.text
    cursor.execute("UPDATE Players SET Height = '{}' WHERE Id = {};".format(message.text, str(message.from_user.id)))
    connect.commit()
    msg = bot.send_message(message.from_user.id, "Поделись интересным фактом о себе")
    bot.register_next_step_handler(msg, interesting_fact)


def interesting_fact(message):
    pl = getPepleFromMessage(message)
    pl.facts.append(message.text)
    cursor.execute(
        "UPDATE Players SET InterestingFact = '{}' WHERE Id = {};".format(message.text, str(message.from_user.id)))
    connect.commit()
    msg = bot.send_message(message.from_user.id, "Ты так хорошо сегодня выглядишь, расскажи что на тебе")
    bot.register_next_step_handler(msg, look_fact)


def look_fact(message):
    pl = getPepleFromMessage(message)
    pl.facts.append('этот человек сегодня надел ' + message.text)
    cursor.execute(
        "UPDATE Players SET LookFact = '{}' WHERE Id = {};".format('этот человек сегодня надел ' + message.text,
                                                                   str(message.from_user.id)))
    connect.commit()

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(telebot.types.KeyboardButton("Овен♈"), telebot.types.KeyboardButton("Телец♉"),
               telebot.types.KeyboardButton("Близнецы♊"),
               telebot.types.KeyboardButton("Рак♋"), telebot.types.KeyboardButton("Лев♌"),
               telebot.types.KeyboardButton("Дева♍"),
               telebot.types.KeyboardButton("Весы♎"), telebot.types.KeyboardButton("Скорпион♏"),
               telebot.types.KeyboardButton("Стрелец♐"),
               telebot.types.KeyboardButton("Козерог♑"), telebot.types.KeyboardButton("Водолей♒"),
               telebot.types.KeyboardButton("Рыбы♓"))

    msg = bot.send_message(message.from_user.id, "кто ты по знаку зодиака?", reply_markup=markup)

    bot.register_next_step_handler(msg, zadiak)


def zadiak(message):
    pl = getPepleFromMessage(message)
    pl.zadiak = message.text[:-1]
    markup = telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.from_user.id, "продолжи фразу:", reply_markup=markup)

    msg = bot.send_message(message.from_user.id, "я по знаку задиака " + message.text[:-1] + " и по этому у меня ...")
    bot.register_next_step_handler(msg, random_facts)


def random_facts(message):
    pl = getPepleFromMessage(message)
    pl.facts.append("этот человек " + pl.zadiak + " и по этому у него " + message.text)
    cursor.execute(
        "UPDATE Players SET RandomFacts = '{}' WHERE Id = {};".format(
            "этот человек " + pl.zadiak + " и по этому у него " + message.text, str(message.from_user.id)))
    connect.commit()

    pl.get_biometry = True
    bot.send_message(message.from_user.id, """\
            пришли мне свое фото (селфи)
            """)


@bot.message_handler(CHECK_BIM=True, content_types=['photo'])
def photo(message):
    bot.send_message(chat_id=message.from_user.id, text="""\
                    подожди, идет обработка!
                    """)
    pl = getPepleFromMessage(message)
    src = '{}.jpg'.format(str(message.from_user.id) + "biometry")

    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    out = open(src, "wb")
    out.write(downloaded_file)
    out.close()
    encodings = testbiometry.GenerateEncodings(src)

    if yandex_Disk.exists("/game/biometry/{}.jpg".format(str(message.from_user.id) + "biometry")):
        print("this file was early uploaded")
        yandex_Disk.remove("/game/biometry/{}.jpg".format(str(message.from_user.id) + "biometry"))
    yandex_Disk.upload(src, "/game/biometry/{}.jpg".format(str(message.from_user.id) + "biometry"))

    remove(src)

    if type(encodings) != str:
        cursor.execute(
            "UPDATE Players SET BiometryEncoding = '{}' WHERE Id = {};".format(encodings, str(message.from_user.id)))
        connect.commit()
        pl.biometry = encodings
        pl.get_biometry = False
        print('Player with name: {} and ID: {} is ready'.format(pl, pl.id))
        bot.send_message(chat_id=message.from_user.id, text="""\
                    Фото принято, мы готовы начать!
                    """, reply_markup=startGame)
    else:
        print('Player with name: {} and ID: {} failed Biomety'.format(pl, pl.id))
        bot.send_message(chat_id=message.from_user.id, text="""\
                            с фото что-то не так, попробуй еще раз
                            """)


@bot.callback_query_handler(lambda answer: answer.data == "Resume")
def game(answer):
    pl = getPepleFromMessage(answer)

    if pl.IsInTwo() == False:
        print('Player {} resumed game.'.format(pl))
        pl.busy = False  # освободился
        ListofPeople = Peoples.copy()
        ListofPeople.remove(pl)
        print("List of players :", ListofPeople)

        availablePeople = []
        for peop in ListofPeople:
            if not (peop in pl.comingPartners) and (peop.busy == False):
                availablePeople.append(peop)

        print("List of possible pair :", availablePeople)
        if len(availablePeople) != 0:
            secondPerson = availablePeople[randint(0, len(availablePeople) - 1)]
            pl.busy = True
            secondPerson.busy = True
            pl.BiometryBusy = True
            secondPerson.BiometryBusy = True

            TwoOfPeples.append([pl, secondPerson])
            print("New pair created between {} and {}".format(pl, secondPerson))

            bot.send_message(chat_id=pl.id, text="Вот тебе наводка на человека, найди его и сделай с ним фото")
            src = 'wanted.jpg'
            if os.path.exists(src):
                remove(src)
            create_foto_of_wanted(secondPerson.height, str(secondPerson.get_fact()))
            wanted = open(src,"rb")
            bot.send_photo(chat_id=pl.id, photo=wanted)
            wanted.close()
            remove(src)


            bot.send_message(chat_id=secondPerson.id,
                             text="Вот тебе наводка на человека, найди его и сделай с ним фото")

            create_foto_of_wanted(pl.height, pl.get_fact())
            wanted = open(src, "rb")
            bot.send_photo(chat_id=secondPerson.id, photo=wanted)
            wanted.close()
            remove(src)

            bot.answer_callback_query(answer.id)

        else:
            print('Player {}  wait for free player'.format(pl))
            bot.send_message(chat_id=answer.from_user.id, text="""\
                                    жди пару
                                    """)

            bot.answer_callback_query(answer.id)
    else:
        print('Player {}  try to find new pair, but is in pair : {} '.format(pl, getTwoPepleFromMessage(answer)))
        bot.send_message(chat_id=answer.from_user.id, text="""\
                        видимо ты уже в паре
                        """)
        bot.answer_callback_query(answer.id)


@bot.message_handler(CHECK_BIM=False, CHECK_BUSY=True, content_types=['photo'])
def photo(message):
    pl1, pl2 = getTwoPepleFromMessage(message)
    src = '{}.jpg'.format(str(pl1) + "_и_" + str(pl2))
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    out = open(src, "wb")
    out.write(downloaded_file)
    out.close()
    bot.send_message(chat_id=message.from_user.id, text="Отлично! Фото принято, сейчас проверим")
    print('Photo from {} downloaded.'.format(getPepleFromMessage(message)))
    result = testbiometry.CheckTwoPresenceOfImage(pl1.biometry, pl2.biometry, src)

    if yandex_Disk.exists("/game/pair_foto/{}.jpg".format(str(pl1) + "_и_" + str(pl2))):
        yandex_Disk.remove("/game/pair_foto/{}.jpg".format(str(pl1) + "_и_" + str(pl2)))
    yandex_Disk.upload(src, ("/game/pair_foto/{}.jpg".format(str(pl1) + "_и_" + str(pl2))))

    remove(src)
    print("the result of the uploaded photo : ", result)
    result = True  # всегда пропускать не смотря на фото
    if result:
        pl1.comingPartners.append(pl2)
        pl2.comingPartners.append(pl1)
        try:
            TwoOfPeples.remove([pl1, pl2])
        except:
            pass
        try:
            TwoOfPeples.remove([pl2, pl1])
        except:
            pass
        print("Pair of {} and {} successfully passed the task.".format(pl1, pl2))
        pl1.BiometryBusy = False
        pl2.BiometryBusy = False
        bot.send_message(chat_id=pl1.id, text='на фото действительно есть ' + str(pl1) + " и " + str(pl2),
                         reply_markup=startGame)
        bot.send_message(chat_id=pl2.id, text='на фото действительно есть ' + str(pl1) + " и " + str(pl2),
                         reply_markup=startGame)


    else:
        print("Pair of {} and {} failed the task, and try again.".format(pl1, pl2))
        bot.send_message(message.chat.id, 'на фото нет нужных людей или фото плохое')
        bot.send_message(message.chat.id, 'попробуйте еще раз')


bot.add_custom_filter(OnBiometry())
bot.add_custom_filter(BusyPleers())

on_heroku = False
if 'DYNO' in os.environ:
    on_heroku = True

if on_heroku == True:

    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    server = Flask(__name__)


    @server.route('/' + TOKEN, methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url=os.environ['WEBHOOK_URL'] + TOKEN)
        return "!", 200


    if __name__ == "__main__":
        print("program start on heroku")
        print("database information")
        connect = psycopg2.connect(dbname=dbname, port=port, user=user, password=password, host=host)
        cursor = connect.cursor()
        init_DB(connect)

        yandex_Disk = yadisk.YaDisk(token=os.environ['YANDEX_DISK_TOKEN'])
        print("check yandex token :", yandex_Disk.check_token())

        #if not os.path.exists('wanted_files/foto.jpg'):
        #   yandex_Disk.download("/game/wanted_foto/foto.jpg", 'wanted_files/foto.jpg')
        if not os.path.exists('foto.jpg'):
                yandex_Disk.download("/game/wanted_foto/foto.jpg", 'foto.jpg')
                print("foto of wanted was from yandex downloaded.")



        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
else:
    if __name__ == "__main__":
        print("program start on computer")
        bot.remove_webhook()

        connect = psycopg2.connect(port="5432", user='postgres', password='1234567890', host='localhost')
        cursor = connect.cursor()
        init_DB(connect)

        yandex_Disk = yadisk.YaDisk(token=os.environ['YANDEX_DISK_TOKEN'])
        print("check yandex token :", yandex_Disk.check_token())
       # if not os.path.exists('wanted_files/foto.jpg'):
       #     yandex_Disk.download("/game/wanted_foto/foto.jpg",'wanted_files/foto.jpg')
        if not os.path.exists('foto.jpg'):
            yandex_Disk.download("/game/wanted_foto/foto.jpg",'foto.jpg')

        bot.polling(none_stop=True, interval=0,timeout=60)
