from p5 import setup, draw, size, background, run, Vector, stroke, circle
import numpy as np


class Boid():
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.max_speed = 5
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec) 


    def show(self):
        stroke(255)
        circle((self.position.x, self.position.y), radius=10)


    def update(self):
        self.position += self.velocity
        self.velocity += self.acceleration
        
        # Velocity limit
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed

        self.acceleration = Vector(*np.zeros(2))

    
    def wall_hit(self):
        x = self.position.x 
        y = self.position.y

        if x > self.width:
            self.position.x = 0
        elif x < 0:
            self.position.x = self.width

        if y > self.height:
            self.position.y = 0
        elif y < 0:
            self.position.y = self.height