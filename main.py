from sys import set_coroutine_origin_tracking_depth

import pygame
import sys
import json
import os

import Button

if not os.path.exists("saves"):
    os.makedirs("saves")
import Pet

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

# @staticmethod
def load(player_name) -> Pet:
    """
    Overrides a method from PyGame library
    :param player_name: string
    :return: Pet
    """
    with open(f"saves/{player_name}.json", "r") as f:
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



    # Jeżeli nie dokonamy wyboru w ciągu 5 minut, zostanie przypisany pikatchu
    # if time_elapsed > 5 * 60 * 60:
    #     pass
    #     # screen.blit(pikachu_image, (270, 190))
    #     # pygame.draw.rect(screen, VIOLET, (270, 400, 200, 50))
    #     # pikachu_text = font.render("Pikachu", True, WHITE)
    #     # screen.blit(pikachu_text, (275, 415))
    # else:
    #     pass
    #     # Przycisk 1: Squirtle
    #     # screen.blit(squirtle_image, (50, 190))
    #     # pygame.draw.rect(screen, BLUE, (50, 400, 200, 50))
    #     # squirtle_text = font.render("Squirtle", True, WHITE)
    #     # screen.blit(squirtle_text, (55, 415))
    #
    #     # # Przycisk 2: Charmander
    #     # screen.blit(charmander_image, (270, 190))
    #     # pygame.draw.rect(screen, RED, (270, 400, 200, 50))
    #     # cat_text = font.render("Charmander", True, WHITE)
    #     # screen.blit(cat_text, (275, 415))
    #     #
    #     # # Przycisk 3: Bulbasaur
    #     # screen.blit(bulbasaur_image, (490, 190))
    #     # pygame.draw.rect(screen, GREEN, (490, 400, 200, 50))
    #     # cat_text = font.render("Bulbasaur", True, WHITE)
    #     # screen.blit(cat_text, (495, 415))




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
                    game_loop(choose_pet(), name)
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


                # if pet is None:
                #     if 50 <= x <= 250 and 400 <= y <= 450:
                #         pet = Pet.Pet("Squirtle")
                #     elif 270 <= x <= 470 and 400 <= y <= 450:
                #         pet = Pet.Pet("Charmander")
                #     elif 490 <= x <= 690 and 400 <= y <= 450:
                #         pet = Pet.Pet("Bulbasaur")
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


# Uruchomienie gry
main_menu()