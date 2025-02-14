import pygame.sprite

class TrafficCar(pygame.sprite.Sprite):
    def __init__(self, image, position, speed, my_car):
        super().__init__()
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.my_car = my_car

    def remove(self):
        if self.rect.top > 800:
            self.kill()
            self.my_car.balance +=5

    def update(self):
        self.rect.y += self.speed
        self.remove()
