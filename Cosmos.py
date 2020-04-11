'''
PROJECT COSMOS
Ryan Myat
Mar 13, 2020
'''

# Import Libraries
import pygame
import math
from math import pi
import random

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

   # Timer
   ast_timer = 300
   num_time = 0
   
   # Lists
   keys = [False, False, False, False]
   lasers = []
   lasers_rot = []
   asteroids = []
   asteroids_rot = []

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

   asteroid1 = pygame.image.load("Images/asteroid_1.png")
   asteoid1_rect = asteroid1.get_rect()

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

      # Screen Wrap Player
      if player_rect.left < -60:
         player_rect.left = 800
      elif player_rect.right > 860:
         player_rect.right = 0
      if player_rect.top < -60:
         player_rect.top = 600
      elif player_rect.bottom > 660:
         player_rect.bottom = 0

      '''
      Dr. Adam, after I edited the code, the rotations of the lasers are inaccurate. I noticed how the first laser is
      always correct but other  lasers aren't. If you shoot antoher laser in the same direction as your first laser,
      it comes out right. Does this mean I have to reset the angle after the first time? If so, how do I reset it?
      '''
      
      # Shoot Lasers
      for i in range(len(lasers)):
         lasers[i][1] += math.cos(lasers[i][0])*5
         lasers[i][2] += math.sin(lasers[i][0])*5

         lasers_rot.append(pygame.transform.rotate(laser, 270-(lasers[i][0]*(180/pi))))

         if lasers[i][1] <= -20 or lasers[i][1] >= 820 or lasers[i][2] <= -20 or lasers[i][2] >= 620:
            del lasers[i]
            del lasers_rot[i]
            break

      '''
      I have managed to get asteroids to come out from the top of the screen. I plan on doing the same for the right,
      left, and bottom sides as well. I tried to rotate the asteroids at random angles but they all seem to come out
      the same. Should I rotate them?
      '''
      
      # Timer
      if life > 0:
         ast_timer -= 1
         
      # Asteroids Timer
      if ast_timer == 0:
         asteroids.append([random.randint(0,90), random.randint(0,800), -30], random.randrange(-1,3,2)])

         # Reset Timer
         ast_timer = 300 - (num_time*2)
         if num_time >= 30:
            num_time = 30
         else:
            num_time += 1
         
      # Move Asteroids
      for i in range(len(asteroids)):
         asteroids[i][1] += asteroids[i][3]
         asteroids[i][2] += 1

         asteroids_rot.append(pygame.transform.rotate(asteroid1, 270-asteroids[i][0]))
         
         if asteroids[i][1] <= -40 or asteroids[i][1] >= 840 or asteroids[i][2] <= -33 or asteroids[i][2] >= 633:
            del asteroids[i]
            break
         
         '''
         I think my collision code works now.
         '''
         
         # Collisions
         for j in range(len(lasers)):
            asteroid1rect=pygame.Rect(asteroid1.get_rect())
            asteroid1rect.left = asteroids[i][1]
            asteroid1rect.top = asteroids[i][2]
            laserrect=pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]

            if asteroid1rect.colliderect(laserrect):
               del asteroids[i]
               del lasers[j]
               del lasers_rot[j]
               break
               
      # -------- Drawing Code -------- #
                           
      # Background
      screen.blit(space, [0,0])
                           
      # Lasers
      for i in range(len(lasers)):
         screen.blit(lasers_rot[i], (lasers[i][1], lasers[i][2]))

      # Player
      screen.blit(player_rot, player_pos)

      # Asteroids
      for i in range(len(asteroids)):
         screen.blit(asteroids_rot[i], (asteroids[i][1], asteroids[i][2]))

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



