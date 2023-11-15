import toml

parameters = "parameters.toml"
directory = toml.load(parameters)["DataBase"]["database_rep"]
liste_couleurs = toml.load(parameters)["couleurs"]
liste_couleurs_rgb = toml.load(parameters)["couleurs"]["rgb"]
liste_profs = toml.load(parameters)["profs"]
ordre_galas = toml.load(parameters)["DataBase"]["ordre_gala"]
galas = toml.load(parameters)["galas"]
semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
old_excel = toml.load(parameters)["DataBase"]["last_bd"]
annee_scolaire = toml.load(parameters)["DataBase"]["annee_scolaire"]
col_verif = toml.load(parameters,)["DataBase"]["col_verif"]
col_saison = toml.load(parameters)["DataBase"]["col_saison"]