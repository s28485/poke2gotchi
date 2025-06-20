"""
A module used for a Pet class
"""
import json
import Button
import pygame

# Kolory
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
VIOLET = (73, 19, 99)

width, height = 800, 600

pygame.init()
pygame.mixer.init()

evolution_lines = {
    'Bulbasaur': ['Bulbasaur', 'Ivysaur', 'Venusaur'],
    'Squirtle': ['Squirtle', 'Wartortle', 'Blastoise'],
    'Charmander': ['Charmander', 'Charmeleon', 'Charizard'],
    'Pikachu': ['Pikachu', 'Raichu', 'AlolanRaichu']
}

font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((width, height))


class Pet:
    """
    A class that represents a pet
    """
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
        self.hunger_increment_interval: int = 100
        self.happiness_increment_interval: int = 100
        self.sleepness_increment_interval: int = 300

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

        self.save_button = Button.Button(
            520, 100, 200, 50,
            text="SAVE",
            color=VIOLET,
            hover_color=(37, 10, 49),
            command=self.save
        )


    def save(self, player_name) -> None:
        """
        A method used for saving a pet into a json file
        :param player_name: Name of a player
        :return: None
        """
        data = {
            "name": self.name,
            "hunger": self.hunger,
            "happiness": self.happiness,
            "sleepiness": self.sleepiness,
            "level": self.level,
            "experience": self.experience
        }
        with open(f"saves/{player_name}.json", "w", encoding='utf-8') as f:
            json.dump(data, f)
        print("Gra zapisana!")


    def level_up(self) -> None:
        """
        A method used for leveling up the pet
        :return: None
        """
        self.level += 1
        if self.level in {25, 50}:
            self.evolve()
        self.experience = 0

    def gain_experience(self) -> None:
        """
        A method used for gaining experience
        :return: None
        """
        self.experience += 1
        if self.experience >= self.max_experience:
            self.level_up()

    def get_experience(self) -> int:
        """
        Getter for pets experience
        :return: A pets experience
        """
        return self.experience

    def evolve(self) -> None:
        """
        A method for evolving the pet
        :return: None
        """
        self.evolution_stage += 1
        self.name = evolution_lines[self.evolution_line][self.evolution_stage]
        self.load_image()

    def feed(self) -> None:
        """
        A method for feeding the pet
        :return: None
        """
        self.hunger = max(self.hunger + 10, 0)

    def play(self) -> None:
        """
        A method for playing with the pet
        :return: None
        """
        self.happiness = min(self.happiness + 10, 100)
        # self.sleepiness = min(self.sleepiness + 20, 100)

    def sleep(self) -> None:
        """
        A method for putting a pet to sleep
        :return: None
        """
        self.sleepiness = max(self.sleepiness + 10, 0)

    def update(self) -> bool:
        """
        A method for updating pets stats
        :return: True if all stats below zero, false otherwise
        """

        if self.hunger <= 0 and self.happiness <= 0 and self.sleepiness <= 0:
            return True

        # For test purposes
        if self.hunger < 50 and self.happiness < 50 and self.sleepiness < 50:
            self.gain_experience()

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

        return False

    def draw(self) -> None:
        """
        A method for drawing the pet
        :return: None
        """
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
        self.save_button.draw(screen)

        options_text = font.render(
            "Press \'q\' to quit game, or \'m\' to enter main menu",
            True,
            (94, 94, 94)
        )
        screen.blit(options_text, (125, 570))

    def load_image(self) -> None:
        """
        A method for loading pets image upon load
        :return: None
        """
        self.image = pygame.transform.scale(
            pygame.image.load(f'assets/{self.name.lower()}.png'),
            (200, 200)
        )
