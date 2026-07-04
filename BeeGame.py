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
clock = pg.time.Clock() 
birds = []
level = 1 
height = 622
width = 900
addedflower = False 
frame = 0 
wait_time = 1
birdcount = 1 
num_flowers = 3 
font = pg.font.SysFont("arial",36)

screen = pg.display.set_mode((width,height))
pg.display.set_caption('BeeGame')

#set up imgs
def generatefilenames(name,count):
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
    "bee": generatefilenames("bee", 3),
    "beeflip":generatefilenames("beeflip",3),
    "flower": generatefilenames("flower", 3),
    "beestart":generatefilenames("beestart",4),
    "beehive": generatefilenames("beehive", 4),
    "flowerbubble": generatefilenames("flowerbubble", 4),
    "WinScreen":generatefilenames("WinScreen",7),
    "blueflowerbubble":generatefilenames("blueflowerbubble",4),
    "orangeflowerbubble":generatefilenames("orangeflowerbubble",4),
    "goldflowerbubble":generatefilenames("goldflowerbubble",4)
}
bird_group = {
    "bird": generatefilenames("bird", 5),
    "birdflip":generatefilenames("birdflip",5),
}

images = load_images(image_groups)

levelup_group = {"WinScreen":generatefilenames("WinScreen",7)}
levelup_images = load_images(levelup_group,(670,670))
levelup_screen = levelup_images["WinScreen"]
blueflower = images["blueflowerbubble"]
goldflower = images["goldflowerbubble"]
orangeflower = images["orangeflowerbubble"]
bee = images["bee"]
beeflip = images["beeflip"]
start = {"beestart" : generatefilenames("beestart",4)}
beestart2 = load_images(start,(600,600))
beestartscreen = beestart2["beestart"]
flower = images["flower"]
bird_images = load_images(bird_group,(190,190))
bird = bird_images["bird"]
birdflip = bird_images["birdflip"]
beehive = images["beehive"]
flowerbubble = images["flowerbubble"]


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
    
    def __init__(self,pos,sprite,game): 
        super().__init__(pos,sprite)

        self.vel = [0,0]
        self.acceleration = 0.8 
        self.friction = 0.9 
        self.max_speed = 5.4
        self.game = game 
    def update(self,screen): 
        
 
        self.draw(screen)
        self.frame = self.frame % len(self.sprite)
        keys = pg.key.get_pressed() 
        self.rect = bee[int(self.frame)].get_rect(topleft=self.pos)
        self.mask = pg.mask.from_surface(bee[int(self.frame)])
        if keys[pg.K_a] and self.pos[0]>0:
            
            self.sprite = beeflip
            self.vel[0] -= self.acceleration
        if keys[pg.K_d]and self.pos[0]< 745:
            self.sprite = bee 
            self.vel[0] += self.acceleration
        if keys[pg.K_w] and self.pos[1] >5: 
           
            self.vel[1] -= self.acceleration 
        if keys[pg.K_s] and self.pos[1]<490: 
            self.vel[1] += self.acceleration 


        if keys[pg.K_b] and self.game.blueflower_collected:
            self.game.power_time = self.game.seconds + 5
            self.game.blue_activate = True 
            self.game.bpower_seconds = self.game.seconds
            self.game.bpressed = True 
        if keys[pg.K_t] and self.game.orangeflower_collected:
            self.game.opower_time = self.game.seconds + 5 
            self.max_speed = 10
            self.acceleration = 1 
            self.game.opower_seconds = self.game.seconds
            self.game.orange_activate = True 
            self.game.opressed = True 
            print('Orange key pressed, activate orange flower',self.max_speed)
            
      
        self.vel[0] = max(-self.max_speed, min(self.max_speed, self.vel[0]))
        self.vel[1] = max(-self.max_speed, min(self.max_speed, self.vel[1]))

        self.vel[0] *= self.friction 
        self.vel[1] *= self.friction 

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.frame += self.animation_speed 



class Bird(Object): 
    def __init__ (self,pos,sprite,game):

        super().__init__(pos,sprite)
        self.vel = [0,0]
        self.acceleration = 0.5 
        self.friction = 0.9 

        self.animation_speed = 0.05 
        self.game = game 
        self.max_speed = random.uniform(self.game.birdmin_speed,self.game.birdmax_speed) 
    def update(self,screen): 
        self.update_animation() 
        self.draw(screen) 
        distancex = self.game.player.pos[0]-self.pos[0]
        distancey = self.game.player.pos[1]-self.pos[1]
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

        
        self.frame = self.frame % len(self.sprite)
        self.rect = bird[int(self.frame)].get_rect(topleft=self.pos)
        self.mask = pg.mask.from_surface(bird[int(self.frame)])
        
        if pg.sprite.collide_mask(self.game.player,self): 
            if self.game.bird_death == True : 
                birds.remove(self)   
                self.game.bird_death = False 
                self.game.goldflower_collected = False 
            else: 
                
                self.game.running = False 
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
    def __init__ (self,pos,sprite,game,color='pink'):
        super().__init__(pos,sprite)
        self.sprite = flowerbubble
        self.frame_index = 0
        self.pos = [random.randint(60,width-100), random.randint(60,height-100)]
        self.color = color 
        self.last_update = pg.time.get_ticks()
        self.animation_delay = 750 
        self.game = game 
    def update(self): 
        self.draw(screen)
        self.update_animation()
        self.frame = self.frame % len(self.sprite)
        self.rect = flowerbubble[int(self.frame)].get_rect(topleft=self.pos)
        self.mask = pg.mask.from_surface(flowerbubble[int(self.frame)])
        
    def collide(self): 
 
        global level 
        global addedflower 

        if game.score == game.goal: 
            if level%5==0: 
                game.player.max_speed += 1
            if level%6 == 0: 
                game.birdmax_speed += 1
                game.birdmin_speed += 0.5
                for b in birds : 
                    b.max_speed += 0.3
            game.score = 0 
            game.levelup = True 
            game.levelup_screen_time = game.seconds + 2.5
            level += 1 
            addedflower = False 
            if level%2==0:
                game.goal += 1
            game.createbirdies()
        if level%5==0 and not addedflower:
            newflower = Flower([0,0],flowerbubble,game)
            Flowers.append(newflower)  
            addedflower = True

        if game.display_score != 0: 
            if game.display_score%20 ==0 or game.display_score == 5: 
                game.goldflower_spawn = True 
            if game.display_score%10 == 0: 
                game.blueflower_spawn = True 
                
            if game.display_score%15 == 0:
                game.orangeflower_spawn = True 
        if pg.sprite.collide_mask(game.player,self):
            
            self.pos = [random.randint(60,width-100), random.randint(60,height-100)]
            game.display_score +=1 
            game.score += 1 
            if self.color == 'gold' : 
                game.goldflower_collected = True 
                game.bird_death = True  
                game.goldflower_spawn = False 
                self.color = 'pink'
                self.sprite = flowerbubble

            if self.color == 'blue': 
                game.blueflower_collected = True 
                self.color = 'pink'
                self.sprite = flowerbubble
                game.blueflower_spawn = False 
            if self.color == 'orange':
                game.orangeflower_collected=True 
                self.color = 'pink'
                game.orangeflower_spawn = False 
                self.sprite = flowerbubble 
    def changeflower (self,color,sprite) : 
        self.color = color
        self.sprite = sprite
    


class Game: 
    def __init__(self): 
        #stuff for like the actual game
        self.running = True 
        self.start_screen = True 
        self.frame = 0
        self.prev_seconds = 0 
        self.goal = 3
        self.bpower_seconds = 0 
        self.seconds = 0 
        self.player = Player([250,250],bee,self)
        self.score = 0
        self.display_score = 0 
        #Flower powerup timer things AND other powerup stuff
        self.opower_seconds = 0 
        self.orangetimer_digit = 0 
        self.orangetimer = 5
        self.opowertime = 0 
        self.bluetimer = 5 
        self.bluetimer_digit = 0 
        self.orange_activate = False 
        self.blue_activate = False 
        self.bpressed = False 
        self.opressed = False 
        #Flowers collected, spawned, ect
        self.blueflower_collected = False 
        self.goldflower_collected = False 
        self.orangeflower_collected = False 
        self.goldflower_spawn = False 
        self.blueflower_spawn = False 
        self.orangeflower_spawn = False 
        self.power_time = 0 
        #variables for win screen things
        self.levelup = False 
        self.levelup_screen_time = 0
        
        #birds
        self.birdmax_speed = 3.5
        self.birdmin_speed = 1.5
        self.bird_death = False 
        
    def gameplay (self):
        while self.running:
            if self.start_screen: 
                self.startscreen() 
            else: 
                for event in pg.event.get():
                    if event.type == pg.QUIT: 
                        pg.quit() 
                    if self.levelup:
                        if event.type == pg.MOUSEBUTTONDOWN:
                            if event.button == 1 or event.button == 3 : 
                                self.levelup = False 
                                self.prev_seconds = self.seconds 
                    
                screen.fill((66, 164, 245))
                self.seconds = (pg.time.get_ticks()//1000) - self.prev_seconds
                if self.goldflower_spawn: 
                    Flower1.changeflower('gold',goldflower)
                if self.blueflower_spawn:
                    Flower2.changeflower('blue',blueflower) 
                if self.orangeflower_spawn:
                    Flower3.changeflower('orange',orangeflower)
                if self.goldflower_collected : 
                    screen.blit(goldflowerD,(width-144,30))
                    
                if self.blueflower_collected and not self.bpressed:
                    screen.blit(blueflowerD,(width-144,90))
                if self.orangeflower_collected and not self.opressed:
                    screen.blit(orangeflowerD,(width-140,150))
                if self.orange_activate:
                    countdown2 = font.render(f"Time Left: {self.orangetimer}",True,('black'))
                    screen.blit(countdown2,(width-210,200))
                    if (self.seconds-self.opower_seconds)>self.orangetimer_digit: 
                        self.orangetimer_digit +=1 
                        self.orangetimer -=1 
                    if (self.seconds) >= self.opower_time: 
                        self.player.max_speed = 6.5
                        self.player.acceleration = 0.8
                        self.opressed = False 
                        self.orangeflower_collected = False 
                        self.orange_activate = False 
                        self.orangetimer_digit = 0 
                        self.orangetimer = 5 

                    
                    
                    
                if not self.levelup: 
                    screen.blit(flower[0],(width-144,-30))
                    self.player.update(screen)

                    for f in Flowers:
                        f.update() 
                        f.collide() 
                    if self.seconds >= wait_time: 
                        for b in birds: 
                            b.update(screen)
                            b.bird_collide()
                            if self.blue_activate:
                                countdown = font.render(f"Time Left: {self.bluetimer}",True,('black'))
                                screen.blit(countdown,(width-210,140))
                                if (self.seconds-self.bpower_seconds)>self.bluetimer_digit: 
                                    self.bluetimer_digit +=1 

                                    self.bluetimer -=1 
                                if self.seconds >= self.power_time: 
                                    self.blue_activate = False 
                                    self.bluetimer = 5 
                                    self.blueflower_collected = False 
                                    self.bpressed = False 
                                    self.bluetimer_digit = 0 
                            else: 
                                b.collide()
                            
                    score_draw = font.render(f"Your current score is: {self.display_score}",True,('black'))
                    screen.blit(score_draw,(width-400,30))
                else: 
                    self.gamelevelup()
                #Bird1.update(screen) 
                #Bird1.collide()
                pg.display.update()
                clock.tick(60)


                if self.running == False :
                    self.youlose()
    def gamelevelup (self): 
        if self.seconds < self.levelup_screen_time : 
            self.frame = self.frame % len(levelup_screen)
            img = levelup_screen[int(self.frame)%len(levelup_screen)]
            screen.blit(img,(width//2-50,-25))
            self.frame += 0.2
            levelupfont = pg.font.SysFont("arial",50)
            score_draw = levelupfont.render(f"Your score is: {self.display_score}",True,('black'))
            screen.blit(score_draw,(150,350))
            level_draw = levelupfont.render(f"Level {level} complete",True,('black'))
            screen.blit(level_draw, (150,425))
            infofont = pg.font.SysFont("arial",30)
            info = infofont.render(f"Click / Wait to continue",True,('black'))
            
            screen.blit(info,(175,500))
        else : 
            self.levelup = False 
            self.prev_seconds = self.seconds  

    def youlose (self) : 
        while not self.running: 
            for event in pg.event.get():
                if event.type == pg.QUIT: 
                    pg.quit() 
                if event.type == pg.MOUSEBUTTONDOWN: 

                    if event.button == 1 or event.button == 3:
                        game.reset_game()
            screen.fill((66, 164, 245)) 
            for event in pg.event.get():
                if event.type == pg.QUIT : 
                    pg.quit() 

            #text
            gameover = font.render("Game Over",True,("black"))
            scoredraw = font.render(f"Your score is: {self.display_score}",True,('black'))
            playagain = font.render("Click to play again",True,('black'))
            
            screen.blit(gameover,(width//2-gameover.get_width()//2,200))
            screen.blit(scoredraw,(width//2-scoredraw.get_width()//2,300))
            screen.blit(playagain,(width//2-playagain.get_width()//2,400))
            pg.display.update()

    def startscreen (self):
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                
                pg.quit() 
            if event.type == pg.MOUSEBUTTONDOWN: 
                if event.button == 1 or event.button == 3: 
                    self.start_screen = False 
        screen.fill((66,164,245))
        clock.tick(60)
        start_text = font.render("Click to start",True,("black"))
        self.frame = self.frame % len(levelup_screen)
        bee_start = beestartscreen[int(self.frame)%len(beestartscreen)]
        beewidth = bee_start.get_width()
        print(450-beewidth)
        screen.blit(bee_start,(width//2-beewidth//2,-20))
        self.frame += 0.05       
        
        startwidth = start_text.get_width()  
        screen.blit(start_text,(width//2-startwidth//2,420))
        pg.display.update() 

    def createbirdies(self):
        spawn_point = True  
        
        birdiex = random.randint(60,width-100)
        birdiey = random.randint(60,height-100)
        while spawn_point: 
            if math.dist((self.player.pos[0],self.player.pos[1]),(birdiex,birdiey))<300:
            
                birdiex = random.randint(60,width-100)
                birdiey = random.randint(60,height-100)
            else : 
                spawn_point = False 
        
        birdie = Bird((birdiex, birdiey),bird,self)
        birds.append(birdie)
    def reset_game(self):
        global birds, Flowers, level
        birds = [] 
        Flowers = [Flower1,Flower2,Flower3]
        self.display_score = 0 
        self.score = 0 
        level = 1 
        self.goal = 3 
        self.opower_seconds = 0 
        self.orangetimer_digit = 0 
        self.orangetimer = 5
        self.opowertime = 0 
        self.bluetimer = 5 
        self.bluetimer_digit = 0 
        self.orange_activate = False 
        self.blue_activate = False 
        self.bpressed = False 
        self.opressed = False 
        #Flowers collected, spawned, ect
        self.blueflower_collected = False 
        self.goldflower_collected = False 
        self.orangeflower_collected = False 
        self.goldflower_spawn = False 
        self.blueflower_spawn = False 
        self.orangeflower_spawn = False 
        self.power_time = 0 
        #variables for win screen things
        self.levelup = False 
        self.levelup_screen_time = 0
        
        #birds
        self.birdmax_speed = 3.5
        self.birdmin_speed = 1
        self.player = Player([250,250],bee,self)
        game.createbirdies()
        self.running = True 
        

#starting the game
game = Game() 



Flower1 = Flower([0,0],flowerbubble,game)
Flower2 = Flower([0,0],flowerbubble,game)
Flower3 = Flower([0,0],flowerbubble,game)
Flowers = [Flower1,Flower2,Flower3]
game.createbirdies()
game.gameplay()
