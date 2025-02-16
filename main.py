from kivy.config import Config

# Configure window size to simulate a typical smartphone format
Config.set('graphics', 'width', '1080')
Config.set('graphics', 'height', '2400')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
#from kivy.graphics import Color, Line
import matplotlib.pyplot as plt
from kivy.uix.image import Image
from kivy.graphics.texture import Texture

class SkullKingApp(App):
    def build(self):
    # Root layout with a background image
        self.root_layout = FloatLayout()

    # Add a background image
        self.background = Image(source='background.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.root_layout.add_widget(self.background)

    # Main UI layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=50, size_hint=(0.9, 0.9), pos_hint={"center_x": 0.5, "center_y": 0.6})

        self.label = Label(text="Enter player names:", size_hint=(1, None), halign="center", valign="middle", height=100, color=(1, 1, 1, 1), font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=2)
        self.label.bind(size=self.label.setter('text_size'))
        self.main_layout.add_widget(self.label)

    # Layout for player name inputs
        self.player_names_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, None))
        self.main_layout.add_widget(self.player_names_layout)

    # Add player input field
        self.player_name_input = TextInput(hint_text="Enter player name", multiline=False, size_hint_y=None, height=80, background_color=(0.2, 0.2, 0.2, 1), foreground_color=(1, 1, 1, 1))
        self.main_layout.add_widget(self.player_name_input)

    # Button to add player
        self.add_player_button = Button(text="Add Player", size_hint=(None, None), width=300, height=80, pos_hint={"center_x": 0.5}, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1), bold=True)
        self.add_player_button.bind(on_press=self.add_player)
        self.main_layout.add_widget(self.add_player_button)

    # Button to confirm players and proceed
        self.confirm_button = Button(text="Confirm players", size_hint=(None, None), width=300, height=80, pos_hint={"center_x": 0.5}, background_color=(0.1, 0.8, 0.5, 1), color=(1, 1, 1, 1), bold=True)
        self.confirm_button.bind(on_press=self.show_bid_inputs)
        self.main_layout.add_widget(self.confirm_button)

        self.players = []  # List to store player names
        self.root_layout.add_widget(self.main_layout)
        return self.root_layout

    def add_player(self, instance):
        player_name = self.player_name_input.text.strip()
        if player_name and player_name not in self.players:
            self.players.append(player_name)
            self.player_names_layout.add_widget(Label(text=player_name, size_hint_y=None, height=40, color=(1, 1, 1, 1), font_size=30))
            self.player_name_input.text = ""  # Clear input field

    def show_bid_inputs(self, instance):
        if not self.players:
            self.label.text = "Please add at least one player!"
            return

        self.main_layout.clear_widgets()
        self.rounds = 10
        self.current_round = 1
        self.bids = {name: [-1] * self.rounds for name in self.players}
        self.received_bids = {name: [-1] * self.rounds for name in self.players}
        self.scores = {name: [-1] * self.rounds for name in self.players}

        self.table_and_input_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1), pos_hint={"center_x": 0.5})
        self.main_layout.add_widget(self.table_and_input_layout)

        self.update_table_and_input()


    def update_table_and_input(self):
        self.table_and_input_layout.clear_widgets()

        table_layout = GridLayout(cols=(len(self.players)*3) + 1, size_hint_x=1, size_hint_y=None, height=1200, pos_hint={"center_x": 0.5})

        table_layout.add_widget(Label(text="Round", size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

        for name in self.players:
            table_layout.add_widget(Label(text=f"{name}\n Score", size_hint_x=0.4, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5, halign="center", valign="middle", text_size=(None, None)))  # Score breiter
            table_layout.add_widget(Label(text="B", size_hint_x=0.1, height=50, font_size=20, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))  # B kleiner
            table_layout.add_widget(Label(text="R", size_hint_x=0.1, height=50, font_size=20, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))  # R auch kleiner

        for round_num in range(1, self.rounds + 1):
            table_layout.add_widget(Label(text=str(round_num), size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

            for name in self.players:
                score = self.scores[name][round_num - 1]
                score_text = "-" if score == -1 else str(score)
                #with score_text.canvas.after:
                    #Color(1, 0, 0, 1)  # Rote Farbe
                    #line = Line(rectangle=(score_text.x, score_text.y, score_text.width, score_text.height), width=2)
                table_layout.add_widget(Label(text=score_text, size_hint_x=0.4, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

                bid = self.bids[name][round_num - 1]
                bid_text = "-" if bid == -1 else str(bid)
                table_layout.add_widget(Label(text=bid_text, size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

                rbid = self.received_bids[name][round_num - 1]
                rbid_text = "-" if rbid == -1 else str(rbid)
                table_layout.add_widget(Label(text=rbid_text, size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

        #scroll_view = ScrollView(size_hint=(1, None), size=(2000, 1000), pos_hint={"center_x": 0.5})
        #with scroll_view.canvas.after:
                #Color(1, 0, 0, 1)  # Rote Farbe
                #line = Line(rectangle=(scroll_view.x, scroll_view.y, scroll_view.width, scroll_view.height), width=2)
        #scroll_view.add_widget(table_layout)
        self.table_and_input_layout.add_widget(table_layout)

        input_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=500, pos_hint={"center_x": 0.5})
        round_label = Label(text=f"Round {self.current_round} - Bids", size_hint_y=None, height=100, color=(1, 1, 1, 1), font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5)
        input_layout.add_widget(round_label)

        self.bid_inputs = {}
        for name in self.players:
            player_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, pos_hint={"center_x": 0.5})
            player_label = Label(text=name, size_hint_x=0.5, color=(1, 1, 1, 1), font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5)
            player_box.add_widget(player_label)

            minus_button = Button(text="-", size_hint_x=0.2, background_color=(0.6, 0.2, 0.2, 1), color=(1, 1, 1, 1), bold=True)
            minus_button.bind(on_press=self.decrease_bid)

            bid_label = Label(text="0", size_hint_x=0.3, color=(1, 1, 1, 1), font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5)

            plus_button = Button(text="+", size_hint_x=0.2, background_color=(0.2, 0.6, 0.2, 1), color=(1, 1, 1, 1), bold=True)
            plus_button.bind(on_press=self.increase_bid)

            self.bid_inputs[name] = bid_label

            player_box.add_widget(minus_button)
            player_box.add_widget(bid_label)
            player_box.add_widget(plus_button)
            input_layout.add_widget(player_box)

        confirm_button = Button(text="Confirm Bids", size_hint_y=None, height=100, pos_hint={"center_x": 0.5}, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1), bold=True)
        confirm_button.bind(on_press=self.lock_bids)
        input_layout.add_widget(confirm_button)

        self.table_and_input_layout.add_widget(input_layout)

    def decrease_bid(self, instance):
        for name, label in self.bid_inputs.items():
            if instance in label.parent.children:
                current_value = int(label.text)
                if current_value > 0:
                    label.text = str(current_value - 1)

    def increase_bid(self, instance):
        for name, label in self.bid_inputs.items():
            if instance in label.parent.children:
                current_value = int(label.text)
                label.text = str(current_value + 1)

    def lock_bids(self, instance):
        for name, label in self.bid_inputs.items():
            self.bids[name][self.current_round - 1] = int(label.text)
        self.show_received_input()

    def show_received_input(self):
        self.table_and_input_layout.clear_widgets()

        table_layout = GridLayout(cols=(len(self.players)*3) + 1, size_hint_x=1, size_hint_y=None, height=1200, pos_hint={"center_x": 0.5})

        table_layout.add_widget(Label(text="Round", size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

        for name in self.players:
            table_layout.add_widget(Label(text=f"{name}\n Score", size_hint_x=0.4, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5, halign="center", valign="middle", text_size=(None, None)))  # Score breiter
            table_layout.add_widget(Label(text="B", size_hint_x=0.1, height=50, font_size=20, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))  # B kleiner
            table_layout.add_widget(Label(text="R", size_hint_x=0.1, height=50, font_size=20, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))  # R auch kleiner

        for round_num in range(1, self.rounds + 1):
            table_layout.add_widget(Label(text=str(round_num), size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

            for name in self.players:
                score = self.scores[name][round_num - 1]
                score_text = "-" if score == -1 else str(score)
                #with score_text.canvas.after:
                    #Color(1, 0, 0, 1)  # Rote Farbe
                    #line = Line(rectangle=(score_text.x, score_text.y, score_text.width, score_text.height), width=2)
                table_layout.add_widget(Label(text=score_text, size_hint_x=0.4, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

                bid = self.bids[name][round_num - 1]
                bid_text = "-" if bid == -1 else str(bid)
                table_layout.add_widget(Label(text=bid_text, size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

                rbid = self.received_bids[name][round_num - 1]
                rbid_text = "-" if rbid == -1 else str(rbid)
                table_layout.add_widget(Label(text=rbid_text, size_hint_x=0.1, height=50, font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=1.5))

        #scroll_view = ScrollView(size_hint=(1, None), size=(2000, 1000), pos_hint={"center_x": 0.5})
        #with scroll_view.canvas.after:
                #Color(1, 0, 0, 1)  # Rote Farbe
                #line = Line(rectangle=(scroll_view.x, scroll_view.y, scroll_view.width, scroll_view.height), width=2)
        #scroll_view.add_widget(table_layout)
        self.table_and_input_layout.add_widget(table_layout)

        input_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=500, pos_hint={"center_x": 0.5}) 
        round_label = Label(text=f"Round {self.current_round} - Received", size_hint_y=None, height=100, color=(1, 1, 1, 1), font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=2)
        input_layout.add_widget(round_label)

        self.received_inputs = {}
        self.extra_points = {name: 0 for name in self.players}  # Neue Variable für Extrapunkte

        for name in self.players:
            player_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, pos_hint={"center_x": 0.5})
            player_label = Label(text=name, size_hint_x=0.5, color=(1, 1, 1, 1), font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=2)
            player_box.add_widget(player_label)

            minus_button = Button(text="-", size_hint_x=0.2, background_color=(0.6, 0.2, 0.2, 1), color=(1, 1, 1, 1), bold=True)
            minus_button.bind(on_press=self.decrease_received)

            received_label = Label(text="0", size_hint_x=0.3, color=(1, 1, 1, 1), font_size=40, bold=True, outline_color=(0, 0, 0, 1), outline_width=2)

            plus_button = Button(text="+", size_hint_x=0.2, background_color=(0.2, 0.6, 0.2, 1), color=(1, 1, 1, 1), bold=True)
            plus_button.bind(on_press=self.increase_received)
    
            plus_ten_button = Button(text="+10", size_hint_x=0.2, background_color=(0.8, 0.6, 0.2, 1), color=(1, 1, 1, 1), bold=True)
            plus_ten_button.bind(on_press=lambda instance, n=name: self.add_extra_points(n))

            self.received_inputs[name] = received_label
    
            player_box.add_widget(minus_button)
            player_box.add_widget(received_label)
            player_box.add_widget(plus_button)
            player_box.add_widget(plus_ten_button)
            input_layout.add_widget(player_box)

    
        

        confirm_button = Button(text="Confirm Received", size_hint_y=None, height=100, pos_hint={"center_x": 0.5}, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1), bold=True)
        confirm_button.bind(on_press=self.lock_received)
        input_layout.add_widget(confirm_button)

        self.table_and_input_layout.add_widget(input_layout)
    
    def add_extra_points(self, player_name):
        self.extra_points[player_name] += 10
        print(f"{player_name} erhält 10 Extrapunkte. Gesamt: {self.extra_points[player_name]}")

    def decrease_received(self, instance):
        for name, label in self.received_inputs.items():
            if instance in label.parent.children:
                current_value = int(label.text)
                if current_value > 0:
                    label.text = str(current_value - 1)

    def increase_received(self, instance):
        for name, label in self.received_inputs.items():
            if instance in label.parent.children:
                current_value = int(label.text)
                label.text = str(current_value + 1)

    def lock_received(self, instance):
        for name, label in self.received_inputs.items():
            self.received_bids[name][self.current_round - 1] = int(label.text)

        for name in self.players:
            bid = self.bids[name][self.current_round - 1]
            received = self.received_bids[name][self.current_round - 1]
            if self.current_round == 1:
                if bid == received:
                    if bid == 0:
                        self.scores[name][self.current_round - 1] = self.current_round * 10
                    else:
                        self.scores[name][self.current_round - 1] = bid * 20
                else:
                    if bid == 0:
                        self.scores[name][self.current_round - 1] = - (self.current_round * 10)
                    else:
                        self.scores[name][self.current_round - 1] = - abs(bid - received) * 10
            else:
                if bid == received:
                    if bid == 0:
                        self.scores[name][self.current_round - 1] = self.scores[name][self.current_round - 2] + self.current_round * 10
                    else:
                        self.scores[name][self.current_round - 1] = self.scores[name][self.current_round - 2] + bid * 20
                else:
                    if bid == 0:
                        self.scores[name][self.current_round - 1] = self.scores[name][self.current_round - 2] - (self.current_round * 10)
                    else:
                        self.scores[name][self.current_round - 1] = self.scores[name][self.current_round - 2] -abs(bid - received) * 10

            self.scores[name][self.current_round - 1] += self.extra_points[name]

        if self.current_round < self.rounds:
            self.current_round += 1
            self.update_table_and_input()
        else:
            self.show_final_scores()

    def show_final_scores(self):
        self.main_layout.clear_widgets()

        score_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1), pos_hint={"center_x": 0.5})
        score_layout.add_widget(Label(text="Final Scores", size_hint_y=None, height=40, color=(1, 1, 1, 1), font_size=20))

        for name, scores in self.scores.items():
            total_score = self.scores[name][self.current_round - 1]
            score_layout.add_widget(Label(text=f"{name}: {total_score} points", size_hint_y=None, height=40, color=(1, 1, 1, 1), font_size=18))

        self.main_layout.add_widget(score_layout)

        self.show_score_graph()

    def show_score_graph(self):
    # Matplotlib-Diagramm erstellen
        plt.figure(figsize=(10, 6))
        for name, scores in self.scores.items():
            rounds = list(range(1, self.current_round + 1))
            plt.plot(rounds, scores[:self.current_round], label=name, marker='o')

        plt.xlabel('Runde')
        plt.ylabel('Punkte')
        plt.title('Spielverlauf')
        plt.legend()
        plt.grid(True)

    # Diagramm als Bild speichern
        plt.savefig("score_graph.png")
        plt.close()

    # Bild in Kivy anzeigen
        self.show_graph_in_app("score_graph.png")

    def show_graph_in_app(self, image_path):
        img = Image(source=image_path, size_hint=(1, 1))
        self.main_layout.add_widget(img)

if __name__ == "__main__":
    SkullKingApp().run()












