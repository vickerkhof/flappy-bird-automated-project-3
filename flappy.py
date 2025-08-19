import pygame
import random

# Screen dimensions
screen_width = 1100
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))


class Flappy():
    def __init__(self):
        # Player state
        self.player_x = 200                           # Bird X position (fixed)
        self.player_y = screen_height / 2             # Bird starting Y position (middle of screen)
        self.player_size = 20                         # Bird radius
        self.momentum = True                          # Whether bird is currently flapping upward
        self.start_y = 0                              # How far upward the flap has moved (resets after 120 px)

        # Game state
        self.run = True
        self.score = 0
        self.plus_score = True                        # Prevents double scoring on a single pipe

    def write(text, font, color, x, y, screen, self):
        """Helper function to draw text on screen."""
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    def play(screen, screen_width, screen_height, self):
        """Main game loop."""
        pipes = []                                    # Each pipe = [x, top_gap, bottom_gap]

        fps = 60
        clock = pygame.time.Clock()

        # Initial draw of bird
        screen.fill("#ffffff")
        pygame.draw.circle(screen, "#000000", (self.player_x, self.player_y), self.player_size, self.player_size)
        pygame.display.update()

        iter = -2  # Controls pipe spawn timing

        while self.run:
            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            # Background
            screen.fill("#ffffff")
            iter += 1
            
            # Spawn new pipes every ~90 frames
            if iter > 90 or iter == -1:
                iter = 0
                new_pipe = [
                    screen_width + 150,                   # Pipe X start (off-screen right)
                    random.randint(200, screen_height-200) # Random gap top Y
                ]
                new_pipe.append(new_pipe[1] + 180)       # Bottom gap (gap size = 180 px)
                pipes.append(new_pipe)

            # Default values (updated when pipe is in front of player)
            len_pipe = screen_width - 200
            len_top_pipe = screen_height / 2
            len_bottom_pipe = screen_height / 2

            # Move pipes and draw them
            for element in pipes:
                if element[0] > -120:  # Still on screen
                    element[0] -= 4    # Move left by 4 px

                    # Top pipe rectangle
                    pipe_top = pygame.Rect(element[0], element[1], 120, element[1])
                    pipe_top.bottomleft = (element[0], element[1])

                    # Bottom pipe rectangle
                    pipe_bottom = pygame.Rect(element[0], element[2], 120, screen_height - element[2])
                    pipe_bottom.topleft = (element[0], element[2])

                    pygame.draw.rect(screen, "#000000", pipe_top)
                    pygame.draw.rect(screen, "#000000", pipe_bottom)
                else:
                    # Pipe went off screen → remove & reward score
                    self.plus_score = False
                    self.score += 10
                    pipes.remove(element)

            # Find the next pipe ahead of the bird
            next_pipe = None
            for element in pipes:
                if element[0] + 120 > self.player_x:
                    next_pipe = element
                    break

            # Update pipe references
            if next_pipe:
                len_pipe = next_pipe[0]
                len_top_pipe = next_pipe[1]
                len_bottom_pipe = next_pipe[2]

            # Score handling when passing pipes
            if len(pipes) > 0:
                if pipes[0][0] < 200 and not self.plus_score:
                    self.plus_score = True
                    self.score += 1

            # Identify current & next pipes
            current_pipe = None
            next_pipe = None
            for element in pipes:
                if element[0] + 120 > self.player_x:
                    if not current_pipe:
                        current_pipe = element
                    else:
                        next_pipe = element
                    break

            # Bird physics
            if self.player_y + self.player_size < screen_height:
                if self.momentum and self.start_y > 120:  # Stop flap after 120 px up
                    self.momentum = False
                    self.start_y = 0
                if self.momentum:
                    self.start_y += 12
                    self.player_y -= 12                  # Move up while flapping
                else:
                    self.player_y += 8                   # Gravity (fall down)
            else:
                # Hit the ground → game over
                self.run = False

            # Round position for cleaner drawing
            self.player_y = round(self.player_y, 1)

            # "Fitness" score calculation (distance-based)
            self.y_middle = abs(self.player_y - len_top_pipe + 90)
            self.score += 10 + (len_pipe - self.y_middle) / 110
            self.progress = 10 + (len_pipe - self.y_middle) / 110

            # Draw player
            pygame.draw.circle(screen, "#000000", (self.player_x, self.player_y), self.player_size, self.player_size)

            # Auto-flap trigger: if bird is too low near pipe gap
            if self.player_y >= len_bottom_pipe - self.player_size - 10:
                self.momentum = True

            # Update screen
            clock.tick(fps)
            pygame.display.update()


# Run the game
fitness = Flappy()
Flappy.play(screen, screen_width, screen_height, fitness)
