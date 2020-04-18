'''
PROJECT COSMOS
Ryan Myat
Mar 13, 2020
'''

# Import Libraries
import pygame, math, random
from pygame.locals import *
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
   speed = 1
   life = 3
   score = 0
   
   # Timer
   ast1_timer = 275
   ast1_num = 0
   ast2_timer = 290
   ast2_num = 0
   bolt_timer = 2000
   bolt_erase = 0
   acc_timer = 0
   
   # Lists
   keys = [False, False, False, False]
   lasers = []
   lasers_rot = []
   asteroids1 = []
   asteroids1_rot = []
   asteroids2 = []
   asteroids2_rot = []

   bolt_pos = []
   
   # Load And Set Up Graphics
   space = pygame.image.load("Images/background.png")
   spaceship = pygame.image.load("Images/spaceship.png")
   player_rect = spaceship.get_rect()
   player_rect.center = (400,300)
   laser = pygame.image.load("Images/laser.png")
   laser_rect = laser.get_rect()
   laser_rect.center = (400,300)
   asteroid1 = pygame.image.load("Images/asteroid_1.png")
   asteroid2 = pygame.image.load("Images/asteroid_2.png")

   bolt = pygame.image.load("Images/bolt.png")   

   life_ship = pygame.image.load("Images/player_life1.png")
   life_x = pygame.image.load("Images/player_life2.png")
   zero = pygame.image.load("Images/number_0.png")
   one = pygame.image.load("Images/number_1.png")
   two = pygame.image.load("Images/number_2.png")
   three = pygame.image.load("Images/number_3.png")

   # Load Sounds
   laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")
   explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
   death_sound = pygame.mixer.Sound("Sounds/death.ogg")
   bolt_sound = pygame.mixer.Sound("Sounds/ping.ogg")

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
         player_rect.top -= speed
      elif keys[2] == True:
         player_rect.bottom += speed
      if keys[1] == True:
         player_rect.left -= speed
      elif keys[3] == True:
         player_rect.right += speed

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
      always accurate but other lasers aren't. If you shoot another laser in the same direction as your first laser,
      it comes out right again. Does this mean I have to reset the angle after the first time? If so, how do I reset it?
      '''
      
      # Shoot Lasers
      for i in range(len(lasers)):
         lasers[i][1] += math.cos(lasers[i][0])*6
         lasers[i][2] += math.sin(lasers[i][0])*6

         lasers_rot.append(pygame.transform.rotate(laser, 270-(lasers[i][0]*(180/pi))))

         if lasers[i][1] <= -20 or lasers[i][1] >= 820 or lasers[i][2] <= -20 or lasers[i][2] >= 620:
            del lasers[i]
            del lasers_rot[i]
            break
      
      # Timer 1
      if life > 0:
         ast1_timer -= 1
         ast2_timer -= 1
         bolt_timer -= 1
         bolt_erase -= 1
         acc_timer -= 1
      
      '''
      I have managed to get asteroids to come out from the top of the screen. I plan on doing the same for the right,
      left, and bottom sides as well. I tried to rotate the asteroids at random angles but they all seem to come out
      with the same rotation. Do you think I should rotate them? If so, how can I fix this?
      '''
         
      # Asteroids Timer 1
      if ast1_timer == 0:
         asteroids1.append([random.randrange(0,360), random.randint(0,800), -30, random.randrange(-1,2,2), random.randint(1,3)])

         # Reset Timer 1
         ast1_timer = 275-(ast1_num*2)
         if ast1_num >= 95:
            ast1_num = 95
         else:
            ast1_num += 1

      # Asteroids Timer 2
      if ast2_timer == 0:
         asteroids2.append([random.randrange(0,360), 800, random.randint(0,600), random.randint(-4,-2), random.randrange(-1,2,2)])

         # Reset Timer 2
         ast2_timer = 300-(ast2_num*3)
         if ast2_num >= 73:
            ast2_num = 73
         else:
            ast2_num += 1
         
      # Move Asteroids 1
      for i in range(len(asteroids1)):

         '''
         Dr. Adam, asteroids[i][1] += asteroids[i][3] goes out of range. I did asteroids[i][1] += asteroids[i][3] 
         so that the asteroids come out in random directions. I do not understand how the code can get out of range.
         Can you help me?
         '''
         
         asteroids1[i][1] += asteroids1[i][3]
         asteroids1[i][2] += asteroids1[i][4]

         asteroids1_rot.append(pygame.transform.rotate(asteroid1, asteroids1[i][0]))
         
         if asteroids1[i][1] <= -40 or asteroids1[i][1] >= 840 or asteroids1[i][2] <= -33 or asteroids1[i][2] >= 633:
            del asteroids1[i]
            del asteroids1_rot[i]
            break
            
         # Collisions 1
         asteroid1rect = pygame.Rect(asteroid1.get_rect())
         asteroid1rect.left = asteroids1[i][1]
         asteroid1rect.top = asteroids1[i][2]
         
         playerrect = pygame.Rect(spaceship.get_rect())
         playerrect.left = player_pos[0]
         playerrect.top = player_pos[1]
         
         if asteroid1rect.colliderect(playerrect):
            death_sound.play()
            del asteroids1[i]
            del asteroids1_rot[i]
            player_rect.center = (400,300)
            life -= 1
         
         # Hits 1
         for j in range(len(lasers)):
            
            laserrect = pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]
            
            if asteroid1rect.colliderect(laserrect):
               explosion_sound.play()
               score += 20
               del asteroids1[i]
               del asteroids1_rot[i]
               del lasers[j]
               del lasers_rot[j]
               break

      # Move Asteroids 2
      for i in range(len(asteroids2)):

         asteroids2[i][1] += asteroids2[i][3]
         asteroids2[i][2] += asteroids2[i][4]

         asteroids2_rot.append(pygame.transform.rotate(asteroid2, asteroids2[i][0]))
         
         if asteroids2[i][1] <= -25 or asteroids2[i][1] >= 825 or asteroids2[i][2] <= -22 or asteroids2[i][2] >= 622:
            del asteroids2[i]
            del asteroids2_rot[i]
            break

         # Collisions 2
         asteroid2rect = pygame.Rect(asteroid2.get_rect())
         asteroid2rect.left = asteroids2[i][1]
         asteroid2rect.top = asteroids2[i][2]
         
         if asteroid2rect.colliderect(playerrect):
            death_sound.play()
            del asteroids2[i]
            del asteroids2_rot[i]
            player_rect.center = (400,300)
            life -= 1
         
         # Hits 2
         for j in range(len(lasers)):
            
            laserrect = pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]
            
            if asteroid2rect.colliderect(laserrect):
               explosion_sound.play()
               score += 25
               del asteroids2[i]
               del asteroids2_rot[i]
               del lasers[j]
               del lasers_rot[j]
               break

      # Bolt Timer
      if bolt_timer == 0:
         bolt_pos.append([random.randint(50,736), random.randint(38,537)])
         bolt_timer = 1575
         bolt_erase = 350

      if bolt_erase == 0:
         bolt_pos = []

      # Collect Bolt
      for i in range(len(bolt_pos)):
         boltrect = pygame.Rect(bolt.get_rect())
         boltrect.left = bolt_pos[i][0]
         boltrect.top = bolt_pos[i][1]

         if playerrect.colliderect(boltrect):
            bolt_sound.play()
            acc_timer = 525
            del bolt_pos[i]

      # Acceleration Timer
      if acc_timer > 0:
         speed = 2
      else:
         speed = 1
      # add a life every certain points
      # Game Over
      if life == 0:
         done = True

      # -------- Drawing Code -------- #
                           
      # Background
      screen.blit(space, [0,0])
                           
      # Lasers
      for i in range(len(lasers)):
         screen.blit(lasers_rot[i], (lasers[i][1], lasers[i][2]))

      # Player
      screen.blit(player_rot, player_pos)

      # Asteroids 1
      for i in range(len(asteroids1)):
         screen.blit(asteroids1_rot[i], (asteroids1[i][1], asteroids1[i][2]))

      # Asteroids 2
      for i in range(len(asteroids2)):
         screen.blit(asteroids2_rot[i], (asteroids2[i][1], asteroids2[i][2]))

      # Bolt
      for i in range(len(bolt_pos)):
         screen.blit(bolt, (bolt_pos[i][0], bolt_pos[i][1]))
      
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
