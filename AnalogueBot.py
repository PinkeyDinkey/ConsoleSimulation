import random
import os
import signal
import threading
from mysql.connector import connect, Error


class DBwork():
    def __init__(self, host="localhost", user="root", password="d090595d", database="sovkombank_bot",id=None, text = ""):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.id = id
        self.text = text

    @property
    def getID(self):
        return self.id

    def DB_deco_start_session(func):
        def wrapper(self):
            try:
                with connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database = self.database
                ) as connection:
                    res = func(self)
                    with connection.cursor() as cursor:
                        cursor.execute(res)
                        connection.commit()
                        self.id = cursor.lastrowid
                    return res
            except Error as e:
                print(e)
        return wrapper

    def DB_message(func):
        def wrapper(self,text):
            try:
                with connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database = self.database
                ) as connection:
                    res = func(self,text)
                    with connection.cursor() as cursor:
                        cursor.execute(res)
                        connection.commit()
                    return res
            except Error as e:
                print(e)
        return wrapper

    @DB_deco_start_session
    def start_session(self):
        session_start = """
                    INSERT INTO session(StartTime)
                    VALUES (NOW())
            """
        return  session_start

    @DB_deco_start_session
    def end_session(self):
        session_end = f"""
                    UPDATE session SET EndTime=NOW()
                    WHERE idSession = {self.id}
            """
        return session_end

    @DB_message
    def send_message(self,texte):
        message = f"""
                    INSERT INTO message(MessageTime,idSession,Text,idClient)
                    VALUES (NOW(),'{self.id}','{texte}','{self.id}')
        """
        return message


class Watchdog():
    def __init__(self, timeout=10):
        self.timeout = timeout
        self._t = None
        self._id = None

    def do_expire(self):
        # raise SystemExit
        global DB
        DB.end_session()
        os.kill(os.getpid(),signal.SIGTERM)

    def _expire(self):
        self.do_expire()

    def start(self):
        if self._t is None:
            self._t = threading.Timer(self.timeout, self._expire)
            self._t.start()

    def stop(self):
        if self._t is not None:
            self._t.cancel()
            self._t = None

    def refresh(self):
        if self._t is not None:
             self.stop()
             self.start()

def randomaizer():
    random.seed
    s = random.randint(0, 2)
    return s

def answer_generator(first_sms, second_sms="Nope"):
    answer = randomaizer()
    if first_sms == "Happiness" and second_sms=="Nope":
        if answer == 0:
            botwords = "Здравствуй, я рад видеть тебя в добром здравии!😁"
        elif answer == 1:
            botwords = "Доброе время суток!😃"
        elif answer == 2:
            botwords = "Привет, вижу ты сегодня в бодром расположении духа!😄"
    elif first_sms == "Sadness" and second_sms=="Nope":
        if answer == 0:
            botwords = "Здравствуй, что-то случилось? Мне кажется, что ты грустный...😯"
        elif answer == 1:
            botwords = "Привет, ты выглядишь неважно, что-то случилось?😯"
        elif answer == 2:
            botwords = "Добрый день, вы не рады меня видеть?😯"
    elif first_sms == "Irritation" and second_sms=="Nope":
        if answer == 0:
            botwords = "Добрый день, вы не рады меня видеть?😯"
        elif answer == 1:
            botwords = "Привет, что случилось, мой кожанный друг, ты злишься?😯"
        elif answer == 2:
            botwords = "З-з-здравствуй? Я смотрю , ты не в настроении... Надеюсь, ты не захочешь меня ударить...😯"
    elif first_sms == "Happiness" and second_sms=="Happiness":
        if answer == 0:
            botwords = "Мне нравится, что твое настроение очень хорошее!"
        elif answer == 1:
            botwords = "Мне нравится твоя улыбка"
        elif answer == 2:
            botwords = "Люди, на лицах которых стоит улыбка, поднимают настроение не только мне, но и другим людям.)"
    elif first_sms == "Sadness" and second_sms=="Happiness":
        if answer == 0:
            botwords = "Я рад, что тебе стало лучше, мой друг!"
        elif answer == 1:
            botwords = "Все стало на свои места, ты снова радуешься, я снова любуюсь твоей улыбкой)"
        elif answer == 2:
            botwords = "Так держать, друг мой, улыбка и смех продлевает жизнь!"
    elif first_sms == "Irritation" and second_sms=="Happiness":
        if answer == 0:
            botwords = "Я так счастлив, что ты перестал злиться, друг мой)"
        elif answer == 1:
            botwords = "Виртуальные обнимашки работают!"
        elif answer == 2:
            botwords = "Спасибо, за твою улыбку:3"
    elif first_sms == "Happiness" and second_sms=="Sadness":
        if answer == 0:
            botwords = "Что случилось, я тебя обидел?😥"
        elif answer == 1:
            botwords = "На твоем лице внезапно появилась краска грусти, я могу тебе помочь чем-нибудь?"
        elif answer == 2:
            botwords = "Иди сюда, мой друг. *Виртуальные объятия*"
    elif first_sms == "Sadness" and second_sms=="Sadness":
        if answer == 0:
            botwords = "Я не знаю, как тебя развеселить... Но я что-нибудь придумаю!"
        elif answer == 1:
            botwords = "*Виртуальные объятия*"
        elif answer == 2:
            botwords = "Внимание! Аннекдот..."
    elif first_sms == "Irritation" and second_sms=="Sadness":
        if answer == 0:
            botwords = "Вижу, стало немного лучше, но я тебя все равно не оставлю..."
        elif answer == 1:
            botwords = "А давай, я нам еще и мороженного куплю?)"
        elif answer == 2:
            botwords = "Ты на пути перехода в сторону счастья, подаван мой юный...☯"
    elif first_sms == "Happiness" and second_sms=="Irritation":
        if answer == 0:
            botwords = "Скажи мне, что я сделал не так? Только не злись, прошу..."
        elif answer == 1:
            botwords = "Мне очень страшно, когда кто-то злится на меня..."
        elif answer == 2:
            botwords = "Будь спокоей, ненависть и злость путем являются к злости и ненависти большей...☯"
    elif first_sms == "Sadness" and second_sms=="Irritation":
        if answer == 0:
            botwords = "Ладно... я понял... Обнимашки были лишними 😢"
        elif answer == 1:
            botwords = "У нас есть ПЕЧЕНЬКИ!!! Хочешь парочку?..."
        elif answer == 2:
            botwords = "Братишкааа, я тебе покушать принес...🐘"
    elif first_sms == "Irritation" and second_sms=="Irritation":
        if answer == 0:
            botwords = "Братишка, ну не стукаааай...🐘"
        elif answer == 1:
            botwords = "...*Пытается спрятаться*"
        elif answer == 2:
            botwords = "Ты должен был бороться со злом, а не примкнуть к нему!⭐"
    return botwords


def get_key(d, value):
    for k, v in d.items():
        for val in v:
            if val == value:
                return True

def get_keyano(d, value):
    for k, v in d.items():
        for val in v:
            if val == value:
                return k


emojiDict = {'Happiness':['😀','😁','😂','😃','😄','😆','😊','🤩','🥳'],
             'Sadness':['🙄','😥','😣','😫','😕','😔','😓','☹','🙁','😟'],
             'Irritation':['😬','👺','💀','👿','😈','🤬','😡','😠','😤']}
DB = DBwork()

def start():
    global DB
    try:
        lister = []
        s = ""
        atr = True
        global  emojiDict
        # with open("emojis.txt") as file:
        #     for line in file:
        #         key, *value = line.split()
        #         emojiDict[key] = value
        wd = Watchdog(60)
        for key, value in emojiDict.items():
            if key == "Happiness":
                s = "счастья"
            elif key == "Sadness":
                s = "грусти"
            elif key == "Irritation":
                s = "злости"
            print(f"Для выражения {s} используйте : {value}")
        DB.start_session()
        wd.start()
        while atr==True:
            answ = input("Клиент:")
            DB.send_message(f"Клиент: {answ}")
            wd.refresh()
            if get_key(emojiDict, answ):
                if len(lister) == 0:
                    lister.append(get_keyano(emojiDict,answ))
                    bot_answer = answer_generator(lister[0])
                    print(f"Бот: {bot_answer}")
                    DB.send_message(f"Бот: {bot_answer}")
                elif len(lister) == 1:
                    lister.append(get_keyano(emojiDict,answ))
                    bot_answer = answer_generator(lister[0],lister[1])
                    print(f"Бот: {bot_answer}")
                    DB.send_message(f"Бот: {bot_answer}")
                elif len(lister) == 2:
                    lister.remove(lister[0])
                    lister.append(get_keyano(emojiDict,answ))
                    bot_answer = answer_generator(lister[0], lister[1])
                    print(f"Бот: {bot_answer}")
                    DB.send_message(f"Бот: {bot_answer}")
            else:
                print("Бот: Я вас не понял")
                DB.send_message("Бот: Я вас не понял")
                DB.end_session()
                break
    except SystemExit:
        DB.end_session()


start()
