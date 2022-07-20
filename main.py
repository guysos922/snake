# importing libraries
from turtle import window_height, window_width
import pygame
import time
import random
 
# Window size
window_x = 720
window_y = 480

snake_starting_pos_x = window_x/2
snake_starting_pos_y = window_y/2
snake_width = 10
snake_height = 10
snake_speed = 10
snake_length = 10
snake_color = 'blue'

food_width = 10
food_height = 10
food_color = 'red'

frames_per_second = 10

 
# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initializing pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Snakes Game')
game_window = pygame.display.set_mode((window_x, window_y))
 
# FPS (frames per second) controller
fps = pygame.time.Clock()
  

done = False    

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        #snake
        self.color = snake_color
        self.speed = snake_speed
        self.length = snake_length
        self.x = snake_starting_pos_x
        self.y = snake_starting_pos_y
        self.score = 0
        self.direction = ""
        self.blockList = []

        self.food_x = round(random.randrange(0, window_x - snake_width) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, window_y - snake_height) / 10.0) * 10.0
        self.food_color = food_color
        for i in range(0, self.length):
            self.blockList.append([snake_starting_pos_x - snake_width * i,snake_starting_pos_y])

    def update(self):
        self.move()
        #draw snake
        for block in self.blockList:
            snake_block =pygame.Rect(block[0], block[1], snake_width, snake_height)
            pygame.draw.rect(game_window,self.color,snake_block)

        food_block =pygame.Rect(self.food_x, self.food_y, food_width, food_height)
        if not food_block.collidepoint(self.x, self.y):
            pygame.draw.rect(game_window,self.food_color,food_block)
        else:
            self.eaten()


    def move(self):
        if self.direction == 'right':
            self.x += self.speed
            self.move_blocks()
            self.blockList.insert(0, [self.x,self.y])
        if self.direction == 'left':
            self.x -= self.speed
            self.move_blocks()
            self.blockList.insert(0, [self.x,self.y])
        if self.direction == 'up':
            self.y -= self.speed
            self.move_blocks()
            self.blockList.insert(0, [self.x,self.y])
        if self.direction == 'down':
            self.y += self.speed
            self.move_blocks()
            self.blockList.insert(0, [self.x,self.y])
    
    def move_blocks(self):
        self.blockList.pop()

    def lost(self):
        if self.x - snake_width > window_x or self.y - snake_height > window_y or self.x<0 or self.y<0:
            return True
        for block in self.blockList:
            if self.blockList.count(block) > 1:
                return True
        return False
    
    def create_food(self):
        self.food_x = round(random.randrange(0, window_x - snake_width) / 10.0) * 10.0
        self.food_y = round(random.randrange(0, window_y - snake_height) / 10.0) * 10.0

    def eaten(self):
        self.create_food()
        self.length +=1
        self.score +=1
        self.blockList.append([self.blockList[len(self.blockList)-1][0]-snake_width,self.blockList[len(self.blockList)-1][1]-snake_height])
        print(len(self.blockList))
        food_block =pygame.Rect(self.food_x, self.food_y, food_width, food_height)
    
    def get_score(self):
        return "score:"+str(self.score)
    
snake = Snake()

score_font = pygame.font.SysFont("comicsansms", 20)
text = score_font.render("score:0", True, 'white')
game_window.blit(text, (50,30))

while not done:  
    #clear the screen before drawing it again 
    game_window.fill(0) 
    #init fps
    fps.tick(frames_per_second)  
    snake.update()
    text = score_font.render(snake.get_score(), True, 'white')
    game_window.blit(text, (50,30))
    #update the screen
    pygame.display.flip()

    if snake.lost() == True:
        done = True
        pygame.quit() 
        exit(0) 

    for event in pygame.event.get(): 
        # If user clicked on close symbol  
        if event.type == pygame.QUIT or done==True:
            done = True
            pygame.quit() 
            exit(0) 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and snake.direction != 'right':
                snake.direction = 'left'
            elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                snake.direction = 'right'
            elif event.key == pygame.K_UP and snake.direction != 'down':
                snake.direction = 'up'
            elif event.key == pygame.K_DOWN and snake.direction != 'up':
                snake.direction = 'down'

