import sqlite3
import telebot
TOKEN = '1979759352:AAEv7ufi6rnNGC0yxFEbgz-kx70aeGTMK_E'
bot = telebot.TeleBot(TOKEN)
import test, testbiometry
from random import randint
from os import remove
import os

from flask import Flask, request
server = Flask(__name__)

connect = sqlite3.connect('game.db')
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

OneBiEnavle = False


class player:
    def __init__(self,id):
        self.id = id
        self.name = ''
        self.biometry = ''
        self.comingPartners = []
        self.get_biometry = "onReg"
        self.busy= True


Peoples=[]
TwoOfPeples=[]

startGame = telebot.types.InlineKeyboardMarkup()
startGame.add(telebot.types.InlineKeyboardButton(text="Погнали!", callback_data="Resume"))

def getPepleFromMessage(message):
    for people in Peoples:
        if people.id == message.from_user.id:
            return people

def getTwoPepleFromMessage(message):
    for Two in TwoOfPeples:
        if Two[0].id == message.from_user.id or Two[1].id == message.from_user.id:
            return Two[0],Two[1]


class OnBiometry(telebot.custom_filters.SimpleCustomFilter):
    key='CHECK_BIM'
    @staticmethod
    def check(message):
        try:
            print(getPepleFromMessage(message).get_biometry)
            return getPepleFromMessage(message).get_biometry

        except :
            print("ну что то не так")

class BusyPleers(telebot.custom_filters.SimpleCustomFilter):
    key='CHECK_BUSY'
    @staticmethod
    def check(message):
        try:
            print(getPepleFromMessage(message).busy)
            return getPepleFromMessage(message).busy
        except :
            print("ну что то не так")


class EnableOneBiometry(telebot.custom_filters.SimpleCustomFilter):
    key='ONE_BIOMETRY'
    @staticmethod
    def check(message):
        return OneBiEnavle




@bot.message_handler(commands=['start'])
def start(message):
    People_id = message.from_user.id
    connect = sqlite3.connect('game.db')
    cursor = connect.cursor()
    cursor.execute("SELECT Id FROM Players WHERE Id = {}".format(str(People_id)))
    data = cursor.fetchall()
    print(data)
    if data ==[]:
        cursor.execute("INSERT INTO Players(Id) VALUES(?);",[People_id])
        connect.commit()
        Peoples.append(player(People_id))
        msg = bot.send_message(message.from_user.id,"""\
        Как тебя зовут?
        """)
        bot.register_next_step_handler(msg, get_name)
    else:# дописать уже зареганого
        cursor.execute("SELECT Name FROM Players WHERE Id = {}".format(str(People_id)))
        Name = cursor.fetchall()[0][0]
        try:
            msg= bot.send_message(message.from_user.id,"Ты "+Name+" ? (Да/Нет)")
            bot.register_next_step_handler(msg, Hueta)
        except:
            pass

def Hueta(message):

    if (message.text).lower() == "да":

        connect = sqlite3.connect('game.db')
        cursor = connect.cursor()

        Peoples.append(player(message.from_user.id))
        pl = getPepleFromMessage(message)
        cursor.execute("SELECT * FROM Players WHERE Id = {}".format(str(pl.id)))
        data = cursor.fetchone()
        pl.name = data[1]
        pl.biometry = test.ReturnEncodingsFromSQL(data[5])
        pl.get_biometry = False

        print('Acount append')

        bot.send_message(chat_id=message.from_user.id,text= """\
                понятно, скоро начнем
                """,reply_markup=startGame)

    elif (message.text).lower() == "нет":


        connect = sqlite3.connect('game.db')
        cursor = connect.cursor()


        cursor.execute("DELETE FROM Players WHERE Id = {}".format(str(message.from_user.id)))
        connect.commit()
        cursor.execute("INSERT INTO Players(Id) VALUES(?);",[message.from_user.id])
        connect.commit()
        Peoples.append(player(message.from_user.id))
        msg = bot.send_message(message.from_user.id, """\
                Как тебя зовут?
                """)
        bot.register_next_step_handler(msg, get_name)
    else:
        bot.send_message(message.from_user.id,"написана хуета, попробуй заново(/start)")



def get_name(message):

    print(message.text)
    pl=getPepleFromMessage(message)
    pl.name=message.text
    connect = sqlite3.connect('game.db')
    cursor = connect.cursor()
    cursor.execute("UPDATE Players SET Name = '{}' WHERE Id = {};".format(message.text,str(message.from_user.id)))
    connect.commit()
    pl.get_biometry = True
    bot.send_message(message.from_user.id, """\
            пришли мне свое фото (селфи)
            """)



@bot.message_handler(CHECK_BIM = True,content_types=['photo'])
@test.benchmark
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
    if type(encodings)!=str:
        connect = sqlite3.connect('game.db')
        cursor = connect.cursor()
        cursor.execute("UPDATE Players SET BiometryEncoding = '{}' WHERE Id = {};".format(encodings, str(message.from_user.id)))
        connect.commit()
        pl.biometry=encodings
        pl.get_biometry=False
        print('Biometri accept')
        bot.send_message(chat_id=message.from_user.id,text= """\
                    Фото принято, мы готовы начать!
                    """,reply_markup=startGame)
    else:
        bot.send_message(chat_id=message.from_user.id, text="""\
                            с фото что-то не так, попробуй еще раз
                            """)
        print(encodings)


@bot.message_handler(CHECK_BIM = False,CHECK_BUSY=True,ONE_BIOMETRY=True,content_types=['photo'])
@test.benchmark
def photo(message):
    print('проверяем еще фото')
    connect = sqlite3.connect('game.db')
    cursor = connect.cursor()
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
    encoding= test.ReturnEncodingsFromSQL(encoding)
    print(encoding)
    result = testbiometry.CheckPresenceOfImage(encoding, src)
    remove(src)
    if result:
        bot.send_message(message.chat.id, 'на фото действительно есть'+Name)
    else:
        bot.send_message(message.chat.id, 'на фото нет'+Name)







@bot.callback_query_handler(lambda answer: answer.data == "Resume")
@test.benchmark
def game(answer):


    pl = getPepleFromMessage(answer)
    print(pl.id)
    flag = True
    print(TwoOfPeples)
    for two in TwoOfPeples:
        if two[0]==pl or two[1]==pl:
            flag=False
    if flag:
        pl.busy = False# освободился

        availablePeople = Peoples.copy()
        print("availablePeople ", availablePeople)
        availablePeople.remove(pl)

        for peop in pl.comingPartners:
            if peop in availablePeople or peop.busy==True :
                availablePeople.remove(peop)
        print(availablePeople)
        if len(availablePeople)!=0:
            secondPerson = availablePeople[randint(0,len(availablePeople)-1)]
            pl.busy = True
            secondPerson.busy = True
            TwoOfPeples.append([pl,secondPerson])
            print("пара создана")
            bot.send_message(chat_id = pl.id, text = "сделай фото с "+secondPerson.name)
            bot.send_message(chat_id = secondPerson.id, text  ="сделай фото с "+pl.name)


            bot.answer_callback_query(answer.id)

        else:
            bot.send_message(chat_id=answer.from_user.id, text="""\
                                    жди пару
                                    """)

            bot.answer_callback_query(answer.id)
    else:
        bot.send_message(chat_id=answer.from_user.id, text="""\
                        видимо ты уже в паре
                        """)
        bot.answer_callback_query(answer.id)



@bot.message_handler(CHECK_BIM = False,CHECK_BUSY=True,content_types=['photo'])
@test.benchmark
def photo(message):
    pl1, pl2 = getTwoPepleFromMessage(message)
    print('проверяем фото пары')
    src = '{}.jpg'.format(str(message.from_user.id) + "mes" + str(message.id))
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    out = open(src, "wb")
    out.write(downloaded_file)
    out.close()
    print('фото загруженно')
    result = testbiometry.CheckTwoPresenceOfImage(pl1.biometry, pl2.biometry, src)
    remove(src)
    print(result)
    if result:
        bot.send_message(chat_id=pl1.id,text= 'на фото действительно есть '+pl1.name+" и "+pl2.name,reply_markup=startGame)
        bot.send_message(chat_id=pl2.id,text= 'на фото действительно есть ' + pl1.name + " и " + pl2.name,reply_markup=startGame)
        pl1.comingPartners.append(pl2)
        pl2.comingPartners.append(pl1)
        print('пробуем удалить')
        try:
            TwoOfPeples.remove([pl1,pl2])
            print("прокатило 1")
        except:
            pass
        try:
            TwoOfPeples.remove([pl2, pl1])
            print("прокатило 2")
        except:
            pass


    else:
        bot.send_message(message.chat.id, 'на фото нет нужных людей или фото плохое')
        bot.send_message(message.chat.id, 'попробуйте еще раз')
bot.add_custom_filter(OnBiometry())
bot.add_custom_filter(BusyPleers())
bot.add_custom_filter(EnableOneBiometry())


@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://botunitaznovobochka.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

