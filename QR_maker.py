from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tableau_appel_gala_generator
import reportlab_qrcode

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
        self.code = student["code"]
        self.qr = self.generate_qr()
        self.nom = student["prénom"] + " " + student["nom"]
        self.tableaux = self.make_text_tableaux(student)
        self.height = height
        self.width = width
        self.x = x
        self.y = y

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
        print(T)
        return T

    def __repr__(self):
        string = self.code + " " + str(self.x) + " " + str(self.y)
        return string


def make_students_qr_list_for_each_gala():
    student_list = tableau_appel_gala_generator.appel_generator()
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
    return [student_qr_list_1, student_qr_list_2, student_qr_list_3]


def make_pdf_qr_labels():
    col_count = 2
    row_count = 7
    label_width = A4[0] / col_count
    label_height = A4[1] / row_count
    etiquettes_data = make_students_qr_list_for_each_gala()
    # Pour chaque gala on vas générer une liste différente d’étiquette avec tous les participants
    for gala in etiquettes_data:
        etiquettes = []
        gala_number = etiquettes_data.index(gala) + 1
        print(gala_number)
        nb_etiquettes = len(gala)
        nb_etiquettes_par_page = col_count * row_count

        # On ajoute les données de taille des étiquettes ainsi que leur coordonnée sur la feuille A4
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
        c = canvas.Canvas(f"etiquettes_G{gala_number}.pdf", pagesize=A4)

        def draw_text(x, y, text, size, font):
            textobject = c.beginText(x, y)
            textobject.setFont(font, size)
            for line in text.splitlines(False):
                textobject.textLine(line.rstrip())
            c.drawText(textobject)

        index = 0

        for etiquette in etiquettes:
            if index % nb_etiquettes_par_page == 0 and index != 0:
                c.showPage()  # ajout d’une nouvelle page pour les étiquettes suivantes
            # On dessine les bordures
            c.rect(etiquette.x, etiquette.y, etiquette.width, etiquette.height)
            x = etiquette.x
            y = etiquette.y
            height = etiquette.height
            width = etiquette.width
            # On dessine le QR Code
            etiquette.qr.drawOn(c, x + (width // 8), y + (height // 8) * 2)
            # On écrit le Prénom & le Nom de l’enfant
            draw_text(x + width // 8,
                      y + (height // 8) * 6,
                      etiquette.nom,
                      14,
                      "Helvetica-Bold")
            # On écrit les différents tableaux de l’enfant
            draw_text(x + (width // 8) * 2.5,
                      y + (height // 8) * 5,
                      etiquette.tableaux,
                      9,
                      "Helvetica")
            index += 1

        c.save()


if __name__ == "__main__":
    make_pdf_qr_labels()
