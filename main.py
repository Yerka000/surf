import random
import pygame
import pygame.freetype
from my_car import MyCar
from road import Road
from traffic import TrafficCar
from button import Button

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Set up the game window
screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption('Surfey Race')
background_color = (0, 0, 0)  # Black background

# Load sounds
my_car_sound = pygame.mixer.Sound('sounds/engine.wav')
crash_sound = pygame.mixer.Sound('sounds/crash.wav')

# Load font for text rendering
font = pygame.freetype.Font(None, 20)

# Create road sprite group
road_group = pygame.sprite.Group()
spawn_road_time = pygame.USEREVENT  # Custom event for spawning roads
pygame.time.set_timer(spawn_road_time, 1000)  # Trigger every second

# Create traffic car sprite group
traffic_cars_group = pygame.sprite.Group()
spawn_traffic_time = pygame.USEREVENT + 1  # Custom event for spawning traffic cars
pygame.time.set_timer(spawn_traffic_time, 1000)  # Trigger every second

# Load menu background image
menu_bg_image = pygame.image.load('images/surf.png')
menu_bg_image = pygame.transform.scale(menu_bg_image, (500, 800))


# Function to load and transform car images
def get_car_image(filename, size, angle):
    image = pygame.image.load(filename)
    image = pygame.transform.scale(image, size)
    image = pygame.transform.rotate(image, angle)
    return image


# Load player car image
my_car_image = get_car_image('images/mercedes.png', (100, 70), -90)

# Load road and game-over images
road_image = pygame.image.load('images/road.png')
road_image = pygame.transform.scale(road_image, (500, 800))

crashed_car_image = pygame.image.load('images/game over.png')
crashed_car_image = pygame.transform.scale(crashed_car_image, (500, 800))

# Load traffic car images
traffic_car_images = [
    get_car_image('images/traffic_car1.png', (100, 70), 90),
    get_car_image('images/traffic_car2.png', (100, 70), -90),
    get_car_image('images/traffic_car3.png', (100, 70), -90)
]

# Initialize road sprites
road = Road(road_image, (250, 400))
road_group.add(road)
road = Road(road_image, (250, 0))
road_group.add(road)

# Load high score from file
score = 0
try:
    with open('highscore.txt', 'r') as f:
        top_score = int(f.read())
except FileNotFoundError:
    top_score = 0  # Default high score if file doesn't exist


# Function to spawn new road segments
def spawn_road():
    road_bg = Road(road_image, (250, -600))  # Spawn above the screen
    road_group.add(road_bg)


# Function to spawn traffic cars at random positions
def spawn_traffic():
    position = (random.randint(40, 460), random.randint(-60, -40))  # Random position on road
    speed = random.randint(7, 20)  # Random speed
    traffic_car = TrafficCar(random.choice(traffic_car_images), position, speed, my_car)
    traffic_cars_group.add(traffic_car)


# Function to update and draw all objects
def draw_all():
    road_group.update()
    road_group.draw(screen)
    traffic_cars_group.update()
    traffic_cars_group.draw(screen)
    my_car.draw(screen)


# Button actions
def button_click_restart_action():
    global score
    traffic_cars_group.empty()
    my_car_sound.play(-1)
    my_car.game_status = 'game'
    score = 0  # Reset score


def button_click_start_action():
    global score
    my_car.game_status = 'game'
    score = 0  # Reset score
    my_car_sound.play(-1)


def button_click_main_menu_action():
    my_car.game_status = 'main_menu'


# Create buttons for UI
button_main_menu = Button(150, 300, 200, 50, "Main Menu",
                          36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_main_menu_action)

button = Button(150, 200, 200, 50, "Restart game",
                36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_restart_action)

button_start = Button(150, 200, 200, 50, "Start Game",
                      36, (255, 255, 255), (0, 0, 255), (0, 0, 128), button_click_start_action)

# Initialize player car
my_car = MyCar((300, 600), my_car_image)
my_car.game_status = 'main_menu'  # Start in main menu
running = True

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Quit game
        if event.type == spawn_road_time and my_car.game_status == 'game':
            spawn_road()  # Add new road
        if event.type == spawn_traffic_time and my_car.game_status == 'game':
            spawn_traffic()  # Add new traffic car
        button.handle_event(event)
        button_start.handle_event(event)
        button_main_menu.handle_event(event)

    # Fill screen with background color
    screen.fill(background_color)

    # Handle game states
    if my_car.game_status == 'game':
        my_car.move()
        draw_all()
        my_car.crash(crash_sound, traffic_cars_group)
        score += 1  # Increase score

    elif my_car.game_status == 'game_over':
        screen.blit(crashed_car_image, (0, 0))
        my_car_sound.stop()
        button.draw(screen)
        button_main_menu.draw(screen)
        if score > top_score:
            top_score = score
            with open('highscore.txt', 'w') as f:
                f.write(str(top_score))  # Save new high score

    elif my_car.game_status == 'main_menu':
        screen.blit(menu_bg_image, (0, 0))
        font.render_to(screen, (150, 100), "Surfey Race", (255, 255, 255))
        button_start.draw(screen)

    # Display score and balance
    font.render_to(screen, (20, 20), f'Score: {score}  Top Score: {top_score}', (255, 255, 255))
    font.render_to(screen, (20, 40), f'Balance: {my_car.balance}', (255, 255, 255))

    # Update screen
    pygame.display.flip()
    clock.tick(my_car.fps)  # Maintain FPS
