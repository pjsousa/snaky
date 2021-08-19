from enum import Enum, auto
from random import choice, sample, randint, seed
from queue import Queue


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

DIRECTIONS = list(Direction)

class CELL_STATE(Enum):
    OUTSIDE = -1
    EMPTY = 0
    FOOD = 1
    SNAKE = 2

CELL_STATE_STR = {
    CELL_STATE.OUTSIDE: "*",
    CELL_STATE.EMPTY: "+",
    CELL_STATE.FOOD: "@",
    CELL_STATE.SNAKE: "#",
}

class Snake():

    def __init__(self, head, direction, pre_food) -> None:
        self.tail = Queue()
        self.direction = direction
        self.last_step = direction
        self.food = pre_food
        self.pre_food = pre_food
        self.head = head
        self.tail.put(head)

    def step(self):
        if self.direction == Direction.UP:
            self.head = self.head[0], self.head[1] - 1
        elif self.direction == Direction.DOWN:
            self.head = self.head[0], self.head[1] + 1
        elif self.direction == Direction.LEFT:
            self.head = self.head[0] - 1, self.head[1]
        elif self.direction == Direction.RIGHT:
            self.head = self.head[0] + 1, self.head[1]

        self.last_step = self.direction

        tail = None
        if self.food > 0:
            self.food -= 1
        else:
            tail = self.tail.get()

        self.tail.put(self.head)

        return self.head, tail
    
    def eat(self):
        self.food += 1

    def change_dir(self, new_dir):
        if self.last_step == Direction.UP and new_dir != Direction.DOWN:
            self.direction = new_dir
        elif self.last_step == Direction.DOWN and new_dir != Direction.UP:
            self.direction = new_dir
        elif self.last_step == Direction.LEFT and new_dir != Direction.RIGHT:
            self.direction = new_dir
        elif self.last_step == Direction.RIGHT and new_dir != Direction.LEFT:
            self.direction = new_dir
        
        return self.direction
    
    def size(self):
        return self.tail.qsize()


class SnakyViewModel():
    def __init__(self, w, h, on_kill=None, on_win=None) -> None:
        self.dimensions = w, h
        self.snakes = []
        self.world = [[CELL_STATE.EMPTY for _ in range(w)] for _ in range(h)]
        self.on_kill = on_kill
        self.on_win = on_win

    def step(self):
        for snake in sample(self.snakes, len(self.snakes)):
            head, tail = snake.step()

            if tail is not None:
                self.world[tail[1]][tail[0]] = CELL_STATE.EMPTY

            state = self.validate(head)

            if state == CELL_STATE.FOOD:
                snake.eat()
                self.world[head[1]][head[0]] = CELL_STATE.SNAKE
                f = self.make_food()
                if f is None:
                    self.finish(snake)
            elif state == CELL_STATE.EMPTY:
                self.world[head[1]][head[0]] = CELL_STATE.SNAKE
            elif state == CELL_STATE.OUTSIDE or state == CELL_STATE.SNAKE:
                self.kill(snake)
        
        return state

        
    def validate(self, pos):
        if pos is None:
            return CELL_STATE.OUTSIDE

        x, y = pos
        if x < 0 or x >= self.dimensions[0] or y < 0 or y >= self.dimensions[1]:
            return CELL_STATE.OUTSIDE

        return self.world[y][x]
    
    def hatch_snake(self, hatch_size=3):
        head = self.random_empty_pos()

        if head != None:
            s = Snake(head, choice(DIRECTIONS), hatch_size)
            self.set_to(head, CELL_STATE.SNAKE)
            self.snakes.append(s)

            return s
        return None

    def make_food(self):
        food = self.random_empty_pos()
        self.set_to(food, CELL_STATE.FOOD)
        return food
    
    def set_to(self, pos, state):
        self.world[pos[1]][pos[0]] = state
    
    def random_empty_pos(self):
        pos = None
        tries = 0
        max_tries = self.dimensions[0] * self.dimensions[1]

        while pos is None or self.validate(pos) != CELL_STATE.EMPTY and tries < max_tries:
            pos = randint(0, self.dimensions[0] - 1), randint(0, self.dimensions[1] - 1)
            tries += 1

        return pos
    
    def change_dir(self, snake, dir):
        self.snakes[snake].change_dir(dir)


    def kill(self, snake):
        if self.on_kill is not None:
            self.on_kill(snake)

    def finish(self, snake):
        if self.on_win is not None:
            self.on_win(snake)
    
    def __str__(self) -> str:
        return "\n".join([ ",".join([ CELL_STATE_STR[x] for x in y ]) for y in self.world])


if __name__ == "__main__":
    vm = SnakyViewModel(4, 3)
    s = vm.hatch_snake(1)
    d = s.change_dir(Direction.DOWN)
    print("head", s.head, d == Direction.DOWN)
    print(str(vm))
    f = vm.make_food()
    vm.step()
    print("food", f)
    print("step")
    print(str(vm))
    vm.step()
    print("step")
    print(str(vm))
    s.change_dir(Direction.LEFT)
    vm.step()
    print("step")
    print(str(vm))
    vm.step()
    print("step")
    print(str(vm))
    s.change_dir(Direction.UP)
    vm.step()
    print("step")
    print(str(vm))
    vm.step()
    print("step")
    print(str(vm))
    s.change_dir(Direction.RIGHT)
    vm.step()
    print("step")
    print(str(vm))



