import pygame
import random


screen_width = 1100
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))


class Flappy():

    def __init__(self):
        self.score = 0
        self.player_x = 200
        self.player_y = screen_height/2
        self.player_size = 20
        self.start_y = 0
        self.plus_score = True
        self.score = 0
        self.momentum = True
        self.run = True


    def write(text, font, color, x, y, screen, self):
        img = font.render(text, True, color)
        screen.blit(img, (x, y))


    def play(screen, screen_width, screen_height, self):
        pipes = []

        fps = 60
        clock = pygame.time.Clock()

        screen.fill("#ffffff")
        pygame.draw.circle(screen, "#000000", (self.player_x, self.player_y), self.player_size, self.player_size)
        pygame.display.update()
        iter = -2

        while self.run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            screen.fill("#ffffff")
            iter += 1
            
            if iter > 90 or iter == -1:
                iter = 0
                new_pipe = [
                    screen_width+150,
                    random.randint(200, screen_height-200)
                ]
                new_pipe.append(new_pipe[1]+180)
                pipes.append(new_pipe)

            len_pipe = screen_width-200
            len_top_pipe = screen_height/2
            len_bottom_pipe = screen_height/2

            for element in pipes:
                if element[0] > -120:
                    element[0] -= 4
                    pipe_top = pygame.Rect(element[0], element[1], 120, element[1])
                    pipe_top.bottomleft = (element[0], element[1])
                    pipe_bottom = pygame.Rect(element[0], element[2], 120, screen_height - element[2])
                    pipe_bottom.topleft = (element[0], element[2])
                    pygame.draw.rect(screen, "#000000", pipe_top)
                    pygame.draw.rect(screen, "#000000", pipe_bottom)
                else:
                    self.plus_score = False
                    self.score += 10
                    pipes.remove(element)

            next_pipe = None
            for element in pipes:
                if element[0] + 120 > self.player_x:
                    next_pipe = element
                    break

            if next_pipe:
                len_pipe = next_pipe[0]
                len_top_pipe = next_pipe[1]
                len_bottom_pipe = next_pipe[2]

            if len(pipes) > 0:
                if pipes[0][0] < 200 and not self.plus_score:
                    self.plus_score = True
                    self.score += 1

            current_pipe = None
            next_pipe = None

            for element in pipes:
                if element[0] + 120 > self.player_x:
                    if not current_pipe:
                        current_pipe = element
                    else:
                        next_pipe = element
                    break

            if self.player_y+self.player_size < screen_height:
                if self.momentum and self.start_y > 120:
                    self.momentum = False
                    self.start_y = 0
                if self.momentum:
                    self.start_y += 12
                    self.player_y -= 12
                else:
                    self.player_y += 8
            else:
                self.run = False
            self.player_y = round(self.player_y, 1)

            self.y_middle = abs(self.player_y-len_top_pipe+90)
            self.score += 10+(len_pipe-self.y_middle)/110
            self.progress = 10+(len_pipe-self.y_middle)/110

            pygame.draw.circle(screen, "#000000", (self.player_x, self.player_y), self.player_size, self.player_size)

            if self.player_y >= len_bottom_pipe-self.player_size-10:
                self.momentum = True

            clock.tick(fps)
            pygame.display.update()


fitness = Flappy()
Flappy.play(screen, screen_width, screen_height, fitness)
