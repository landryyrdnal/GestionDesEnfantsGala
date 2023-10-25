from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors.focus import FocusBehavior
import family_for_gala_generator
import tableau_appel_gala_generator
import logic


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
        nom_enfant, T1, T2, T3, T4 = logic.scan_code(text, df, gala)
        self.ids.scan_input.text=""
        self.ids.choree_1.text = T1
        self.ids.choree_2.text = T2
        self.ids.choree_3.text = T3
        self.ids.choree_4.text = T4
        self.ids.just_scanned.text = nom_enfant # pour afficher le texte qui vient juste d’être scanné en haut de l’input
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
    df = tableau_appel_gala_generator.appel_generator()
    GalaApp().run()