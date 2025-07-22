import pygame
import random
import tiles
import Timer
import os
import sys


def resource_path(path: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(getattr(sys, "_MEIPASS"), os.path.normpath(path))
    else:
        return os.path.join(os.path.dirname(__file__), os.path.normpath(path))


class Game:
    def __init__(self):
        pygame.init()
        self.monitor_size = pygame.display.Info()
        self.font = pygame.font.SysFont("Times New Roman", 40)
        self.small_font = pygame.font.SysFont("Times New Roman", 20)
        pygame.display.set_caption("Piano Tiles")
        pygame.display.set_icon(pygame.image.load(resource_path("Images/Icon.png")))
        self.screen = pygame.display.set_mode((285, 510), pygame.RESIZABLE)
        self.enter_full_screen_icon = pygame.image.load(resource_path("Images/Enter Fullscreen Icon.png")).convert_alpha()
        self.exit_full_screen_icon = pygame.image.load(resource_path("Images/Exit Fullscreen Icon.png")).convert_alpha()
        self.menu_icon = pygame.image.load(resource_path("Images/Menu.png")).convert_alpha()
        self.window_width = 285
        self.window_height = 510
        self.screen_width = 285
        self.screen_height = 510
        self.text = ["Click the black tiles in order from", "bottom to top as they move down", "the screen. Click and hold the", "bottom of the long tiles, and a bar", "will start moving up the long tile", "as the long tile moves down. Let", "go when the bar reaches the top", "of the long tile. If a tile moves out", "of the bottom of the screen", "without getting clicked, or you", "accidentally click the background,", "you lose.", "", "Written in Python, made using", "Pygame."]
        self.song_list = ["Snail Speed", "Medium", "Impossible", "Progressive"]
        self.song = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.starting_speed = [25, 55, 85, 10]
        self.speed_increase = [5, 15, 5, 40]
        self.speed_up = 1
        self.speed_up_animation = False
        self.speed_up_target = 0
        self.selected_song = 0
        self.song_num = 0
        self.score = 0
        self.high_score = 0
        self.page_num = 0
        self.total_page_num = 0
        self.tile_list = []
        self.started = False
        self.tile_num = 0
        self.tile_generated = 0
        self.tile_clicked = 0
        self.first_frame = True
        self.mistake_first_frame = False
        self.result_first_frame = False
        self.tile_missed = False
        self.animate_reverse = False
        self.blink_timer = Timer.timer()
        self.blink_count = 0
        self.click_pos = 0
        if len(self.song_list) % 5 == 0:
            self.total_page_num = len(self.song_list) // 5
        else:
            self.total_page_num = len(self.song_list) // 5 + 1
        self.mode = "Main"
        self.full_screen = False
        self.display = True
        self.gameRun = True
        self.fps = 30
        self.clock = pygame.time.Clock()
        while self.gameRun:
            self.clock.tick(self.fps)
            if self.mode == "Main":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if mouse_pos[0] > self.screen_width - 28 and mouse_pos[0] < self.screen_width - 2 and mouse_pos[1] > self.screen_height - 28 and mouse_pos[1] < self.screen_height - 2:
                            self.full_screen = not self.full_screen
                            if self.full_screen:
                                self.screen = pygame.display.set_mode((self.monitor_size.current_w, self.monitor_size.current_h), pygame.FULLSCREEN)
                            else:
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                        elif mouse_pos[0] > 0 and mouse_pos[0] < self.screen_width and mouse_pos[1] > 0 and mouse_pos[1] < self.screen_height // 2:
                            self.mode = "Song_Select"
                        elif mouse_pos[0] > 0 and mouse_pos[0] < self.screen_width and mouse_pos[1] > self.screen_height // 2 and mouse_pos[1] < self.screen_height - 28:
                            self.mode = "About"
                    elif event.type == pygame.VIDEORESIZE:
                        if not self.full_screen:
                            self.window_width = event.w
                            self.window_height = event.h
                            if self.window_width < 285:
                                self.window_width = 285
                            if self.window_height < 510:
                                self.window_height = 510
                            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.full_screen:
                                self.full_screen = False
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                self.screen_size = pygame.display.Info()
                self.screen_width = self.screen_size.current_w
                self.screen_height = self.screen_size.current_h
                self.screen.fill((255, 255, 255))
                pygame.draw.rect(self.screen, (0, 0, 0), [0, 0, self.screen_width, self.screen_height // 2], 0)
                self.screen.blit(self.font.render("Start", False, (255, 255, 255)), (self.screen_width // 2 - self.font.size("Start")[0] // 2, self.screen_height // 4 - self.font.size("Start")[1] // 2))
                self.screen.blit(self.font.render("About", False, (0, 0, 0)), (self.screen_width // 2 - self.font.size("About")[0] // 2, self.screen_height // 4 * 3 - self.font.size("About")[1] // 2))
                if self.full_screen:
                    self.screen.blit(self.exit_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                else:
                    self.screen.blit(self.enter_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                pygame.display.update()
            elif self.mode == "Song_Select":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if mouse_pos[0] > self.screen_width - 28 and mouse_pos[0] < self.screen_width - 2 and mouse_pos[1] > self.screen_height - 28 and mouse_pos[1] < self.screen_height - 2:
                            self.full_screen = not self.full_screen
                            if self.full_screen:
                                self.screen = pygame.display.set_mode((self.monitor_size.current_w, self.monitor_size.current_h), pygame.FULLSCREEN)
                            else:
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                        elif mouse_pos[0] > 5 and mouse_pos[0] < 5 + self.small_font.size("Previous")[0] and mouse_pos[1] > self.screen_height - self.small_font.size("Previous")[1] - 25 and mouse_pos[1] < self.screen_height - 25:
                            if self.page_num > 0:
                                self.page_num -= 1
                        elif mouse_pos[0] > self.screen_width - self.small_font.size("Next")[0] - 5 and mouse_pos[0] < self.screen_width - 5 and mouse_pos[1] > self.screen_height - self.small_font.size("Next")[1] - 25 and mouse_pos[1] < self.screen_height - 25:
                            if self.page_num + 1 < self.total_page_num:
                                self.page_num += 1
                        elif mouse_pos[0] > self.screen_width // 2 - self.small_font.size("Back")[0] // 2 and mouse_pos[0] < self.screen_width // 2 + self.small_font.size("Back")[0] // 2 and mouse_pos[1] > self.screen_height - 20 and mouse_pos[1] < self.screen_height:
                            self.mode = "Main"
                        else:
                            self.song_num = 0
                            for song in range(self.page_num * 5, self.page_num * 5 + 5):
                                if mouse_pos[0] > self.screen_width - 75 and mouse_pos[0] < self.screen_width - 60 + self.small_font.size("Start")[0] + 15 and mouse_pos[1] > self.song_num * 55 + 23 and mouse_pos[1] < self.song_num * 55 + 53:
                                    self.selected_song = self.page_num * 5 + self.song_num
                                    self.tile_generated = 0
                                    self.tile_num = 1
                                    self.mode = "Game"
                                    row = random.randint(1, 4)
                                    self.tile_list.append(tiles.tile(row, self.screen_height - self.tile_num * 132))
                                    self.tile_num = 2
                                    while self.screen_height - (self.tile_num - 1) * 132 >= 0 and self.tile_generated < len(self.song[self.selected_song]):
                                        row = random.randint(1, 4)
                                        if self.tile_list[self.tile_num - 2].row == row:
                                            ran = random.randint(0, 1)
                                            if self.tile_list[self.tile_num - 2].row == 1:
                                                row = random.randint(2, 4)
                                            elif self.tile_list[self.tile_num - 2].row == 2:
                                                if ran == 0:
                                                    row = 1
                                                else:
                                                    row = random.randint(3, 4)
                                            elif self.tile_list[self.tile_num - 2].row == 3:
                                                if ran == 1:
                                                    row = random.randint(1, 2)
                                                else:
                                                    row = 4
                                            elif self.tile_list[self.tile_num - 2].row == 4:
                                                row = random.randint(1, 3)
                                        self.tile_list.append(tiles.tile(row, self.screen_height - self.tile_num * 132))
                                        self.tile_generated += 1
                                        self.tile_num += 1
                                    self.fps = self.starting_speed[self.selected_song]
                                    break
                                self.song_num += 1
                    elif event.type == pygame.VIDEORESIZE:
                        if not self.full_screen:
                            self.window_width = event.w
                            self.window_height = event.h
                            if self.window_width < 285:
                                self.window_width = 285
                            if self.window_height < 510:
                                self.window_height = 510
                            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.full_screen:
                                self.full_screen = False
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                self.song_num = 0
                self.screen_size = pygame.display.Info()
                self.screen_width = self.screen_size.current_w
                self.screen_height = self.screen_size.current_h
                self.screen.fill((0, 255, 255))
                for song in range(self.page_num * 5, self.page_num * 5 + 5):
                    if song < len(self.song_list):
                        pygame.draw.rect(self.screen, (255, 255, 255), [4, self.song_num * 55 + 4, self.screen_width - 8, 50], 0)
                        self.screen.blit(self.small_font.render(self.song_list[song], False, (0, 0, 0)), (8, self.song_num * 55 + 4))
                        pygame.draw.circle(self.screen, (55, 255, 255), [self.screen_width - 60, self.song_num * 55 + 38], 15, 0)
                        pygame.draw.rect(self.screen, (55, 255, 255), [self.screen_width - 60, self.song_num * 55 + 23, self.small_font.size("Start")[0], 30], 0)
                        pygame.draw.circle(self.screen, (55, 255, 255), [self.screen_width - 60 + self.small_font.size("Start")[0], self.song_num * 55 + 38], 15, 0)
                        self.screen.blit(self.small_font.render("Start", False, (0, 0, 0)), (self.screen_width - 60, self.song_num * 55 + 26))
                        self.song_num += 1
                    else:
                        break
                self.screen.blit(self.small_font.render("Previous", False, (0, 0, 0)), (5, self.screen_height - self.small_font.size("Previous")[1] - 25))
                self.screen.blit(self.small_font.render("Next", False, (0, 0, 0)), (self.screen_width - self.small_font.size("Next")[0] - 5, self.screen_height - self.small_font.size("Next")[1] - 25))
                self.screen.blit(self.small_font.render(str(self.page_num + 1) + "/" + str(self.total_page_num), False, (0, 0, 0)), (self.screen_width // 2 - self.small_font.size(str(self.page_num + 1) + "/" + str(self.total_page_num))[0] // 2, self.screen_height - self.small_font.size(str(self.page_num + 1) + "/" + str(self.total_page_num))[1] - 25))
                self.screen.blit(self.small_font.render("Back", False, (0, 0, 0)), (self.screen_width // 2 - self.small_font.size("Back")[0] // 2, self.screen_height - 20))
                if self.full_screen:
                    self.screen.blit(self.exit_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                else:
                    self.screen.blit(self.enter_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                pygame.display.update()
            elif self.mode == "About":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if mouse_pos[0] > self.screen_width - 28 and mouse_pos[0] < self.screen_width - 2 and mouse_pos[1] > self.screen_height - 28 and mouse_pos[1] < self.screen_height - 2:
                            self.full_screen = not self.full_screen
                            if self.full_screen:
                                self.screen = pygame.display.set_mode((self.monitor_size.current_w, self.monitor_size.current_h), pygame.FULLSCREEN)
                            else:
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                        elif mouse_pos[0] > self.screen_width // 2 - self.small_font.size("Back")[0] // 2 and mouse_pos[0] < self.screen_width // 2 + self.small_font.size("Back")[0] // 2 and mouse_pos[1] > 290 and mouse_pos[1] < 290 + self.small_font.size("Back")[1]:
                            self.mode = "Main"
                    elif event.type == pygame.VIDEORESIZE:
                        if not self.full_screen:
                            self.window_width = event.w
                            self.window_height = event.h
                            if self.window_width < 285:
                                self.window_width = 285
                            if self.window_height < 510:
                                self.window_height = 510
                            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.full_screen:
                                self.full_screen = False
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                self.screen_size = pygame.display.Info()
                self.screen_width = self.screen_size.current_w
                self.screen_height = self.screen_size.current_h
                self.screen.fill((255, 255, 255))
                for line in range(0, len(self.text)):
                    self.screen.blit(self.small_font.render(self.text[line], True, (0, 0, 0)), (self.screen_width // 2 - 140, 19 * line))
                if self.full_screen:
                    self.screen.blit(self.exit_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                else:
                    self.screen.blit(self.enter_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                self.screen.blit(self.small_font.render("Back", True, (0, 0, 0)), (self.screen_width // 2 - self.small_font.size("Back")[0] // 2, 290))
                pygame.display.update()
            elif self.mode == "Game":
                rect_list = []
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if self.started:
                            if self.tile_clicked < len(self.tile_list):
                                if mouse_pos[0] >= self.tile_list[self.tile_clicked].pos_x and mouse_pos[0] <= self.tile_list[self.tile_clicked].pos_x + self.tile_list[self.tile_clicked].width and mouse_pos[1] >= self.tile_list[self.tile_clicked].pos_y and mouse_pos[1] <= self.tile_list[self.tile_clicked].pos_y + self.tile_list[self.tile_clicked].height and (not self.tile_list[self.tile_clicked].clicked):
                                    self.tile_list[self.tile_clicked].clicked = True
                                    self.tile_list[self.tile_clicked].color = (184, 184, 184)
                                    self.tile_clicked += 1
                                    self.score += 1
                                elif mouse_pos[1] >= self.tile_list[0].pos_y and self.score == 0:
                                    pass
                                else:
                                    found = False
                                    for tile in self.tile_list:
                                        if mouse_pos[0] >= tile.pos_x and mouse_pos[0] <= tile.pos_x + tile.width and mouse_pos[1] >= tile.pos_y and mouse_pos[1] <= tile.pos_y + tile.height:
                                            found = True
                                            break
                                    if not found:
                                        if mouse_pos[1] > self.tile_list[len(self.tile_list) - 1].pos_y:
                                            self.click_pos = mouse_pos
                                            self.tile_missed = False
                                            self.mistake_first_frame = True
                                            self.mode = "Mistake"
                            elif self.tile_list[len(self.tile_list) - 1].clicked:
                                found = False
                                for tile in self.tile_list:
                                    if mouse_pos[0] >= tile.pos_x and mouse_pos[0] <= tile.pos_x + tile.width and mouse_pos[1] >= tile.pos_y and mouse_pos[1] <= tile.pos_y + tile.height:
                                        found = True
                                        break
                                if not found:
                                    if mouse_pos[1] > self.tile_list[len(self.tile_list) - 1].pos_y:
                                        self.click_pos = mouse_pos
                                        self.tile_missed = False
                                        self.mistake_first_frame = True
                                        self.mode = "Mistake"
                        else:
                            if mouse_pos[0] > self.tile_list[0].pos_x and mouse_pos[0] < self.tile_list[0].pos_x + self.tile_list[0].width and mouse_pos[1] > self.tile_list[0].pos_y and mouse_pos[1] < self.tile_list[0].pos_y + self.tile_list[0].height:
                                rect_list.append(pygame.Rect(self.tile_list[0].pos_x, self.tile_list[0].pos_y, self.tile_list[0].width, self.tile_list[0].height))
                                self.tile_list.pop(0)
                                self.started = True
                    elif event.type == pygame.VIDEORESIZE:
                        self.first_frame = True
                        if not self.full_screen:
                            self.window_width = event.w
                            self.window_height = event.h
                            if self.window_width < 285:
                                self.window_width = 285
                            if self.window_height < 510:
                                self.window_height = 510
                            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.full_screen:
                                self.full_screen = False
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                if self.speed_up != 0:
                    if self.speed_up == 1:
                        if self.tile_generated == len(self.song[self.selected_song]) // 3:
                            self.speed_up_animation = True
                            self.speed_up_target = self.fps + self.speed_increase[self.selected_song]
                            self.speed_up = 2
                    elif self.speed_up == 2:
                        if self.tile_generated == len(self.song[self.selected_song]) // 3 * 2:
                            self.speed_up_animation = True
                            self.speed_up_target = self.fps + self.speed_increase[self.selected_song]
                            self.speed_up = 0
                if self.speed_up_animation and self.fps < self.speed_up_target:
                    self.fps += 1
                self.screen_size = pygame.display.Info()
                self.screen_width = self.screen_size.current_w
                self.screen_height = self.screen_size.current_h
                self.screen.fill((255, 255, 255))
                if self.started:
                    for tile in range(0, len(self.tile_list)):
                        if self.mode == "Game":
                            self.tile_list[tile].update(self.screen_width)
                            self.tile_list[tile].move(5)
                        if self.tile_list[tile].pos_y >= 0 and self.tile_list[tile].pos_y + self.tile_list[tile].height <= self.screen_height:
                            pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height], 0)
                        elif self.tile_list[tile].pos_y < 0:
                            pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, 0, self.tile_list[tile].width, self.tile_list[tile].height + self.tile_list[tile].pos_y], 0)
                        elif self.tile_list[tile].pos_y + self.tile_list[tile].height > self.screen_height and self.tile_list[tile].pos_y < self.screen_height:
                            pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height - (self.tile_list[tile].pos_y + self.tile_list[tile].height - self.screen_height)], 0)
                    self.screen.blit(self.font.render(str(self.score), False, (255, 0, 0)), (self.screen_width // 2 - self.font.size(str(self.score))[0] // 2, 0))
                    if self.tile_generated < len(self.song[self.selected_song]):
                        if self.tile_list[len(self.tile_list) - 1].pos_y > -5:
                            row = random.randint(1, 4)
                            if self.tile_list[len(self.tile_list) - 1].row == row:
                                ran = random.randint(0, 1)
                                if self.tile_list[len(self.tile_list) - 1].row == 1:
                                    row = random.randint(2, 4)
                                elif self.tile_list[len(self.tile_list) - 1].row == 2:
                                    if ran == 0:
                                        row = 1
                                    else:
                                        row = random.randint(3, 4)
                                elif self.tile_list[len(self.tile_list) - 1].row == 3:
                                    if ran == 1:
                                        row = random.randint(1, 2)
                                    else:
                                        row = 4
                                elif self.tile_list[len(self.tile_list) - 1].row == 4:
                                    row = random.randint(1, 3)
                            self.tile_generated += 1
                            if self.tile_clicked >= len(self.song[self.selected_song]):
                                pass
                            else:
                                self.tile_list.append(tiles.tile(row, -132))
                    tile = 0
                    while tile < len(self.tile_list):
                        if self.tile_list[tile].pos_y >= self.screen_height:
                            if self.tile_list[tile].clicked:
                                self.tile_list.pop(tile)
                                self.tile_clicked -= 1
                            else:
                                if self.mode == "Game":
                                    self.tile_missed = True
                                    self.mistake_first_frame = True
                                    self.result_first_frame = True
                                    self.mode = "Mistake"
                        tile += 1
                    if len(self.tile_list) == 0:
                        self.fps = 30
                        self.result_first_frame = True
                        self.mode = "Result"
                else:
                    for tile in range(0, len(self.tile_list)):
                        self.tile_list[tile].update(self.screen_width)
                        if self.tile_list[tile].pos_y >= 0 and self.tile_list[tile].pos_y + self.tile_list[tile].height <= self.screen_height:
                            pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height], 0)
                        elif self.tile_list[tile].pos_y < 0:
                            pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, 0, self.tile_list[tile].width, self.tile_list[tile].height + self.tile_list[tile].pos_y], 0)
                        elif self.tile_list[tile].pos_y + self.tile_list[tile].height > self.screen_height and self.tile_list[tile].pos_y < self.screen_height:
                            pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height - (self.tile_list[tile].pos_y + self.tile_list[tile].height - self.screen_height)], 0)
                    self.screen.blit(self.small_font.render("Start", True, (255, 255, 255)), (self.tile_list[0].pos_x + 15, self.tile_list[0].pos_y + 50))
                    self.screen.blit(self.font.render("0", False, (255, 0, 0)), (self.screen_width // 2 - self.font.size("0")[0] // 2, 0))
                if self.first_frame:
                    self.first_frame = False
                    pygame.display.update()
                else:
                    for tile in range(len(self.tile_list)):
                        if self.tile_list[tile].pos_y >= 0 and self.tile_list[tile].pos_y + self.tile_list[tile].height <= self.screen_height:
                            rect_list.append(pygame.Rect(self.tile_list[tile].pos_x, self.tile_list[tile].pos_y - 5, self.tile_list[tile].width, self.tile_list[tile].height + 5))
                        elif self.tile_list[tile].pos_y < 0:
                            rect_list.append(pygame.Rect(self.tile_list[tile].pos_x, 0, self.tile_list[tile].width, self.tile_list[tile].height + self.tile_list[tile].pos_y))
                        elif self.tile_list[tile].pos_y + self.tile_list[tile].height > self.screen_height and self.tile_list[tile].pos_y < self.screen_height:
                            rect_list.append(pygame.Rect(self.tile_list[tile].pos_x, self.tile_list[tile].pos_y - 5, self.tile_list[tile].width, (self.tile_list[tile].height + 5) - (self.tile_list[tile].pos_y + self.tile_list[tile].height - self.screen_height)))
                    rect_list.append(pygame.Rect(0, self.screen_height - 5, self.screen_width, 5))
                    rect_list.append(pygame.Rect(self.screen_width // 2 - self.font.size(str(self.score))[0] // 2, 0, self.font.size(str(self.score))[0], self.font.size(str(self.score))[1]))
                    pygame.display.update(rect_list)
            elif self.mode == "Mistake":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.VIDEORESIZE:
                        self.first_frame = True
                        if not self.full_screen:
                            self.window_width = event.w
                            self.window_height = event.h
                            if self.window_width < 285:
                                self.window_width = 285
                            if self.window_height < 510:
                                self.window_height = 510
                            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.full_screen:
                                self.full_screen = False
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                self.screen_size = pygame.display.Info()
                self.screen_width = self.screen_size.current_w
                self.screen_height = self.screen_size.current_h
                if self.mistake_first_frame:
                    self.fps = 30
                    if self.tile_missed:
                        self.animate_reverse = True
                    else:
                        row = 0
                        while not self.click_pos[1] >= self.tile_list[0].pos_y - 132 * row and self.click_pos[1] <= self.tile_list[0].pos_y - 132 * row + 132:
                            row += 1
                        if self.tile_list[row].pos_y + self.tile_list[row].height >= self.screen_height or self.tile_list[row].pos_y <= 0:
                            self.animate_reverse = True
                    mistake_first_frame_width = self.screen_width
                    mistake_first_frame_height = self.screen_height
                    self.mistake_first_frame = False
                if self.animate_reverse:
                    if self.tile_missed:
                        if self.tile_list[0].pos_y + self.tile_list[0].height >= self.screen_height:
                            for tile in range(0, len(self.tile_list)):
                                self.tile_list[tile].pos_y -= 5
                        else:
                            self.animate_reverse = False
                    else:
                        if self.tile_list[row].pos_y + self.tile_list[row].height >= self.screen_height:
                            for tile in range(0, len(self.tile_list)):
                                self.tile_list[tile].pos_y -= 5
                        elif self.tile_list[row].pos_y <= 0:
                            for tile in range(0, len(self.tile_list)):
                                self.tile_list[tile].pos_y += 5
                        else:
                            self.animate_reverse = False
                if not self.blink_timer.is_initialized():
                    self.blink_timer.reset()
                if self.blink_timer.get_time() > 0.3 and self.blink_timer.is_initialized() and (not self.animate_reverse):
                    self.display = not self.display
                    self.blink_count += 1
                    self.blink_timer.reset()
                if self.blink_count > 6:
                    self.result_first_frame = True
                    self.mode = "Result"
                self.screen.fill((255, 255, 255))
                for tile in range(0, len(self.tile_list)):
                    if tile == 0 and self.tile_missed and (not self.animate_reverse):
                        self.tile_list[0].update(self.screen_width)
                        if self.display:
                            if self.tile_list[tile].pos_y >= 0 and self.tile_list[tile].pos_y + self.tile_list[tile].height <= self.screen_height:
                                pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height], 0)
                            elif self.tile_list[tile].pos_y < 0:
                                pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, 0, self.tile_list[tile].width, self.tile_list[tile].height + self.tile_list[tile].pos_y], 0)
                            elif self.tile_list[tile].pos_y + self.tile_list[tile].height > self.screen_height and self.tile_list[tile].pos_y < self.screen_height:
                                pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height - (self.tile_list[tile].pos_y + self.tile_list[tile].height - self.screen_height)], 0)
                        else:
                            continue
                    self.tile_list[tile].update(self.screen_width)
                    if self.tile_list[tile].pos_y >= 0 and self.tile_list[tile].pos_y + self.tile_list[tile].height <= self.screen_height:
                        pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height], 0)
                    elif self.tile_list[tile].pos_y < 0:
                        pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, 0, self.tile_list[tile].width, self.tile_list[tile].height + self.tile_list[tile].pos_y], 0)
                    elif self.tile_list[tile].pos_y + self.tile_list[tile].height > self.screen_height and self.tile_list[tile].pos_y < self.screen_height:
                        pygame.draw.rect(self.screen, self.tile_list[tile].color, [self.tile_list[tile].pos_x, self.tile_list[tile].pos_y, self.tile_list[tile].width, self.tile_list[tile].height - (self.tile_list[tile].pos_y + self.tile_list[tile].height - self.screen_height)], 0)
                if (not self.tile_missed) and self.display:
                    if self.click_pos[0] > mistake_first_frame_width // 2 - 142 and self.click_pos[0] < mistake_first_frame_width // 2 - 71:
                        pygame.draw.rect(self.screen, (255, 0, 0), [self.screen_width // 2 - 142, self.tile_list[row].pos_y, 71, 132], 0)
                    elif self.click_pos[0] >= mistake_first_frame_width // 2 - 71 and self.click_pos[0] < mistake_first_frame_width // 2:
                        pygame.draw.rect(self.screen, (255, 0, 0), [self.screen_width // 2 - 71, self.tile_list[row].pos_y, 71, 132], 0)
                    elif self.click_pos[0] >= mistake_first_frame_width // 2 and self.click_pos[0] < mistake_first_frame_width // 2 + 71:
                        pygame.draw.rect(self.screen, (255, 0, 0), [self.screen_width // 2, self.tile_list[row].pos_y, 71, 132], 0)
                    elif self.click_pos[0] >= mistake_first_frame_width // 2 + 71 and self.click_pos[0] < mistake_first_frame_width // 2 + 142:
                        pygame.draw.rect(self.screen, (255, 0, 0), [self.screen_width // 2 + 71, self.tile_list[row].pos_y, 71, 132], 0)
                    else:
                        pygame.draw.rect(self.screen, (255, 0, 0), [0, 0, self.screen_width // 2 - 142, self.screen_height], 0)
                        pygame.draw.rect(self.screen, (255, 0, 0), [self.screen_width // 2 + 142, 0, self.screen_width // 2 - 142, self.screen_height], 0)
                self.screen.blit(self.font.render(str(self.score), False, (255, 0, 0)), (self.screen_width // 2 - self.font.size(str(self.score))[0] // 2, 0))
                pygame.display.update()
            elif self.mode == "Result":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.gameRun = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if mouse_pos[0] > self.screen_width - 28 and mouse_pos[0] < self.screen_width - 2 and mouse_pos[1] > self.screen_height - 28 and mouse_pos[1] < self.screen_height - 2:
                            self.full_screen = not self.full_screen
                            if self.full_screen:
                                self.screen = pygame.display.set_mode((self.monitor_size.current_w, self.monitor_size.current_h), pygame.FULLSCREEN)
                            else:
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                        elif mouse_pos[0] > 8 and mouse_pos[0] < 40 + self.small_font.size("Menu")[0] and mouse_pos[1] > self.screen_height - 72 and mouse_pos[1] < self.screen_height - 49:
                            self.mode = "Main"
                            self.score = 0
                    elif event.type == pygame.VIDEORESIZE:
                        self.first_frame = True
                        if not self.full_screen:
                            self.window_width = event.w
                            self.window_height = event.h
                            if self.window_width < 285:
                                self.window_width = 285
                            if self.window_height < 510:
                                self.window_height = 510
                            self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.full_screen:
                                self.full_screen = False
                                self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                if self.result_first_frame:
                    self.tile_list.clear()
                    self.tile_clicked = 0
                    self.tile_generated = 0
                    self.first_frame = True
                    self.blink_count = 0
                    self.speed_up_animation = False
                    self.started = False
                    self.speed_up = 1
                    self.display = True
                    self.blink_timer.initialized = False
                    new_score = False
                    if self.score > self.high_score:
                        new_score = True
                        self.high_score = self.score
                    self.result_first_frame = False
                self.screen_size = pygame.display.Info()
                self.screen_width = self.screen_size.current_w
                self.screen_height = self.screen_size.current_h
                self.screen.fill((0, 255, 255))
                self.screen.blit(self.font.render("Your score:", True, (255, 255, 255)), (self.screen_width // 2 - self.font.size("Your score")[0] // 2, 0))
                self.screen.blit(self.font.render(str(self.score), True, (255, 255, 255)), (self.screen_width // 2 - self.font.size(str(self.score))[0] // 2, 45))
                if new_score:
                    self.screen.blit(self.small_font.render("New high score!", True, (255, 255, 255)), (self.screen_width // 2 - self.small_font.size("New high score!")[0] // 2, 100))
                self.screen.blit(self.menu_icon, (8, self.screen_height - 72))
                self.screen.blit(self.small_font.render("Menu", True, (0, 0, 0)), (40, self.screen_height - 72))
                if self.full_screen:
                    self.screen.blit(self.exit_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                else:
                    self.screen.blit(self.enter_full_screen_icon, (self.screen_width - 28, self.screen_height - 28))
                pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Game()
