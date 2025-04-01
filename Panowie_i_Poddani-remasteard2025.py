import random
import pickle


class Game:
    def __init__(self):
        self.player = {
            'resources': 100,
            'lands': 1,
            'vassals': 0,
            'soldiers': 0,
            'military_power': 0
        }
        self.ai_players = [
            {
                'resources': 100,
                'lands': 1,
                'vassals': 0,
                'soldiers': 0,
                'military_power': 0
            } for _ in range(3)
        ]
        self.turn = 0

    def save_game(self):
        with open("game_save.pkl", "wb") as f:
            pickle.dump(self, f)
        print("Gra została zapisana.")

    def load_game(self):
        try:
            with open("game_save.pkl", "rb") as f:
                game = pickle.load(f)
            return game
        except FileNotFoundError:
            print("Brak zapisanej gry.")
            return self

    def display_status(self):
        print("\n--- Stan Gry ---")
        print(
            f"Gracz - Zasoby: {self.player['resources']}, Ziemie: {self.player['lands']}, Poddani: {self.player['vassals']}, Wojsko: {self.player['soldiers']}, Siła militarna: {self.player['military_power']}")
        for idx, ai in enumerate(self.ai_players, start=1):
            print(
                f"AI{idx} - Zasoby: {ai['resources']}, Ziemie: {ai['lands']}, Poddani: {ai['vassals']}, Wojsko: {ai['soldiers']}, Siła militarna: {ai['military_power']}")
        print("-------------------")

    def collect_taxes(self, player):
        taxes = player['vassals'] * 10
        player['resources'] += taxes
        print(f"Zbierasz podatki: +{taxes} zasobów.")

    def expand_land(self, player):
        if player['resources'] >= 50:
            player['lands'] += 1
            player['resources'] -= 50
            print("Zakupiono ziemię!")
        else:
            print("Za mało zasobów na zakup ziemi.")

    def recruit_vassal(self, player):
        if player['resources'] >= 30:
            player['vassals'] += 1
            player['resources'] -= 30
            print("Zwerbowano poddanego!")
        else:
            print("Za mało zasobów na zwerbowanie poddanego.")

    def recruit_soldiers(self, player):
        if player['resources'] >= 20:
            player['soldiers'] += 5
            player['resources'] -= 20
            player['military_power'] += 10
            print("Zwerbowałeś wojsko!")
        else:
            print("Za mało zasobów na rekrutację wojska.")

    def ai_turn(self, ai):
        action = random.choice(['collect_taxes', 'expand_land', 'recruit_vassal', 'recruit_soldiers'])
        if action == 'collect_taxes':
            self.collect_taxes(ai)
        elif action == 'expand_land':
            self.expand_land(ai)
        elif action == 'recruit_vassal':
            self.recruit_vassal(ai)
        elif action == 'recruit_soldiers':
            self.recruit_soldiers(ai)
        print(f"Ruch AI: {action}")

    def fight(self, ai):
        player_strength = self.player['military_power'] + self.player['soldiers']
        ai_strength = ai['military_power'] + ai['soldiers']
        print(f"Siła gracza: {player_strength}, Siła AI: {ai_strength}")

        if player_strength > ai_strength:
            print("Gratulacje! Pokonałeś AI.")
            ai['resources'] -= 30
            ai['lands'] -= 1
            self.player['resources'] += 50
            self.player['lands'] += 1
            ai['soldiers'] = max(ai['soldiers'] - ai['soldiers'] // 5, 0)
            self.player['soldiers'] = max(self.player['soldiers'] - self.player['soldiers'] // 5, 0)
            print("Po walce, obaj tracą część wojska.")
        elif player_strength < ai_strength:
            print("AI pokonało Cię!")
            self.player['resources'] -= 30
            self.player['lands'] -= 1
            self.player['soldiers'] = max(self.player['soldiers'] - self.player['soldiers'] // 5, 0)
            ai['soldiers'] = max(ai['soldiers'] - ai['soldiers'] // 5, 0)
            print("Po walce, obaj tracą część wojska.")
        else:
            print("Remis! Żadne z was nie wygrało.")

    def random_event(self):
        events = [
            ("Burza! Straciłeś część zasobów i wojska.", -20, -10, -5),
            ("Susza. Straciłeś część zasobów.", -30, 0, 0),
            ("Żniwa okazały się udane! Zyskujesz dodatkowe zasoby.", 50, 0, 0)
        ]
        event = random.choice(events)
        print(f"\n--- Zdarzenie: {event[0]} ---")

        self.player['resources'] += event[1]
        #self.player['lands'] += event[2]
        self.player['soldiers'] = max(self.player['soldiers'] + event[3], 0)

        for ai in self.ai_players:
            ai['resources'] += event[1]
            ai['lands'] += event[2]
            ai['soldiers'] = max(ai['soldiers'] + event[3], 0)

    def game_turn(self):
        self.turn += 1
        print(f"\nTura {self.turn}")
        self.display_status()

        if self.turn % 3 == 0:
            self.random_event()

        action = input(
            "Wybierz akcję: [1] Zbieraj podatki, [2] Kup ziemię, [3] Zwerbuj poddanego, [4] Zwerbuj wojsko, [5] Walka z AI, [6] Zapisz grę, [7] Załaduj grę: ")

        if action == '1':
            self.collect_taxes(self.player)
        elif action == '2':
            self.expand_land(self.player)
        elif action == '3':
            self.recruit_vassal(self.player)
        elif action == '4':
            self.recruit_soldiers(self.player)
        elif action == '5':
            ai_idx = int(input("Wybierz AI do walki (1, 2, 3): ")) - 1
            if 0 <= ai_idx < len(self.ai_players):
                self.fight(self.ai_players[ai_idx])
            else:
                print("Niepoprawny wybór AI.")
        elif action == '6':
            self.save_game()
        elif action == '7':
            self = self.load_game()
        else:
            print("Niepoprawna akcja.")

        for idx, ai in enumerate(self.ai_players, start=1):
            print(f"\nRuch AI{idx}:")
            self.ai_turn(ai)

    def show_intro(self):
        print("mfire development przedstawia")
        print("Panowie i Poddani - Remastered 2025")
        print("\nNaciśnij Enter, aby rozpocząć grę...")
        input()

    def start_game(self):
        self.show_intro()
        while True:
            self.game_turn()


if __name__ == "__main__":
    game = Game()
    game.start_game()
