from datetime import datetime

import customtkinter
from tkinter import Canvas, Scrollbar, BOTH, VERTICAL, HORIZONTAL

from subjects import classes, Subject, find_day, find_week, find_tutors


lab_neutral = '#5b94d9'
lab_chose = '#0571f5'
pro_neutral = '#a6a63d'
pro_chose = '#f0f01f'
wyk_neutral = '#ba6750'
wyk_chose = '#ed1509'
wrong = '#97999c'


def calculate_time_difference(time_str1, time_str2):
    # Parsowanie czasu z łańcuchów znaków do obiektów datetime
    time_format = "%H:%M"
    datetime1 = datetime.strptime(time_str1, time_format)
    datetime2 = datetime.strptime(time_str2, time_format)

    # Obliczanie różnicy czasu
    time_difference = datetime2 - datetime1

    # Zamiana różnicy czasu na liczbę minut
    minutes_difference = time_difference.total_seconds() / 60

    return int(minutes_difference)

def start_at_used_time(time_str1, time_str2, time_str3):
    # Parsowanie czasu z łańcuchów znaków do obiektów datetime
    time_format = "%H:%M"
    datetime1 = datetime.strptime(time_str1, time_format)
    datetime2 = datetime.strptime(time_str2, time_format)
    datetime3 = datetime.strptime(time_str3, time_format)

    # Obliczanie różnicy czasu
    if datetime1 <= datetime3 <= datetime2:
        return True
    else:
        return False


class AppFrame(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="#000000", border_color="#000000")  # Ustawienie koloru tła dla ramki

        # customtkinter.set_appearance_mode("dark")
        # customtkinter.set_default_color_theme("blue")

        # Tworzenie obszaru przewijania
        self.canvas = Canvas(self, bg="#000000", highlightthickness=0)
        self.scrollbar_vertical = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.scrollbar_horizontal = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
        self.scrollable_frame = customtkinter.CTkFrame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Dodawanie paska przewijania wewnątrz ramki
        self.scrollbar_vertical.pack(side="right", fill="y")
        self.scrollbar_horizontal.pack(side="bottom", fill="x")

        # Dodawanie paska przewijania
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)

        self.buttons = []
        self.i = 0

        # Godziny wierszy
        start_time = 7 * 60  # 7:00 in minutes
        end_time = 20 * 60 + 1  # 19:00 in minutes

        frame = customtkinter.CTkFrame(self.scrollable_frame, fg_color="#3d3678")  # Set background color to white
        frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        for row in range(start_time, end_time, 60):
            time_label = customtkinter.CTkLabel(frame, text=f"{row // 60:02d}:{row % 60:02d}", width=100, height=80)
            time_label.grid(row=(row - start_time) // 60 + 1, column=0, sticky="ne")

        # Nagłówki kolumn
        days_of_week = ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek']
        for col, day in enumerate(days_of_week):
            label = customtkinter.CTkLabel(self.scrollable_frame, text=day, width=200, height=25, fg_color="#3d3678")
            label.grid(row=0, column=col + 1, sticky="nsew", padx=20, pady=20)

            frame = customtkinter.CTkFrame(self.scrollable_frame, fg_color="black")
            frame.grid(row=1, column=col + 1, sticky="nsew", padx=20, pady=20)

            self.add_buttons(frame, day)

        # Konfiguracja rozciągania ramki
        self.columnconfigure(0, weight=1)
        for col in range(1, len(days_of_week) + 1):
            self.columnconfigure(col, weight=1)

        for row in range(1, (end_time - start_time) // 60 + 2):
            self.rowconfigure(row, weight=1)

        # Ustawienia przewijania
        self.canvas.pack(side="left", fill=BOTH, expand=True)

    def add_buttons(self, frame, day):

        def button_event(x):
            # Get the text of the clicked button
            button_text = self.buttons[x].cget("text")

            # Split the text into lines and get the second line as name_id
            name_id = button_text.split('\n')[1]
            day = button_text.split('\n')[4]
            _start_time = button_text.split('\n')[7]
            end_time = button_text.split('\n')[8]

            # Check if the button is already in chosen color
            current_color = self.buttons[x].cget("fg_color")
            if current_color == "#c508cc":
                # Reset colors for all buttons with the same name_id
                for i, button in enumerate(self.buttons):
                    other_name_id = button.cget("text").split('\n')[1]
                    if other_name_id == name_id:
                        # Reset to default colors based on class type
                        if subjects[i].type_of_classes == "Zajęcia laboratoryjne":
                            color = lab_neutral
                        elif subjects[i].type_of_classes == "Wykład":
                            color = wyk_neutral
                        elif subjects[i].type_of_classes == "Projekt":
                            color = pro_neutral
                        button.configure(fg_color=color)
            else:
                # Change the color of the clicked button to chosen color
                self.buttons[x].configure(fg_color="#c508cc")
                # Change the color of all other buttons with the same name_id to white
                for i, button in enumerate(self.buttons):
                    if i != x:
                        other_day = button.cget("text").split('\n')[4]
                        other_start_time = button.cget("text").split('\n')[7]
                        other_end_time = button.cget("text").split('\n')[8]
                        other_name_id = button.cget("text").split('\n')[1]
                        if other_name_id == name_id:
                            button.configure(fg_color=wrong)
                        if other_day == day:
                            if start_at_used_time(_start_time, end_time, other_start_time) or start_at_used_time(_start_time, end_time, other_end_time):
                                other_color = button.cget("fg_color")
                                if other_color != wrong:
                                    if button_text.split('\n')[5] != "tydzień: każdy":
                                        if button_text.split('\n')[5] == "tydzień: parzyste" and\
                                                button.cget("text").split('\n')[5] == "tydzień: nieparzyste":
                                            pass
                                        elif button_text.split('\n')[5] == "tydzień: nieparzyste" and\
                                             button.cget("text").split('\n')[5] == "tydzień: parzyste":
                                            pass
                                        else:
                                            for _i, _button in enumerate(self.buttons):
                                                _other_name_id = _button.cget("text").split('\n')[1]
                                                if _other_name_id == other_name_id and _other_name_id != name_id:
                                                    if subjects[_i].type_of_classes == "Zajęcia laboratoryjne":
                                                        color = lab_neutral
                                                    elif subjects[_i].type_of_classes == "Wykład":
                                                        color = wyk_neutral
                                                    elif subjects[_i].type_of_classes == "Projekt":
                                                        color = pro_neutral
                                                    _button.configure(fg_color=color)
                                    else:
                                        for _i, _button in enumerate(self.buttons):
                                            _other_name_id = _button.cget("text").split('\n')[1]
                                            if  _other_name_id == other_name_id and _other_name_id != name_id:
                                                if subjects[_i].type_of_classes == "Zajęcia laboratoryjne":
                                                    color = lab_neutral
                                                elif subjects[_i].type_of_classes == "Wykład":
                                                    color = wyk_neutral
                                                elif subjects[_i].type_of_classes == "Projekt":
                                                    color = pro_neutral
                                                _button.configure(fg_color=color)

        list_of_classes = [[]]
        numberOfColumns = 1

        for clas in subjects:
            if clas.day == day:
                clas_time = calculate_time_difference(clas.start_time, clas.end_time)
                start_time = calculate_time_difference("7:00", clas.start_time)

                column = 0
                for col in range(numberOfColumns):
                    i = 0
                    for element in list_of_classes[col]:
                        if not start_at_used_time(element.start_time, element.end_time, clas.start_time):
                            i += 1
                        else:
                            break
                    if i == len(list_of_classes[col]):
                        column = col
                        break
                    column += 1

                if len(list_of_classes) <= column:
                    list_of_classes.append([clas])
                    numberOfColumns += 1
                else:
                    list_of_classes[column].append(clas)

                _text = clas.name + '\n' + clas.type_of_classes + '\n' + 'grupa: ' + str(clas.group) + '\n' + str(
                    clas.tutors) + '\n' + clas.start_time + '\n' + clas.start_time + '\n' + clas.end_time

                color = ""
                if clas.type_of_classes == "Zajęcia laboratoryjne":
                    color = lab_neutral
                elif clas.type_of_classes == "Wykład":
                    color = wyk_neutral
                elif clas.type_of_classes == "Projekt":
                    color = pro_neutral

                button = customtkinter.CTkButton(master=frame, text=str(clas),
                                                 font=("Helvetica", 10),
                                                 command=lambda x=self.i: button_event(x),
                                                 width=100,
                                                 height=int((clas_time / 60) * 80),
                                                 compound="left", anchor="n", fg_color=color)
                button.grid(row=0, column=column, sticky="nwe", pady=((start_time / 60) * 80 + 40), padx=2)
                self.buttons.append(button)
                clas.button = button
                self.i += 1


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1080x720")
        self.title("Układacz Planu 4.99")

        app_frame = AppFrame(self)
        app_frame.grid(row=0, column=0, sticky="nsew")

        # Konfiguracja rozciągania aplikacji
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


subjects = []
for c in classes:
    subject = Subject(
        name=c["name"],
        name_id=c["name-id"],
        day=find_day(c.find(slot="dialog-event").text.split(",")[0].strip()),
        start_time=c.find(slot="dialog-event").text.split(",")[1].split("-")[0].strip(),
        end_time=c.find(slot="dialog-event").text.split(",")[1].split("-")[1].strip(),
        type_of_classes=c.find(slot="dialog-info").text.split(",")[0].strip(),
        group=int(c.find(slot="dialog-info").text.split(",")[1].split()[1].strip()),
        week=find_week(c.find(slot="dialog-event").text.split(",")[0]),
        tutors=find_tutors(c.find(slot="dialog-person")),
        building=c.find(slot="info").text.split("bud.")[1].split(")")[0].strip(),
        room=c.find(slot="info").text.split("(")[1].split(",")[0])

    subjects.append(subject)
    # print(subject)
app = App()
app.mainloop()
