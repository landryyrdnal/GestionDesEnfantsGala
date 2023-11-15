import openpyxl
import data_base_process
import toml
import re
import datetime
import openpyxl
from openpyxl.styles import *
import pandas as pd

parameters = "parameters.toml"
var_semaine, useless = data_base_process.process_data_base()
liste_profs = toml.load(parameters)["profs"]


class CoursOrdreGala:
    def __init__(self, jour, heure, prof, duree, gala, ordre_passage):
        self.jour = jour
        self.heure = heure
        self.prof = prof
        self.duree = duree
        self.gala = gala
        self.ordre_passage = ordre_passage

    def __repr__(self):
        if self.ordre_passage < 10:
            ordre = "0" + str(self.ordre_passage)
        else:
            ordre = str(self.ordre_passage)
        return str(" G" + str(self.gala) + " T" + ordre + " " + self.jour[:2] + " " + self.heure + " " + self.prof)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if self.jour == other.jour and self.heure == other.heure and self.prof == other.prof and self.gala == other.gala and self.ordre_passage == other.ordre_passage:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.gala == other.gala:
            if self.ordre_passage > other.ordre_passage:
                return True
            else:
                return False
        raise AssertionError(f"les chorégraphies {self} et {other} n'appartiennent pas au même gala"
                             f"elles doivent appartenir au même Gala pour pouvoir être comparées." )




def ordre_de_passage_creator():
    """
    sert à faire la liste des cours dans l’ordre du gala
    :return: retourne une liste de cours du type CoursOrdreGala
    """
    # Ouverture du fichier excel qui gère l’ordre de passage du gala de l’année
    ordre_gala = toml.load(parameters)["DataBase"]["ordre_gala"]
    workbook = pd.read_excel(ordre_gala)
    ordre_de_passage = []

    for index, row in workbook.iterrows():
        cours = CoursOrdreGala(jour=row["Jour"],
                               heure=row["Heure"],
                               prof=row["Professeur"],
                               duree=row["Durée"],
                               gala=row["Gala"],
                               ordre_passage=row["Ordre de Passage"])
        ordre_de_passage.append(cours)
    return ordre_de_passage

# cherche dans la liste des cours avec durée le cours correspondant
def find_the_good_class_time(ordre_de_passage, jour, heure, prof):
    for course in ordre_de_passage:
        if course.heure == heure and course.jour == jour and course.prof == prof["nom"]:
            return course

    raise AssertionError


def search_heure(string):
    try:
        pattern = re.compile("[0-9][0-9]h[0-9][0-9]")
        return pattern.findall(string)[0]
    except IndexError:
        pattern = re.compile("[0-9]h[0-9][0-9]")
        return "0" + pattern.findall(string)[0]


def search_prof(string):
    for prof in liste_profs:
        if re.search(liste_profs[prof]["nom"], string):
            return liste_profs[prof]
        #elif re.search(liste_profs[prof]["diminutif"], string):
        #    return liste_profs[prof]


def search_jour(string):
    jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    for jour in jours:
        if re.search(jour, string):
            return jour
        
def time_between_two_courses(ordre_de_passage,first: CoursOrdreGala, second: CoursOrdreGala):
    # retourne le temps de changement entre deux passages pour se changer
    found = False
    index = ordre_de_passage.index(first) + 1
    tot_time = datetime.timedelta()
    while not found:
        if ordre_de_passage[index] != second:
            tot_time += datetime.timedelta(hours=ordre_de_passage[index].duree.hour,
                                           minutes=ordre_de_passage[index].duree.minute,
                                           seconds=ordre_de_passage[index].duree.second)
            index += 1
        else:
            found = True
        minutes = tot_time.seconds // 60
        secondes = tot_time.seconds % 60
        if minutes >= 60:
            heures = minutes // 60
            minutes = minutes % 60
        else:
            heures = 00
    return str(heures) + ":" + str(minutes) + ":" + str(secondes)


def list_every_student():
    students = []
    for level in var_semaine:
        for course in level:
            for student in course.liste_eleves:
                students.append(student)
    return students


def make_gala_student_list():
    ordre_de_passage = ordre_de_passage_creator()
    student_list = list_every_student()
    student_gala_list = []
    for student in student_list:
        G1_courses = []
        G2_courses = []
        G3_courses = []
        principal_course = find_the_good_class_time(ordre_de_passage=ordre_de_passage,
                                                    jour=student["cours"].jour,
                                                    heure=student["cours"].heure,
                                                    prof=student["cours"].prof)
        if principal_course.gala == 1 and principal_course not in G1_courses:
            G1_courses.append(principal_course)
        elif principal_course.gala == 2 and principal_course not in G2_courses:
            G2_courses.append(principal_course)
        elif principal_course.gala == 3 and principal_course not in G3_courses:
            G3_courses.append(principal_course)
        # on ajoute les autres cours
        for string in student["Autres cours"].split("|"):
            if len(string) > 1:
                prof = search_prof(string)
                heure = search_heure(string)
                jour = search_jour(string)
                course = find_the_good_class_time(ordre_de_passage, jour, heure, prof)
                if course.gala == 1 and course not in G1_courses:
                    G1_courses.append(course)
                elif course.gala == 2 and course not in G2_courses:
                    G2_courses.append(course)
                elif course.gala == 3 and course not in G3_courses:
                    G3_courses.append(course)
                # tri des cours en fonction de l’ordre de passage
                G1_courses = sorted(G1_courses)
                G2_courses = sorted(G2_courses)
                G3_courses = sorted(G3_courses)
        eleve = {"nom": student["Nom"], "prénom": student["Prénom"], "G1": G1_courses, "G2": G2_courses,
                 "G3": G3_courses, "téléphone": student["Téléphone"], "mail": student["Mail"]}
        if eleve not in student_gala_list:
            student_gala_list.append(eleve)
    return student_gala_list

if __name__ == "__main__":
    pass