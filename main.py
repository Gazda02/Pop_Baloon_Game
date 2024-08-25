import pygame as pg
from random import randrange


class Game:
    def __init__(self, difficulty: int):
        """
        Settings and screen initialization

        :param difficulty: level of difficulty form 0 (tutorial) to 4 (very hard)
        """
        # Konfifuracja
        self.difficulty = difficulty
        self.window_wide: int = 1280
        self.window_hight: int = 720
        self.max_tic: float = 500  # 500
        self.delta_tiem: float = 0
        self.gravity: float = 0.00
        self.inertial: float = 5
        self.baloon: pg.Vector2 = pg.Vector2(0, 0)
        self.__score: int = 0

        self.acceleration_delta: float = 0.00
        self.baloon_r: int = 100
        self.acceleration_level_delta: float = 0
        self.baloon_r_level_delta: int = 0

        # ustawia poziom trudności
        self.difficulty_level()

        # Inicjalizacja
        self.window = pg.display.set_mode((self.window_wide, self.window_hight))
        self.position = pg.Vector2(self.window_wide / 2, self.window_hight / 2)
        self.speed = pg.Vector2(0, -0.00001)  # żeby był dobrze zwrócony na początku
        self.acceleration = pg.Vector2(0, 0)
        self.box = pg.Rect(self.position.x, self.position.y, 50, 50)
        self.clock = pg.time.Clock()
        self.baloon_position()

    def start(self) -> tuple:
        """Metoda główna"""
        pg.init()
        while self.__score < 1:
            # ogarnianie eventów(działań na oknie)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__score = 11
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.__score = 11
            self.draw()
            self.distance_check()
            # zmniejszenie prędkości przez tiki
            '''jeśli główna się tyle razy że zostanie spełniony warunek tej pętli niżej to
            # a chuj to yrzeba przekninić na spokojnie xDDD'''
            self.delta_tiem += self.clock.tick() / 1000.0
            while self.delta_tiem > 1 / self.max_tic:
                self.delta_tiem -= 1 / self.max_tic
                self.tick()
        if self.__score == 1:
            time = pg.time.get_ticks() / 1000
        else:
            time = None
        pg.quit()
        return self.difficulty, time

    def tick(self) -> None:
        """Cała magia sterowania"""
        # input
        if pg.key.get_pressed()[pg.K_w]:
            self.acceleration += pg.Vector2(0, -self.acceleration_delta)
        if pg.key.get_pressed()[pg.K_s]:
            self.acceleration += pg.Vector2(0, self.acceleration_delta)
        if pg.key.get_pressed()[pg.K_a]:
            self.acceleration += pg.Vector2(-self.acceleration_delta, 0)
        if pg.key.get_pressed()[pg.K_d]:
            self.acceleration += pg.Vector2(self.acceleration_delta, 0)

        self.border_check()

        # fizyka
        '''JA NIE WIEM MOŻE TO DO OSOBNEJ METODY DAĆ'''
        self.acceleration *= 1 / self.inertial
        self.speed -= pg.Vector2(0, -self.gravity)

        self.speed += self.acceleration
        self.position += self.speed
        # self.speed -= 0.003 * self.speed
        self.acceleration *= 0  # 0

    def border_check(self) -> None:
        """Ustawienie barier na granicach planszy"""
        if self.position.x < 0:
            self.speed.x *= 0
            self.acceleration.x *= 0
            self.position.x = 0
        if self.position.x > self.window_wide:
            self.speed.x *= 0
            self.acceleration.x *= 0
            self.position.x = self.window_wide
        if self.position.y < 0:
            self.speed.y *= 0
            self.acceleration.y *= 0
            self.position.y = 0
        if self.position.y > self.window_hight:
            self.speed.y *= 0
            self.acceleration.y *= 0
            self.position.y = self.window_hight

    def draw(self) -> None:
        """Rysuje strzałkę i balonik na ekranie"""
        self.window.fill((0, 0, 0))
        self.score_show()

        # rysowanie balonika
        pg.draw.circle(self.window, (220, 0, 0), self.baloon, self.baloon_r)

        # rysowanie strzałki
        pg.draw.polygon(self.window, (155, 155, 155), self.triangle())
        pg.display.flip()

    def score_show(self) -> None:
        """Wyświetlanie czasu oraz pozostałych baloników"""
        # Pobranie czasu gry
        time = pg.time.get_ticks()

        # Ustawnienie powieszchni
        time_display = pg.font.Font(None, 30)
        score_display = pg.font.Font(None, 30)

        # Ustawienie wartości oraz kolru
        time_display = time_display.render(str(time / 1000), True, (255, 255, 255))
        score_display = score_display.render(str(10 - self.__score), True, (255, 255, 255))

        # Nałożenie powieszchni na ekran i ustawneine w odpowiednim miejscu
        self.window.blit(time_display, (self.window_wide - 60, 10))
        self.window.blit(score_display, (10, 10))

    def triangle(self) -> list:
        """Zorientowanie strzałki"""
        triangle_points = [pg.Vector2(0, 0), pg.Vector2(20, 40), pg.Vector2(-20, 40)]
        # Kąt między wektorem prędkości a osią OY
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
        """Wylosowanie pozycji balonika"""
        '''BO LOSUJE SIĘ TEŻ NA POZYCJI STRZAŁKI A TO ŹLE'''
        # Wylosowanie współrzędnych balonika
        if self.difficulty <= 2:
            x = randrange(self.baloon_r, self.window_wide - self.baloon_r)
            y = randrange(self.baloon_r, self.window_hight - self.baloon_r)
        else:
            # Balonik tylko na środku jeśli pooziom trudności to 3 lub więcej
            x = randrange(self.window_wide // 4, (self.window_wide // 4) * 3)
            y = randrange(self.window_hight // 4, (self.window_hight // 4) * 3)
        # Wpisanie wartości x i y do położenia balonika
        self.baloon = pg.Vector2(x, y)

    def distance_check(self) -> None:
        """Sprawdza czy strzałka wlecaiła w balonik"""
        if self.baloon.distance_to(self.position) < self.baloon_r:
            # zmiejszenie średnicy balonika zależnie od poziomu
            self.baloon_r -= self.baloon_r_level_delta
            # rysowanie nowego balonika
            self.baloon_position()
            # przyśpieszenie strzałki
            self.acceleration_delta += self.acceleration_level_delta
            # doliczenie punktu
            self.__score += 1

    def difficulty_level(self) -> None:
        """Ustawia odpwiednie wartości zależnie od poziomu trudności"""
        if self.difficulty == 0:
            self.acceleration_delta = 0.01
            self.baloon_r = 110
            self.acceleration_level_delta = 0
            self.baloon_r_level_delta = 0
        elif self.difficulty == 1:
            self.acceleration_delta = 0.03
            self.baloon_r = 110
            self.acceleration_level_delta = 0.005
            self.baloon_r_level_delta = 5
        elif self.difficulty == 2:
            self.acceleration_delta = 0.03
            self.baloon_r = 110
            self.acceleration_level_delta = 0.01
            self.baloon_r_level_delta = 8
        elif self.difficulty == 3:
            self.acceleration_delta = 0.05
            self.baloon_r = 110
            self.acceleration_level_delta = 0.02
            self.baloon_r_level_delta = 10
        elif self.difficulty == 4:
            self.acceleration_delta = 0.5
            self.baloon_r = 91
            self.acceleration_level_delta = 0.2
            self.baloon_r_level_delta = 10
        else:
            pass
            # tu ma być wyjątek "Lvl_error"


'''if __name__ == "__main__":
    g = Game(1)
    g.game()'''
