"""Obstacles component: Create moving obstacles for the llama to jump over
Jack Andrews
29/3/23"""
import pygame
import random

WIDTH = 620
HEIGHT = 200
FPS = 30


class Game:
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    ground_img = pygame.image.load("assets/ground.png")
    ground_img = pygame.transform.smoothscale(ground_img, [WIDTH, 1])
    cactus_img = pygame.image.load("assets/cactus.png")
    obstacles = []
    # Keeping track of all cactuses on screen
    speed = 10
    # Controlling how much the cactuses move per frame
    group_size = 0
    # How many spawn at a time

    @classmethod
    def draw(cls):
        cls.win.fill(0xFFFFFF)
        cls.win.blit(cls.ground_img, [0, 132])
        for obstacle in cls.obstacles:
            cls.win.blit(obstacle[0], [obstacle[1], 100])

    @classmethod
    def create_obstacles(cls):
        cls.group_size = random.randint(1, 3)
        for i in range(cls.group_size):
            cls.obstacles.append([cls.cactus_img, WIDTH + i * 20])
            # Spacing each of the cacti apart so they don't spawn on top of
            # each other

    @classmethod
    def update_obstacles(cls):
        new_obstacles = []
        for obstacle in cls.obstacles:
            if obstacle[1] > -5:
                # If the obstacle is not completely offscreen
                new_obstacles.append(obstacle)
        if len(cls.obstacles) == 0:
            # Spawns new cacti if there are none
            cls.create_obstacles()
            return
        for i in range(len(new_obstacles)):
            new_obstacles[i][1] -= cls.speed
            # Moving the obstacles left

        cls.obstacles = new_obstacles

    @classmethod
    def check_collisions(cls, llama):
        try:
            min_x = min(cls.obstacles, key=lambda x: x[1])[1]-10
            max_x = min_x + (len(cls.obstacles) * 20)+10
            x_bounds = range(min_x, max_x)
        except ValueError:
            return False
        if llama.x in x_bounds and llama.y > 65:
            # TODO
            pass


class Llama:
    Y_VELOCITY = JUMP_HEIGHT = 24
    Y_GRAVITY = 4
    stand_img = pygame.image.load("assets/Llama.png")
    r_leg_img = pygame.image.load("assets/Llama3.png")
    l_leg_img = pygame.image.load("assets/Llama2.png")

    def __init__(self):
        self.counter = 0
        self.x = 50
        self.y = 100
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


def main():
    pygame.init()
    icon_img = pygame.image.load("assets/llama_icon.png")
    clock = pygame.time.Clock()
    pygame.display.set_icon(icon_img)
    pygame.display.set_caption("Llama Game")
    llama = Llama()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_SPACE] | key_pressed[pygame.K_UP]:
            llama.is_jumping = True

        if llama.is_jumping:
            llama.jump()
            # This gets called on every frame until the llama touches the
            # ground
        Game.draw()
        llama.draw()
        Game.check_collisions(llama)
        Game.update_obstacles()
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
