import toml
import os

parameters = "parameters.toml"
directory = toml.load(parameters)["DataBase"]["database_rep"]
fichiers_modif_dir = toml.load(parameters)["DataBase"]["fichiers_modif_dir"]
result_dir = toml.load(parameters)["DataBase"]["result_dir"]
liste_couleurs = toml.load(parameters)["couleurs"]
liste_couleurs_rgb = toml.load(parameters)["couleurs"]["rgb"]
liste_profs = toml.load(parameters)["profs"]
ordre_galas = toml.load(parameters)["DataBase"]["ordre_gala"]
ordre_galas = os.path.join(fichiers_modif_dir, ordre_galas)
galas = toml.load(parameters)["galas"]
semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
old_excel = toml.load(parameters)["DataBase"]["last_db"]
annee_scolaire = toml.load(parameters)["DataBase"]["annee_scolaire"]
col_verif = toml.load(parameters,)["DataBase"]["col_verif"]
col_saison = toml.load(parameters)["DataBase"]["col_saison"]
last_db = toml.load(parameters)["DataBase"]["last_db"]
last_db = last_db = os.path.join(directory, last_db)