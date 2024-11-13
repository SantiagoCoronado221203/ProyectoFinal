import pygame.font

class Button:
    
    def __init__(self, ai_game, msg):
        """Inicializar atributos del boton"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #Establecer las dimensiones y propiedades del boton.
        self.width, self.height = 200,50
        self.button_color = (210,105,30)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Construir el boton y centrarlo.
        self.rect = pygame.Rect (0,0,self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #El mensaje delñ boton debe prepararse una sola vez.
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """convierte el mensaje en una imagen renderizada y centra el texto en el bonton"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button (self):
        """Dibujar el boton en blanco y luego dibujar el mensaje"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)