from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tableau_appel_gala_generator
import reportlab_qrcode
import os
from parameters import liste_profs, galas, result_dir, liste_couleurs_rgb as colors




def make_qr(data: str):
    """
    Génère un QR code à partir de la donnée entrée en paramètre
    :param data: une str de la donnée à scanner
    :return: une image du type reportlab_qrcode.QRCodeImage
    """
    qr = reportlab_qrcode.QRCodeImage(data, size=20 * mm, border=0)
    return qr


class Etiquette_qr():
    def __init__(self, student, height=0, width=0, x=0, y=0):
        """
        Classe qui sert à stocker les information utiles pour l’étiquette QR du Gala à agrafer sur le sac
        :param student: ligne d’un df pandas du type pandas.core.series.Series
        :param height: hauteur de l’étiquette
        :param width: largeur de l’étiquette
        :param x: position x de départ de l’étiquette
        :param y: position y de départ de l’étiquette
        """
        self.student = student
        self.code = student["code"]
        self.qr = self.generate_qr()
        self.nom = self.make_nom(student)
        self.tableaux = self.make_text_tableaux(student)
        self.sac_color = self.get_sac_col(student)
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def make_nom(self, student):
        nom = student["prénom"] + " " + student["nom"]
        if len(nom) > 26:
            nom = nom[:26]+"."
        return nom

    def get_sac_col(self, student):
        if len(student["cours G1"])>0:
            for prof_ in liste_profs:
                if liste_profs[prof_]["nom"] == student["cours G1"][0].prof:
                    sac_G1 = {"text":liste_profs[prof_]["couleur_sac"],
                              "color":liste_profs[prof_]["fond"],
                              "font":liste_profs[prof_]["couleur"]}
        else: 
            sac_G1 = None
        if len(student["cours G2"])>0:
            for prof_ in liste_profs:
                if liste_profs[prof_]["nom"] == student["cours G2"][0].prof:
                    sac_G2 = {"text":liste_profs[prof_]["couleur_sac"],
                              "color":liste_profs[prof_]["fond"],
                              "font":liste_profs[prof_]["couleur"]}
        else: 
            sac_G2 = None
        if len(student["cours G3"])>0:
            for prof_ in liste_profs:
                if liste_profs[prof_]["nom"] == student["cours G3"][0].prof:
                    sac_G3 = {"text":liste_profs[prof_]["couleur_sac"],
                              "color":liste_profs[prof_]["fond"],
                              "font":liste_profs[prof_]["couleur"]}
        else: 
            sac_G3 = None
        
        return {"G1":sac_G1, "G2":sac_G2, "G3":sac_G3}

    def generate_qr(self):
        image = make_qr(self.code)
        return image

    def make_text_tableaux(self, student):
        T = ""
        if len(student["cours G1"]) > 0:
            for i in student["cours G1"]:
                T += str(i) + "\n"
        if len(student["cours G2"]) > 0:
            for i in student["cours G2"]:
                T += str(i) + "\n"
        if len(student["cours G3"]) > 0:
            for i in student["cours G3"]:
                T += str(i) + "\n"
        return T

    def __repr__(self):
        string = "Étiquette " + self.code
        return string


def make_students_qr_list_for_each_gala(student_list):
    """
    Sert à créer trois liste, une pour chaque gala, dans lesquelles tous les enfants qui y participent sont listés
    :return: Une liste de trois liste pour chaque Gala. Dans chaque liste de Gala les éléments sont de type Etiquette_qr
    il y en a une par enfant
    """

    student_qr_list_1 = []
    student_qr_list_2 = []
    student_qr_list_3 = []
    for index, student in student_list.iterrows():
        if len(student["cours G1"]) > 0:
            student_qr_list_1.append(Etiquette_qr(student))
        if len(student["cours G2"]) > 0:
            student_qr_list_2.append(Etiquette_qr(student))
        if len(student["cours G3"]) > 0:
            student_qr_list_3.append(Etiquette_qr(student))
    result = [student_qr_list_1, student_qr_list_2, student_qr_list_3]
    for i in result:
        i.sort(key=lambda x:x.student[f"cours G{result.index(i)+1}"][0])
    return result


def make_pdf_qr_labels(etiquettes_data):
    """
    Cette fonction sert à créer les trois fichiers pdf avec toutes les étiquettes QR de chaque Gala
    :return: rien du tout, créer seulement trois fichiers pdf : « etiquettes_G1.pdf », etc.
    """
    col_count = 2
    row_count = 7
    label_width = A4[0] / col_count
    label_height = A4[1] / row_count
    # Pour chaque gala on vas générer une liste différente d’étiquette avec tous les participants
    for gala in etiquettes_data:
        etiquettes = []
        gala_number = etiquettes_data.index(gala) + 1
        nb_etiquettes = len(gala)
        nb_etiquettes_par_page = col_count * row_count

        # Pour chaque étiquette on ajoute les données de taille des
        # étiquettes ainsi que leur coordonnée sur la feuille A4
        index = 0
        for page in range((nb_etiquettes // (nb_etiquettes_par_page)) + 1):
            for row in range(row_count):
                for col in range(col_count):
                    if index < len(gala):
                        etiquette = gala[index]
                        etiquette.height = label_height
                        etiquette.width = label_width
                        etiquette.x = col * label_width
                        etiquette.y = A4[1] - (row + 1) * label_height
                        etiquettes.append(etiquette)
                        index += 1
                        print(str(index), str(etiquette.code), "x", str(etiquette.x), "y", str(etiquette.y))

        # création du fichier pdf
        file_path = os.path.join(result_dir, f"étiquettes_G{gala_number}.pdf")
        c = canvas.Canvas(file_path, pagesize=A4)

        def set_color(color):
            color = colors[color]
            c.setFillColorRGB(color[0] / 255, color[1] / 255, color[2] / 255)
        def draw_text(x, y, text, size, font, rotation, font_col="noir"):
            """
            Sous fonction qui sert à faciliter l’écriture du texte sur le pdf
            :param x: la position x de départ
            :param y: la position y de départ
            :param text: le texte à écrire
            :param size: la taille du texte
            :param font: la police du texte
            :param rotation: un bool qui autorise la rotation à 90°
            :return: ne retourne rien : imprime directement sur le pdf le texte
            à l’aide d’un objet de type reportlab.pdfgen.textobject.PDFTextObject
            """
            # FONCTIONS D’IMPRESSION
            # Sous fonction qui permet d’écrire le texte de la bonne couleur


            # si le texte a besoin d’être écrit à 90°
            if rotation:
                c.rotate(90)
                c.setFontSize(size)
                set_color(font_col)
                # on inverse la place du x et du y étant donné que le canvas est tourné de 90°
                c.drawString(y, -x, text)
                c.rotate(-90)
            else:
                #c.setFillColor(toml.load(parameters)["couleurs"][bg])
                textobject = c.beginText(x, y)
                textobject.setFont(font, size)
                set_color(font_col)
                for line in text.splitlines(False):
                    textobject.textLine(line.rstrip())
                c.drawText(textobject)

        # IMPRESSION DES ÉTIQUETTES
        index = 0
        for etiquette in etiquettes:
            # Si la page en cours est déjà remplie
            if index % nb_etiquettes_par_page == 0 and index != 0:
                c.showPage()  # ajout d’une nouvelle page pour les étiquettes suivantes
            # On dessine les bordures de l’étiquette
            c.rect(etiquette.x, etiquette.y, etiquette.width, etiquette.height)
            x = etiquette.x
            y = etiquette.y
            height = etiquette.height
            width = etiquette.width
            # Impression du QR code
            etiquette.qr.drawOn(c, x + (width // 8), y + (height // 8) * 2)
            # Impression du Prénom & du Nom de l’enfant
            draw_text(x + width // 8,
                      y + (height // 8) * 6.5,
                      etiquette.nom,
                      16,
                      "Helvetica-Bold",
                      False)
            # Impression des différents tableaux de l’enfant
            draw_text(x + (width // 8) * 2.65,
                      y + (height // 8) * 5,
                      etiquette.tableaux,
                      9,
                      "Helvetica",
                      False)
            # Impression du n° de Gala
            gala_color = galas[f"gala_{str(gala_number)}"]["couleur"]
            draw_text(x + (width//10)*1.15,
                      y + (height//6)*0.75,
                      f"GALA {str(gala_number)}",
                      25,
                      "Helvetica-Bold",
                      True,
                      gala_color)
            index += 1

            # Impression du logo
            c.drawImage("logo_noir.png", x + (width//10)*8, y + (height//6)*1.6, 18*mm, 18*mm, mask='auto')

            # Impression du rectangle de couleur
            x1, x2 = x + (width//8)*0.96, x + (width//8) * 7.04
            y1, y2 = y + (height//10)*0.6, y + (height//10) * 2.1
            set_color(etiquette.sac_color[f'G{str(gala_number)}']['color'])
            c.rect(x1, y1, x2 - x1, y2 - y1, fill=1, stroke=0)


            # Impression du texte de la couleur du sac
            text_sac = f"Sac {etiquette.sac_color[f'G{str(gala_number)}']['text']}"
            draw_text(x + (width // 8),
                      y + (height // 10),
                      text_sac,
                      12,
                      "Helvetica",
                      False,
                      etiquette.sac_color[f"G{str(gala_number)}"]["font"])
        c.save()


if __name__ == "__main__":
    student_list = tableau_appel_gala_generator.appel_generator()
    etiquettes_data = make_students_qr_list_for_each_gala(student_list)
    make_pdf_qr_labels(etiquettes_data)
