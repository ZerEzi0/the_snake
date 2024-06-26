# Импортируем необходимые модули
import pygame as pg
from random import randint, choice

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Инициализация PyGame
pg.init()

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')

# Настройка времени
clock = pg.time.Clock()


# Константы для размеров поля и сетки
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# Базовый класс для игровых объектов
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
            self, position=CENTER_POSITION,
            body_color=SNAKE_COLOR,
            border_color=BOARD_BACKGROUND_COLOR
    ):
        self.position = position
        self.body_color = body_color
        self.border_color = border_color

    def draw(self):
        """Указание на реализацию абстрактного метода"""
        raise NotImplementedError(
            f'Подкласс {self.__class__.__name__} должен'
            'реализовывать абстрактный метод'
        )


# Класс для яблока
class Apple(GameObject):
    """Класс обозначает яблоко в игре."""

    def __init__(self,
                 body_color=APPLE_COLOR,
                 border_color=BORDER_COLOR):
        super().__init__(
            CENTER_POSITION,
            body_color, border_color
        )
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """Определяет случайную позицию яблока"""
        if occupied_positions is None:
            occupied_positions = []
        while self.position in occupied_positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self):
        """Рисует яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)


# Класс для змейки
class Snake(GameObject):
    """Класс обозначает змейку в игре."""

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        super().__init__(
            CENTER_POSITION,
            body_color, border_color
        )
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Определяет голову змейки"""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в соответствии с текущим направлением."""
        x, y = self.direction
        head_x, head_y = self.get_head_position()
        new = (
            ((head_x + (x * GRID_SIZE)) % SCREEN_WIDTH),
            ((head_y + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        )
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def draw(self):
        """Рисует змейку на экране."""
        for p in self.positions:
            rect = pg.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, self.border_color, rect, 1)


# Функция обработки действий пользователя
def handle_keys(snake):
    """Обрабатывает действия пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


# Основная функция игры
def main():
    """Основная функция игры."""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
