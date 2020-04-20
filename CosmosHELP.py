'''
Chapter 11
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
   game_over = False
   speed = 1
   laser_speed = 6
   life = 3
   score = 0
   
   # Timer
   ast1_timer = 325
   ast1_num = 0
   ast2_timer = 350
   ast2_num = 0
   ast3_timer = 380
   ast3_num = 0
   ast4_timer = 365
   ast4_num = 0
   bolt_timer = 3000
   bolt_erase = 0
   acc_timer = 0
   
   # Lists
   keys = [False, False, False, False]
   lasers = []
   lasers_rot = []
   asteroids1 = []
   asteroids2 = []
   asteroids3 = []
   asteroids4 = []
   explode = []
   bolt_pos = []
   
   # Load And Set Up Graphics
   space = pygame.image.load("Images/background.png")
   spaceship = pygame.image.load("Images/spaceship.png")
   player_rect = spaceship.get_rect()
   player_rect.center = (400,300)
   laser = pygame.image.load("Images/laser.png")
   laser_rect = laser.get_rect()
   laser_rect.center = (400,300)
   asteroid1_image = pygame.image.load("Images/asteroid_1.png")
   asteroid2_image = pygame.image.load("Images/asteroid_2.png")
   asteroid3_image = pygame.image.load("Images/asteroid_3.png")
   explosion_image = pygame.image.load("Images/asteriod_exploded.png")
   asteroid4_image = pygame.image.load("Images/asteroid_4.png")
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
            if game_over == False:
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

      # The problem is in the shoot laser code.  lasers_rot.append(...)
      # you don't want to keep appending to lasers_rot every time you move the laser.
      # this list will get very long quickly.
      # just set lasers_rot[i] = pygame.transform.rotate..
      
      # Shoot Lasers
      for i in range(len(lasers)):
         lasers[i][1] += math.cos(lasers[i][0])*laser_speed
         lasers[i][2] += math.sin(lasers[i][0])*laser_speed
         lasers_rot.append(pygame.transform.rotate(laser, 270-(lasers[i][0]*(180/pi))))
         
         #lasers_rot[i] = pygame.transform.rotate(laser, 270-(lasers[i][0]*(180/pi)))
          
         
         '''

         Dr. Adam, it says IndexError: list assignment index out of range for lasers_rot[i] = pygame.transform.rotate(laser, 270-(lasers[i][0]*(180/pi))) 
         Please help me. I do not know how to fix this.
         
         '''

         '''
         Dr. Adam, I tried playing around with lasers_rot = pygame.transform.rotate(laser, 270-(lasers[i][0]*(180/pi)))
         when I do that, the later laser comes out correct but the ones before change rotation as well
         it seems like all lasers will go in one and same direction
         I am confused.
         '''
         
         if lasers[i][1] <= -20 or lasers[i][1] >= 820 or lasers[i][2] <= -20 or lasers[i][2] >= 620:
            del lasers[i]
            del lasers_rot[i]
            break
      
      # Timer 
      if life > 0:
         ast1_timer -= 1
         ast2_timer -= 1
         ast3_timer -= 1
         ast4_timer -= 1
         bolt_timer -= 1
         bolt_erase -= 1
         acc_timer -= 1
      
      # Asteroids Timer 1
      if ast1_timer == 0:
         asteroids1.append([random.randint(0,800), 630, random.randrange(-1,2,2), random.randint(-3,0)])

         # Reset Timer 1
         ast1_timer = 325-(ast1_num*2)
         if ast1_num >= 125:
            ast1_num = 125
         else:
            ast1_num += 1

      # Asteroids Timer 2
      if ast2_timer == 0:
         asteroids2.append([800, random.randint(0,600), random.randint(-4,-2), random.randrange(-1,2,2)])

         # Reset Timer 2
         ast2_timer = 350-(ast2_num*3)
         if ast2_num >= 100:
            ast2_num = 100
         else:
            ast2_num += 1

      # Asteroids Timer 3
      if ast3_timer == 0:
         asteroids3.append([random.randint(0,800), -44, random.randrange(-1,2,2), 2])

         # Reset Timer 3
         ast3_timer = 380-(ast3_num*3)
         if ast3_num >= 90:
            ast3_num = 90
         else:
            ast3_num += 1

      # Asteroids Timer 4
      if ast4_timer == 0:
         asteroids4.append([-32, random.randint(0,600), random.randint(1,4), random.randrange(-1,2,2)])

         # Reset Timer 3
         ast4_timer = 340-(ast4_num*2)
         if ast4_num >= 130:
            ast4_num = 130
         else:
            ast4_num += 1
      
      # Move Asteroids 1
      for i in range(len(asteroids1)):

         '''
         asteroids1[i][0] += asteroids1[i][2] and asteroids1[i][1] += asteroids1[i][3] gets out of range sometimes
         it also happens sometimes to asteroids2, 3, and explode lists
         please help
         '''
         # Oh I see, it is probably happening when you delete asteroids1.  You need to break out of the for loop when you 
         # do otherwise it will go out of range.  For example, line 286.  Also at line 294 it is a nested loop
         # so the break statement will exit out of only one loop.


         """
         Dr. Adam, I already added break's after I delete elements from the lists for asteroids. Am I missing any breaks?
         Or is it because of something else?
         """

         
         asteroids1[i][0] += asteroids1[i][2]
         asteroids1[i][1] += asteroids1[i][3]
         
         if asteroids1[i][0] <= -40 or asteroids1[i][0] >= 840 or asteroids1[i][1] <= -33 or asteroids1[i][1] >= 633:
            del asteroids1[i]
            break
            
         # Collisions 1
         asteroid1rect = pygame.Rect(asteroid1_image.get_rect())
         asteroid1rect.left = asteroids1[i][0]
         asteroid1rect.top = asteroids1[i][1]
         
         playerrect = pygame.Rect(spaceship.get_rect())
         playerrect.left = player_pos[0]
         playerrect.top = player_pos[1]
         
         if asteroid1rect.colliderect(playerrect):
            death_sound.play()
            del asteroids1[i]
            player_rect.center = (400,300)
            life -= 1
            break
         
         # Hits 1
         for j in range(len(lasers)):
            
            laserrect = pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]
            
            if asteroid1rect.colliderect(laserrect):
               explosion_sound.play()
               score += 15
               del asteroids1[i]
               del lasers[j]
               del lasers_rot[j]
               break         
      
      # Move Asteroids 2
      for i in range(len(asteroids2)):

         asteroids2[i][0] += asteroids2[i][2]
         asteroids2[i][1] += asteroids2[i][3]
         
         if asteroids2[i][0] <= -25 or asteroids2[i][0] >= 825 or asteroids2[i][1] <= -22 or asteroids2[i][1] >= 622:
            del asteroids2[i]
            break
         
         # Collisions 2
         asteroid2rect = pygame.Rect(asteroid2_image.get_rect())
         asteroid2rect.left = asteroids2[i][0]
         asteroid2rect.top = asteroids2[i][1]
         
         if asteroid2rect.colliderect(playerrect):
            death_sound.play()
            del asteroids2[i]
            player_rect.center = (400,300)
            life -= 1
            break
         
         # Hits 2
         for j in range(len(lasers)):
            
            laserrect = pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]
            
            if asteroid2rect.colliderect(laserrect):
               explosion_sound.play()
               score += 20
               del asteroids2[i]
               del lasers[j]
               del lasers_rot[j]
               break

      # Move Asteroids 3
      for i in range(len(asteroids3)):

         asteroids3[i][0] += asteroids3[i][2]
         asteroids3[i][1] += asteroids3[i][3]
         
         if asteroids3[i][0] <= -54 or asteroids3[i][0] >= 854 or asteroids3[i][1] <= -45 or asteroids3[i][1] >= 644:
            del asteroids3[i]
            break
         
         # Collisions 3
         asteroid3rect = pygame.Rect(asteroid3_image.get_rect())
         asteroid3rect.left = asteroids3[i][0]
         asteroid3rect.top = asteroids3[i][1]
         
         if asteroid3rect.colliderect(playerrect):
            death_sound.play()
            del asteroids3[i]
            player_rect.center = (400,300)
            life -= 1
            break
         
         # Hits 3
         for j in range(len(lasers)):
            
            laserrect = pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]
            
            if asteroid3rect.colliderect(laserrect):
               explosion_sound.play()
               score += 5
               del asteroids3[i]
               del lasers[j]
               del lasers_rot[j]
               explode.append([laserrect.left, laserrect.top, random.randint(-3,0), random.randrange(-1,2,2)])
               explode.append([laserrect.left, laserrect.top, random.randint(1,4), random.randrange(-1,2,2)])
               break

      # Move Asteroids 4
      for i in range(len(asteroids4)):

         asteroids4[i][0] += asteroids4[i][2]
         asteroids4[i][1] += asteroids4[i][3]
         
         if asteroids4[i][0] <= -33 or asteroids4[i][0] >= 832 or asteroids4[i][1] <= -29 or asteroids4[i][1] >= 629:
            del asteroids4[i]
            break
         
         # Collisions 4
         asteroid4rect = pygame.Rect(asteroid4_image.get_rect())
         asteroid4rect.left = asteroids4[i][0]
         asteroid4rect.top = asteroids4[i][1]
         
         if asteroid4rect.colliderect(playerrect):
            death_sound.play()
            del asteroids4[i]
            player_rect.center = (400,300)
            life -= 1
            break
         
         # Hits 2
         for j in range(len(lasers)):
            
            laserrect = pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]
            
            if asteroid4rect.colliderect(laserrect):
               explosion_sound.play()
               score += 10
               del asteroids4[i]
               del lasers[j]
               del lasers_rot[j]
               break
            
      # Explosion
      for i in range(len(explode)):

         explode[i][0] += explode[i][2]
         explode[i][1] += explode[i][3]
         
         if explode[i][0] <= -25 or explode[i][0] >= 825 or explode[i][1] <= -22 or explode[i][1] >= 622:
            del explode[i]
            break

         # Exploded Collisions 
         explosionrect = pygame.Rect(explosion_image.get_rect())
         explosionrect.left = explode[i][0]
         explosionrect.top = explode[i][1]
         
         if explosionrect.colliderect(playerrect):
            death_sound.play()
            del explode[i]
            player_rect.center = (400,300)
            life -= 1
            break
         
         # Hits 2
         for j in range(len(lasers)):
            
            laserrect = pygame.Rect(laser.get_rect())
            laserrect.left = lasers[j][1]
            laserrect.top = lasers[j][2]
            
            if explosionrect.colliderect(laserrect):
               explosion_sound.play()
               score += 25
               del explode[i]
               del lasers[j]
               del lasers_rot[j]
               break

      # Bolt Timer
      if bolt_timer == 0:
         bolt_pos.append([random.randint(50,736), random.randint(38,537)])
         bolt_timer = 2300
         bolt_erase = 375

      if bolt_erase == 0:
         bolt_pos = []

      # Collect Bolt
      for i in range(len(bolt_pos)):
         boltrect = pygame.Rect(bolt.get_rect())
         boltrect.left = bolt_pos[i][0]
         boltrect.top = bolt_pos[i][1]

         if playerrect.colliderect(boltrect):
            bolt_sound.play()
            acc_timer = 535
            del bolt_pos[i]
         
      # Acceleration Timer
      if acc_timer > 0:
         speed = 2
         laser_speed = 7
      else:
         speed = 1
         laser_speed = 6

      # Game Over
      if life == 0:
         game_over = True
         
      # -------- Drawing Code -------- #
                           
      # Background
      screen.blit(space, [0,0])
                           
      # Lasers
      if game_over == False:
         for i in range(len(lasers)):
            screen.blit(lasers_rot[i], (lasers[i][1], lasers[i][2]))

      # Player
      if game_over == False:
         screen.blit(player_rot, player_pos)

      # Asteroids 1
      for i in range(len(asteroids1)):
         screen.blit(asteroid1_image, (asteroids1[i][0], asteroids1[i][1]))

      # Asteroids 2
      for i in range(len(asteroids2)):
         screen.blit(asteroid2_image, (asteroids2[i][0], asteroids2[i][1]))

      # Asteroids 3
      for i in range(len(asteroids3)):
         screen.blit(asteroid3_image, (asteroids3[i][0], asteroids3[i][1]))

      # Asteroids 4
      for i in range(len(asteroids4)):
         screen.blit(asteroid4_image, (asteroids4[i][0], asteroids4[i][1]))
         
      # Explosions
      for i in range(len(explode)):
         screen.blit(explosion_image, (explode[i][0], explode[i][1]))

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

##      # Game Over
##      if game_over == True:
##         screen.blit()
         
      # Update Screen
      pygame.display.flip()

      # Limit Frames Per Second
      clock.tick(60)

   # Close Window And Quit
   pygame.quit()

if __name__=='__main__':
    main()
