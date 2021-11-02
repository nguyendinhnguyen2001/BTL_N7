import pygame
import time
import sys
import random
pygame.init()
SCREEN_WIDTH = 520
SCREEN_HEIGHT = 520
0
GRIDSIZE = 20
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
PAUSE = (0, 0)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(65, 105, 255)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gray = pygame.Color(128, 128, 128)
# load ảnh
Imgsnake = pygame.transform.scale(
    pygame.image.load('head.jpg'), (GRIDSIZE, GRIDSIZE))
Imgfood = pygame.transform.scale(
    pygame.image.load('covid.png'), (GRIDSIZE, GRIDSIZE))
ImgItem1 = pygame.transform.scale(
    pygame.image.load('fruit1.png'), (GRIDSIZE, GRIDSIZE))
ImgItem2 = pygame.transform.scale(
    pygame.image.load('tim.jpg'), (GRIDSIZE, GRIDSIZE))


class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)]
        self.direction = PAUSE
        self.GAME_OVER = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x*GRIDSIZE))), (cur[1] + (y*GRIDSIZE)))
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.GAME_OVER = True
        elif new[0] < 20 or new[0] > (SCREEN_WIDTH-40) or new[1] < 20 or new[1] > (SCREEN_HEIGHT-40):
            self.GAME_OVER = True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        for pos in self.positions:
            surface.blit(Imgsnake, pygame.Rect(
                pos[0], pos[1], GRIDSIZE, GRIDSIZE))

    def handle_keys(self, time, count):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_OVER = True
            elif event.type == pygame.KEYDOWN:
                time.get_damage(count)
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)


class Food(object):
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(1, GRID_WIDTH-2) *
                         GRIDSIZE, random.randint(1, GRID_HEIGHT-2) * GRIDSIZE)

    def draw(self, surface):
        surface.blit(Imgfood, pygame.Rect(
            self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))


class Item(object):
    def __init__(self, option):
        self.position = (0, 0)
        self.randomize_position()
        self.optionItem = option

    def randomize_position(self):
        self.position = (random.randint(1, GRID_WIDTH-2) *
                         GRIDSIZE, random.randint(1, GRID_HEIGHT-2) * GRIDSIZE)

    def draw(self, surface):
        if self.optionItem == 1:
            surface.blit(ImgItem1, pygame.Rect(
                self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))
        elif self.optionItem == 2:
            surface.blit(ImgItem2, pygame.Rect(
                self.position[0], self.position[1], GRIDSIZE, GRIDSIZE))


class Time(object):
    def __init__(self):
        self.current_time = 0
        self.maximum_time = 960
        self.time_length = 480
        self.check_time = False

    def update(self):
        self.current_time += 40

    def get_damage(self, amount):
        if self.current_time > 0:
            self.current_time -= amount
        else:
            self.current_time = 0
            self.check_time = True

    def get_time(self):
        self.current_time = self.maximum_time

    def draw(self, surface):
        pygame.draw.rect(
            surface, red, (20, SCREEN_HEIGHT-10, (self.current_time*self.time_length)/self.maximum_time, SCREEN_HEIGHT-10))
        pygame.draw.rect(
            surface, black, (20, SCREEN_HEIGHT-10, self.time_length, SCREEN_HEIGHT-10), 2)


def main():
    GAME_CLOSED = False
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT+20))
    pygame.display.set_caption('Snake Covid-19 Nhom 7')
    surface.fill(white)
    pygame.draw.rect(
        surface, gray, (20, 20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40), 2)
    snake = Snake()
    food = Food()
    item1 = Item(1)
    item2 = Item(2)
    time = Time()
    time.get_time()
    Itemflat = False
    Item_timeflat = False
    score = 0
    check = 0
    check_TIME = 0
    while not GAME_CLOSED:
        while snake.GAME_OVER == True:
            pygame.draw.rect(
                surface, gray, (20, 20, SCREEN_WIDTH-40, SCREEN_HEIGHT-40), 2)
            font_style = pygame.font.SysFont("consolas", 18)
            if score >= 100:
                surface.blit(font_style.render("You Win! Press C-Play again or Q-quit",
                                               True, black), [SCREEN_WIDTH/8, SCREEN_HEIGHT/3])
            else:
                surface.blit(font_style.render("You lost! Press C-Play again or Q-quit",
                                               True, black), [SCREEN_WIDTH/8, SCREEN_HEIGHT/3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        GAME_CLOSED = True
                        snake.GAME_OVER = False
                    if event.key == pygame.K_c:
                        main()
        clock.tick(8)
        snake.handle_keys(time, 4)
        snake.move()
        surface.fill(white)
        pygame.draw.rect(surface, gray, (20, 20,
                         SCREEN_WIDTH-40, SCREEN_HEIGHT-40), 2)
        if snake.get_head_position() == food.position:
            snake.length += 1
            score += 1
            check += 1
            check_TIME += 1
            food.randomize_position()
        if check > 0 and check % 5 == 0:
            Itemflat = True
        if check_TIME > 0 and check_TIME % 24 == 0:
            Item_timeflat = True
        if Item_timeflat == True:
            item2.draw(surface)
            if snake.get_head_position() == item2.position:
                time.update()
                check_TIME = 0
                Item_timeflat = False
        if Itemflat == True:
            item1.draw(surface)
            if snake.get_head_position() == item1.position:
                score += 5
                check = 0
                Itemflat = False
        if score >= 100:
            snake.GAME_OVER = True
        if time.check_time == True:
            snake.GAME_OVER = True
        snake.draw(surface)
        food.draw(surface)
        time.draw(surface)
        myfont = pygame.font.SysFont("consolas", 12)
        text = myfont.render("Score: {0}".format(score), 1, (0, 0, 0))
        surface.blit(text, (5, 10))
        pygame.display.update()
        pygame.display.flip()


main()
