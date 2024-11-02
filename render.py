from .pygw import Game
from .snake import Snake, UP, DOWN, LEFT, RIGHT
import pygame as pg

WIDTH = 540
HEIGHT = 600

class PySnake(Game):

  def __init__(self, board_size: int = 50, game_speed: int = 5):
    super().__init__()
    self.board_size = board_size
    self.snake = Snake(board_size)

    self.title = 'Snake'
    self.fps = 60
    self.game_speed = game_speed
    self.size = (WIDTH, HEIGHT)
    self.font = pg.font.SysFont("arial", 25)

    self.frame_counter = 0
    self.slowed = False

  def setup(self):
    self.snake.reset()

  def loop(self):
    self.frame_counter += 1
    if self.frame_counter >= self.game_speed:
      self.frame_counter = 0
      self.snake.move()
      if self.snake.game_over:
        self.snake.reset()

  def onEvent(self, event):
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_SPACE:
        if not self.slowed:
          self.game_speed *= 2
          self.slowed = True
    if event.type == pg.KEYUP:
      if event.key == pg.K_UP:
        if self.snake.body[0][2] != DOWN:
          self.snake.head_dir = UP
      elif event.key == pg.K_DOWN:
        if self.snake.body[0][2] != UP:
          self.snake.head_dir = DOWN
      elif event.key == pg.K_LEFT:
        if self.snake.body[0][2] != RIGHT:
          self.snake.head_dir = LEFT
      elif event.key == pg.K_RIGHT:
        if self.snake.body[0][2] != LEFT:
          self.snake.head_dir = RIGHT
      elif event.key == pg.K_SPACE:
        if self.slowed:
          self.game_speed /= 2
          self.slowed = False

  def onRender(self):
    self.draw_bg()
    self.draw_snake()

  def draw_bg(self):
    self.window.surface.fill((0, 0, 0))
    self.window.surface.blit(self.font.render(f"Score: {self.snake.score}", 1, (255,)*3), (230, 540))
    pg.draw.line(self.window.surface, (255,)*3, (20, 20), (20, WIDTH - 20))
    pg.draw.line(self.window.surface, (255,)*3, (20, 20), (WIDTH - 20, 20))
    pg.draw.line(self.window.surface, (255,)*3, (WIDTH - 20, 20), (WIDTH - 20, WIDTH - 20))
    pg.draw.line(self.window.surface, (255,)*3, (20, WIDTH - 20), (WIDTH - 20, WIDTH - 20))

  def draw_snake(self):
    node_size = (WIDTH - 40) / self.board_size
    pg.draw.rect(self.window.surface, (0, 177, 0), (node_size * self.snake.food_position[0] + 21, node_size * self.snake.food_position[1] + 21, node_size - 1, node_size - 1))
    for i, item in enumerate(self.snake.body):
      if i == 0:
        pg.draw.rect(self.window.surface, (255, 255, 0), (node_size * item[0] + 21 + (node_size - 1) // 2 - (node_size - 1) // 2, node_size * item[1] + 21 + (node_size - 1) // 2 - (node_size - 1) // 2, (node_size - 1), (node_size - 1)))
      else:
        pg.draw.rect(self.window.surface, (255, 0, 0), (node_size * item[0] + 21 + (node_size - 1) // 2 - (node_size - 1) // 2, node_size * item[1] + 21 + (node_size - 1) // 2 - (node_size - 1) // 2, (node_size - 1), (node_size - 1)))
