import os
import pandas as pd
import tableau_appel_gala_generator
import QR_maker
from parameters import last_db, old_excel, result_dir

def liste_eleves_reliquat():
    # création de l’ancienne base de donnée des enfants (étiquettes déjà imprimées à un moment T, la version du fichier
    # excel est à préciser dans parameters.toml)
    old_student_list = tableau_appel_gala_generator.appel_generator(False, last_db)
    # création de la nouvelle base de donnée des enfants
    new_student_list = tableau_appel_gala_generator.appel_generator()

    def get_modif(old_student_list, new_student_list):
        enfants_modifies = pd.DataFrame(columns=old_student_list.columns)

        for index, old_student in old_student_list.iterrows():
            code = old_student['code']

            # Trouver l'élève correspondant dans la nouvelle base de données
            new_student = new_student_list[new_student_list['code'] == code]

            # S'il n'y a pas de correspondance, l'élève a été supprimé
            if new_student.empty:
                continue

            # Comparer les cours G1, G2 et G3
            cours_modifies = (
                    old_student['cours G1'] != new_student['cours G1'].values[0] or
                    old_student['cours G2'] != new_student['cours G2'].values[0] or
                    old_student['cours G3'] != new_student['cours G3'].values[0]
            )

            # Si les cours ont changé, ajouter l'élève à la base de données des enfants modifiés
            if cours_modifies:
                # on modifie les noms et les prénoms afin d’identifier les changements
                new_student["nom"] = "NEW_" + new_student["nom"]
                new_student["prénom"] = "NEW_" + new_student["prénom"]
                old_student["nom"] = "OLD_" + old_student["nom"]
                old_student["prénom"] = "OLD_" + old_student["prénom"]
                enfants_modifies = enfants_modifies.append(old_student, ignore_index=True)
                enfants_modifies = enfants_modifies.append(new_student, ignore_index=True)

        return enfants_modifies

    # on détermine quels enfants on été ajoutés
    enfants_ajoutes = new_student_list[~new_student_list['code'].isin(old_student_list['code'])]

    # on détermine quels enfants ont été enlevés
    enfants_supprimes = old_student_list[~old_student_list['code'].isin(new_student_list['code'])]

    # on détermine quels enfants ont été modifiés
    enfants_modif = get_modif(old_student_list, new_student_list)

    # On consigne les trois listes d’enfants ajoutés, enlevés et modifiés dans le fichier excel
    nom_fichier = f'Reliquats depuis le dernier tirage le {old_excel.split(".xlsx")[0]}.xlsx'
    path = os.path.join(result_dir, nom_fichier)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        # Enregistrer le DataFrame des enfants ajoutés sur une feuille nommée 'Enfants_Ajoutés'
        enfants_ajoutes.to_excel(writer, sheet_name='Enfants Ajoutés', index=False)
        # Imprimer le DataFrame des enfants supprimés sur une feuille nommée 'Enfants_Supprimés'
        enfants_supprimes.to_excel(writer, sheet_name='Enfants Supprimés', index=False)
        # Imprimer le DataFrame des enfans modifiés
        enfants_modif.to_excel(writer, sheet_name="Enfants Modifiés", index=False)
        # Enregistrer le fichier excel des reliquats
        writer.save()
        print(f"fichier excel des reliquats enregistré sous '{nom_fichier}' ")

    # Faire l’impression des étiquettes des enfants en plus
    etiquettes_data = QR_maker.make_students_qr_list_for_each_gala(enfants_ajoutes)
    QR_maker.make_pdf_qr_labels(etiquettes_data)
    print("impression des étiquettes des enfants en plus terminée")

if __name__ == "__main__":
    liste_eleves_reliquat()