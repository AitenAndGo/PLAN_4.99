import pandas as pd
from bs4 import BeautifulSoup
import requests


url = 'https://web.usos.pwr.edu.pl/kontroler.php?_action=katalog2/przedmioty/pokazPlanGrupyPrzedmiotow&grupa_kod=MTR-SI-sem.6&cdyd_kod=2023%2F24-L'
respons = requests.get(url)

soup = BeautifulSoup(respons.text, 'html.parser')
table = soup.find("usos-timetable")

days = soup.find_all("timetable-day")
classes = soup.find_all("timetable-entry")


def find_day(s):
    days = ["poniedziałek", "wtorek", "środa", "czwartek", "piątek"]
    for day in days:
        if day in s:
            return day


def find_week(s):
    week = ["każdy", "nieparzyste", "parzyste"]
    for w in week:
        if w in s:
            return w


def find_tutors(tutors_object):
    names = []
    if tutors_object != None:
        tutors = tutors_object.find_all("a")
        for tutor in tutors:
            name = tutor.text.strip()
            names.append(name)

        return names
    else:
        return ""


class Subject():
    def __init__(self, name, name_id, day, start_time, end_time, type_of_classes, group, week, tutors, building,
                 room) -> None:
        self.name = name
        self.name_id = name_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.type_of_classes = type_of_classes
        self.group = group
        self.week = week  # każdy / parzyste / nieparzyste
        self.tutors = tutors
        self.building = building
        self.room = room
        self.button = None

    def __str__(self) -> str:
        return f"{self.name}\n" \
               f"{self.name_id}\n" \
               f"{self.type_of_classes}\n" \
               f"GROUPA: {self.group}\n" \
               f"{self.day}\n" \
               f"tydzień: {self.week}\n" \
               f"prowadzący: {self.tutors}\n" \
               f"{self.start_time}\n" \
               f"{self.end_time}\n" \
