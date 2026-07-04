"""
Hi, in this game you are the bee, who has to collect flowers to power your beehive. If you fail the beehive dies :(. How long can YOU survive? 
#blue flowers give you invincibility for (5) seconds if you collect one and then press b
#orange flowers give you a speed boost for (5) seconds if you collect one and press o 
#yellow flowers allow you to kill the next bird that sucessfuly collides with you. (happens automatically no button needed)



"""
#settings
#setup
import pygame as pg 
import random
import math 
pg.init() 
#variables and stuff to set stuff up
win = False 
birds = []
level = 1 
goal = 4
bpressed = False 
running = True 
height = 800
addedflower = False 
orange_activate = False 
blueflower_collected = False 
width = 1100
clock = pg.time.Clock() 
power_time = 0 
opower_time = 0 
display_score = 0 
frame = 0 
birdmax_speed = 3.5
birdmin_speed = 1 
goldflower_spawn = False  
opressed = False 
blue_activate = False 
blueflower_spawn = False 
orangeflower_spawn = False 
orangeflower_collected = False 

score = 0 
wait_time = 1
win_screen_time = 0 
bird_death = False 
goldflower_collected = False 
birdcount = 1 
num_flowers = 3 
font = pg.font.SysFont("arial",36)
screen = pg.display.set_mode((width,height))
pg.display.set_caption('bee')

#set up imgs
def generate_filenames(name,count):
    return [f"{name}{i}.png" for i in range(1,count+1) ]

def load_images(groups,size=(150,150)): 
    loaded = {} 
    for key, file_list in groups.items(): 
        loaded[key] = [] 
        for file in file_list : 
            img = pg.image.load(file).convert_alpha()
            img = pg.transform.scale(img,size)
            loaded[key].append(img)
    return loaded 

image_groups = {
    "bee": generate_filenames("bee", 3),
    "beeflip":generate_filenames("beeflip",3),
    "flower": generate_filenames("flower", 3),
    "beestart":generate_filenames("beestart",4),
    "beehive": generate_filenames("beehive", 4),
    "flowerbubble": generate_filenames("flowerbubble", 4),
    "WinScreen":generate_filenames("WinScreen",7),
    "blueflowerbubble":generate_filenames("blueflowerbubble",4),
    "orangeflowerbubble":generate_filenames("orangeflowerbubble",4),
    "goldflowerbubble":generate_filenames("goldflowerbubble",4)
}
bird_group = {
    "bird": generate_filenames("bird", 5),
    "birdflip":generate_filenames("birdflip",5),
}
win_group = {"WinScreen":generate_filenames("WinScreen",7)}
images = load_images(image_groups)
bird_images = load_images(bird_group,(190,190))
win_images = load_images(win_group,(800,800))
blueflower = images["blueflowerbubble"]
goldflower = images["goldflowerbubble"]
orangeflower = images["orangeflowerbubble"]
bee = images["bee"]
beeflip = images["beeflip"]
start = {"beestart" : generate_filenames("beestart",4)}
beestart2 = load_images(start,(600,600))
beestartscreen = beestart2["beestart"]
flower = images["flower"]
bird = bird_images["bird"]
birdflip = bird_images["birdflip"]
beehive = images["beehive"]
flowerbubble = images["flowerbubble"]
win_screen = win_images["WinScreen"]

#flower display images for scoreboard
orangeflowerD = pg.image.load('orangeflower.png').convert_alpha()
orangeflowerD = pg.transform.scale(orangeflowerD,(150,150))
goldflowerD = pg.image.load('goldflower.png').convert_alpha()
goldflowerD = pg.transform.scale(goldflowerD,(150,150))
blueflowerD = pg.image.load('blueflower.png').convert_alpha()
blueflowerD = pg.transform.scale(blueflowerD,(150,150))

#Parent class 
class Object(pg.sprite.Sprite): 
    def __init__ (self,pos,sprite): 
        self.pos = list(pos)
        self.sprite = sprite 
        self.frame = 0 
        self.animation_speed = 0.2 
        
    def update_animation(self,speed=0.2): 
        self.frame += speed 
    
    def draw(self,screen): 
        img = self.sprite[int(self.frame)%len(self.sprite)]
        screen.blit(img,self.pos)


class Player(Object): 
    
    def __init__(self,pos,sprite): 
        super().__init__(pos,sprite)

        self.vel = [0,0]
        self.acceleration = 0.5 
        self.friction = 0.9 
        self.max_speed = 6.5 
    def update(self,screen): 
        global blue_activate
        global bpower_seconds 
        global opower_seconds
        global power_time 
        global opower_time
        global orange_activate
        global seconds 
        global bpressed 
        global opressed 
        global blueflower_collected
        global orangeflower_collected
        self.draw(screen)
        self.frame = self.frame % len(self.sprite)
        keys = pg.key.get_pressed() 
        self.rect = bee[int(self.frame)].get_rect(topleft=self.pos)
        self.mask = pg.mask.from_surface(bee[int(self.frame)])
        if keys[pg.K_a] and self.pos[0] > -5:
            
            self.sprite = beeflip
            self.vel[0] -= self.acceleration
        if keys[pg.K_d]and self.pos[0]< 965:
            self.sprite = bee 
            self.vel[0] += self.acceleration
        if keys[pg.K_w] and self.pos[1] >0: 
            self.vel[1] -= self.acceleration 
        if keys[pg.K_s] and self.pos[1]<680: 
            self.vel[1] += self.acceleration 
        if keys[pg.K_b] and blueflower_collected:
            power_time = seconds + 5
            blue_activate = True 
            bpower_seconds = seconds
            bpressed = True 
        if keys[pg.K_t] and orangeflower_collected:
            opower_time = seconds + 5 
            self.max_speed = 10
            self.acceleration = 1 
            opower_seconds = seconds
            orange_activate = True 
            opressed = True 
            print('Orange key pressed, activate orange flower',self.max_speed)
            
      
        self.vel[0] = max(-self.max_speed, min(self.max_speed, self.vel[0]))
        self.vel[1] = max(-self.max_speed, min(self.max_speed, self.vel[1]))

        self.vel[0] *= self.friction 
        self.vel[1] *= self.friction 

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.frame += self.animation_speed 



class Bird(Object): 
    def __init__ (self,pos,sprite):
        global birdmax_speed 
        global birdmin_speed
        super().__init__(pos,sprite)
        self.vel = [0,0]
        self.acceleration = 0.5 
        self.friction = 0.9 
        self.max_speed = random.uniform(birdmin_speed,birdmax_speed) 
        self.animation_speed = 0.05 

    def update(self,screen): 
        self.update_animation() 
        self.draw(screen) 
        distancex = player.pos[0]-self.pos[0]
        distancey = player.pos[1]-self.pos[1]
        if distancex <= 0: 
            self.sprite = bird 
            self.vel[0] -= self.acceleration
        else: 
            self.sprite = birdflip
            self.vel[0] += self.acceleration
        if distancey <= 0: 
            self.vel[1] -= self.acceleration 
        else: 
            self.vel[1] += self.acceleration 
        
        
        self.vel[0] = max(-self.max_speed, min(self.max_speed, self.vel[0]))
        self.vel[1] = max(-self.max_speed, min(self.max_speed, self.vel[1]))

        self.vel[0] *= self.friction 
        self.vel[1] *= self.friction 

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.frame += self.animation_speed 

    def collide(self):
        global bird_death  
        global goldflower_collected 
        global running 
        self.frame = self.frame % len(self.sprite)
        self.rect = bird[int(self.frame)].get_rect(topleft=self.pos)
        self.mask = pg.mask.from_surface(bird[int(self.frame)])
        
        if pg.sprite.collide_mask(player,self): 
            if bird_death == True : 
                birds.remove(self)   
                bird_death = False 
                goldflower_collected = False 
            else: 
                
                running = False 
    def bird_collide(self):
        min_distance = 60 
        for b in birds:
            if b is self: 
                continue 

            dx = self.pos[0]-b.pos[0]
            dy = self.pos[1] - b.pos[1]
            distance = (dx**2 + dy**2) ** 0.5

            if distance < min_distance: 
                if distance == 0 : 
                    dx = random.choice(-1,1)
                    dy = random.choice(-1,1)
                    distance = (dx**2 + dy**2) ** 0.5

                movex = (dx/distance)*1.5
                movey = (dy/distance)*1.5

                self.pos[0]+=movex
                self.pos[1]+=movey
                b.pos[0]-=movex
                b.pos[1]-=movey
    
class Flower(Object): 
    def __init__ (self,pos,sprite,color='pink'):
        super().__init__(pos,sprite)
        self.sprite = flowerbubble
        self.frame_index = 0
        self.pos = [random.randint(60,width-100), random.randint(60,height-100)]
        self.color = color 
        self.last_update = pg.time.get_ticks()
        self.animation_delay = 750 

    def update(self): 
        self.draw(screen)
        self.update_animation()
        self.frame = self.frame % len(self.sprite)
        self.rect = flowerbubble[int(self.frame)].get_rect(topleft=self.pos)
        self.mask = pg.mask.from_surface(flowerbubble[int(self.frame)])
        
    def collide(self): 
        global score 
        global display_score 
        global win_screen_time
        global win 
        global seconds 
        global goal 
        global bird_death 
        global orangeflower_collected
        global level 
        global orangeflower_spawn 
        global goldflower_spawn
        global goldflower_collected 
        global addedflower 
        global blueflower_collected
        global blueflower_spawn 
        global birdmax_speed
        global birdmin_speed
        if score == goal: 
            if level%5==0: 
                player.max_speed += 1
            if level%6 == 0: 
                print('BIRDLEVELUP')
                birdmax_speed += 1
                birdmin_speed += 0.5
                for b in birds : 
                    b.max_speed += 0.3
            score = 0 
            win = True 
            win_screen_time = seconds + 2.5
            level += 1 
            addedflower = False 
            goal += 1
            create_birdies()
        if level%5==0 and not addedflower:
            flower = Flower([0,0],flowerbubble)
            Flowers.append(flower)  
            addedflower = True

        if display_score != 0: 
            if display_score%20 ==0 or display_score == 5: 
                goldflower_spawn = True 
            if display_score%10 == 0: 
                blueflower_spawn = True 
                
            if display_score%15 == 0:
                orangeflower_spawn = True 
        if pg.sprite.collide_mask(player,self):
            
            self.pos = [random.randint(60,width-100), random.randint(60,height-100)]
            display_score +=1 
            score += 1 
            if self.color == 'gold' : 
                goldflower_collected = True 
                bird_death = True  
                goldflower_spawn = False 
                self.color = 'pink'
                self.sprite = flowerbubble

            if self.color == 'blue': 
                blueflower_collected = True 
                self.color = 'pink'
                self.sprite = flowerbubble
                blueflower_spawn = False 
            if self.color == 'orange':
                orangeflower_collected=True 
                self.color = 'pink'
                orangeflower_spawn = False 
                self.sprite = flowerbubble 
    def changeflower (self,color,sprite) : 
        self.color = color
        self.sprite = sprite
    

#creating things from classes
player = Player([250,250],bee)


Flower1 = Flower([0,0],flowerbubble)
Flower2 = Flower([0,0],flowerbubble)
Flower3 = Flower([0,0],flowerbubble)
Flowers = [Flower1,Flower2,Flower3]



#creating the birdie army! 
def create_birdies():
    spawn_point = True  
    
    birdiex = random.randint(60,width-100)
    birdiey = random.randint(60,height-100)
    while spawn_point: 
        if math.dist((player.pos[0],player.pos[1]),(birdiex,birdiey))<300:
        
            birdiex = random.randint(60,width-100)
            birdiey = random.randint(60,height-100)
        else : 
            spawn_point = False 
    
    birdie = Bird((birdiex, birdiey),bird)
    birds.append(birdie)
create_birdies()
bluetimer_digit = 0 
bluetimer = 5 
orangetimer = 5 
orangetimer_digit = 0 
start_screen = True  
prev_seconds = 0 
bpower_seconds = 0
opower_seconds = 0 
while running:
    if start_screen: 
        
        clock.tick(60)
        start_text = font.render("Click to start",True,("black"))
        screen.blit(start_text,(400,400))

        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running = False 
                pg.quit() 
            if event.type == pg.MOUSEBUTTONDOWN: 
                if event.button == 1: 
                    start_screen = False 
        screen.fill((66,164,245))
        continue 
    else: 
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                running = False 
                pg.quit() 
            if win:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1: 
                        win = False 
                        prev_seconds = seconds 
            
        screen.fill((66, 164, 245))
        seconds = (pg.time.get_ticks()//1000) - prev_seconds
        if goldflower_spawn: 
            Flower1.changeflower('gold',goldflower)
        if blueflower_spawn:
            Flower2.changeflower('blue',blueflower) 
        if orangeflower_spawn:
            Flower3.changeflower('orange',orangeflower)
        if goldflower_collected : 
            screen.blit(goldflowerD,(width-144,30))
            
        if blueflower_collected and not bpressed:
            screen.blit(blueflowerD,(width-144,90))
        if orangeflower_collected and not opressed:
            screen.blit(orangeflowerD,(width-140,150))
        if orange_activate:
            countdown2 = font.render(f"Time Left: {orangetimer}",True,('black'))
            screen.blit(countdown2,(width-210,200))
            if (seconds-opower_seconds)>orangetimer_digit: 
                orangetimer_digit +=1 
                orangetimer -=1 
            if (seconds) >= opower_time: 
                player.max_speed = 5
                opressed = False 
                orangeflower_collected = False 
                orange_activate = False 
                orangetimer_digit = 0 
                orangetimer = 5 

              
            
            
        if win == False : 
            screen.blit(flower[0],(width-144,-30))
            player.update(screen)

            for f in Flowers:
                f.update() 
                f.collide() 
            if seconds >= wait_time: 
                for b in birds: 
                    b.update(screen)
                    b.bird_collide()
                    if blue_activate:
                        countdown = font.render(f"Time Left: {bluetimer}",True,('black'))
                        screen.blit(countdown,(width-210,140))
                        if (seconds-bpower_seconds)>bluetimer_digit: 
                            bluetimer_digit +=1 

                            bluetimer -=1 
                        if seconds >= power_time: 
                            blue_activate = False 
                            bluetimer = 5 
                            blueflower_collected = False 
                            bpressed = False 
                            bluetimer_digit = 0 
                    else: 
                        b.collide()
                    
            score_draw = font.render(f"Your current score is: {display_score}",True,('black'))
            screen.blit(score_draw,(width-400,30))
        else: 
            if seconds < win_screen_time : 
                frame = frame % len(win_screen)
                img = win_screen[int(frame)%len(win_screen)]
                screen.blit(img,(width//2-250,0))
                frame += 0.2
                info = font.render(f"Left Click / Wait to continue",True,('black'))
                score_draw = font.render(f"Your score is: {display_score}",True,('black'))
                screen.blit(score_draw,(100,450))
                level_draw = font.render(f"Level {level} complete",True,('black'))
                screen.blit(level_draw, (100,550))
                screen.blit(info,(100,650))
            else : 
                win = False 
                prev_seconds = seconds 
        #Bird1.update(screen) 
        #Bird1.collide()
        pg.display.update()
        clock.tick(60)


        while running == False :
            screen.fill((66, 164, 245)) 
            for event in pg.event.get():
                if event.type == pg.QUIT : 
                    running = False 
                    pg.quit() 
            gameover = font.render("Game Over",True,("black"))
            score_draw = font.render(f"Your score is: {display_score}",True,('black'))
            screen.blit(score_draw,(400,394))
            screen.blit(gameover,(420,294))
            pg.display.update()