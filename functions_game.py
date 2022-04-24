import sys 
import pygame
import random  
from pygame.locals import * 

#Parte 4 
def createPipe(window_height, window_width,game_images):
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()
      
    # generating random height of pipes
    y2 = offset + random.randrange(
      60, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))  
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        
        # upper Pipe
        {'x': pipeX, 'y': -y1},
        
          # lower Pipe
        {'x': pipeX, 'y': y2}  
    ]
    return pipe



	#Parte 5
def isGameOver(horizontal, vertical, up_pipes, down_pipes, elevation, game_images):
    if vertical > elevation - 25 or vertical < 0: 
        return True
  
    # Checking if bird hits the upper pipe or not
    for pipe in up_pipes:    
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] 
           and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
            
    # Checking if bird hits the lower pipe or not
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False







	#Parte 6
def flappygame(window_width, game_images, elevation, window, framepersecond, framepersecond_clock, window_height,asumpciones):
	your_score = 0
	horizontal = int(window_width/5)
	vertical = int(window_height/2)
	ground = 0
	mytempheight = 100

	# Generating two pipes for blitting on window
	first_pipe = createPipe(window_height,window_width, game_images)
	second_pipe = createPipe(window_height, window_width, game_images)
	third_pipe = createPipe(window_height, window_width, game_images)

	# List containing lower pipes
	down_pipes = [
		{'x': window_width+300,
		'y': first_pipe[1]['y']},
		{'x': window_width+300+(window_width/3),
		'y': second_pipe[1]['y']},
		{'x': window_width+300+(window_width/3)*2,
		'y': third_pipe[1]['y']},
	]

	# List Containing upper pipes
	up_pipes = [
		{'x': window_width+300,
		'y': first_pipe[0]['y']},
		{'x': window_width+300+(window_width/3),
		'y': second_pipe[0]['y']},
		{'x': window_width+300+(window_width/3)*2,
		'y': third_pipe[0]['y']},
	]

	pipeVelX = 4 #pipe velocity along x

	bird_velocity_y = -9 # bird velocity
	bird_Max_Vel_Y = 10
	bird_Min_Vel_Y = -8
	birdAccY = 1
	
	# velocity while flapping
	bird_flap_velocity = -8
	
	# It is true only when the bird is flapping
	bird_flapped = False
	while True:
		# Handling the key pressing events
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			
			if ((event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP))):
				if vertical > 0:
					bird_velocity_y = bird_flap_velocity
					bird_flapped = True
		
		if (vertical>up_pipes[0]['y']+ game_images['pipeimage'][0].get_height()+asumpciones[0] and vertical>asumpciones[1]+down_pipes[0]['y']):
			bird_velocity_y = bird_flap_velocity
			bird_flapped = True
		# This function will return true if the flappybird is crashed
		game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes, elevation, game_images)
		if game_over:
			return your_score

		# check for your_score
		playerMidPos = horizontal + game_images['flappybird'].get_width()/2
		for pipe in up_pipes:
			pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
			if pipeMidPos <= playerMidPos < pipeMidPos + 4:
				# Printing the score
				your_score += 1

		if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
			bird_velocity_y += birdAccY

		if bird_flapped:
			bird_flapped = False
		playerHeight = game_images['flappybird'].get_height()
		vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

		# move pipes to the left
		for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
			upperPipe['x'] -= pipeVelX
			lowerPipe['x'] -= pipeVelX

		# Add a new pipe when the first is about
		# to cross the leftmost part of the screen
		if 0 < up_pipes[0]['x'] < 30:
			newpipe = createPipe(window_height, window_width,game_images)
			up_pipes.append(newpipe[0])
			down_pipes.append(newpipe[1])
			up_pipes.pop(0)
			down_pipes.pop(0)

		# Lets blit our game images now
		window.blit(game_images['background'], (0, 0))
		for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
			window.blit(game_images['pipeimage'][0],
						(upperPipe['x'], upperPipe['y']))
			window.blit(game_images['pipeimage'][1],
						(lowerPipe['x'], lowerPipe['y']))

		window.blit(game_images['sea_level'], (ground, elevation))
		window.blit(game_images['flappybird'], (horizontal, vertical))
		
		# Fetching the digits of score.
		numbers = [int(x) for x in list(str(your_score))]
		width = 0
		
		# finding the width of score images from numbers.
		for num in numbers:
			width += game_images['scoreimages'][num].get_width()
		Xoffset = (window_width - width)/1.1
		
		# Blitting the images on the window.
		for num in numbers:
			window.blit(game_images['scoreimages'][num], (Xoffset, window_width*0.02))
			Xoffset += game_images['scoreimages'][num].get_width()
			
		# Refreshing the game window and displaying the score.
		pygame.display.update()
		
		# Set the framepersecond
		framepersecond_clock.tick(framepersecond)
