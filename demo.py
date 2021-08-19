from snaky.snaky_contoller import SnakyController
import pyglet
from pyglet import window
from pyglet.window import key
from pyglet import shapes
from snaky import SnakyController, CELL_STATE, Direction

COLORS = {
    CELL_STATE.OUTSIDE: (0,0,0),
    CELL_STATE.EMPTY: (229, 204, 255),
    CELL_STATE.FOOD: (200, 40, 100),
    CELL_STATE.SNAKE: (40, 200, 90)
}

class SnakyView(pyglet.window.Window):

    def __init__(self, pixel_dims, grid_dims):
        super().__init__(pixel_dims[0], pixel_dims[1], "Snaky")
        self.time = 0
        self.batch = pyglet.graphics.Batch()
        self.pixel_dims = pixel_dims
        self.grid_dims = grid_dims
        self.grid = None
        self.cell_size = self.pixel_dims[0] / self.grid_dims[0]

        self.make_grid()

        self.vm = SnakyController(grid_dims[0], grid_dims[1], on_kill=self.on_killed, on_win=self.on_win)
        self.snake = self.vm.hatch_snake(3)
        f = self.vm.make_food()

        self.killed = False

        self.score_label = pyglet.text.Label(text="Score: 0", x=10, y=pixel_dims[1] - 30, batch=self.batch)

    def make_grid(self):
        self.grid = []

        for row in range(self.grid_dims[1]):
            grid_row = []
            self.grid.append(grid_row)

            for col in range(self.grid_dims[0]):
                square = shapes.Rectangle(self.cell_size * col, self.cell_size*row, self.cell_size, self.cell_size, color=(0, 0, 0), batch=self.batch)

                grid_row.append(square)


    def on_draw(self):
        """Clear the screen and draw shapes"""
        self.clear()
        self.batch.draw()

    def on_killed(self, snake, controller):
        self.killed = True

    def on_win(self, snake, controller):
        pass

    def update(self, delta_time):
        """Animate the shapes"""
        self.time += delta_time

        if not self.killed:
            state = self.vm.step()

            for col in range(self.grid_dims[0]):
                for row in range(self.grid_dims[1]):
                    s = self.grid[self.grid_dims[1] - 1 - row][col]
                    s.color = COLORS[self.vm.world[row][col]]

            self.score_label.text = f"Score: {self.snake.size() - 4}"

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.W:
            self.snake.change_dir(Direction.UP)
        elif symbol == pyglet.window.key.S:
            self.snake.change_dir(Direction.DOWN)
        elif symbol == pyglet.window.key.A:
            self.snake.change_dir(Direction.LEFT)
        elif symbol == pyglet.window.key.D:
            self.snake.change_dir(Direction.RIGHT)



if __name__ == "__main__":
    
    demo = SnakyView((720, 480), (40, 20))
    pyglet.clock.schedule_interval(demo.update, 1/10)
    pyglet.app.run()
