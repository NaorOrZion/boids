from p5 import setup, draw, size, background, run
import numpy as np
from boid import Boid

WIDTH = 1000
HEIGHT = 700
BOIDS = 30

# Create Boids instances
flock = [Boid(*np.random.rand(2)*1000, WIDTH, HEIGHT) for _ in range(BOIDS)]


def setup():
    # This function triggers just once
    size(WIDTH, HEIGHT)  # instead of create_canvas


def draw():
    # This function triggers indefinitely
    background(30, 30, 47)

    for boid in flock:
        boid.show()
        boid.update()
        boid.wall_hit()


run()
