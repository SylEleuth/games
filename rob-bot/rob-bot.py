#       ______   _____   ______        ______    _____   _______
#      |_____/  |     |  |_____]  ___  |_____]  |     |     |
#      |    \_  |_____|  |_____]       |_____]  |_____|     |
#


import pygame


class Game:
    def __init__(self):
        pygame.init()

        self.load_assets()
        self.draw_map()

        # 1 - game background, 2 - panel background, 3 - normal text
        # 4 - walls, 5 - panel border
        self.colors = [
            (29, 32, 33),
            (40, 40, 40),
            (235, 219, 178),
            (69, 133, 136),
            (254, 128, 25),
        ]
        self.lives = 3

        self.pause = True  # start the game paused
        self.menu_start = True  # menu on start
        self.menu = False  # this menu is for paused game after start
        self.win = False  # and this menu is shown when You win
        self.lose = False  # and this one when losing

        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False

        self.robot_speed = 2
        self.ghost_speed = 2

        self.robot_starting_position()
        self.ghosts_starting_position()

        self.window_width = self.wall_size * self.map_width
        self.window_height = self.wall_size * self.map_height
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        self.clock = pygame.time.Clock()

        pygame.display.set_caption("Rob-bot")

    def load_assets(self):
        try:
            self.robot = pygame.transform.scale(pygame.image.load("robot.png"), (40, 40))

            self.coin = pygame.transform.scale(pygame.image.load("coin.png"), (10, 10))

            self.door = pygame.image.load("door.png")

            # I need four different variables becasue each ghost has different starting
            # position and moves in a different direction
            self.ghost_1 = pygame.transform.scale(
                pygame.image.load("monster.png"), (40, 40)
            )
            self.ghost_2 = pygame.transform.scale(
                pygame.image.load("monster.png"), (40, 40)
            )
            self.ghost_3 = pygame.transform.scale(
                pygame.image.load("monster.png"), (40, 40)
            )
            self.ghost_4 = pygame.transform.scale(
                pygame.image.load("monster.png"), (40, 40)
            )
        except:
            print("Couldn't load one or more assets!")
            quit()

    def render_text(self, string: str, size: int, color: int, shift: int = 0):
        self.font = pygame.font.SysFont("sans-serif", size)

        text = self.font.render(string, True, self.colors[color - 1])

        text_rect = text.get_rect(
            center=(self.window_width // 2, (self.window_height // 2) + shift)
        )

        self.window.blit(text, text_rect)

    def draw_map(self):
        # 0 - corridors where coins are and where robot can move
        # 1 - walls
        # 2 - same as 0 but without coins

        self.map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        self.map_width = len(self.map[0])
        self.map_height = len(self.map)
        self.wall_size = 40

        self.walls: list = []
        self.coins: list = []

        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.map[y][x] == 1:
                    self.walls.append(
                        pygame.Rect(
                            x * self.wall_size,
                            y * self.wall_size,
                            self.wall_size,
                            self.wall_size,
                        )
                    )

                if self.map[y][x] == 0:
                    center_x = self.wall_size // 2
                    center_y = self.wall_size // 2
                    self.coins.append(
                        self.coin.get_rect(
                            center=(
                                (x * self.wall_size) + center_x,
                                (y * self.wall_size) + center_y,
                            )
                        )
                    )

    def keymapping(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_right = False
                    self.to_up = False
                    self.to_down = False
                    self.to_left = True

                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                    self.to_left = False
                    self.to_up = False
                    self.to_down = False

                if event.key == pygame.K_UP:
                    self.to_up = True
                    self.to_right = False
                    self.to_left = False
                    self.to_down = False

                if event.key == pygame.K_DOWN:
                    self.to_down = True
                    self.to_right = False
                    self.to_left = False
                    self.to_up = False

                # Game starts paused and using Escape won't work
                # Also won't work when win or lose panel is displayed
                # It will only work when the game is already running
                if event.key == pygame.K_ESCAPE:
                    if self.menu_start:
                        self.pause = True

                    elif not self.menu_start or not self.win or not self.lose:
                        self.pause = not self.pause
                        self.menu = not self.menu

                # Key options when game starts
                if self.pause and self.menu_start:
                    # "s" will just remove panel and reveal the game
                    if event.key == pygame.K_s:
                        self.pause = not self.pause
                        self.menu_start = not self.menu_start

                    if event.key == pygame.K_q:
                        quit()

                # Key options if Escape is used during game, You've lost or won
                if self.menu or self.win or self.lose:
                    # Reset the game
                    if event.key == pygame.K_n:
                        # self.menu = not self.menu
                        self.pause = not self.pause
                        self.new_game()

                    if event.key == pygame.K_q:
                        quit()

    def create_exit(self):
        window_center_x = self.window_width // 2
        window_center_y = self.window_height // 2

        robot_center_x = self.robot_x + self.robot.get_width() // 2
        robot_center_y = self.robot_y + self.robot.get_height() // 2

        door_rect = self.door.get_rect(center=(window_center_x, window_center_y))
        self.window.blit(self.door, door_rect)

        if (
            window_center_x - 10 < robot_center_x < window_center_x + 10
            and window_center_y - 20 < robot_center_y < window_center_y + 20
        ):
            self.pause = True
            self.win = True

    def ghosts_starting_position(self):
        self.ghost_1_x = self.wall_size * 4
        self.ghost_1_y = self.wall_size * 8
        self.ghost_2_x = self.wall_size * 12
        self.ghost_2_y = self.wall_size * 8
        self.ghost_3_x = self.wall_size * 8
        self.ghost_3_y = self.wall_size * 3
        self.ghost_4_x = self.wall_size * 8
        self.ghost_4_y = self.wall_size * 13

    def robot_starting_position(self):
        self.robot_x = self.wall_size * 8
        self.robot_y = self.wall_size * 8

    def add_ghosts(self):
        self.ghost_1_rect = self.ghost_1.get_rect(
            topleft=(self.ghost_1_x, self.ghost_1_y)
        )
        self.ghost_2_rect = self.ghost_2.get_rect(
            topleft=(self.ghost_2_x, self.ghost_2_y)
        )
        self.ghost_3_rect = self.ghost_3.get_rect(
            topleft=(self.ghost_3_x, self.ghost_3_y)
        )
        self.ghost_4_rect = self.ghost_4.get_rect(
            topleft=(self.ghost_4_x, self.ghost_4_y)
        )

        self.ghost_1_y += self.ghost_speed
        self.ghost_2_y -= self.ghost_speed
        self.ghost_3_x += self.ghost_speed
        self.ghost_4_x -= self.ghost_speed

    def collision_detection(self):
        if self.lives == 0:
            self.pause = True
            self.lose = True

        for wall in self.walls:
            robot_contact = wall.colliderect(
                self.robot_x,
                self.robot_y,
                self.robot.get_width(),
                self.robot.get_height(),
            )

            if robot_contact:
                if self.to_left:
                    self.robot_x += self.robot_speed

                if self.to_right:
                    self.robot_x -= self.robot_speed

                if self.to_up:
                    self.robot_y += self.robot_speed

                if self.to_down:
                    self.robot_y -= self.robot_speed

            ghost_contact = wall.colliderect(
                self.ghost_1_x,
                self.ghost_1_y,
                self.ghost_1.get_width(),
                self.ghost_1.get_height(),
            )

            if ghost_contact:
                if self.ghost_speed > 0:
                    self.ghost_speed = -2
                else:
                    self.ghost_speed = 2

        for coin in self.coins:
            robot_contact = coin.colliderect(
                self.robot_x,
                self.robot_y,
                self.robot.get_width(),
                self.robot.get_height(),
            )

            if robot_contact:
                self.coins.remove(coin)

        # make the rect for the robot little smaller than it's size
        # to overlap a ghost when in contact
        ghost_1_contact = self.ghost_1_rect.colliderect(
            self.robot_x + 15,
            self.robot_y + 15,
            self.robot.get_width() - 30,
            self.robot.get_height() - 30,
        )

        ghost_2_contact = self.ghost_2_rect.colliderect(
            self.robot_x + 15,
            self.robot_y + 15,
            self.robot.get_width() - 30,
            self.robot.get_height() - 30,
        )

        ghost_3_contact = self.ghost_3_rect.colliderect(
            self.robot_x + 15,
            self.robot_y + 15,
            self.robot.get_width() - 30,
            self.robot.get_height() - 30,
        )

        ghost_4_contact = self.ghost_4_rect.colliderect(
            self.robot_x + 15,
            self.robot_y + 15,
            self.robot.get_width() - 30,
            self.robot.get_height() - 30,
        )

        if ghost_1_contact or ghost_2_contact or ghost_3_contact or ghost_4_contact:
            self.robot_starting_position()
            self.ghosts_starting_position()
            self.to_right = False
            self.to_left = False
            self.to_up = False
            self.to_down = False
            pygame.time.delay(1000)
            self.lives -= 1

    def robot_movement(self):
        if self.to_left:
            self.robot_x -= self.robot_speed

        if self.to_right:
            self.robot_x += self.robot_speed

        if self.to_up:
            self.robot_y -= self.robot_speed

        if self.to_down:
            self.robot_y += self.robot_speed

        # Corridor in the middle of the map is connected on both sides
        if self.robot_y == 320:
            if self.robot_x < 0 - self.robot.get_width():
                self.robot_x = self.window_width
            if self.robot_x > self.window_width:
                self.robot_x = 0 - self.robot.get_width()

    def new_game(self):
        self.robot_starting_position()
        self.ghosts_starting_position()
        self.win = False
        self.lose = False
        self.lives = 3
        self.draw_map()

    def draw_window(self):
        for wall in self.walls:
            pygame.draw.rect(self.window, self.colors[3], wall)

        for coin in self.coins:
            self.window.blit(self.coin, coin)

        self.window.blit(self.ghost_1, self.ghost_1_rect)
        self.window.blit(self.ghost_2, self.ghost_2_rect)
        self.window.blit(self.ghost_3, self.ghost_3_rect)
        self.window.blit(self.ghost_4, self.ghost_4_rect)

        self.render_text(f"Lives: {self.lives}", 36, 1, -320)

        if len(self.coins) == 0:
            self.create_exit()

        self.window.blit(self.robot, (self.robot_x, self.robot_y))

    def pause_window(self):
        # stop the robot
        self.to_right = False
        self.to_left = False
        self.to_up = False
        self.to_down = False

        pygame.draw.rect(
            self.window,
            self.colors[4],
            (0, 0, self.window_width, self.window_height),
        )
        pygame.draw.rect(
            self.window,
            self.colors[1],
            (10, 10, self.window_width - 20, self.window_height - 20),
        )

        if self.menu_start:
            self.start_panel()

        if self.menu:
            self.menu_panel()

        if self.win:
            pygame.time.delay(500)
            self.win_panel()

        if self.lose:
            self.lose_panel()

    def start_panel(self):
        info_text: list = []
        line_shift = 28

        robot_text = "R O B - B O T"

        info_text.append('"Rob-bot" is very simple clone of famous Pac-man game')
        info_text.append("To finish it You have to gather all coins")
        info_text.append(
            "When You'll do it, the door will appear in the middle of the map"
        )
        info_text.append("Going through them will end the game")
        info_text.append(
            "You start with 3 lives, everytime You bump on a ghost You'll lose one"
        )
        info_text.append("Number of lives left is displayed at the top of the screen")
        info_text.append("When You lose all 3 the game is over")
        info_text.append("After that You can start again")

        menu_text1 = 'Press "q" to quit'
        menu_text2 = 'Press "s" to start'

        self.render_text(robot_text, 140, 5, -200)

        for t in info_text:
            self.render_text(t, 28, 3, -120 + line_shift)
            line_shift += 28

        self.render_text(menu_text1, 28, 3, 175)
        self.render_text(menu_text2, 28, 3, 225)

    def menu_panel(self):
        robot_text = "R O B - B O T"
        pause_text = 'Game paused, press "Escape" key to resume'
        or_text = "or"
        quit_text = 'Press "q" to quit'
        start_text = 'Press "n" to start a new game'
        self.render_text(robot_text, 140, 5, -200)
        self.render_text(pause_text, 28, 3, -50)
        self.render_text(or_text, 28, 3, 25)
        self.render_text(quit_text, 28, 3, 100)
        self.render_text(start_text, 28, 3, 150)

    def win_panel(self):
        win_text1 = "Congratulations! You've won!"
        win_text2 = 'Press "q" to quit'
        win_text3 = 'Press "n" to start a new game'
        self.render_text(win_text1, 46, 3, -130)
        self.render_text(win_text2, 28, 3, 10)
        self.render_text(win_text3, 28, 3, 50)

    def lose_panel(self):
        win_text1 = "I'm sorry but You've lost"
        win_text2 = 'Press "q" to quit'
        win_text3 = 'Press "n" to start a new game'
        self.render_text(win_text1, 46, 3, -130)
        self.render_text(win_text2, 28, 3, 10)
        self.render_text(win_text3, 28, 3, 50)

    def main_loop(self):
        while True:
            self.keymapping()
            self.robot_movement()
            self.add_ghosts()
            self.collision_detection()

            self.window.fill(self.colors[0])

            if self.pause:
                self.pause_window()
            else:
                self.draw_window()

            pygame.display.update()
            self.clock.tick(60)


Game().main_loop()
