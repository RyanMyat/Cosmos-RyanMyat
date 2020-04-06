'''
PROJECT COSMOS
Ryan Myat
Mar 13, 2020
'''

# Import Libraries 
import pygame
import math
from math import pi

# -------- Main Function -------- #

def main():
   
   # Initialize Game
   pygame.init()

   screen = pygame.display.set_mode((800,600))

   pygame.display.set_caption(" C O S M O S ")

   clock = pygame.time.Clock()

   # Variables
   done = False
   life = 3
   shoot = False
   draw_laser = False
   
   # Lists
   keys = [False, False, False, False]
   lasers = []

   # Load And Set Up Graphics
   space = pygame.image.load("Images/background.png")
   
   spaceship = pygame.image.load("Images/spaceship.png")
   player_rect = spaceship.get_rect()
   player_rect.center = (400,300)

   life_ship = pygame.image.load("Images/player_life1.png")
   life_x = pygame.image.load("Images/player_life2.png")

   zero = pygame.image.load("Images/number_0.png")
   one = pygame.image.load("Images/number_1.png")
   two = pygame.image.load("Images/number_2.png")
   three = pygame.image.load("Images/number_3.png")

   laser = pygame.image.load("Images/laser.png")
   laser_rect = laser.get_rect()

   # Load Sounds
   laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")
   
   
   # -------- Main Program Loop -------- #
   
   while not done:

      for event in pygame.event.get():
         
         # User Clicks Quit
         if event.type == pygame.QUIT:
            done = True

         # User Presses Down On A Key
         elif event.type == pygame.KEYDOWN:             
            if event.key == pygame.K_w:
               keys[0] = True
            elif event.key == pygame.K_a:
               keys[1] = True
            elif event.key == pygame.K_s:
               keys[2] = True
            elif event.key == pygame.K_d:
               keys[3] = True
               
         # User Lets Up On A Key      
         elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
               keys[0] = False
            elif event.key == pygame.K_a:
               keys[1] = False
            elif event.key == pygame.K_s:
               keys[2] = False
            elif event.key == pygame.K_d:
               keys[3] = False

         # User Presses Down On Mouse
         elif event.type == pygame.MOUSEBUTTONDOWN:
            laser_sound.play()
            cursor = pygame.mouse.get_pos()
            lasers.append([math.atan2(cursor[1]-(player_pos[1]+30), cursor[0]-(player_pos[0]+30)), player_pos[0]+26, player_pos[1]+27])
            
      # -------- Game Logic -------- #

      # Move Player
      if keys[0] == True:
         player_rect.top -= 1
      elif keys[2] == True:
         player_rect.bottom += 1
      if keys[1] == True:
         player_rect.left -= 1
      elif keys[3] == True:
         player_rect.right += 1

      # Rotate Player
      cursor = pygame.mouse.get_pos()
      angle = math.atan2(cursor[1]-player_rect.centery, cursor[0]-player_rect.centerx) 
      player_rot = pygame.transform.rotate(spaceship, 270-(angle*180/pi))
      player_pos = (player_rect.centerx-player_rot.get_rect().centerx, player_rect.centery-player_rot.get_rect().centery)

      # Screen Wrap 
      if player_rect.left < -60:
         player_rect.left = 800
      elif player_rect.right > 860:
         player_rect.right = 0
      if player_rect.top < -60:
         player_rect.top = 600
      elif player_rect.bottom > 660:
         player_rect.bottom = 0

      # Shoot Lasers      
      if shoot == True:

         for i in lasers:
            i[1] += math.cos(i[0])*5
            i[2] += math.sin(i[0])*5
            for j in lasers:
               laser1 = pygame.transform.rotate(laser, 270-(j[0]*(180/pi)))
               draw_laser = True

      # -------- Drawing Code -------- #

      # Background 
      screen.blit(space, [0,0])

      # Lasers
      if draw_laser == True:
         screen.blit(laser1, (j[1], j[2]))
      
      # Player 
      screen.blit(player_rot, player_pos)

      # Life 
      screen.blit(life_ship, [45,45])
      screen.blit(life_x, [75,45])

      if life == 3:
         screen.blit(three, [98,45])
      elif life == 2:
         screen.blit(two, [98,45])
      elif life == 1:
         screen.blit(one, [98,45])
      else:
         screen.blit(zero, [98,45])
      
      # Update Screen
      pygame.display.flip()

      # Limit Frames Per Second
      clock.tick(60)

   # Close Window And Quit
   pygame.quit()

if __name__=='__main__':    
    main()
          
          

