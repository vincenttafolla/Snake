import pygame
import random

#Define game settings
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255,255,255)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,225)
COLOR_RED = (255,0,0)
BLOCK_SIZE = 18
GAP_SIZE = 2
BLOCK_COUNT = 25
BOARD_SIZE = BLOCK_COUNT * (BLOCK_SIZE + GAP_SIZE) + GAP_SIZE
FRAMES_PER_SECOND = 5

pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption('SNAKE!')

daniel = pygame.image.load("Daniel-2.png")
score_font = pygame.font.SysFont('Arial', 26, True)

game_display = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))

class GameObject():
   def __init__(self, xcor, ycor, color):
       self.xcor = xcor
       self.ycor = ycor
       self.color = color
       self.size = BLOCK_SIZE

class Snake():
    def __init__(self):
       self.is_alive = True
       self.just_ate_apple = False
       self.speed = BLOCK_SIZE + GAP_SIZE
       self.create_initial_snake()
       self.move_right()
    def create_initial_snake(self):
        self.body = []
        for i in range(7, 10):
           starting_xcor = self.speed * i + GAP_SIZE
           starting_ycor = self.speed * 12 + GAP_SIZE
           self.create_new_head(starting_xcor, starting_ycor)
    def move_left(self):
       self.direction = "LEFT"
    def move_right(self):
       self.direction = "RIGHT"
    def move_up(self):
       self.direction = "UP"
    def move_down(self):
       self.direction = "DOWN"
    def create_new_head(self, new_xcor, new_ycor):
        self.body.insert(0, GameObject(new_xcor, new_ycor, COLOR_RED))
        
    def show(self):
        head = self.body[0]
        new_xcor = head.xcor
        new_ycor = head.ycor
        if self.direction == "RIGHT":
           new_xcor = head.xcor + self.speed
        elif self.direction == "LEFT":
           new_xcor = head.xcor - self.speed
        elif self.direction == "UP":
           new_ycor = head.ycor - self.speed
        elif self.direction == "DOWN":
           new_ycor = head.ycor + self.speed

        self.create_new_head(new_xcor, new_ycor)

        if self.just_ate_apple == False:
           self.body.pop()
        self.just_ate_apple = False

        if self.has_hit_wall():
            self.is_alive = False

        for block in self.body:
           pygame.draw.rect(game_display, block.color, pygame.Rect(block.xcor, block.ycor, block.size, block.size))
    def has_hit_wall(self):
        head = self.body[0]
        return head.xcor < 0 \
            or head.ycor < 0 \
            or head.xcor + head.size > BOARD_SIZE \
            or head.ycor + head.size > BOARD_SIZE
    def grow(self):
       self.just_ate_apple = True
    def collides_with_itself(self):
        for x in range(1, len(self.body)):
            if is_collision(self.body[0], self.body[x]):
                self.is_alive = False

class Apple():
   def __init__(self):
       self.xcor = 0
       self.ycor = 0
       self.size = BLOCK_SIZE
       self.color = COLOR_RED
       self.change_location()
   def change_location(self):
       self.xcor = random.randrange(0, BLOCK_COUNT) * (BLOCK_SIZE + GAP_SIZE) + GAP_SIZE
       self.ycor = random.randrange(0, BLOCK_COUNT) * (BLOCK_SIZE + GAP_SIZE) + GAP_SIZE
   def show(self):
      # pygame.draw.rect(game_display, self.color, pygame.Rect(self.xcor, self.ycor, self.size, self.size))
      game_display.blit(daniel, (self.xcor, self.ycor))


def is_collision(a, b):
   if a.xcor + a.size > b.xcor and a.xcor < b.xcor + b.size \
   and a.ycor + a.size > b.ycor and a.ycor < b.ycor + b.size:
       return True
   else:
       return False
def handle_events(snake):
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           snake.is_alive = False

       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_LEFT:
               if snake.direction != "RIGHT":
                    snake.move_left()
           elif event.key == pygame.K_RIGHT:
               if snake.direction != "LEFT":
                    snake.move_right()
           elif event.key == pygame.K_UP:
               if snake.direction != "DOWN":
                    snake.move_up()
           elif event.key == pygame.K_DOWN:
               if snake.direction != "UP":
                    snake.move_down()

snake = Snake()
apple = Apple()
score = 0

# Main Game Loop
while snake.is_alive:

    handle_events(snake)

    game_display.blit(game_display, (0, 0))
    game_display.fill(COLOR_WHITE)

    snake.collides_with_itself()

    if is_collision(snake.body[0], apple):
       apple.change_location()
       snake.grow()
       FRAMES_PER_SECOND += 1
       score += 1

    apple.show()
    snake.show()
    score_text = score_font.render(str(score), False, COLOR_BLUE)
    game_display.blit(score_text, (0,0))

    pygame.display.flip()
    clock.tick(FRAMES_PER_SECOND)

pygame.quit()