import pandas as pd


def find_index_kid(code, df:pd.DataFrame):
    # Retourne l'index de l'enfant dans la dataframe
    try:
        index_enfant = df.loc[df["code"] == code].index.tolist()[0]
    except IndexError:  # si le code lu est mauvais l,index de code ne se trouvera pas dans la df
        index_enfant = None
    return index_enfant


def scan_code(code: str, df: pd.DataFrame, gala: str):
    # On initialise les valeurs par défaut en cas d'échec de lecture
    T1, T2, T3, T4 = '', '', '', ''
    other_g = ""
    # on cherche l'index de la ligne correspondant au code de l'enfant
    index_enfant = find_index_kid(code, df)
    # on récupère le nom et le prénom de l'enfant
    if index_enfant != None:
        nom_enfant = df.at[index_enfant, "prénom"] + ' ' + df.at[index_enfant, 'nom']
        # on récupère la ou les chorées que l'enfant fait pendant ce Gala
        galas = [1, 2, 3]
        for i in galas:
            if gala == f'Gala {galas.index(i) + 1}':
                # todo: trier les chorées pour qu'elles soient affichées dans l'ordre

                chorees = sorted(df.at[index_enfant, f'Cours G{galas.index(i) + 1}'])
                if len(chorees) > 0:
                    T1 = str(chorees[0])
                if len(chorees) > 1:
                    T2 = str(chorees[1])
                if len(chorees) > 2:
                    T3 = str(chorees[2])
                if len(chorees) > 3:
                    T4 = str(chorees[4])
        # On indiaue tous les Galas que fait l'enfant
        for i in galas:
            col = f'Cours G{galas.index(i) + 1}'
            if len(df.at[index_enfant, col]) > 0:
                if col == 'Cours G1':
                    other_g = other_g + '❶'
                elif col == 'Cours G2':
                    other_g = other_g + '❷'
                elif col == 'Cours G3':
                    other_g = other_g + '❸'

        return nom_enfant, T1, T2, T3, T4, other_g
    else :
        return 'Erreur de lecture', '', '', '', '', ''