from kivy.config import Config

Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '2400')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from collections import deque

# Gerätestandorte mit Bildsymbolen
geraete = [
    {'pos': (0.8, 0.3), 'symbol': 'Laufband.png', 'name': 'Laufband', 'übung': 'Laufband.png', 'typ': 'laufband'},
    {'pos': (0.8, 0.7), 'symbol': 'Bankdruecken.png', 'name': 'Bankdruecken', 'übung': 'Bankdruecken.png', 'typ': 'brust'},
    {'pos': (0.8, 0.63), 'symbol': 'BrustMaschine.png', 'name': 'Brustmaschine', 'übung': 'BrustMaschine.png', 'typ': 'brust'},
    {'pos': (0.2, 0.35), 'symbol': 'BrustMaschineZwei.png', 'name': 'Brustmaschine 2', 'übung': 'BrustMaschineZwei.png', 'typ': 'brust'},
    {'pos': (0.55, 0.45), 'symbol': 'Dips.png', 'name': 'Dips', 'übung': 'Dips.png', 'typ': 'trizeps'},
    {'pos': (0.7, 0.7), 'symbol': 'Kabel.png', 'name': 'Kabelzug', 'übung': 'Kabel.png', 'typ': 'kabel'},
    {'pos': (0.7, 0.63), 'symbol': 'Hantel.png', 'name': 'Hanteltraining', 'übung': 'Hantel.png', 'typ': 'hantel'}
]

class GymMap(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.add_widget(Image(source='gym raumplan für app.png', allow_stretch=True, keep_ratio=False, pos_hint={"center_x": 0.5, "center_y": 0.5})) #size_hint=(1, 0.6) 
        
        self.aktuelle_uebung = 'Laufband'
        #self.muskelgruppen = {'brust': 0, 'schulter': 0, 'trizeps': 0}
        self.abgeschlossene_uebungen = set()
        self.letzteÜbungstypen = deque()

        self.kabelcount = 0
        self.hantelcount = 0
        
        self.symbols = {}
        for geraet in geraete:
            img = Image(source=geraet['symbol'], size_hint=(0.1, 0.1), pos_hint={'x': geraet['pos'][0], 'y': geraet['pos'][1]})
            img.bind(on_touch_down=lambda instance, touch, g=geraet: self.show_exercise(g, touch))
            self.symbols[geraet['name']] = img
            self.add_widget(img)
            
            if geraet['name'] != self.aktuelle_uebung:
                img.opacity = 0.5

    def show_exercise(self, geraet, touch):
        if not self.symbols[geraet['name']].collide_point(*touch.pos):
            return
        
        if geraet['name'] in self.abgeschlossene_uebungen or not self.is_uebung_erlaubt(geraet):
            return
        
        popup = ModalView(size_hint=(0.8, 0.5))
        layout = RelativeLayout()
        
        if geraet['typ'] in ['hantel', 'kabel']:
            if not 'trizeps' in self.letzteÜbungstypen and not 'schulter' in self.letzteÜbungstypen: 
                title = Label(text="Trizeps oder Schulter", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.9}, bold=True, font_size=24)
                layout.add_widget(title)

                exercise_img = Image(source=geraet['übung'], size_hint=(1, 0.7), pos_hint={'x': 0, 'y': 0.1})
                layout.add_widget(exercise_img)

                close_button = Button(text='Weiter', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
                close_button.bind(on_release=lambda instance: (popup.dismiss(), self.waehle_muskelgruppe(geraet)))
                layout.add_widget(close_button) 
            
            elif not 'trizeps' in self.letzteÜbungstypen: 
                title = Label(text="Trizeps", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.9}, bold=True, font_size=24)
                layout.add_widget(title)

                exercise_img = Image(source=geraet['übung'], size_hint=(1, 0.7), pos_hint={'x': 0, 'y': 0.1})
                layout.add_widget(exercise_img)

                close_button = Button(text='Weiter', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
                close_button.bind(on_release=lambda instance: (self.letzteÜbungstypen.append('trizeps'), self.next_exercise(popup, geraet)))
                layout.add_widget(close_button)

            elif not 'schulter' in self.letzteÜbungstypen:
                title = Label(text="Schultern", size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.9}, bold=True, font_size=24)
                layout.add_widget(title)

                exercise_img = Image(source=geraet['übung'], size_hint=(1, 0.7), pos_hint={'x': 0, 'y': 0.1})
                layout.add_widget(exercise_img)

                close_button = Button(text='Weiter', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
                close_button.bind(on_release=lambda instance: (self.letzteÜbungstypen.append('schulter'), self.next_exercise(popup, geraet)))
                layout.add_widget(close_button)

  

        else:
            title = Label(text=geraet['name'], size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.9}, bold=True, font_size=24)
            layout.add_widget(title)

            exercise_img = Image(source=geraet['übung'], size_hint=(1, 0.7), pos_hint={'x': 0, 'y': 0.1})
            layout.add_widget(exercise_img)

            close_button = Button(text='Weiter', size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
            close_button.bind(on_release=lambda instance: self.next_exercise(popup, geraet))
            layout.add_widget(close_button)
        
        popup.add_widget(layout)
        popup.open()
    
    def next_exercise(self, popup, abgeschlossenes_geraet):
        popup.dismiss()
        
        if abgeschlossenes_geraet['typ'] == 'kabel':
            self.kabelcount += 1
        if abgeschlossenes_geraet['typ'] == 'hantel':
            self.hantelcount += 1
        if self.kabelcount == 2 or self.hantelcount == 2: 
            self.abgeschlossene_uebungen.add(abgeschlossenes_geraet['name'])
        
        if abgeschlossenes_geraet['typ'] == 'laufband':
            self.abgeschlossene_uebungen.add(abgeschlossenes_geraet['name'])
            self.aktualisiere_verfuegbarkeit()
            return
        elif not abgeschlossenes_geraet['typ'] in ['hantel', 'kabel']:
            self.letzteÜbungstypen.append(abgeschlossenes_geraet['typ'])
            self.abgeschlossene_uebungen.add(abgeschlossenes_geraet['name'])
    
        self.aktualisiere_verfuegbarkeit()
    
    def waehle_muskelgruppe(self, geraet):
        popup = ModalView(size_hint=(0.5, 0.3))
        layout = RelativeLayout()
        
        button_trizeps = Button(text='Trizeps', size_hint=(0.5, 1), pos_hint={'x': 0, 'y': 0})
        button_schulter = Button(text='Schulter', size_hint=(0.5, 1), pos_hint={'x': 0.5, 'y': 0})
        
        button_trizeps.bind(on_release=lambda instance: self.setze_muskelgruppe(popup, 'trizeps'))
        button_schulter.bind(on_release=lambda instance: self.setze_muskelgruppe(popup, 'schulter'))
        
        layout.add_widget(button_trizeps)
        layout.add_widget(button_schulter)
        
        popup.add_widget(layout)
        popup.open()

        
        if geraet['typ'] == 'kabel':
            self.kabelcount += 1
        if geraet['typ'] == 'hantel':
            self.hantelcount += 1
        if self.kabelcount == 2 or self.hantelcount == 2: 
            self.abgeschlossene_uebungen.add(geraet['name'])
    
    def setze_muskelgruppe(self, popup, muskelgruppe):
        popup.dismiss()
        self.letzteÜbungstypen.append(muskelgruppe)
        self.aktualisiere_verfuegbarkeit()
    
    def is_uebung_erlaubt(self, geraet):
        if geraet['name'] in self.abgeschlossene_uebungen:
            return False
        
        if len(self.letzteÜbungstypen) == 1:
            if geraet['typ'] == self.letzteÜbungstypen[0]:
                return False
            
        if len(self.letzteÜbungstypen) == 2:
            if geraet['typ'] == self.letzteÜbungstypen[0] or geraet['typ'] == self.letzteÜbungstypen[1]:
                return False
            
        if geraet['typ'] in ['hantel', 'kabel']:
            if 'trizeps' in self.letzteÜbungstypen and 'schulter' in self.letzteÜbungstypen:
                return False
        
        return True
    
    def aktualisiere_verfuegbarkeit(self):
        if len(self.letzteÜbungstypen) == 3:
            self.letzteÜbungstypen.popleft()
        for geraet in geraete:
            self.symbols[geraet['name']].opacity = 1.0 if self.is_uebung_erlaubt(geraet) else 0.5
        
        print(self.letzteÜbungstypen)

class GymApp(App):
    def build(self):
        return GymMap()

if __name__ == "__main__":
    GymApp().run()













