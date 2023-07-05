import pygame as pg
import sys
from random import randrange
from rocket import Rocket


class Game:
    def __init__(self):
        # Konfifuracja
        self.window_wide: int = 1280
        self.window_hight: int = 720
        # self.box_x: int = 50
        # self.box_y: int = 50
        self.max_tic: float = 500  # 500
        self.delta_tiem: float = 0
        self.gravity: float = 0.00
        self.inertial: float = 5
        self.acceleration_delta: float = 0.08

        self.baloon: pg.Vector2 = pg.Vector2(0, 0)
        self.baloon_r: int = 150
        self.score: int = 0

        # Inicjalizacja
        pg.init()
        self.window = pg.display.set_mode((self.window_wide, self.window_hight), display=1)
        self.position = pg.Vector2(self.window_wide / 2, self.window_hight / 2)
        self.speed = pg.Vector2(0, -0.00001)  # żeby był dobrze zwrócony na początku
        self.acceleration = pg.Vector2(0, 0)
        # self.player = Rocket(self)
        # self.box = pg.Rect(self.player.position.x, self.player.position.y, self.box_x, self.box_y)
        self.box = pg.Rect(self.position.x, self.position.y, 50, 50)
        self.clock = pg.time.Clock()
        self.baloon_position()

    def game(self):
        while self.score < 10:
            # ogarnianie eventów(działań na oknie)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit(0)
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit(0)
            self.draw()
            self.distance_check()
            # zmniejszenie prędkości przez tiki
            '''jeśli główna się tyle razy że zostanie spełniony warunek tej pętli niżej to
            # a chuj to yrzeba przekninić na spokojnie xDDD'''
            self.delta_tiem += self.clock.tick() / 1000.0
            while self.delta_tiem > 1 / self.max_tic:
                self.delta_tiem -= 1 / self.max_tic
                # self.keys()
                self.tick()
        else:
            print(f'You win!\nYour time is: {pg.time.get_ticks()/1000}sec')

    # def tick(self):
        # self.player.tick()

    def add_force(self, force):
        self.acceleration += force

    def tick(self):
        # input
        if pg.key.get_pressed()[pg.K_w]:
            self.add_force(pg.Vector2(0, -self.acceleration_delta))
        if pg.key.get_pressed()[pg.K_s]:
            self.add_force(pg.Vector2(0, self.acceleration_delta))
        if pg.key.get_pressed()[pg.K_a]:
            self.add_force(pg.Vector2(-self.acceleration_delta, 0))
        if pg.key.get_pressed()[pg.K_d]:
            self.add_force(pg.Vector2(self.acceleration_delta, 0))

        """if self.box.y < 0 or self.box.x < 0 or self.box.y > self.window_hight - self.box_y or\
           self.box.x > self.window_wide - self.box_x:
            self.speed *= 0
            # self.acceleration *= 0"""

        # fizyka
        self.acceleration *= 1 / self.inertial
        self.speed -= pg.Vector2(0, -self.gravity)

        self.speed += self.acceleration
        self.position += self.speed
        # self.box.x = self.position.x
        # self.box.y = self.position.y
        # self.speed -= 0.003 * self.speed
        self.acceleration *= 0  # 0

        if self.position.x < 0:
            self.speed.x *= 0
            self.acceleration.x *= 0
            self.position.x = 0
        elif self.position.x > self.window_wide:
            self.speed.x *= 0
            self.acceleration.x *= 0
            self.position.x = self.window_wide
        if self.position.y < 0:
            self.speed.y *= 0
            self.acceleration.y *= 0
            self.position.y = 0
        elif self.position.y > self.window_hight:
            self.speed.y *= 0
            self.acceleration.y *= 0
            self.position.y = self.window_hight

    # def keys(self) -> None:
        # self.player.keys()

    def draw(self) -> None:
        self.window.fill((0, 0, 0))
        # rysowanie balonika
        pg.draw.circle(self.window, (220, 0, 0), self.baloon, self.baloon_r)

        # rysowanie strzałki
        pg.draw.polygon(self.window, (155, 155, 155), self.triangle())
        pg.display.flip()

    def triangle(self) -> list:
        triangle_points = [pg.Vector2(0, 0), pg.Vector2(20, 40), pg.Vector2(-20, 40)]
        angle = self.speed.angle_to(pg.Vector2(0, 1))

        # ruch strzałki
        for index, point in enumerate(triangle_points):
            # ustawnie strzałki w kierunku ruchu
            point = point.rotate(angle)
            # odwrócenie osi Y
            point.y *= -1
            # poruszanie się strzałki
            point += self.position
            triangle_points[index] = point
        return triangle_points

    def baloon_position(self) -> None:
        x = randrange(self.baloon_r, self.window_wide - self.baloon_r)
        y = randrange(self.baloon_r, self.window_hight - self.baloon_r)
        self.baloon = pg.Vector2(x, y)

    def distance_check(self):
        if self.baloon.distance_to(self.position) < self.baloon_r:
            self.baloon_position()
            self.score += 1
            self.level_up()
            print(self.score)

    def level_up(self):
        self.baloon_r -= 10
        self.acceleration_delta += 0.05


if __name__ == "__main__":
    g = Game()
    g.game()
