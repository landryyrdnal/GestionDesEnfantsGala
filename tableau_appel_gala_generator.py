import unidecode
import gala_library
import pandas as pd



#ordre_de_passage = gala_library.ordre_de_passage_creator()
def appel_generator():
    # importation de la liste des enfants
    gala_student_list = gala_library.make_gala_student_list()

    # Préparation du dataframe qui sera utilisé pour scanner les gens
    df = []
    for student in gala_student_list:
        code = unidecode.unidecode(student["prénom"] + "_" + student["nom"]).replace(" ", "_")
        G1 = False
        G2 = False
        G3 = False
        if len(student["G1"]) > 0:
            G1 = True
        if len(student["G2"]) > 0:
            G2 = True
        if len(student["G3"]) > 0:
            G3 = True
        df.append({"prénom": student["prénom"],
                   "nom": student["nom"],
                   "code": code,
                   "téléphone": student["téléphone"],
                   "G1": G1,
                   "G2": G2,
                   "G3": G3,
                   "Cours G1": student["G1"],
                   "Cours G2": student["G2"],
                   "Cours G3": student["G3"],
                   "Entrée rep. G1": False,
                   "Sortie rep. G1": False,
                   "Entrée G1": False,
                   "Entrée rep. G2": False,
                   "Sortie rep. G2": False,
                   "Entrée G2": False,
                   "Entrée rep. G3": False,
                   "Sortie rep. G3": False,
                   "Entrée G3": False})

    df = pd.DataFrame(df)
    print(df)
    return df
