import unidecode
import gala_library
import pandas as pd




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
                   "cours G1": student["G1"],
                   "cours G2": student["G2"],
                   "cours G3": student["G3"],
                   "entrée rep. G1": False,
                   "sortie rep. G1": False,
                   "entrée G1": False,
                   "entrée rep. G2": False,
                   "sortie rep. G2": False,
                   "entrée G2": False,
                   "entrée rep. G3": False,
                   "sortie rep. G3": False,
                   "entrée G3": False})

    df = pd.DataFrame(df)
    return df

if __name__ == "__main__":
    appel_generator()