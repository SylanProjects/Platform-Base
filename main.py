import pygame as pg
import sys
from settings import *
from sprites import *
from tilemap import *
from os import path
import math


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        #self.running = True
        self.load_data()
        self.mouse_pos = (0, 0)
        self.mouse_test = 0
        self.text_posy = 10
        self.draw_count = False

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map_folder = path.join(game_folder, 'maps')
        self.default_font = path.join(img_folder, 'prstart.ttf')

        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (TILESIZE, TILESIZE))

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        #self.player = Player()
        self.map = TiledMap(path.join(self.map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                            tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'wall':
                Wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        self.playing = True
        while self.playing:
            #self.clock.tick(FPS)
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def check_for_collision(self):

        if self.mouse_pos[0] - self.camera.max_right > self.player.pos[0] - TILESIZE * 1.5 and self.mouse_pos[0] -  self.camera.max_right < self.player.pos[0] + TILESIZE * 1.5 and self.mouse_pos[1] - self.camera.max_bttm > self.player.pos[1] - TILESIZE / 2 and self.mouse_pos[1] - self.camera.max_bttm < self.player.pos[1] + (TILESIZE * 2):
            self.mouse_collision = True
        else:
            self.mouse_collision = False

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_collision = False
        self.check_for_collision()


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                    self.quit()
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0] == 1:
                    self.mouse_test += 1

                    if self.mouse_collision == False:
                        self.draw_box(self.mouse_pos[0], self.mouse_pos[1])
                    else:
                        pass


    def round_num(self, n):
        z = math.modf(n)
        if z[0] < 0.5:
	           n = math.floor(n)
        else:
	           n = math.ceil(n)
        return n

    def draw_box(self, x, y):

        if self.camera.max_right < 0:
            x -= self.camera.max_right - 1
        else:
            x = x
        if self.camera.max_bttm < 0:
            y -= self.camera.max_bttm - 1
        else:
            y = y
        g = x / TILESIZE
        x = int(g) * TILESIZE
        h = y / TILESIZE
        y = int(h) * TILESIZE

        Wall(self, x, y - TILESIZE, TILESIZE, TILESIZE)
        Platform(self, x, y)



    def draw(self):


        self.screen.blit(self.map_img, self.camera.apply(self.map))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.draw_text("Mouse:{}".format(self.mouse_pos), self.default_font, 15, WHITE,
                        10, 10, align="topleft")
        self.draw_text("Mouse:{}".format(self.mouse_test), self.default_font, 15, WHITE,
                        10, 30, align="topleft")
        self.draw_text("max right position:{}".format(self.camera.max_right), self.default_font, 15, WHITE,
                        10, 50, align="topleft")
        self.draw_text("Player position:{}".format(self.player.pos[1]), self.default_font, 15, WHITE,
                        10, 70, align="topleft")
        self.draw_text("Mouse collision:{}".format(self.mouse_collision), self.default_font, 15, WHITE,
                        10, 90, align="topleft")

        pg.display.flip()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        pass


    def show_go_screen(self):
        pass


    def wait_for_key(self):
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False




g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()


pg.quit()
