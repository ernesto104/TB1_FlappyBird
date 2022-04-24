# For generating random height of pipes
import random  
import sys 
import pygame
import math
from pygame.locals import * 
import functions_game

def anilment(temperatura,factor_enfriamiento,limite_inferior,
             solucion_inicial,f_mutacion,f_practica,
window_width, game_images, elevation, window, framepersecond, framepersecond_clock, window_height
             ):
    sol_actual=solucion_inicial
    sol_mejor=solucion_inicial
    energia_mejor=f_practica(window_width, game_images, elevation, window, framepersecond, framepersecond_clock, window_height,sol_mejor)
    energia_actual=energia_mejor
    sol_nueva=None
    while True:
        sol_nueva=f_mutacion(sol_actual)
        energia_actual=f_practica(window_width, game_images, elevation, window, framepersecond, framepersecond_clock, window_height,sol_actual)
        energia_nueva=f_practica(window_width, game_images, elevation, window, framepersecond, framepersecond_clock, window_height,sol_nueva)
        if(energia_nueva<energia_actual):
            prob_cambio=1
        else:
             prob_cambio=math.exp((energia_actual-energia_nueva)/temperatura)
        if random.random()<= prob_cambio:
            sol_actual=sol_nueva
        if(energia_nueva<energia_actual):
            sol_mejor=sol_nueva
            energia_mejor=energia_nueva
        temperatura=temperatura*(1-factor_enfriamiento)
        if(temperatura<=limite_inferior):
            break;
    print(f"limites finales {sol_mejor[0]},{sol_mejor[1]}")
    return sol_mejor
def mutacion(limites):
        if(random.randint(0,1)):
                if(random.randint(0,1)):limites[0]=limites[0]+10
                else:limites[0]=limites[0]-10
        else:
                if(random.randint(0,1)):limites[1]=limites[1]+10
                else:limites[1]=limites[1]-10
        print(f"limites mutados {limites[0]},{limites[1]}")
        return limites

  
# Global Variables for the game
window_width = 600
window_height = 499
  
# set height and width of window
window = pygame.display.set_mode((window_width, window_height))   
elevation = window_height * 0.8
game_images = {}      
framepersecond = 32
pipeimage = 'images/pipe.png'
background_image = 'images/background.jpg'
birdplayer_image = 'images/bird.png'
sealevel_image = 'images/base.jfif'




# program where the game starts
if __name__ == "__main__":		
	
	# For initializing modules of pygame library
	pygame.init()
	framepersecond_clock = pygame.time.Clock()
	
	# Sets the title on top of game window
	pygame.display.set_caption('Flappy Bird Game')	

	# Load all the images which we will use in the game
	# images for displaying score
	game_images['scoreimages'] = (
		pygame.image.load('images/0.png').convert_alpha(),
		pygame.image.load('images/1.png').convert_alpha(),
		pygame.image.load('images/2.png').convert_alpha(),
		pygame.image.load('images/3.png').convert_alpha(),
		pygame.image.load('images/4.png').convert_alpha(),		
		pygame.image.load('images/5.png').convert_alpha(),
		pygame.image.load('images/6.png').convert_alpha(),
		pygame.image.load('images/7.png').convert_alpha(),
		pygame.image.load('images/8.png').convert_alpha(),
		pygame.image.load('images/9.png').convert_alpha()
	)
	game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()				
	game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
	game_images['background'] = pygame.image.load(background_image).convert_alpha()
	game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage)
														.convert_alpha(),
														180),
								pygame.image.load(pipeimage).convert_alpha())

	print("WELCOME TO THE FLAPPY BIRD GAME")
	print("Press space or enter to start the game")


#Parte 3
# iniciamos valores adivinados
asumimos=[30,-30]
energia=0

while True:

		# sets the coordinates of flappy bird
		horizontal = int(window_width/5)
		vertical = int((window_height - game_images['flappybird'].get_height())/2)
		
		# for selevel
		ground = 0
		while True:
			for event in pygame.event.get():

				# if user clicks on cross button, close the game
				if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
					pygame.quit()
					
					# Exit the program
					sys.exit()

				# If the user presses space or up key,
				# start the game for them
				elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
					print("entrenamiento")
					asumimos=anilment(1000,0.0003,0.0001,asumimos,mutacion,functions_game.flappygame,window_width, game_images, elevation, window,
                                                          framepersecond, framepersecond_clock, window_height)
					print("oficial:")
					functions_game.flappygame(window_width, game_images, elevation, window, framepersecond, framepersecond_clock, window_height,asumimos)
				
				# if user doesn't press anykey Nothing happen
				else:
					window.blit(game_images['background'], (0, 0))
					window.blit(game_images['flappybird'], (horizontal, vertical))
					window.blit(game_images['sea_level'], (ground, elevation))
					
					# Just Refresh the screen
					pygame.display.update()		
					
					# set the rate of frame per second
					framepersecond_clock.tick(framepersecond)





