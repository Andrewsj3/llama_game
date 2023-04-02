"""Improved collision system and obstacle spawning
Jack Andrews
2/4/23"""
import pygame
import random
from sys import argv

WIDTH = 620
HEIGHT = 200
FPS = 30


class Game:
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    ground_img = pygame.image.load("assets/ground.png")
    ground_img = pygame.transform.smoothscale(ground_img, [WIDTH, 3])
    cactus_img = pygame.image.load("assets/cactus.png")
    font = pygame.font.Font("assets/PressStart.ttf", 12)
    icon_img = pygame.image.load("assets/llama_icon.png")
    clock = pygame.time.Clock()
    pygame.display.set_icon(icon_img)
    pygame.display.set_caption("Llama Game")
    obstacles = []
    # Keeping track of all cactuses on screen
    speed = 10
    # Controlling how much the cactuses move per frame
    group_size = 0
    # How many spawn at a time
    max_group_size = 4
    # The most that can spawn at a time
    score = 0
    high_score = 0

    @classmethod
    def draw(cls, high_score):
        cls.win.fill(0xFFFFFF)
        cls.win.blit(cls.ground_img, [0, 132])
        message(str(cls.score).rjust(5, "0"), (0, 0, 0,), [570, 20])
        message(f"HI {str(high_score).rjust(5, '0')}", (0, 0, 0,), [480, 20])
        # Drawing scores onto the screen
        for obstacle in cls.obstacles:
            cls.win.blit(obstacle[0], [obstacle[1], 100])

    @classmethod
    def load_high_score(cls):
        try:
            with open("highscore.txt") as f:
                high_score = int(f.read())
                return high_score
        except IOError:
            # No highscore exists yet
            return 0

    @classmethod
    def save_high_score(cls):
        high_score = cls.load_high_score()
        if cls.score > high_score:
            with open("highscore.txt", 'w') as f:
                f.write(str(cls.score))

    @classmethod
    def create_obstacles(cls):
        cls.group_size = random.randint(
            cls.max_group_size - 3, cls.max_group_size)
        for i in range(cls.group_size):
            cls.obstacles.append([cls.cactus_img, WIDTH + i * 20])
            # Spacing each of the cacti apart so they don't spawn on top of
            # each other

    @classmethod
    def update_obstacles(cls):
        if cls.score % 1000 == 0 and cls.score != 0:
            cls.speed += 3
            cls.max_group_size += 1
            # Speeding the game up so it becomes more difficult over time
        cls.obstacles = [ob for ob in cls.obstacles if ob[1] > -5]
        if not len(cls.obstacles):
            cls.create_obstacles()
        elif len(cls.obstacles) == 1 and cls.obstacles[0][1] < WIDTH // 3:
            cls.create_obstacles()
        elif len(cls.obstacles) == 2 and cls.obstacles[0][1] < WIDTH // 3\
                and cls.obstacles[1][1] < WIDTH // 2:
            cls.create_obstacles()
        for i in range(len(cls.obstacles)):
            cls.obstacles[i][1] -= cls.speed
            # Moving the obstacles left

    @classmethod
    def check_collisions(cls, llama):
        if llama.x < 0:
            # Checking for the offscreen llama
            return False
        for sprite in cls.obstacles:
            cactus_rect = sprite[0].get_rect(topleft=(sprite[1], 100))
            llama_rect = llama.stand_img.get_rect(topleft=(llama.x, llama.y))
            # Now using get_rect for more accurate measurements
            if pygame.Rect.colliderect(cactus_rect, llama_rect):
                return True
        return False


class Llama:
    Y_VELOCITY = JUMP_HEIGHT = 16.8
    Y_GRAVITY = 2.4
    stand_img = pygame.image.load("assets/Llama.png")
    r_leg_img = pygame.image.load("assets/Llama3.png")
    l_leg_img = pygame.image.load("assets/Llama2.png")

    def __init__(self, x, y):
        self.counter = 0
        self.x = x
        self.y = y
        self.vel = self.Y_VELOCITY
        self.imgs = {0: self.stand_img, 1: self.r_leg_img, 2: self.l_leg_img}
        self.is_jumping = False
        self.draw()

    def draw(self):
        if not self.is_jumping:
            self.counter += 1
            # Determines which llama sprite will be displayed this frame
            selection = self.counter // 2 % 2
            # Makes it so that the image selected changes only after two frames
            # instead of 1
            Game.win.blit(self.imgs[selection + 1], [self.x, self.y])
        else:
            # When the llama is jumping, we want the default sprite
            Game.win.blit(self.imgs[0], [self.x, self.y])

    def jump(self):
        self.y -= self.vel
        self.vel -= self.Y_GRAVITY
        if self.vel < -self.JUMP_HEIGHT:
            self.y += 100 - self.y
            # Sets llama's y position to the default 100
            self.is_jumping = False
            # Flag set only after the llama touches the ground
            self.vel = self.Y_VELOCITY
        self.draw()


def message(text, text_col, coords, bg_col=None):
    txt = Game.font.render(text, True, text_col, bg_col)
    text_box = txt.get_rect(center=coords)
    Game.win.blit(txt, text_box)


def main():
    llama = Llama(60, 100)
    if '-m' in argv[1:]:
        llama2 = Llama(30, 100)
        # Allows the user to toggle multiplayer by passing the -m flag
    else:
        llama2 = Llama(-50, -50)
        # llama2 still needs to exist for the program to work,
        # but we just place it offscreen
    # Multiplayer suggested by Jess
    high_score = Game.load_high_score()

    while True:
        Game.score += Game.speed // 10
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_SPACE]:
            llama.is_jumping = True
        if key_pressed[pygame.K_UP]:
            llama2.is_jumping = True

        if llama.is_jumping:
            llama.jump()
            # This gets called on every frame until the llama touches the
            # ground
        if llama2.is_jumping:
            llama2.jump()
        Game.draw(high_score)
        llama.draw()
        llama2.draw()
        if any([Game.check_collisions(i) for i in [llama, llama2]]):
            break
        Game.update_obstacles()
        pygame.display.update()
        Game.clock.tick(FPS)

    while True:
        message("You died! Press space to play again or Esc to quit",
                (0, 0, 0), [WIDTH // 2, 80])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game.save_high_score()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Game.win.fill(0xFFFFFF)
                    Game.speed = 10
                    Game.save_high_score()
                    Game.score = 0
                    Game.max_group_size = 4
                    Game.obstacles = []
                    # Resetting attributes of Game to default
                    main()
                elif event.key == pygame.K_ESCAPE:
                    Game.save_high_score()
                    pygame.quit()
                    exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
