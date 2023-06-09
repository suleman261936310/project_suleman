# suleman romail
# comp 111 C
#261936310

#projec

import pygame
from os import path
import time
import random

pygame.font.init()

width=700
height=700
win= pygame.display.set_mode((width,height))
pygame.display.set_caption("Space Invading Game")

#loading images
img_dir = path.join(path.dirname(__file__), 'SULEMAN GAME')


aes3 = pygame.image.load(path.join(img_dir, "asteroid.png")).convert()
aes2 = pygame.image.load(path.join(img_dir, "meteorite.png")).convert()
enemy_spaceship = pygame.image.load(path.join(img_dir, "pixel_ship_green_small.png")).convert()
player_spaceship = pygame.image.load(path.join(img_dir, "playerShip1.png")).convert()
laser_light = pygame.image.load(path.join(img_dir, "pixel_laser_blue.png")).convert()
bg = pygame.transform.scale(pygame.image.load(path.join(img_dir, "background.png")).convert(),(width,height))

class Laser: #laser used to destroy
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self,window):
        window.blit(self.img,(self.x,self.y))

    def move(self,vel):
        self.y += vel

    def off_screen(self,height):
        return not(self.y <= height and self.y >=0)
    
    def collision(self,obj):
        return collide(self,obj)
        

class Ship: #parent class for player amd enemyship
    COOLDOWN = 30
    
    def __init__(self,x,y,health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0 #letting the ship cool before laser

    def draw(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y,50,50))
        window.blit(self.ship_img,(self.x,self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self,vel,obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
            
            

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
        


    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y,self.laser_img)  #composition laser obj in ship class
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
            

    def get_width(self):
        return self.ship_img.get_width()  #so that ship doesnt goes out of screen
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship): #inherits from ship class
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = player_spaceship
        self.laser_img = laser_light
        self.mask = pygame.mask.from_surface(self.ship_img) #this mask tells where pixels are in image
        self.max_health = health

    def move_lasers(self,vel,objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    def draw(self,window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y + self.ship_img.get_height()+10,self.ship_img.get_width(),10))
        pygame.draw.rect(window,(0,255,0),(self.x,self.y + self.ship_img.get_height()+10,self.ship_img.get_width()*((self.health)/self.max_health),10))
            
            


class Enemy(Ship):  #enemy ship
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = enemy_spaceship
        self.laser_img = laser_light
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20,self.y,self.laser_img)  #composition laser obj in enemy class
            self.lasers.append(laser)
            self.cool_down_counter = 1
            

class Asteroid(Ship): #aesteroid class
    SIZE_MAP = {
        "big": (aes3),
        "medium":(aes2)
        }
    def __init__(self,x,y,size,health=100):
        super().__init__(x,y)
        self.ship_img = self.SIZE_MAP[size]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self,vel):
        self.y += vel

        
def collide(obj1,obj2):
    offset_x = obj2.x - obj1.x
    offset_y= obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) != None


#main
def main():
    run = True
    FPS = 60
    level = 0
    lives = 10
    main_font = pygame.font.SysFont('arial',20) #will use this font to draw
    lost_font = pygame.font.SysFont('arial',40)


    enemies = []
    wave_length = 1
    enemy_vel = 4

    asteroids = []
    wave_length_aes = 1
    aes_vel = 4
    
    laser_vel = 5
    
    player_vel = 5

    player=Player(300,600) #making object of player 

    
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    
    def redraw_window(): #will redraw everytime loops run
        win.blit(bg,(0,0)) #drawing the bg image on the screen
        #draw text
        lives_label = main_font.render(f"Lives: {lives}",1,(255,255,255))
        level_label = main_font.render(f"Level: {level}",1,(255,255,255))

        win.blit(lives_label,(10,10))
        win.blit(level_label,(width - level_label.get_width()-10,10))

        for enemy in enemies: #drawing enemies on screen
            enemy.draw(win)

        for asteroid in asteroids: #drawing aesteroids
            asteroid.draw(win)
        
        player.draw(win) #the ship object is drawn

        if lost:  # display the losing message
            lost_label = lost_font.render("You Lost!",1,(255,255,255))
            win.blit(lost_label,(width/2 - lost_label.get_width()/2,350))            

        
        pygame.display.update()
    

    while run:
        clock.tick(FPS)
        redraw_window()
        

        if lives <= 0 or player.health<=0: #to make sure the games stops when lives or health is zero
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS *3:  #will quit the game if lost
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_length += 3   #increasing enemy after every level and spawning them
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50,width-100),random.randrange(-1500,-100))
                enemies.append(enemy)
        if len(asteroids) == 0:
            level += 1
            wave_length_aes += 3   #increasing aesteroids after every level and spawning them
            for i in range(wave_length_aes):
                asteroid = Asteroid(random.randrange(50,width-100),random.randrange(-1500,-100),random.choice(["big","medium"]))
                asteroids.append(asteroid)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # making keys and making sure not to go off the screen
        keys = pygame.key.get_pressed() #returns pressed key
        if keys[pygame.K_LEFT] and player.x - player_vel > 0: #moves left
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < width: #moves right
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0: #moves
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15< height: #moves down 
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:   #enemy will move
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel,player)
            if random.randrange(0,2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            
            elif enemy.y + enemy.get_height() > height: #to make sure the live decreases
                lives -= 1
                enemies.remove(enemy)

        for asteroid in asteroids:   #aesteroid will move
            asteroid.move(enemy_vel)  
            if asteroid.y + asteroid.get_height() > height: #to make sure the live decreases
                lives -= 1
                asteroids.remove(asteroid)

            
      

        player.move_lasers(-laser_vel, enemies) #players will use laser and check that laser has collide with enemies
        player.move_lasers(-laser_vel, asteroids)

def main_menu():
    title_font = pygame.font.SysFont("arial",70)
    run = True
    while run:

        
        pygame.display.update()        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()


            
main()



main_menu()
