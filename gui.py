import os
from  collections import defaultdict
from tkinter import *
import mail as m


class Window(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.center_window(150, 110)
        self.parent.title("IMAP")
        self.parent.iconbitmap("icon.ico")
        self.tag = 0
        self.login = ""
        self.password = ""
        self.host = ""
        self.port = 993
        self.dictionary = defaultdict()
        self.enter()
        self.attachments = []

    def center_window(self, width, height):
        self.w = width
        self.h = height
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - self.w) / 2
        y = (sh - self.h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (self.w, self.h, x, y))

    def enter(self):
        text_ip = Label(text="Введите значение IP")
        entry_ip = Entry()
        text_port = Label(text="Введите значение порта")
        entry_port = Entry()
        button_enter = Button(self.parent, text="ОК", width=10, height=1, cursor="hand2",
                              command=lambda: delete_all())
        text_ip.grid(row=1, column=0)
        entry_ip.grid(row=2, column=0)
        text_port.grid(row=3, column=0)
        entry_port.grid(row=4, column=0)
        button_enter.grid(row=5, column=0)

        def delete_all():
            self.ip = entry_ip.get()
            self.port = entry_port.get()
            if self.ip == '64.233.162.108' or self.ip == '64.233.162.109':
                self.host = 'imap.gmail.com'
            elif self.ip == '213.180.204.124':
                self.host = 'imap.yandex.ru'
            elif self.ip == '94.100.180.90':
                self.host = 'imap.mail.ru'
            widgets = self.parent.grid_slaves()
            for widget in widgets:
                widget.destroy()
            self.authorising()

    def authorising(self):
        self.center_window(200, 150)
        text = Label(text="Для входа - авторизируйтесь")
        text_login = Label(text="Введите логин")
        entry_login = Entry()
        text_password = Label(text="Введите пароль")
        entry_password = Entry(show="*")
        button_enter = Button(self.parent, text="Войти", width=10, height=1, cursor="hand2",
                              command=lambda: delete_all())
        image = PhotoImage(file="eye.png")
        button_echo = Button(self.parent, image=image, width=22, height=20, cursor="hand2", command=lambda: change_tag(entry_password))
        button_echo.image = image
        text.grid(row=0, column=0)
        text_login.grid(row=1, column=0)
        entry_login.grid(row=2, column=0)
        text_password.grid(row=3, column=0)
        entry_password.grid(row=4, column=0)
        button_enter.grid(row=5, column=0)
        button_echo.grid(row=4, column=1)

        def change_tag(entry):
            password = entry.get()
            if self.tag == 0:
                self.tag = 1
                entry = Entry()
            else:
                self.tag = 0
                password = entry.get()
                entry = Entry(show="*")
            entry.insert(0, password)
            self.password = entry.get()
            entry.grid(row=4, column=0)

        def delete_all():
            self.login = entry_login.get()
            self.password = entry_password.get()
            widgets = self.parent.grid_slaves()
            for widget in widgets:
                widget.destroy()
            self.toolbar()

    def toolbar(self):
        self.center_window(300, 150)
        button_message = Button(self.parent, text="Сообщения", width=10, height=1, cursor="hand2",
                                command=lambda: self.upload_messages())
        button_message.grid(row=0, column=0)

        button_send = Button(self.parent, text="Новое\nсообщение", width=10, height=2, cursor="hand2",
                                command=lambda: new_message())
        button_send.grid(row=1, column=0)

        button_catalogue = Button(self.parent, text="Новое\nсообщение", width=10, height=2, cursor="hand2",
                             command=lambda: new_message())
        button_catalogue.grid(row=1, column=0)

        def new_message():
            self.center_window(500, 350)
            label_to = Label(self.parent, text='кому')
            label_to.grid(row=4, column=4)
            label_subject = Label(self.parent, text='тема')
            label_subject.grid(row=5, column=4)
            to = Text(width=30, height=1)
            to.grid(row=4, column=5)
            subject = Text(width=30, height=1)
            subject.grid(row=5, column=5)
            text = Text(width=30, height=10)
            text.grid(row=6, column=5)
            button = Button(self.parent, text="Отправить", width=10, height=2, cursor="hand2",
                                 command=lambda: delete_all())
            button.grid(row=7, column=5)
            scroll = Scrollbar(command=text.yview)
            scroll.grid(row=6, column=6, sticky=N + S)
            text.config(yscrollcommand=scroll.set)

            def delete_all():
                m.send_message(text.get(0.0, END), self.login, self.password, to.get(0.0, END), subject.get(0.0, END))
                widgets = self.parent.grid_slaves()
                for widget in widgets:
                    widget.destroy()
                self.toolbar()

    def get_messages(self):
        scrollbar = Scrollbar(self.parent, orient="vertical")
        scrollbar1 = Scrollbar(self.parent, orient="horizontal")
        scrollbar2 = Scrollbar(self.parent, orient="horizontal")
        scrollbar3 = Scrollbar(self.parent, orient="horizontal")
        scrollbar4 = Scrollbar(self.parent, orient="horizontal")
        listbox_from = Listbox(self.parent, yscrollcommand=scrollbar.set)
        listbox_date = Listbox(self.parent, yscrollcommand=scrollbar.set)
        listbox_subject = Listbox(self.parent, yscrollcommand=scrollbar.set)
        self.listbox_body = Listbox(self.parent, yscrollcommand=scrollbar.set)

        gotten_messages = m.get_all_messages(self.login, self.password, self.port, self.host)
        messages = gotten_messages[0]
        self.dictionary = gotten_messages[1]

        def scroll():
            listbox_from.yview()
            listbox_date.yview()
            listbox_subject.yview()
            self.listbox_body.yview()
        scrollbar.config(command=scroll)
        scrollbar1.config(command=listbox_from.xview)
        scrollbar2.config(command=listbox_date.xview)
        scrollbar3.config(command=listbox_subject.xview)
        scrollbar4.config(command=self.listbox_body.xview)

        for message in messages:
            listbox_from.insert(END, message[0])
            listbox_date.insert(END, message[1])
            listbox_subject.insert(END, message[2])
            self.listbox_body.insert(END, message[3])
        listbox_from.grid(row=1, column=0)
        listbox_date.grid(row=1, column=1)
        listbox_subject.grid(row=1, column=2)
        self.listbox_body.grid(row=1, column=3)
        scrollbar.grid(row=1, column=4, sticky=N + S)
        scrollbar1.grid(row=2, column=0, sticky=E + W)
        scrollbar2.grid(row=2, column=1, sticky=E + W)
        scrollbar3.grid(row=2, column=2, sticky=E + W)
        scrollbar4.grid(row=2, column=3, sticky=E + W)
        self.listbox_body.bind('<Double-1>', lambda x: self.show_message(self.listbox_body.get(self.listbox_body.curselection())))
        label = Label(self.parent, text="Для просмотра сообщения, дважды кликните на него")
        label.grid(row=3, column=0, columnspan=4)

    def upload_messages(self):
        self.center_window(520, 250)
        self.get_messages()

    def show_message(self, text):
        message = Text(width=30, height=10)
        message.insert(0.0, text)
        message.grid(row=6, column=0, columnspan=4)
        scroll = Scrollbar(command=message.yview)
        scroll.grid(row=6, column=3, sticky=N + S)
        message.config(yscrollcommand=scroll.set)
        button = Button(self.parent, text="Скачать вложения", command=lambda:
        m.get_attachments(self.dictionary[str(self.listbox_body.curselection())]))
        button.grid(row=7, column=0, columnspan=4)
        self.center_window(520, 500)


def main():
    root = Tk()
    Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
