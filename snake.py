import numpy as np

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

HEAD = -2
FOOD = 1
TAIL = -1
EMPTY = 0

class Snake:

  def __init__(self, board_size: int = 20):
    self.board_size = board_size
    self.board = np.zeros((board_size, board_size), dtype=int)
    self.body = []
    self.food_position = [0, 0]
    self.game_over = False
    self.score = 0
    self.head_dir = UP

  def __repr__(self):
    rep_str = []
    for y in range(self.board_size):
        row = []
        for x in range(self.board_size):
            if self.board[y][x] in [HEAD, TAIL]:
              row.append('@')
            else:
              row.append(str(self.board[y][x]))
        rep_str.append(' '.join(row))
    return '\n'.join(rep_str)

  def reset(self, tail_count: int = 2):
    self.game_over = False
    self.score = 0
    self.body.clear()
    self.board = np.zeros((self.board_size, self.board_size), dtype=int)
    self.head_dir = np.random.choice([UP, DOWN, LEFT, RIGHT])
    if self.head_dir == DOWN:
      x = np.random.randint(0, self.board_size - 1)
      y = np.random.randint(tail_count, self.board_size - 1)
    elif self.head_dir == RIGHT:
      x = np.random.randint(tail_count, self.board_size - 1)
      y = np.random.randint(0, self.board_size - 1)
    elif self.head_dir == UP:
      x = np.random.randint(0, self.board_size - 1)
      y = np.random.randint(0, self.board_size - (tail_count + 1))
    elif self.head_dir == LEFT:
      x = np.random.randint(0, self.board_size - (tail_count + 1))
      y = np.random.randint(0, self.board_size - 1)
    self.board[y][x] = HEAD
    self.body.append([x, y, self.head_dir])
    for _ in range(tail_count):
      self.add_tail()
    self.create_food()

  def create_food(self):
    if len(self.body) <= (self.board_size * self.board_size) // 2:
      while True:
        self.food_position = [np.random.randint(0, self.board_size - 1), np.random.randint(0, self.board_size - 1)]
        if self.board[self.food_position[1]][self.food_position[0]] == EMPTY:
          break
    else:
      empty_nodes = []
      for y in range(self.board_size):
        for x in range(self.board_size):
          if self.board[y][x] == EMPTY:
            empty_nodes.append([x, y])
      self.food_position = empty_nodes[np.random.choice(len(empty_nodes))]
    self.board[self.food_position[1]][self.food_position[0]] = FOOD

  def add_tail(self):
    tail = self.body[-1].copy()
    if tail[2] == UP:
      tail[1] += 1
    elif tail[2] == DOWN:
      tail[1] -= 1
    elif tail[2] == LEFT:
      tail[0] += 1
    elif tail[2] == RIGHT:
      tail[0] -= 1
    self.board[tail[1]][tail[0]] = TAIL
    self.body.append(tail)

  def food_check(self):
    if self.body[0][0] == self.food_position[0] and self.body[0][1] == self.food_position[1]:
      self.score += 1
      self.add_tail()
      self.create_food()

  def move(self):
    last_dir = self.head_dir
    for i, block in enumerate(self.body):
      tmp_dir = self.body[i][2]
      self.body[i][2] = last_dir
      last_dir = tmp_dir
      self.move_block(block, i)
    self.food_check()
    return not self.game_over

  def move_block(self, block, idx):
    x = block[0]
    y = block[1]
    dir = block[2]
    if dir == UP:
      if y == 0 or self.board[y - 1][x] == TAIL:
        self.game_over = True
      else:
        self.board[y - 1][x] = TAIL if idx != 0 else HEAD
        block[1] -= 1
    elif dir == DOWN:
      if y == self.board_size - 1 or self.board[y + 1][x] == TAIL:
        self.game_over = True
      else:
        self.board[y + 1][x] = TAIL if idx != 0 else HEAD
        block[1] += 1
    elif dir == RIGHT:
      if x == self.board_size - 1 or self.board[y][x + 1] == TAIL:
        self.game_over = True
      else:
        self.board[y][x + 1] = TAIL if idx != 0 else HEAD
        block[0] += 1
    elif dir == LEFT:
      if x == 0 or self.board[y][x - 1] == TAIL:
        self.game_over = True
      else:
        self.board[y][x - 1] = TAIL if idx != 0 else HEAD
        block[0] -= 1
    self.board[y][x] = EMPTY
