import pygame
import random
import math

#initilaise
pygame.init()

#screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Boids Simulation")

#Margins
leftmargin = 200
rightmargin = 1000
topmargin = 150
bottommargin = 450

#Set up colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

#Hyper parameters
dot_radius = 2
protected_range_raduis = 8
visual_range_raduis = 40
avoidfactor = 0.05
matchingfactor = 0.05
centeringfactor = 0.0005
turnfactor = 0.2
minspeed = 3
maxspeed = 6
predator_range_raduis = 80
escape_factor = 0.5


class bird:
    def __init__(self):
        self.x=random.randint(leftmargin, rightmargin)
        self.y=random.randint(topmargin, bottommargin)
        self.vx=4
        self.vy=4
        self.angle = 0

    def update_position(self):
        self.x+=self.vx
        self.y+=self.vy

        angle = math.atan2(self.vy, self.vx)
        angle_degrees = math.degrees(angle)
        self.angle = angle_degrees

        if self.x < leftmargin:
            self.vx += turnfactor
        if self.x > rightmargin:
            self.vx -= turnfactor
        if self.y < topmargin:
            self.vy += turnfactor
        if self.y > bottommargin:
            self.vy -= turnfactor

    def compute_distance(self,bird):
        return math.sqrt((self.x-bird.x)**2+(self.y-bird.y)**2)
    
    def check_separation(self,other_birds):
        close_dx = 0
        close_dy = 0
        for bird in other_birds:
            if self.compute_distance(bird) < protected_range_raduis:
                close_dx += self.x-bird.x
                close_dy += self.y-bird.y
        #update velocity
        if close_dx != 0 or close_dy != 0:
            magnitude = math.sqrt(close_dx**2 + close_dy**2)
            self.vx += (close_dx/magnitude)*avoidfactor
            self.vy += (close_dy/magnitude)*avoidfactor

    def check_alignment(self,other_birds):
        xvel_avg = 0
        yvel_avg = 0
        neighboring_birds = 0
        for bird in other_birds:
            if self.compute_distance(bird) < visual_range_raduis:
                xvel_avg += bird.vx
                yvel_avg += bird.vy
                neighboring_birds += 1
        if neighboring_birds>0:
            xvel_avg /= neighboring_birds
            yvel_avg /= neighboring_birds
            magnitude = math.sqrt(xvel_avg**2 + yvel_avg**2)
            self.vx += (xvel_avg/magnitude)*matchingfactor
            self.vy += (xvel_avg/magnitude)*matchingfactor

    def check_cohesion(self,other_birds):
        xpos_avg = 0
        ypos_avg = 0
        neighboring_birds = 0
        for bird in other_birds:
            if self.compute_distance(bird) < visual_range_raduis:
                xpos_avg += bird.x
                ypos_avg += bird.y
                neighboring_birds += 1
        if neighboring_birds>0:
            xpos_avg = xpos_avg/neighboring_birds
            ypos_avg = ypos_avg/neighboring_birds
            dx = xpos_avg - self.x
            dy = ypos_avg - self.y
            magnitude = math.sqrt(dx**2 + dy**2)
            if magnitude!=0:
                self.vx += (dx / magnitude) * centeringfactor
                self.vy += (dy / magnitude) * centeringfactor

    def check_speedlimit(self):
        speed = math.sqrt(self.vx**2+self.vy**2)
        if speed > maxspeed :
            self.vx = (self.vx/speed)*maxspeed
            self.vy = (self.vy/speed)*maxspeed
        if speed < minspeed:
            self.vx = (self.vx/speed)*minspeed
            self.vy = (self.vy/speed)*minspeed

    def escape_predator(self,predator):
        if self.compute_distance(predator) < predator_range_raduis:
            if predator.x < self.x:
                self.vx += predator.vx * escape_factor if predator.vx > 0 else -predator.vx * escape_factor
            else:
                self.vx -= predator.vx * escape_factor if predator.vx < 0 else -predator.vx * escape_factor

            if predator.y < self.y:
                self.vy += predator.vy * escape_factor if predator.vy > 0 else -predator.vy * escape_factor
            else:
                self.vy -= predator.vy * escape_factor if predator.vy < 0 else -predator.vy * escape_factor

birds = [bird() for _ in range(200)]

predator = bird()

#set up gam loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    #handle event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bird in birds:
        #update dot position
        bird.update_position()

        bird.check_separation(birds)
        bird.check_alignment(birds)
        bird.check_cohesion(birds)
        bird.check_speedlimit()
        #bird.escape_predator(predator)
        
        # Draw the dot
        pygame.draw.circle(screen, RED, (bird.x, bird.y), dot_radius)
    #predator.update_position()
    #pygame.draw.circle(screen, GREEN, (predator.x, predator.y), dot_radius*2)

    # Update the display
    pygame.display.flip()

    #cape the frame rate
    clock.tick(100)

#Quit Pygame
pygame.quit()
    


