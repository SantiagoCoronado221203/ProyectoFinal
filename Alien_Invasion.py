import sys
import pygame
import json
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
import random
from raindrop import Raindrop


class AlienInvasion:
    """Clase general para administrar los archivos y el comportamiento del juego."""

    def __init__(self):
        """Inicializar el juego y crear recursos del juego."""
        pygame.init()
        self.settings = Settings()

        # Configuración de pantalla completa con doble buffer para reducir parpadeo
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height        
        pygame.display.set_caption("Alien Invasion")

        # Cargar y redimensionar la imagen de fondo al tamaño de la pantalla
        self.background = pygame.image.load(r"imagenes/fondo.png") 
        self.background = pygame.transform.scale(
            self.background, (self.settings.screen_width, self.settings.screen_height)
        )
        
        #Crea el grupo de gotas de lluvia
        self.raindrops = pygame.sprite.Group ()
        
        # Crear otros elementos del juego
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        self.play_button = Button(self, "Play")
        self.restart_button = Button(self, "Reiniciar")
        
        #Estado Pausa
        self.paused = False

        # Límite de fotogramas
        self.clock = pygame.time.Clock()

    def run_game(self):
        """Inicial el bucle principal del juego"""
        while True:
            self._check_events()  # Verifica los eventos de entrada
            
            if self.stats.game_active and not self.paused:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_raindrops ()
            
            self._update_screen()  # Actualiza toda la pantalla una vez por ciclo
            self.clock.tick(60)  # Limita el bucle a 60 FPS para evitar parpadeo

    def _update_raindrops(self):
        """Actualiza la posicion de la gotas de lluvia y crea nuevas gotas"""
        #Crea una nueva gota aleatoriamente
        if random.randint(0,0) == 0:
            new_raindrop = Raindrop(self)
            self.raindrops.add(new_raindrop)
            
        #Actualizala psosiond de las gotas existentes
        self.raindrops.update()
        
        #Elimina las gotas que han desparecido de la pantalla
        for raindrop in self.raindrops.copy():
            if raindrop.check_disappeared():
                self.raindrops.remove(raindrop)   
    
    def _create_fleet(self):
        """Crear la flota de aliens"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = (available_space_y // (2 * alien_height))-1

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Crear un alien y colocarlo en la fila"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_events(self):
        """Responde a las pulsaciones de teclas y a los eventos del ratón"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
                    self._start_game()
                elif (self.paused or (not self.stats.game_active and self.stats.ships_left==0)) and self.restart_button.rect.collidepoint(mouse_pos):
                    self._start_game()
                    
    def _start_game(self):
        """Inicia un nuevo juego y restablece todos los recursos"""
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # Eliminar todos los aliens y balas, y crear una nueva flota
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()

        # Quitar la pausa si estaba activada y ocultar el cursor
        self.paused = False
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Responder a las pulsaciones de teclas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()  # Guardar al salir
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._toggle_pause()
        elif event.key == pygame.K_r:
            self._reset_high_score()
            
    def _reset_high_score(self):
        """Reinicia la puntuación máxima a 0"""
        self.stats.reset_high_score()
        self.sb.prep_high_score()  
            
    def _toggle_pause (self):
        """Aleternar el estado pausado"""
        self.paused = not self.paused
        if self.paused:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
            
        

    def _check_keyup_events(self, event):
        """Responder a las teclas liberadas"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Iniciar un nuevo juego cuando el jugador hace clic en 'Play'"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Eliminar aliens y balas, y crear una nueva flota
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Crear una nueva bala y añadirla al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Actualizar posición de las balas y eliminar las antiguas"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respuesta a las colisiones entre balas y aliens"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

            if self.stats.score > self.stats.high_score:
                self.stats.high_score = self.stats.score
                self.stats.save_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Actualizar posición de los aliens"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Responder si algún alien ha llegado al borde"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Mover flota y cambiar de dirección"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Responder cuando el barco es golpeado por un alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            self.paused = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Comprueba si algún alien ha llegado al fondo de la pantalla"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        """Actualizar imágenes y pasar a la nueva pantalla"""
        self.screen.blit(self.background, (0, 0))  # Dibujar el fondo

        #Dibujar la lluvia
        self.raindrops.draw (self.screen)
        
        # Dibujar nave, balas y aliens
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Mostrar marcador
        self.sb.show_score()

        # Mostrar botón si el juego está inactivo
        if not self.stats.game_active:
            #Mostrar game over si se han acabado los barcos
            if self.stats.ships_left == 0:
                self._show_game_over_and_restart_button()
            else:
                self.play_button.draw_button() 
            
        #Mostrar el mensaje de pausa y reiniciar
        elif self.paused:
            self._show_pause_message_and_restart_button()
            

        # Actualizar pantalla
        pygame.display.flip()
        
    def _show_pause_message_and_restart_button(self):
        """Dibuja un mensaje de pausa en la pantalla y boton de reinicio"""
        #Posision mensaje pausa
        pause_font = pygame.font.SysFont(None, 74)
        pause_text = pause_font.render ("PAUSA", True, (210,105,30))
        pause_rect = pause_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(pause_text, pause_rect)
        
        # Posicionar el botón "Reiniciar" debajo del mensaje "Pausa"
        self.restart_button.rect.centerx = self.screen.get_rect().centerx
        self.restart_button.rect.top = pause_rect.bottom + 20  # Espacio debajo de "Pausa"
        self.restart_button._prep_msg("Reiniciar")
        self.restart_button.draw_button()
        
        
    def _show_game_over_and_restart_button(self):
        """Muestra el mensaje Game Over en el centro de la pantalla y el botón 'Reiniciar' debajo"""
        # Dibuja el mensaje "Game Over" en el centro de la pantalla
        game_over_font = pygame.font.SysFont(None, 74)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 50))
        self.screen.blit(game_over_text, game_over_rect)

        # Posicionar el botón "Reiniciar" debajo del mensaje "Game Over"
        self.restart_button.rect.centerx = self.screen.get_rect().centerx
        self.restart_button.rect.top = game_over_rect.bottom + 20  # Espacio debajo del mensaje
        self.restart_button._prep_msg("Reiniciar")
        self.restart_button.draw_button()


if __name__ == "__main__":
    # Crear instancia de juego y ejecutarlo
    ai = AlienInvasion()
    ai.run_game()
