import pathlib
from pathlib import Path
class Task:
    def __init__(self, name, type_of_task, text, file_src, key):
        self.name = name

        self.type = type_of_task
        self.text = text

        self.current_task_type = self.type[0]
        self.current_task = self.text[0]

        self.file_src = file_src
        self.key = key

    def next_task(self):
        if len(self.type)-1 > self.type.index(self.current_task_type):
            self.current_task_type = self.type[self.type.index(self.current_task_type)+1]
            self.current_task = self.text[self.current_task.index(self.current_task)+1]

    def __repr__(self):
        return self.name

    def check_key(self, key):
        if str(key).lower().strip() == str(self.key).lower().strip():
            return True
        return False

    def get_file(self):
        if self.file_src != "":
            return   str(Path(pathlib.Path.cwd(), 'task_file',str(self.file_src)))
        return False



Tasks = [Task("1", ["simply_photo", "text"], ["Выпейте на брудершафт, пришли фото выполнения задания", "угадайте страну по фото"],
               "австралия.jpg", 'австралия'),

         Task("2", ["simply_photo", "text"], ["Сделайте шот и выпейте его без рук, пришли фото выполнения задания", "ваше следующее задание ( ответ - 1 слово ) :"],
               "дыхание.png", 'дыхание'),

         Task("3", ["simply_photo", "text"], ["Одновременно шлепните кого-то по жопе, пришли фото выполнения задания", "ваше следующее задание ( ответ - 1 слово ) :"],
               "фуга.jpg", 'фуга'),

         Task("4", ["simply_photo", "text"], ["Нарисуйте на память друг другу портрет и пришлите его фото", "угадайте страну по фото"],
               "греция.jpg", 'греция'),

         Task("5", ["simply_photo", "text"], ["Выпить с криком 'за короля' и пришлите фото чекающихся напитков", "вам досталось самое сложное, разгадайте кроссворд и из первых букв составить слово"],
               "скорпион.jpg", 'скорпион'),

         Task("6", ["simply_photo", "text"], ["подойти к Диме и сказать тост в его честь, сделать фото", "задание делалось под шафе, но нужно слово отгадать"],
              "темнота.png", 'темнота'),

         Task("7", ["simply_photo", "text"], ["пришлите фото как будто вы порно звезды", "угадайте какой город (я не угадал)"],
               "стамбул.jpg", 'стамбул'),

         Task("8", ["simply_photo", "text"], ["сфоткайтесь как будто вы герои мема", "если вы тоже ебали эти загадки, то угадайте эту страну"],
               "россия.jpg", 'россия'),

         Task("9", ["simply_photo", "text"], ["подойти к Диме и произнести тост по кавказски и сфоткаться", "'Шуп оё рпнётуйута ебзё г тбнфя впмэщфя лбтусям' - ну не принял я с утра таблетки, но ответ слово, а подсказка: +-1"],
              "", 'крышка'),

         Task("10", ["simply_photo", "text"], ["сделать фото как будто вы часы и показать сколько сейчас время", "'Впмэщё шбтб, нёоэщё нйофуь.'- а я немножечко шалю, подсказка: шалю на +-1"],
               "", 'секунда'),

         Task("11", ["simply_photo", "text"], ["выпейти и расскажите другому что вас ебет, и фоточку не забудте", "'Как называют маленькую свинью полицейского' - кто знает тот знает, а кто не знает тот не знает ауф"],
               "", 'пигмент'),

         ]

