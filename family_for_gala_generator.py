import gala_library
import pandas as pd


gala_students = gala_library.make_gala_student_list()

df = pd.DataFrame(gala_students)
# Nettoyage des doublons
df = df.drop_duplicates(subset=['nom', 'prénom'])

print(df)
# Triez le DataFrame par nom de famille, numéro de téléphone des parents et mail des parents
df = df.sort_values(by=['nom', 'téléphone', 'mail'])

# Regroupez les enfants par nom de famille
grouped = df.groupby(by=['nom', "téléphone", "mail"])

# Initialisez une liste pour stocker les groupes de frères et sœurs

# Parcourez chaque groupe
for nom_famille, groupe in grouped:
    G1G2 = False
    G1G3 = False
    G2G3 = False
    G1G2G3 = False
    # Si le groupe a plus d'un enfant, ce sont des frères et sœurs
    if len(groupe) > 1:
        G1 = False
        G2 = False
        G3 = False
        for student in groupe:
            if student["G1"] > 0:
                G1 = True
            if student["G2"] > 0:
                G2 = True
            if student["G3"] > 0:
                G3 = True
        if G1 and G2 and G3:
            G1G2G3 = True
        elif G1 and G2:
            G1G2 = True
        elif G1 and G3:
            G1G3 = True
        elif G2 and G3:
            G2G3 = True
        for student in groupe:
            student["G1G2G3"] = G1G2G3
            student["G1G2"] = G1G2
            student["G1G3"] = G1G3
            student["G2G3"] = G2G3



# Affichez les groupes de frères et sœurs triés
for groupe in groupes_fraternelles:
    print(groupe)
    print(type(groupe))
# Ou vous pouvez également stocker les groupes dans un nouveau DataFrame si nécessaire
nouveau_dataframe = pd.concat(groupes_fraternelles)
nouveau_dataframe.to_excel("familles.xlsx")
# Affichez le nouveau DataFrame trié
print(nouveau_dataframe)