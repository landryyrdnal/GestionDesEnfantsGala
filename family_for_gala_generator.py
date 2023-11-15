import gala_library
import pandas as pd

# On prend la liste des élèves du gala et on la transforme en dataframe
gala_students = gala_library.make_gala_student_list()
df = pd.DataFrame(gala_students)

# On nettoie les doublons
df = df.drop_duplicates(subset=['nom', 'prénom'])

# Trie du DataFrame par nom de famille, numéro de téléphone des parents et mail des parents
df = df.sort_values(by=['nom', 'téléphone', 'mail'])

# On regroupe les enfants par nom de famille similaires, tel similaires et mails similaires,
grouped = df.groupby(by=['nom', "téléphone", "mail"])

# Initialisation d’une liste pour stocker les groupes de frères et sœurs
family = []

# On parcours chaque groupe pour déterminer les enfants dans plusieurs galas
for nom_famille, groupe in grouped:
    groupe['G1G2'] = False
    groupe['G1G3'] = False
    groupe['G2G3'] = False
    groupe['G1G2G3'] = False
    # Si le groupe a plus d'un enfant, c’est une famille
    if len(groupe) > 1:
        # On cherche dans quels galas les membres de la famille participent
        G1 = False
        G2 = False
        G3 = False
        for index, student in groupe.iterrows():
            if len(student["G1"]) > 0:
                G1 = True
            if len(student["G2"]) > 0:
                G2 = True
            if len(student["G3"]) > 0:
                G3 = True
        # On assigne les multiples galas si la famille participe à plusieurs galas
        G1G2 = False
        G1G3 = False
        G2G3 = False
        G1G2G3 = False
        # Si la famille participe à plusieurs galas alors on l’indique
        if G1 and G2 and G3:
            G1G2G3 = True
        elif G1 and G2:
            G1G2 = True
        elif G1 and G3:
            G1G3 = True
        elif G2 and G3:
            G2G3 = True
        # On ajoute les colonnes des multiples galas dans la famille
        for index, student in groupe.iterrows():
            groupe.at[index, "G1G2G3"] = G1G2G3
            groupe.at[index, "G1G2"] = G1G2
            groupe.at[index, "G1G3"] = G1G3
            groupe.at[index, "G2G3"] = G2G3
        # On ajoute la famille au groupe des familles
        family.append(groupe)

# on rassemble toutes les familles en un nouveau dataframe
family_df = pd.concat(family)

# on exporte le dataframe dans un fichier excel
excel = "familles.xlsx"
family_df.to_excel(excel)

print(f"Tableau des familles terminé dans {excel}")