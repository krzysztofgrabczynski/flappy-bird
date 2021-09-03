import pygame, sys
from player import Player
from pipes import Pipes
from button import Button
from random import randint


class Game():
    def __init__(self):
        # initialization pygame
        pygame.init()

        # setting game parameters
        self.fps = 120
        self.timer = 10000000
        self.background = pygame.image.load("image/background.png")
        self.width = self.background.get_width()
        self.height = self.background.get_height()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Flappy Bird")

        self.sounds = [pygame.mixer.Sound("sounds/sfx_hit.wav"),
                       pygame.mixer.Sound("sounds/sfx_point.wav"),
                       pygame.mixer.Sound("sounds/sfx_wing.wav"),
                       pygame.mixer.Sound("sounds/sfx_swooshing.wav")]

        self.scrolling_bg_x = 0
        self.scrolling_bg_speed = 0
        self.scrolling_bg_x_index = 0

        self.border_up = pygame.rect.Rect(0, 0, self.width, 1)
        self.border_down = pygame.rect.Rect(0, 705, self.width, 1)

        self.player = Player(self)
        self.score = 0
        self.score_index = 0
        self.score_tmp = 0
        self.score_check = True

        self.pipes_index = 0
        self.pipes_gap = 180
        self.pipes_list = [Pipes(self, 700, 500, 40, self.pipes_gap)]

        self.start_text = pygame.font.Font.render(pygame.font.SysFont("calibri", 18), "click space", True, (0, 0, 0))

        self.play_button = Button(self, 420, 325, "play_button", 165, 95)
        self.exit_button = Button(self, 415, 425, "exit_button", 165, 95)

        self.start_tick_info = False
        self.game_over_info = False
        self.click_SPACE_check = False
        self.run = False

        # initialization menu
        self.menu()

        #### main loop ###
        while self.run is True:
            pygame.time.Clock().tick(self.fps)
            if self.start_tick_info is False:
                self.start_tick()
            self.score_text = pygame.font.Font.render(pygame.font.SysFont("calibri", 48), str(self.score), True, (0, 0, 0))
            self.check_event()
            self.draw_background()
            if self.start_tick_info is True and self.game_over_info is False:
                self.player.tick()
                self.check_score()
            self.collisions()
            self.add_pipe()
            self.draw()
            pygame.display.update()

        # game definitions
    def menu(self):
        title = pygame.image.load("image/title.png")
        title = pygame.transform.scale(title, (550, 170))
        while True:
            self.check_event()
            if self.play_button.click() is True:
                self.run = True
                self.sounds[3].play()
                break
            if self.exit_button.click() is True:
                self.sounds[3].play()
                pygame.quit()
                sys.exit(0)
            self.window.blit(self.background, (0, 0))
            self.window.blit(title, (230, 80))
            self.play_button.draw()
            self.exit_button.draw()
            pygame.display.update()

    def draw(self):
        pygame.draw.rect(self.window, (0, 200, 200), self.border_up)
        pygame.draw.rect(self.window, (255, 255, 255), self.border_down)

        self.player.draw()

        for pipe in self.pipes_list:
            pipe.draw(self.scrolling_bg_x_index)

        if self.start_tick_info is False:
            self.window.blit(self.start_text, (self.player.player.x-25, self.player.player.y+40))
        if self.game_over_info is False:
            self.window.blit(self.score_text, (self.width/2, 20))

    def check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                self.click_SPACE_check = False

    def collisions(self):
        if self.player.player.colliderect(self.border_up):
            self.player.player.top = self.border_up.bottom - 1
            self.player.y_speed = 0
            self.player.y_acceleration = 0
            self.game_over()
        if self.player.player.colliderect(self.border_down):
            self.player.player.bottom = self.border_down.top
            self.player.y_speed = 0
            self.player.y_acceleration = 0
            self.game_over()

        for pipe in self.pipes_list:
            if pipe.pipe_bottom.colliderect(self.player.player):
                self.player.y_speed = 0
                self.player.y_acceleration = 0
                self.game_over()
            elif pipe.pipe_top.colliderect(self.player.player):
                self.player.y_speed = 0
                self.player.y_acceleration = 0
                self.game_over()

    def draw_background(self):
        # scrolling background definition
        self.window.blit(self.background, (self.scrolling_bg_x, 0))
        self.window.blit(self.background, (self.width+self.scrolling_bg_x, 0))
        if self.scrolling_bg_x <= - self.width:
            self.window.blit(self.background, (self.scrolling_bg_x, 0))
            self.scrolling_bg_x = 0
        self.scrolling_bg_x -= self.scrolling_bg_speed

        # increasing scrolling background speed by the score
        if self.score_check is True:
            self.score_tmp = self.score
        if self.score_tmp % 5 == 0 and self.score != 0 and self.score_check is True:
            self.scrolling_bg_speed += 1
            self.score_check = False
        if self.score_tmp != self.score:
            self.score_check = True

        if self.start_tick_info is True:
            self.scrolling_bg_x_index += self.scrolling_bg_speed

    def start_tick(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.game_over_info is False:
            self.scrolling_bg_speed = 4
            self.start_tick_info = True

    def game_over(self):
        self.sounds[0].play()
        self.game_over_info = True
        self.scrolling_bg_speed = 0

        self.draw()
        game_over_text = pygame.font.Font.render(pygame.font.SysFont("calibri", 180), "Score: " + str(self.score), True, (0, 0, 0))
        game_over_text.set_alpha(180)
        self.window.blit(game_over_text, (220, 280))
        pygame.display.update()
        while self.timer > 0:
            self.timer -= 1
        self.timer = 10000000

        pygame.quit()
        sys.exit(0)

    def add_pipe(self):
        random_y = randint(275, 625)
        if self.scrolling_bg_x_index % 400 == 0:
            self.pipes_list.append(Pipes(self, self.pipes_list[self.pipes_index].x + 400, random_y, 40, self.pipes_gap))
            self.pipes_index += 1

    def check_score(self):
        if self.player.player.left > self.pipes_list[self.score_index].pipe_bottom.left+30:
            self.score += 1
            self.score_index += 1
            self.sounds[1].play()


if __name__ == "__main__":
    Game()









