#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Importacion de los módulos
import pygame
from pygame.locals import *
import os
import sys

# ----------------------------------------------
# Constantes, como anchos y largo de pantalla, etc.
# ----------------------------------------------

SCREEN_WIDTH = 626
SCREEN_HEIGHT = 470
FULLSCREEN_WIDTH = 1500
FULLSCREEN_HEIGHT = 780
LINE_HEIGHT = 50
SCORE_LIMIT = 2
CUP_WIDTH = 182
CUP_HEIGHT = 193
IMG_DIR = "img"
SND_DIR = "snd"

# ----------------------------------------------
# Clases y Funciones utilizadas
# ----------------------------------------------

def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print("Error, no se puede cargar la imagen: " + ruta)
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (ej: png)
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def load_sound(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Intentar cargar el sonido
    try:
	    sonido = pygame.mixer.Sound(ruta)
    except (pygame.error) as message:
	    print ("No se pudo cargar el sonido:", ruta)
	    sonido = None
    return sonido

# ----------------------------------------------
# Sprites (clases) de los objetos del juego
# ----------------------------------------------

class Pelota(pygame.sprite.Sprite):
    "La bola y su comportamiento en la pantalla"
    
    def __init__(self):
	    pygame.sprite.Sprite.__init__(self)
	    self.image = load_image("bola.png", IMG_DIR, True)
	    self.rect = self.image.get_rect()
	    #self.rect.centerx = SCREEN_WIDTH/2
	    #self.rect.centery = SCREEN_HEIGHT/2
	    self.rect.centerx = FULLSCREEN_WIDTH/2
	    self.rect.centery = FULLSCREEN_HEIGHT/2
	    self.speed = [4, 3]

    def update(self, marcador, sonido_punto=None):
        """if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
	        self.speed[0] = -self.speed[0]
	        sonido_punto.play()
	        self.rect.centerx = SCREEN_WIDTH / 2
	        self.rect.centery = SCREEN_HEIGHT / 2
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]"""
        if self.rect.left < 0 or self.rect.right > FULLSCREEN_WIDTH:
	        self.speed[0] = -self.speed[0]
	        if self.rect.left < 0:
	           marcador.punto2()
	           self.speed[0] += 1
	           #punto del jugador 2
	        else:
	            marcador.punto1()
	            self.speed[0] += 1
			    #punto del jugador 1
	        sonido_punto.play()
	        self.rect.centerx = FULLSCREEN_WIDTH / 2 - 11
	        self.rect.centery = FULLSCREEN_HEIGHT / 2 - 11
        if self.rect.top < LINE_HEIGHT or self.rect.bottom > FULLSCREEN_HEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.move_ip((self.speed[0], self.speed[1]))
    
    def ganador(self):
	    x = load_image("cup.png", IMG_DIR, True)
	    self.image = pygame.transform.smoothscale(x, (CUP_WIDTH, CUP_HEIGHT))
	    self.rect.centerx = (FULLSCREEN_WIDTH - CUP_WIDTH)/2
	    self.rect.centery = (FULLSCREEN_HEIGHT - CUP_HEIGHT)/2
    
    def colision(self, objetivo, sonido_golpe=None):
	    if self.rect.colliderect(objetivo.rect):
		    self.speed[0] = -self.speed[0]
		    sonido_golpe.play()

class Marcador():
	def __init__(self):
		self.jugador1 = 0
		self.jugador2 = 0
		self.ganador = 0
	
	def punto1(self):
		self.jugador1 += 1
		if (self.jugador1 > SCORE_LIMIT-1):
			self.ganador = 1
			#El jugador 1 ganó
	
	def punto2(self):
		self.jugador2 += 1
		if (self.jugador2 > SCORE_LIMIT-1):
			self.ganador = 2
			#El jugador 2 ganó
			
class Paleta(pygame.sprite.Sprite):
    "Define el comportamiento de las paletas de ambos jugadores"
    
    def __init__(self, x, type=1):
	    pygame.sprite.Sprite.__init__(self)
	    if (type == 1):
	        self.image = load_image("paddle1.png", IMG_DIR, True)
	    else:
	        self.image = load_image("paddle2.png", IMG_DIR, True)
	    self.rect = self.image.get_rect()
	    self.rect.centerx = x
	    """self.rect.centery = SCREEN_HEIGHT/2"""
	    self.rect.centery = FULLSCREEN_HEIGHT/2

    def humano(self):
	    # control de que la paleta no salga de la pantalla
        """if self.rect.bottom >= SCREEN_HEIGHT:
	        self.rect.bottom = SCREEN_HEIGHT"""
        if self.rect.bottom >= FULLSCREEN_HEIGHT:
	        self.rect.bottom = FULLSCREEN_HEIGHT
        elif self.rect.top <= LINE_HEIGHT:
            self.rect.top = LINE_HEIGHT
    
    def cpu(self, pelota):
	    self.speed = [0, 3.3]
	    #if pelota.speed[0] >= 0 and pelota.rect.centerx >= SCREEN_WIDTH / 2:
	    if pelota.speed[0] >= 0 and pelota.rect.centerx >= FULLSCREEN_WIDTH / 2:
	        if self.rect.centery > pelota.rect.centery:
	            self.rect.centery -= self.speed[1]
	        if self.rect.centery < pelota.rect.centery:
	            self.rect.centery += self.speed[1]
		    
# ----------------------------------------------
# Funcion principal del juego
# ----------------------------------------------

def main():    
    # creamos la ventana y le indicamos un titulo:
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT), 0, 32)
    #screen = pygame.display.set_mode((1500, 780), pygame.FULLSCREEN)
    
    pygame.display.set_caption("Tutorial pygame - pong simple")
    
    fuente = pygame.font.Font(None, 45)
    
    # se cargan los objetos
    fondo = load_image("fondoPong1600.jpg", IMG_DIR)
    #fondo = pygame.transform.scale(f, (FULLSCREEN_WIDTH, FULLSCREEN_HEIGHT))
    bola = Pelota()
    marcador = Marcador()
    jugador1 = Paleta(25, type=1)
    #jugador2 = Paleta(SCREEN_WIDTH - 25)
    jugador2 = Paleta(FULLSCREEN_WIDTH - 25, type=2)
    sonido_golpe = load_sound("tennis.ogg", SND_DIR)
    sonido_punto = load_sound("aplausos.ogg", SND_DIR)
    
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 25) # Activa repeticion de teclas
    pygame.mouse.set_visible(False)
    
    # el bucle principal del juego
    while True:
	    clock.tick(60)
	    pos_mouse = pygame.mouse.get_pos()
	    mov_mouse = pygame.mouse.get_rel()
	    
	    jugador1.humano()
	    jugador2.cpu(bola)
	    bola.update(marcador, sonido_punto)
	    
	    bola.colision(jugador1,sonido_golpe)
	    bola.colision(jugador2,sonido_golpe)

	    for event in pygame.event.get():
	        if event.type == pygame.QUIT:
		        sys.exit(0)
	        elif event.type == pygame.KEYDOWN:
		        if event.key == K_w:
			        jugador1.rect.centery -= 8
		        elif event.key == K_s:
		            jugador1.rect.centery += 8
		        elif event.key == K_ESCAPE:
			        sys.exit(0)
	        #elif mov_mouse[1] != 0:
		        #jugador1.rect.centery = pos_mouse[1]
        
        # actualizar la pantalla
	    if marcador.ganador != 0:
		    texto = "Ganador: jugador %d" % (marcador.ganador)
		    desp = 135
		    bola.ganador()
	    else:
	        texto = "%d  |  %d" % (marcador.jugador1, marcador.jugador2)
	        desp = 42
	    
	    mensaje = fuente.render(texto, 1, (255, 255, 255))
	    
	    #pygame.draw.aaline(fondo, (191, 191, 191), (0, LINE_HEIGHT), (FULLSCREEN_WIDTH, LINE_HEIGHT))
	    pygame.draw.line(fondo, (191, 191, 191), (0, LINE_HEIGHT), (FULLSCREEN_WIDTH, LINE_HEIGHT), 4)
	    screen.blit(fondo, (0,0))
	    screen.blit(mensaje, (FULLSCREEN_WIDTH/2 - desp, 10))
	    screen.blit(bola.image, bola.rect)
	    screen.blit(jugador1.image, jugador1.rect)
	    screen.blit(jugador2.image, jugador2.rect)
	    pygame.display.flip()
	    
	    if marcador.ganador != 0:
	        while True:
	            for event in pygame.event.get():
	                if event.type == pygame.QUIT:
		                sys.exit(0)
	                elif event.type == pygame.KEYDOWN:
	                    if event.key == K_ESCAPE:
	                        sys.exit(0)

if __name__ == "__main__":
    pygame.init()
    main()
