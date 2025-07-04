"""
Module used for pygame initialization
"""
import sys
import json
import os
import pygame
import Pet
import Button

if not os.path.exists("saves"):
    os.makedirs("saves")


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

font = pygame.font.SysFont(None, 36)

# Obrazki do wyboru pokemona i skalowanie do odpowiednich rozmiarów
squirtle_image = pygame.transform.scale(pygame.image.load("assets/squirtle.png"), (200, 200))
charmander_image = pygame.transform.scale(pygame.image.load("assets/charmander.png"), (200, 200))
bulbasaur_image = pygame.transform.scale(pygame.image.load("assets/bulbasaur.png"), (200, 200))
pikachu_image = pygame.transform.scale(pygame.image.load("assets/pikachu.png"), (200, 200))

def load(player_name) -> Pet:
    """
    Overrides a method from PyGame library
    :param player_name: Name of the player
    :return: A pet object loaded from json data
    """
    with open(f"saves/{player_name}.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    pet = Pet.Pet(data["name"])
    pet.hunger = data["hunger"]
    pet.happiness = data["happiness"]
    pet.sleepiness = data["sleepiness"]
    pet.level = data["level"]
    pet.experience = data["experience"]
    return pet

# Funkcja, która rysuje menu wyboru zwierzaka
def choose_pet() -> Pet:
    """
    A function that displays available pets and lets player choose from them
    :return: A chosen pet object
    """
    screen.fill(BLACK)
    title_text = font.render("Wybierz swojego pokemona!", True, WHITE)
    screen.blit(title_text, (250, 50))

    buttons = [
        Button.Button(50, 400, 200, 50, "Squirtle", BLUE, (0, 0, 150)),
        Button.Button(270, 400, 200, 50, "Charmander", RED, (150, 0, 0)),
        Button.Button(490, 400, 200, 50, "Bulbasaur", GREEN, (0, 150, 0))
    ]

    screen.blit(squirtle_image, (50, 190))
    screen.blit(charmander_image, (270, 190))
    screen.blit(bulbasaur_image, (490, 190))

    clicked_button = None
    while not clicked_button:
        for b in buttons:
            b.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_button = next(button for button in buttons if button.is_pressed(event.pos))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return Pet.Pet('Pikachu')
            pygame.display.update()
    return Pet.Pet(clicked_button.text)

def player_select_menu() -> None:
    """
    A function that displays a player selection menu
    :return: None
    """
    while True:
        screen.fill(BLACK)
        title = font.render("Wybierz gracza", True, WHITE)
        screen.blit(title, (300, 50))

        files = [f[:-5] for f in os.listdir("saves") if f.endswith(".json")]

        buttons = [
            Button.Button(300, 120 + len(files) * 60, 200, 50, 'Nowy Gracz', GREEN, (0, 150, 0))
        ]

        # Lista graczy
        for i, name in enumerate(files):
            buttons.append(Button.Button(300, 120 + i * 60, 200, 50, name, BLUE, (0, 0, 150)))

        for button in buttons:
            button.draw(screen)

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
                    game_loop(choose_pet(), name)
                    return


# Nowy gracz - okno do wpisania nazwy
def get_user_name() -> str:
    """
    A function that displays the text field where user can type his name
    :return: new player name
    """
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
                if event.key == pygame.K_RETURN:
                    return user_text
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, input_rec, 1)
        text_surface = font.render(user_text, True, (255, 255, 255))
        screen.blit(font.render("Podaj imię gracza: ", True, WHITE), (20, 140))
        screen.blit(text_surface, (input_rec.x + 5, input_rec.y + 5))
        input_rec.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
        clock.tick(60)


def main_menu() -> None:
    """
    Function that displays the main menu.
    :return: None
    """
    while True:
        screen.fill(BLACK)
        screen.blit(font.render("Pokegotchi", True, WHITE), (330, 100))

        buttons = [
            Button.Button(300, 250, 200, 50, "Zagraj", GREEN, (0, 150, 0)),
            Button.Button(300, 350, 200, 50, "Wyjdź", RED, (75, 0, 0))
        ]

        for button in buttons:
            button.draw(screen)

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

                if 500 >= x >= 400 >= y >= 250:
                    pygame.quit()
                    sys.exit()


def game_loop(pet=None, player_name=None) -> None:
    """
    Function which runs the game loop
    :param pet: object of chosen pet
    :param player_name: name of a player
    :return: None
    """
    running = True
    lost = False
    while running:
        screen.fill(BLACK)

        if not lost:
            pet.update()
            pet.draw()
        else:
            lost_text = font.render(f'{player_name}, you\'ve lost', True, WHITE)
            options_text = font.render("Press \'q\' to quit game, or \'m\' to enter main menu",
                                       True,
                                       (94, 94, 94))
            lost_rect = lost_text.get_rect(center=(width // 2, height // 2))
            screen.blit(lost_text, lost_rect)
            screen.blit(options_text, (125, 570))

        lost = pet.update()

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
            if event.type == pygame.MOUSEBUTTONDOWN and not lost:
                x, y = event.pos

                if 60 <= x <= 260 and 500 <= y <= 550:
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

main_menu()
