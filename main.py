import random
import pygame
import pygame.freetype
from my_car import MyCar
from road import Road
from traffic import TrafficCar
from button import Button
from difficulty import get_difficulty_settings  # Импортируем настройки сложности

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption('Surfey Race')
background_color = (0, 0, 0)

my_car_sound = pygame.mixer.Sound('sounds/engine.wav')
my_car_sound.play(-1)

crash_sound = pygame.mixer.Sound('sounds/crash.wav')

font = pygame.freetype.Font(None, 20)

road_group = pygame.sprite.Group()
spawn_road_time = pygame.USEREVENT
pygame.time.set_timer(spawn_road_time, 1000)

traffic_cars_group = pygame.sprite.Group()
spawn_traffic_time = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_traffic_time, 1000)

def get_car_image(filename, size, angle):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)
    return image

my_car_image = get_car_image('images/mercedes.png', (100, 70), -90)
road_image = pygame.image.load('images/road.png')
road_image = pygame.transform.scale(road_image, (500, 800))
crashed_car_image = pygame.image.load('images/crashed_mercedes.jpg')
crashed_car_image = pygame.transform.scale(crashed_car_image, (500, 800))

traffic_car_images = [
    get_car_image('images/traffic_car1.png', (100, 70), 90),
    get_car_image('images/traffic_car2.png', (100, 70), -90),
    get_car_image('images/traffic_car3.png', (100, 70), -90)
]

road = Road(road_image, (250, 400))
road_group.add(road)
road = Road(road_image, (250, 0))
road_group.add(road)

score = 0
try:
    with open('highscore.txt', 'r') as f:
        top_score = int(f.read())
except FileNotFoundError:
    top_score = 0

def spawn_road():
    road_bg = Road(road_image, (250, -600))
    road_group.add(road_bg)

def spawn_traffic():
    settings = get_difficulty_settings(difficulty)  # Получаем настройки сложности
    position = (random.randint(40, 460), random.randint(-60, -40))
    speed = random.randint(*settings['traffic_speed_range'])  # Используем настройки
    traffic_car = TrafficCar(random.choice(traffic_car_images), position, speed, my_car)
    traffic_cars_group.add(traffic_car)
    pygame.time.set_timer(spawn_traffic_time, settings['spawn_interval'])  # Устанавливаем интервал

def draw_all():
    road_group.update()
    road_group.draw(screen)
    traffic_cars_group.update()
    traffic_cars_group.draw(screen)
    my_car.draw(screen)

def button_click_restart_action():
    global score
    traffic_cars_group.empty()
    my_car_sound.play(-1)
    my_car.game_status = 'game'
    score = 0

def button_click_repair_action():
    global score
    if my_car.balance < 30:
        return
    my_car.balance -= 30
    traffic_cars_group.empty()
    my_car_sound.play(-1)
    my_car.game_status = 'game'
    score = 0

def button_click_start_action():
    my_car.game_status = 'difficulty_select'  # Переход к выбору сложности

def button_click_easy_action():
    global difficulty
    difficulty = 'easy'
    my_car.game_status = 'game'  # Начинаем игру после выбора сложности

def button_click_medium_action():
    global difficulty
    difficulty = 'medium'
    my_car.game_status = 'game'  # Начинаем игру после выбора сложности

def button_click_hard_action():
    global difficulty
    difficulty = 'hard'
    my_car.game_status = 'game'  # Начинаем игру после выбора сложности

button = Button(150, 200, 200, 50, "Restart game",
                36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_restart_action)

button_repair = Button(0, 500, 500, 50, "Repair car and restart",
                       36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_repair_action)

button_start = Button(150, 200, 200, 50, "Start Game",
                      36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_start_action)

button_easy = Button(150, 200, 200, 50, "Easy",
                     36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_easy_action)

button_medium = Button(150, 300, 200, 50, "Medium",
                       36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_medium_action)

button_hard = Button(150, 400, 200, 50, "Hard",
                     36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_hard_action)

my_car = MyCar((300, 600), my_car_image)
difficulty = 'easy'
my_car.game_status = 'main_menu'  # Начинаем с главного меню
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_road_time:
            spawn_road()
        if event.type == spawn_traffic_time:
            spawn_traffic()
        button.handle_event(event)
        button_repair.handle_event(event)
        button_start.handle_event(event)
        button_easy.handle_event(event)  # Обработка событий для кнопки Easy
        button_medium.handle_event(event)  # Обработка событий для кнопки Medium
        button_hard.handle_event(event)  # Обработка событий для кнопки Hard

    screen.fill(background_color)
    if my_car.game_status == 'game':
        my_car.move()
        draw_all()
        my_car.crash(crash_sound, traffic_cars_group)
        score += 1
    elif my_car.game_status == 'game_over':
        screen.blit(crashed_car_image, (0, 0))
        my_car_sound.stop()
        button.draw(screen)
        button_repair.draw(screen)
        if score > top_score:
            top_score = score
            with open('highscore.txt', 'w') as f:
                f.write(str(top_score))
    elif my_car.game_status == 'difficulty_select':
        screen.fill((50, 50, 50))
        font.render_to(screen, (150, 100), "Select Difficulty Level", (255, 255, 255))
        button_easy.draw(screen)
        button_medium.draw(screen)
        button_hard.draw(screen)
    elif my_car.game_status == 'main_menu':
        screen.fill((50, 50, 50))
        font.render_to(screen, (150, 100), "Surfey Race", (255, 255, 255))
        button_start.draw(screen)

    font.render_to(screen, (20, 20), f'Score: {score}  Top Score: {top_score}', (255, 255, 255), (0, 0, 0))
    font.render_to(screen, (20, 40), f'Balance: {my_car.balance}', (255, 255, 255), (0, 0, 0))
    pygame.display.flip()
    clock.tick(my_car.fps)