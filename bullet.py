import pygame
from pygame.sprite import Sprite


class Bullet (Sprite):
    """Una clase para manejar las balas disparadas desde la nave"""
    
    def __init__ (self, ai_game):
        """Crea un obejto de bala en la posición actual de la nave"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        #Cargar una imagen para las balas
        self.image = pygame.image.load(r"imagenes/bala.bmp")        
        self.rect = self.image.get_rect()
        
        #Cree una rectangulo de viñeta en (0,0) y luego estabnlezca la posicion correcta
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #Almacena la psición de la viñeta como un valor decimal.
        self.y = float(self.rect.y)
    
    def update (self):
        """Mueve la bala hacia arriba de la pantalla"""
        #Actualiza la posición de la bala.
        self.y -= self.settings.bullet_speed
        #Actualiza la posicón recta
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Dibuja la bala hacia la pantalla"""
        self.screen.blit (self.image, self.rect)