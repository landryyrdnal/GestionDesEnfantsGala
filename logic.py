import pandas as pd


def scan_code(code:str, df:pd.DataFrame, gala:str):
    # On initialise les valeurs par défaut en cas d'échec de lecture
    T1, T2, T3, T4 = '', '', '', ''
    nom_enfant = 'Erreur de lecture'
    try:
        # on cherche l'index de la ligne correspondant au code de l'enfant
        index_enfant = df.loc[df["code"] == code].index.tolist()[0]
        # on récupère le nom et le prénom de l'enfant
        nom_enfant = df.at[index_enfant, "prénom"] + ' ' + df.at[index_enfant, 'nom']
        # on récupère la ou les chorées que l'enfant fait pendant ce Gala
        galas = [1,2,3]
        for i in galas:
            if gala == f'Gala {galas.index(i)+1}':
                # todo: trier les chorées pour qu'elles soient affichées dans l'ordre
                chorees = df.at[index_enfant, f'Cours G{galas.index(i)+1}']
                if len(chorees)>0:
                    T1 = str(chorees[0])
                if len(chorees)>1:
                    T2 = str(chorees[1])
                if len(chorees)>2:
                    T3 = str(chorees[2])
                if len(chorees)>3:
                    T4 = str(chorees[4])
                # todo: préciser si l'élève fait un autre gala ou non
    except IndexError: # si le code lu est mauvais l,index de code ne se trouvera pas dans la df
        pass
    return nom_enfant, T1, T2, T3, T4