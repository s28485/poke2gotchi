import pygame
import sys
import json
import os

if not os.path.exists("saves"):
    os.makedirs("saves")
import Button

# Inicjalizacja Pygame
pygame.init()
pygame.mixer.init()

# Timer wyboru zwierzaka
start_time = pygame.time.get_ticks()

# Okno
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pokegotchi")

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
VIOLET = (73, 19, 99)

# Czcionki
font = pygame.font.SysFont(None, 36)

# Obrazki do wyboru pokemona i skalowanie do odpowiednich rozmiarów
squirtle_image = pygame.transform.scale(pygame.image.load("assets/squirtle.png"), (200, 200))
charmander_image = pygame.transform.scale(pygame.image.load("assets/charmander.png"), (200, 200))
bulbasaur_image = pygame.transform.scale(pygame.image.load("assets/bulbasaur.png"), (200, 200))
pikachu_image = pygame.transform.scale(pygame.image.load("assets/pikachu.png"), (200, 200))

evolution_lines = {
    'Bulbasaur': ['Bulbasaur', 'Ivysaur', 'Venusaur'],
    'Squirtle': ['Squirtle', 'Wartortle', 'Blastoise'],
    'Charmander': ['Charmander', 'Charmeleon', 'Charizard'],
    'Pikachu': ['Pikachu', 'Raichu', 'AlolanRaichu']
}


# Tworzenie klasy Pokemon
class Pet:
    def __init__(self, name):

        # Pet properties
        self.name: str = name
        for k, v in evolution_lines.items():
            if self.name in v:
                self.evolution_line = k
        self.hunger: int = 100  # 0 - głodny, 100 - najedzony
        self.happiness: int = 100  # 0 - smutny, 100 - szczęśliwy
        self.sleepiness: int = 100  # 0 - śpiący, 100 - wyspany
        self.experience: int = 0  # EXP
        self.max_experience: int = width - 12
        self.evolution_stage: int = evolution_lines[self.evolution_line].index(self.name)
        self.level: int = 1
        self.image = None

        # Timers and intervals
        self.hunger_timer: int = 0  # Licznik czasu głodu (w klatkach)
        self.happiness_timer: int = 0
        self.sleepiness_timer: int = 0
        self.hunger_increment_interval: int = 100  # Co ile klatek głód ma wzrosnąć (np. co 5 klatek)
        self.happiness_increment_interval: int = 100  # Co ile klatek szczęście ma wzrosnąć (np. co 5 klatek)
        self.sleepness_increment_interval: int = 300  # Co ile klatek zmęczenie ma wzrosnąć (np. co 5 klatek)

        self.load_image()

        self.feed_button = Button.Button(
            x=60, y=500, width=200, height=50,
            text = "Feed",
            color = BLUE,
            hover_color = (0, 0, 150),
            command=self.feed
        )

        self.play_button = Button.Button(
            x=290, y=500, width=200, height=50,
            text="Play",
            color=GREEN,
            hover_color=(0, 150, 0),
            command=self.play
        )

        self.sleep_button = Button.Button(
            x=520, y=500, width=200, height=50,
            text="Sleep",
            color=RED,
            hover_color=(150, 0, 0),
            command=self.sleep
        )


    def save(self, player_name) -> None:
        data = {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "sleepiness": self.sleepiness,
            "level": self.level,
            "experience": self.experience
        }
        with open(f"saves/{player_name}.json", "w") as f:
            json.dump(data, f)
        print("Gra zapisana!")


    def level_up(self) -> None:
        self.level += 1
        if self.level == 25 or self.level == 50:
            self.evolve()
        self.experience = 0

    def gain_experience(self) -> None:
        self.experience += 1
        if self.experience >= self.max_experience:
            self.level_up()

    def get_experience(self) -> int:
        return self.experience

    def evolve(self) -> None:
        self.evolution_stage += 1
        self.name = evolution_lines[self.evolution_line][self.evolution_stage]
        self.load_image()

    def feed(self) -> None:
        self.hunger = max(self.hunger + 10, 0)

    def play(self) -> None:
        self.happiness = min(self.happiness + 10, 100)
        # self.sleepiness = min(self.sleepiness + 20, 100)

    def sleep(self) -> None:
        self.sleepiness = max(self.sleepiness + 10, 0)

    def update(self) -> None:
        # For test purposes
        if self.hunger < 50 and self.happiness < 50 and self.sleepiness < 50:
            self.gain_experience()

        # TODO: Jeśli wszystkie parametry spadną do 0, gra powinna się zakończyć.

        self.hunger_timer += 1
        if self.hunger_timer >= self.hunger_increment_interval:
            self.hunger = min(self.hunger - 1, 100)  # Zmniejszamy najedzenie o 1
            self.hunger_timer = 0  # Resetujemy licznik

        self.happiness_timer += 1
        if self.happiness_timer >= self.happiness_increment_interval:
            self.happiness = min(self.happiness - 1, 100)  # Zmniejszamy szczęście
            self.happiness_timer = 0  # Resetujemy licznik

        self.sleepiness_timer += 1
        if self.sleepiness_timer >= self.sleepness_increment_interval:
            self.sleepiness = min(self.sleepiness - 1, 100)  # Zmniejszamy wypoczęcie
            self.sleepiness_timer = 0  # Resetujemy licznik

    def draw(self) -> None:
        # Rysuj pokemona
        screen.blit(self.image, (250, 250))

        # Rysuj pasek expa
        pygame.draw.rect(screen, WHITE, (5, 5, 790, 50))
        pygame.draw.rect(screen, RED, (6, 6, self.get_experience(), 48))

        # Rysowanie statusów
        hunger_text = font.render(f"Najedzony: {self.hunger}", True, WHITE)
        happiness_text = font.render(f"Szczęście: {self.happiness}", True, WHITE)
        sleep_text = font.render(f"Wyspany: {self.sleepiness}", True, WHITE)
        level_text = font.render(f"Poziom: {self.level}", True, BLACK)

        screen.blit(hunger_text, (20, 60))
        screen.blit(happiness_text, (20, 100))
        screen.blit(sleep_text, (20, 140))
        screen.blit(level_text, (320, 20))

        # Przyciski interakcji
        self.feed_button.draw(screen)
        self.play_button.draw(screen)
        self.sleep_button.draw(screen)

        # pygame.draw.rect(screen, BLUE, (60, 500, 200, 50))
        # feed_text = font.render("Nakarm", True, WHITE)
        # screen.blit(feed_text, (75, 515))
        #
        # pygame.draw.rect(screen, GREEN, (290, 500, 200, 50))
        # play_text = font.render("Baw się", True, WHITE)
        # screen.blit(play_text, (310, 515))
        #
        # pygame.draw.rect(screen, RED, (520, 500, 200, 50))
        # sleep_text = font.render("Śpij", True, WHITE)
        # screen.blit(sleep_text, (545, 515))
        #
        pygame.draw.rect(screen, VIOLET, (520, 100, 200, 50))
        sleep_text = font.render("SAVE", True, WHITE)
        screen.blit(sleep_text, (545, 115))

        options_text = font.render("Press \'q\' to quit game, or \'m\' to enter main menu", True, (94, 94, 94))
        screen.blit(options_text, (125, 570))

    def load_image(self):
        self.image = pygame.transform.scale(pygame.image.load(f'assets/{self.name.lower()}.png'), (200, 200))


@staticmethod
def load(player_name) -> Pet:
    """
    Overrides a method from PyGame library
    :param player_name: string
    :return: Pet
    """
    with open(f"saves/{player_name}.json", "r") as f:
        data = json.load(f)
    pet = Pet(data["name"])
    pet.hunger = data["hunger"]
    pet.happiness = data["happiness"]
    pet.sleepiness = data["sleepiness"]
    pet.level = data["level"]
    pet.experience = data["experience"]
    return pet

# Funkcja, która rysuje menu wyboru zwierzaka
def choose_pet() -> None:
    current_time = pygame.time.get_ticks()
    time_elapsed = current_time - start_time

    screen.fill(BLACK)
    title_text = font.render("Wybierz swojego pokemona!", True, WHITE)
    screen.blit(title_text, (250, 50))

    # buttons = [
    #     Button(50, 400, 200, 50, "Squirtle", BLUE, (0, 0, 150),
    #            lambda: Pet("Squirtle")),
    #     Button(270, 400, 200, 50, "Charmander", RED, (150, 0, 0),
    #            lambda: Pet("Charmander")),
    #     Button(490, 400, 200, 50, "Bulbasaur", GREEN, (0, 150, 0),
    #            lambda: Pet("Bulbasaur"))
    # ]
    #
    # screen.blit(squirtle_image, (50, 190))
    # screen.blit(charmander_image, (270, 190))
    # screen.blit(bulbasaur_image, (490, 190))
    #
    # for b in buttons:
    #     b.draw(screen)
    #     b.handle_event(event)

    # Jeżeli nie dokonamy wyboru w ciągu 5 minut, zostanie przypisany pikatchu
    if time_elapsed > 5 * 60 * 60:
        screen.blit(pikachu_image, (270, 190))
        pygame.draw.rect(screen, VIOLET, (270, 400, 200, 50))
        pikachu_text = font.render("Pikachu", True, WHITE)
        screen.blit(pikachu_text, (275, 415))
    else:
        # Przycisk 1: Squirtle
        screen.blit(squirtle_image, (50, 190))
        pygame.draw.rect(screen, BLUE, (50, 400, 200, 50))
        squirtle_text = font.render("Squirtle", True, WHITE)
        screen.blit(squirtle_text, (55, 415))

        # Przycisk 2: Charmander
        screen.blit(charmander_image, (270, 190))
        pygame.draw.rect(screen, RED, (270, 400, 200, 50))
        cat_text = font.render("Charmander", True, WHITE)
        screen.blit(cat_text, (275, 415))

        # Przycisk 3: Bulbasaur
        screen.blit(bulbasaur_image, (490, 190))
        pygame.draw.rect(screen, GREEN, (490, 400, 200, 50))
        cat_text = font.render("Bulbasaur", True, WHITE)
        screen.blit(cat_text, (495, 415))

    pygame.display.update()


def player_select_menu():
    while True:
        screen.fill(BLACK)
        title = font.render("Wybierz gracza", True, WHITE)
        screen.blit(title, (300, 50))

        files = [f[:-5] for f in os.listdir("saves") if f.endswith(".json")]

        # Lista graczy
        for i, name in enumerate(files):
            pygame.draw.rect(screen, BLUE, (300, 120 + i * 60, 200, 50))
            screen.blit(font.render(name, True, WHITE), (320, 130 + i * 60))

        # Nowy gracz
        pygame.draw.rect(screen, GREEN, (300, 120 + len(files) * 60, 200, 50))
        screen.blit(font.render("Nowy gracz", True, BLACK), (310, 130 + len(files) * 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, name in enumerate(files):
                    if 300 <= x <= 500 and 120 + i * 60 <= y <= 170 + i * 60:
                        pet = load(name)
                        game_loop(pet, name)
                        return

                # Dodaj Nowy gracz - aktualnie wpisywany z konsoli
                new_index_y = 120 + len(files) * 60
                if 300 <= x <= 500 and new_index_y <= y <= new_index_y + 50:
                    name = get_user_name()
                    pygame.display.set_mode([800, 600])
                    pet = None
                    game_loop(pet, name)
                    return


# Nowy gracz - okno do wpisania nazwy
def get_user_name() -> str:
    clock = pygame.time.Clock()
    pygame.display.set_mode([400, 400])
    user_text = ''
    input_rec = pygame.Rect(20, 180, 140, 40)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
                if event.key == pygame.K_RETURN:
                    return user_text

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, input_rec, 1)
        text_surface = font.render(user_text, True, (255, 255, 255))
        screen.blit(font.render("Podaj imię gracza: ", True, WHITE), (20, 140))
        screen.blit(text_surface, (input_rec.x + 5, input_rec.y + 5))
        input_rec.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)


def main_menu() -> None:
    while True:
        screen.fill(BLACK)
        screen.blit(font.render("Pokegotchi", True, WHITE), (330, 100))

        pygame.draw.rect(screen, GREEN, (300, 250, 200, 50))
        screen.blit(font.render("Zagraj", True, BLACK), (360, 260))

        pygame.draw.rect(screen, RED, (300, 350, 200, 50))
        screen.blit(font.render("Wyjdź", True, BLACK), (360, 360))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if 500 >= x >= 300 >= y >= 250:
                    player_select_menu()
                    return


# Główna pętla gry
def game_loop(pet=None, player_name=None):
    running = True

    while running:
        screen.fill(BLACK)

        if pet is None:
            choose_pet()
        else:
            pet.update()
            pet.draw()


            # EXP bar i przyciski jak wcześniej...

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pet and player_name:
                    pet.save(player_name)
                if event.key == pygame.K_m:
                    main_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos


                if pet is None:
                    if 50 <= x <= 250 and 400 <= y <= 450:
                        pet = Pet("Squirtle")
                    elif 270 <= x <= 470 and 400 <= y <= 450:
                        pet = Pet("Charmander")
                    elif 490 <= x <= 690 and 400 <= y <= 450:
                        pet = Pet("Bulbasaur")
                elif 60 <= x <= 260 and 500 <= y <= 550:
                    pet.feed()
                    pet.gain_experience()
                elif 290 <= x <= 490 and 500 <= y <= 550:
                    pet.play()
                    pet.gain_experience()
                elif 520 <= x <= 720 and 500 <= y <= 550:
                    pet.sleep()
                    pet.gain_experience()
                elif 520 <= x <= 720 and 100 <= y <= 150:
                    pet.save(player_name)

        pygame.display.update()


# Uruchomienie gry
main_menu()