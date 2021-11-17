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
            return self.file_src
        return False


Tasks = [Task("1", ["simply_photo", "text"], ["первое задание для 1-го задания", "это первое задание, ключ - 1"], "foto.jpg", '1'),
         Task("2", ["simply_photo", "text"], ["первое задание для 2-го задания", "это второе задание, ключ - 2"], "foto.jpg", '2')]
print(Tasks[1].get_file() != False)
