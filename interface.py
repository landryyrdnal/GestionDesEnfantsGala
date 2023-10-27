from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors.focus import FocusBehavior
import family_for_gala_generator
import tableau_appel_gala_generator
import logic
import records


# Définition des écrans
# Écran du choix entre Gala 1, 2 et 3
class GalaWindow(Screen):
    def press(self, gala):
        # on assigne la variable gala au texte de la page suivante
        self.manager.ids.entry_exit_window.ids.gala_number.text = gala


# Écran du choix entre l’entrée en répétition, la sortie de répétition et l’entrée au gala
class EntryExitWindow(Screen):
    pass



# Écran de scan des QR
class ScanWindow(Screen):
    def validate(self, text):
        gala = self.manager.ids.entry_exit_window.ids.gala_number.text
        nom_enfant, T1, T2, T3, T4, other_g = logic.scan_code(text, input_df, gala)
        # On ajoute l'enfant a la base de donnée finale s'il existe
        records.record_kid(code_kid=text,
                           current_gala=gala,
                           record_col='', # todo: Définir les bonnes variables dans le fichier kv
                           output_df=output_df,
                           input_df=input_df)
        # Effacement du text dans le TextInput
        self.ids.scan_input.text = ""
        # Affichage des cours de l'enfant scanné
        self.ids.choree_1.text = T1
        self.ids.choree_2.text = T2
        self.ids.choree_3.text = T3
        self.ids.choree_4.text = T4
        # Affichage des autres galas de l'enfant
        self.ids.autre_gala.text = other_g
        # Affichage du nom de l'enfant scanné
        self.ids.just_scanned.text = nom_enfant  # pour afficher le texte qui vient juste d’être scanné en haut de l’input
        # Repointage du focus sur le TextInput après le scan
        FocusBehavior.focus = True


# Définition du screen manager
class WindowManager(ScreenManager):
    pass


# Définition du fichier de design KV
kv = Builder.load_file("interface.kv")


class GalaApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    input_df = tableau_appel_gala_generator.appel_generator()
    # Définition de la db de sortie
    output_df =  input_df
    output_df['Entrée rep. G1'] = False
    output_df['Sortie rep. G1'] = False
    output_df['Entrée Gala G1'] = False
    output_df['Entrée rep. G2'] = False
    output_df['Sortie rep. G2'] = False
    output_df['Entrée Gala G2'] = False
    output_df['Entrée rep. G3'] = False
    output_df['Sortie rep. G3'] = False
    output_df['Entrée Gala G3'] = False
    print(output_df)
    GalaApp().run()
