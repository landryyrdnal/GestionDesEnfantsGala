import toml

parameters = "parameters.toml"
liste_couleurs = toml.load(parameters)["couleurs"]
liste_couleurs_rgb = toml.load(parameters)["couleurs"]["rgb"]
liste_profs = toml.load(parameters)["profs"]
ordre_galas = toml.load(parameters)["DataBase"]["ordre_gala"]
galas = toml.load(parameters)["galas"]
semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]