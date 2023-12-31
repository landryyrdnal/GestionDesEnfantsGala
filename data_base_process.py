import datetime
import re as re
import pandas as pd
import unidecode
import os
from parameters import liste_profs, annee_scolaire, semaine, col_verif, directory, col_saison


def process_data_base(last=True, last_excel=""):

    debug = False

    def load_excel_db():
        """Cette fonction sert à charger la base de donnée excel d’export Assoconnect
        la plus récente dans le répertoire des bases de données
        :return une str du chemin complet du fichier"""
        liste_db = os.listdir(directory)
        liste_xlsx = []
        for db in liste_db:
            if db.endswith("_export.xlsx"):
                liste_xlsx.append(db)
        liste_xlsx.sort()
        return os.path.join(directory, liste_xlsx[-1])



    class NiveauDanse():

        def __init__(self, nom_niveau: str):
            self.nom_niveau = nom_niveau
            self.discipline = self.def_discipline()
            self.liste_cours = []

        def def_discipline(self) -> str:
            """
            Détermine la discipline à partir du titre du niveau
            :return: le nom de la discipline (str)
            """
            if re.search("Classique", self.nom_niveau):
                return "Classique"
            elif re.search("Modern Jazz", self.nom_niveau):
                return "Jazz"
            elif re.search("Contemporain", self.nom_niveau):
                return "Contemporain"
            elif re.search("Caractère", self.nom_niveau):
                return "Caractère"
            elif re.search("Éveil", self.nom_niveau):
                return "Eveil/Initiation"
            elif re.search("Eveil", self.nom_niveau):
                return "Eveil/Initiation"
            elif re.search("Initiation", self.nom_niveau):
                return "Eveil/Initiation"
            elif re.search("Baroque", self.nom_niveau):
                return "Baroque"
            elif re.search("Barre au Sol", self.nom_niveau):
                return "Barre au Sol"

        def __repr__(self):
            return self.nom_niveau + " " + self.discipline + " " + str(self.liste_cours)


    class CoursDanse():
        def __init__(self, nom_cours: str, discipline: str = ""):
            self.nom_cours = nom_cours
            self.jour = self.def_jour()
            self.heure = self.def_heure()
            self.prof = self.def_prof()
            self.liste_eleves = []
            self.nb_eleves = 0
            self.df = {}
            self.discipline = discipline
            # Cette fonction est à retravailler ne fonctionne pas en l'état
            self.niveau = self.def_niveau()

        def __repr__(self):
            return "CoursDanse_" + str(self.jour) + "_" + str(self.heure) + "_" + str(self.prof["nom"] + "_" + str(self.nb_eleves))

        def __eq__(self, other):
            if self.jour == other.jour and self.heure == other.heure and self.prof == other.prof:
                return True
            else:
                return False


        def def_jour(self):
            jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
            for jour in jours:
                if re.search(jour, self.nom_cours):
                    return jour

        def def_niveau(self):
            result = self.nom_cours.split(self.prof["nom"])[1]
            return result

        # retourne l'heure sous la forme 15h30
        def def_heure(self):
            try:
                pattern = re.compile("[0-9][0-9]h[0-9][0-9]")
                return pattern.findall(self.nom_cours)[0]
            except IndexError:
                pattern = re.compile("[0-9]h[0-9][0-9]")
                return "0" + pattern.findall(self.nom_cours)[0]

        def def_prof(self):
            for prof in liste_profs:
                if re.search(liste_profs[prof]["nom"], self.nom_cours):
                    if debug:
                        print("prof trouvé pour le cours {} :{}".format(self.nom_cours, liste_profs[prof]["nom"]))
                    return liste_profs[prof]


    def chercher_cours(niveau, workbook):
        """
        Recherche tous les cours dans la colonne "niveau" et les rassemble
        dans une liste, tous les cours sont du type CoursDanse
        :param niveau: string du nom de la colonne dans laquelle sont
        inscrit des cours ex: « Éveil  Initiation 4 à 6 ans saison 23-24 »
        :return:une liste de cours du type CoursDanse contenant
        tous les cours existants dans la colonne "niveau" de la base de donnée
        """
        liste_noms_cours = []
        discipline = niveau.discipline
        # on cherche tous les cours du niveau et on le met dans la liste liste_cours
        for index in workbook.index:
            if workbook.loc[index, niveau.nom_niveau] != 0 and type(workbook.loc[index, niveau.nom_niveau]) == str:
                cours = workbook.loc[index, niveau.nom_niveau].split("|")
                for i in cours:
                    if i not in liste_noms_cours:
                        liste_noms_cours.append(i)
        # on fait de chaque élément de la liste un élément de la classe CoursDanse
        liste_cours = []
        for i in liste_noms_cours:
            liste_cours.append(CoursDanse(i, discipline))
        return liste_cours


    def add_value(list, key, eleve):
        list.append(eleve.get(key))


    def fill_planning(workbook):
        """
        Fonction qui liste tous les cours et les peuples avec les élèves.
        :return: Retourne la variable var_semaine qui contient tous les cours avec
        pour chacun les précisions sur le prof et la liste des élèves
        :type: liste des jours [lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche]
        qui contiennent chacun une sous liste [tous les cours du jour] chaque cours est du type CoursDanse
        """

        if debug:
            print("début du processus d’analyse de la base de donnée")
        # On recherche tous les niveaux de cours en fonction de l’année
        liste_niveaux = []
        for col in workbook:
            if re.search(f"saison {annee_scolaire}", col):
                if col == "Cours de danse choisi(s)" or col == "Cours d'essai":
                    pass
                else:
                    liste_niveaux.append(NiveauDanse(nom_niveau=col))

        # On génère la liste de cours pour chaque niveau de cours
        # (niveau étant élément de liste_niveau de class NiveauDanse)
        for niveau in liste_niveaux:
            niveau.liste_cours = chercher_cours(niveau, workbook)

        # Pour chaque cours, on recherche les élèves qui sont dedans
        for niveau in liste_niveaux:
            for cours in niveau.liste_cours:
                liste_eleves = []
                # On recherche dans toutes les cases non vides du tableau les cours qui existent
                for index, row in workbook.iterrows():
                    case = workbook[niveau.nom_niveau][index]
                    if case != 0 and case != "":
                        # Si la case correspond au cours
                        for i in str(case).split("|"):
                            if i == cours.nom_cours:
                                # On recherche tous les autres cours que fait l'élève en dehors du cours en cours
                                list_autres_cours = []
                                for niv in liste_niveaux:
                                    if row[niv.nom_niveau] != 0:
                                        for e in str(row[niv.nom_niveau]).split("|"):
                                            if e != cours.nom_cours and e != "nan":
                                                list_autres_cours.append(e)
                                        autres_cours = ""
                                        for i in list_autres_cours:
                                            autres_cours += i + " | "

                                # on détermine l'âge de l'élève à partir de sa date de naissance
                                try:
                                    age = int((datetime.datetime.now() - row["Date de naissance"]).days / 365)
                                except TypeError:
                                    print("Age non trouvé pour {} {}".format(row["Nom"], row["Prénom"]))
                                    age = "?"
                                except ValueError:
                                    print("Age non trouvé pour {} {}".format(row["Nom"], row["Prénom"]))
                                    age = "?"

                                # telephone
                                telephone = str(row["Téléphone mobile"])
                                if len(telephone) >= 10:
                                    telephone = "0" + telephone[2] + " " + telephone[3] + telephone[4] + " " + telephone[
                                        5] + \
                                                telephone[6] + " " + telephone[7] + telephone[8] + " " + telephone[9] + \
                                                telephone[10]

                                eleve = {"ID": row["ID du Contact"],
                                         "Nom": row["Nom"],
                                         "Prénom": row["Prénom"],
                                         "Âge": age,
                                         "Genre": row["Sexe"],
                                         "Téléphone": telephone,
                                         "Mail": row["Email"],
                                         "Autres cours": autres_cours,
                                         "cours": cours}
                                # on ne prends en compte que les élèves vérifiés.
                                if row[col_verif] == "oui" and row[col_saison] == "Oui":
                                    liste_eleves.append(eleve)
                                else:
                                    print(
                                        f"{eleve['Nom']} {eleve['Prénom']} a son inscription {annee_scolaire} non vérifiée.")
                # on trie la liste des élèves par prénoms
                liste_eleves.sort(key=lambda x: unidecode.unidecode(x["Prénom"]))
                # on ajoute la liste des élèves à l'instance de la classe CoursDanse
                cours.liste_eleves = liste_eleves
                # on ajoute le nb d'élèves à l'instance de la classe CoursDanse
                cours.nb_eleves = len(cours.liste_eleves)

        for niveau in liste_niveaux:
            for cours in niveau.liste_cours:
                df = {}
                prenom, nom, age, genre, autres_cours, telephone, mail, id = [], [], [], [], [], [], [], []
                for eleve in cours.liste_eleves:
                    add_value(prenom, "Prénom", eleve)
                    add_value(nom, "Nom", eleve)
                    add_value(age, "Âge", eleve)
                    add_value(genre, "Genre", eleve)
                    add_value(autres_cours, "Autres cours", eleve)
                    add_value(telephone, "Téléphone", eleve)
                    add_value(mail, "Mail", eleve)
                    add_value(id, "ID", eleve)

                df["Prénom"] = prenom
                df["Nom"] = nom
                df["Âge"] = age
                df["Genre"] = genre
                df["Autres cours"] = autres_cours
                df["Téléphone"] = telephone
                df["Mail"] = mail
                df["ID"] = id
                # ajout de la df du cours à l'instance de la classe CoursDanse
                df = pd.DataFrame(df)
                cours.df = df

        # tri des cours dans la semaine

        lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche = [], [], [], [], [], [], []
        var_semaine = [lundi, mardi, mercredi, jeudi, vendredi, samedi, dimanche]
        for niveau in liste_niveaux:
            for cours in niveau.liste_cours:
                for jour in semaine:
                    if cours.jour == jour:
                        # on évite les doublons
                        if cours not in var_semaine[semaine.index(jour)]:
                            var_semaine[semaine.index(jour)].append(cours)

        for jour in var_semaine:
            jour.sort(reverse=False, key=lambda x: (x.heure, x.nom_cours))
        return var_semaine, liste_niveaux


    def load_excel(last=True, last_excel = ""):
        """

        :param last: True s’il faut utiliser la dernière base de donnée exportée.
        :param last_excel: str du nom du vieux fichier excel utilisé pour la comparaison
        :return:
        """
        # Définition de la base de donnée à utiliser
        try:
            if last:
                fichier_excel = load_excel_db()
                workbook = pd.read_excel(fichier_excel, engine='openpyxl')
            else:
                fichier_excel = last_excel
                workbook = pd.read_excel(fichier_excel, engine='openpyxl')
        # Si le fichier excel d’export n’a pas été ouvert et enregistré par excel le code ne fonctionnera pas.
        except ValueError as error:
            print(error)
            print(f"⚠️ ATTENTION il faut ouvrir le fichier {fichier_excel} une fois avec Excel et l’enregistrer via Excel"
                  " puis relancer le programme,"
                  "le fichier est corrompu par Assoconnect.")
        return workbook

    # chargement du fichier excel
    workbook = load_excel(last, last_excel)

    # traitement du fichier excel
    var_semaine, liste_niveaux = fill_planning(workbook)
    if last_excel != "":
        print(f"La base de donnée {last_excel} a été traitée")
    else:
        print("La dernière base de donnée a été traitée")
    return var_semaine, liste_niveaux



if __name__ == "__main__":
    var_semaine, liste_niveaux =  process_data_base()

    print(var_semaine)
    print("______________________")
    print(liste_niveaux)