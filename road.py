import pygame


class Road(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def remove(self):
        if self.rect.top > 800:
            self.kill()

    def update(self):
        self.rect.y += 3
        self.remove()
