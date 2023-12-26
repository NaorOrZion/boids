from p5 import setup, draw, size, background, run, Vector, stroke, circle, dist
import numpy as np

MAX_SPEED = 5
MAX_FORCE = 0.5
STROKE = 255
BOID_RADIUS = 10
BOID_VALID_AREA_RADIUS = 200


class Boid():
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.max_speed = MAX_SPEED
        self.position = Vector(x, y)
        vec = (np.random.rand(2) - 0.5)*10
        self.velocity = Vector(*vec)

        vec = (np.random.rand(2) - 0.5)/2
        self.acceleration = Vector(*vec) 


    def show(self):
        stroke(STROKE)
        circle((self.position.x, self.position.y), radius=BOID_RADIUS)


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


    def align(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vec = Vector(*np.zeros(2))

        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < BOID_VALID_AREA_RADIUS:
                avg_vec += boid.velocity
                total += 1

        if total > 0:
            avg_vec /= total
            avg_vec = Vector(*avg_vec)
            avg_vec = (avg_vec /np.linalg.norm(avg_vec)) * self.max_speed
            steering = avg_vec - self.velocity

        return steering
    

    
    def cohesion(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        center_of_mass = Vector(*np.zeros(2))
        for boid in boids:
            if np.linalg.norm(boid.position - self.position) < BOID_VALID_AREA_RADIUS:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            center_of_mass = Vector(*center_of_mass)
            vec_to_com = center_of_mass - self.position

            if np.linalg.norm(vec_to_com) > 0:
                vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed

            steering = vec_to_com - self.velocity

            if np.linalg.norm(steering) > MAX_FORCE:
                steering = (steering /np.linalg.norm(steering)) * MAX_FORCE

        return steering
    

    def separation(self, boids):
        steering = Vector(*np.zeros(2))
        total = 0
        avg_vector = Vector(*np.zeros(2))
        for boid in boids:
            distance = np.linalg.norm(boid.position - self.position)
            if self.position != boid.position and distance < BOID_VALID_AREA_RADIUS:
                diff = self.position - boid.position
                diff /= distance
                avg_vector += diff
                total += 1

        if total > 0:
            avg_vector /= total
            avg_vector = Vector(*avg_vector)
            if np.linalg.norm(steering) > 0:
                avg_vector = (avg_vector / np.linalg.norm(steering)) * self.max_speed

            steering = avg_vector - self.velocity

            if np.linalg.norm(steering) > MAX_FORCE:
                steering = (steering /np.linalg.norm(steering)) * MAX_FORCE

        return steering


    def apply_behaviour(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        seperation = self.separation(boids)

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += seperation
    