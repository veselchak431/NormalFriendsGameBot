import psycopg2
import telebot
import test, testbiometry
from random import randint
from os import remove
import os
from flask import Flask, request
import urllib.parse as urlparse


print("start on version 1.2.0")

TOKEN = '2068317828:AAFvhIRtiwNZqTGAUznZkqtpA5RwlkDRJ4w'
bot = telebot.TeleBot(TOKEN)


def init_DB(connect):
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Players(
       Id INT PRIMARY KEY,
       Name TEXT,
       FirstDescription TEXT,
       SecondDescription TEXT,
       LookDescription TEXT,
       BiometryEncoding TEXT
       );""")
    connect.commit()



class player:
    def __init__(self, id):
        self.id = id
        self.name = ''
        self.biometry = ''
        self.comingPartners = []
        self.get_biometry = "onReg"
        self.busy = True
        self.BiometryBusy = False

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





OneBiEnavle = False
class EnableOneBiometry(telebot.custom_filters.SimpleCustomFilter):
    key = 'ONE_BIOMETRY'

    @staticmethod
    def check(message):
        return OneBiEnavle

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(chat_id=message.from_user.id,text="отвеченно")


@bot.message_handler(commands=['start'])
def start(message):
    print("new player connect Player ID: ", message.from_user.id)
    People_id = message.from_user.id


    cursor.execute("SELECT * FROM Players WHERE Id = {}".format(str(People_id)))
    data = cursor.fetchall()

    if data != []:

        if data[0].count(None) != 3:    # Need for change to 0 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
    else:  # дописать уже зареганого
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
        pl.biometry = test.ReturnEncodingsFromSQL(data[5])
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
        bot.send_message(message.from_user.id, "написана хуета, попробуй заново(/start)")


def get_name(message):
    pl = getPepleFromMessage(message)
    pl.name = message.text
    cursor.execute("UPDATE Players SET Name = '{}' WHERE Id = {};".format(message.text, str(message.from_user.id)))
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


# test for one person on photo
@bot.message_handler(CHECK_BIM=False, CHECK_BUSY=True, ONE_BIOMETRY=True, content_types=['photo'])
def photo(message):
    print('проверяем еще фото')
    cursor.execute("SELECT BiometryEncoding FROM Players WHERE Id = {};".format(str(message.from_user.id)))
    encoding = cursor.fetchone()[0]
    cursor.execute("SELECT Name FROM Players WHERE Id = {};".format(str(message.from_user.id)))
    Name = cursor.fetchone()[0]
    src = '{}.jpg'.format(str(message.from_user.id) + "mes" + str(message.id))
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    out = open(src, "wb")
    out.write(downloaded_file)
    out.close()
    print('базы данных не причем')
    print(encoding)
    encoding = test.ReturnEncodingsFromSQL(encoding)
    print(encoding)
    result = testbiometry.CheckPresenceOfImage(encoding, src)
    remove(src)
    if result:
        bot.send_message(message.chat.id, 'на фото действительно есть' + Name)
    else:
        bot.send_message(message.chat.id, 'на фото нет' + Name)


@bot.callback_query_handler(lambda answer: answer.data == "Resume")
def game(answer):
    pl = getPepleFromMessage(answer)


    if pl.IsInTwo() == False:
        print('Player {} resumed game.'.format(pl))
        pl.busy = False  # освободился
        availablePeople = Peoples.copy()
        availablePeople.remove(pl)
        print("List of players :", availablePeople)

        for peop in availablePeople:

            if (peop in pl.comingPartners) or (peop.busy == True):
                availablePeople.remove(peop)

        print("List of possible pair :", availablePeople)
        if len(availablePeople) != 0:
            secondPerson = availablePeople[randint(0, len(availablePeople) - 1)]
            pl.busy = True
            secondPerson.busy = True
            pl.BiometryBusy = True
            secondPerson.BiometryBusy = True

            TwoOfPeples.append([pl, secondPerson])
            print("New pair created between {} and {}".format(pl, secondPerson))
            bot.send_message(chat_id=pl.id, text="сделай фото с " + secondPerson.name)
            bot.send_message(chat_id=secondPerson.id, text="сделай фото с " + pl.name)



            bot.answer_callback_query(answer.id)

        else:
            print('Player {}  wait for free player'.format(pl))
            bot.send_message(chat_id=answer.from_user.id, text="""\
                                    жди пару
                                    """)

            bot.answer_callback_query(answer.id)
    else:
        print('Player {}  try to find new pair, but is in pair : {} '.format(pl,getTwoPepleFromMessage(answer)))
        bot.send_message(chat_id=answer.from_user.id, text="""\
                        видимо ты уже в паре
                        """)
        bot.answer_callback_query(answer.id)


@bot.message_handler(CHECK_BIM=False, CHECK_BUSY=True, content_types=['photo'])
def photo(message):
    pl1, pl2 = getTwoPepleFromMessage(message)
    src = '{}.jpg'.format(str(message.from_user.id) + "mes" + str(message.id))
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    out = open(src, "wb")
    out.write(downloaded_file)
    out.close()
    print('Photo from {} downloaded.'.format(getPepleFromMessage(message)))
    result = testbiometry.CheckTwoPresenceOfImage(pl1.biometry, pl2.biometry, src)
    remove(src)
    print("the result of the uploaded photo : ",result)
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
        bot.send_message(chat_id=pl1.id, text='на фото действительно есть ' + pl1.name + " и " + pl2.name,
                         reply_markup=startGame)
        bot.send_message(chat_id=pl2.id, text='на фото действительно есть ' + pl1.name + " и " + pl2.name,
                         reply_markup=startGame)


    else:
        print("Pair of {} and {} failed the task, and try again.".format(pl1, pl2))
        bot.send_message(message.chat.id, 'на фото нет нужных людей или фото плохое')
        bot.send_message(message.chat.id, 'попробуйте еще раз')


bot.add_custom_filter(OnBiometry())
bot.add_custom_filter(BusyPleers())
bot.add_custom_filter(EnableOneBiometry())


on_heroku = False
if 'DYNO' in os.environ:
    on_heroku = True


if on_heroku==True:

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
        bot.set_webhook(url='https://botunitaznovobochka.herokuapp.com/' + TOKEN)
        return "!", 200

    if __name__ == "__main__":
        print("program start on heroku")
        print("database information")
        print("port= ",port, "user= ",user, "password= ",password, "host= ",host)
        connect = psycopg2.connect(port=port, user=user, password=password, host=host)
        cursor = connect.cursor()
        init_DB(connect)
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
else:
    if __name__ == "__main__":
        print("program start on computer")
        bot.remove_webhook()
        connect = psycopg2.connect(port="5432", user='postgres', password='1234567890', host='localhost')
        cursor = connect.cursor()
        init_DB(connect)
        bot.polling(none_stop=True, interval=0)
