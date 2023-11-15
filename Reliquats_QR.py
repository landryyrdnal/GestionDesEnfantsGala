import QR_maker
import data_base_process
import toml
import os

def liste_eleves_reliquat():
    # choix de la version du fichier à comparer.
    parameters = "parameters.toml"
    directory = toml.load(parameters)["DataBase"]["database_rep"]
    last_db = toml.load(parameters)["DataBase"]["last_bd"]
    last_db = os.path.join(directory, last_db)

    var_semaine_old, liste_niveau_old = data_base_process.process_data_base(False, last_db)
    var_semaine, liste_niveau = data_base_process.process_data_base()
    print("____________________________")
    print(var_semaine_old)
    print("____________________________")
    print(var_semaine)
    print(len(var_semaine_old), len(var_semaine))
if __name__ == "__main__":
    liste_eleves_reliquat()