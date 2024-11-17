import pygame
from math import cos, sin
from math import pi as PI
from Vector2 import *
import copy
import numpy as np

G = 9.8
m1 = 1
m2 = 1
friction = .2
dt = 0
force = 0
fear = 1

def EnforcePendulum1(theta_1, theta_2, thetaDot_1, thetaDot_2):
    return (-m2*thetaDot_1**2*sin(theta_1 - theta_2)*cos(theta_1 - theta_2) + m2*G*sin(theta_2)*cos(theta_1 - theta_2) - m2*thetaDot_2**2*sin(theta_1 - theta_2) - (m1 + m2)*G*sin(theta_1)) / ((m1 + m2) - m2*cos(theta_1 - theta_2)**2) - friction * np.sign(thetaDot_1)

def EnforcePendulum2(theta_1, theta_2, thetaDot_1, thetaDot_2):
    return (m2*thetaDot_2**2*sin(theta_1 - theta_2)*cos(theta_1 - theta_2) + (m1 + m2)*G*sin(theta_1)*cos(theta_1 - theta_2) + thetaDot_1**2*sin(theta_1-theta_2)*(m1 + m2) - G*sin(theta_2)*(m1 + m2)) / ((m1 + m2) - m2*cos(theta_1 - theta_2)**2) - friction * np.sign(thetaDot_2)


class State:
    def __init__(self, theta1 = 0, vel1=0, theta2=0, vel2=0):
        self.theta1 = theta1
        self.vel1 = vel1
        self.theta2 = theta2
        self.vel2 = vel2
        self.distance = pow(PI - theta1, 2) + fear * pow(vel1, 2) + pow(PI - theta2, 2) + fear * pow(vel2, 2)

    def Update(self, dir1, dir2):
        _theta1 = copy.copy(self.theta1)
        _vel1 = copy.copy(self.vel1)
        _theta2 = copy.copy(self.theta2)
        _vel2 = copy.copy(self.vel2)

        _vel1 += (EnforcePendulum1(_theta1, _theta2, _vel1, _vel2) + dir1) * dt
        _vel2 += (EnforcePendulum2(_theta1, _theta2, _vel1, _vel2) + dir2) * dt

        _theta1 += _vel1 * dt
        _theta2 += _vel2 * dt

        return State(_theta1, _vel1, _theta2, _vel2)
    
    def Unfold(self):
        states = []
        for i in np.arange(0, 9):
            id = base_three(i).rjust(2, "0")
            _state = self.Update((int(id[0])-1) * force, (int(id[1])-1) * force)
            states.append(_state)
        return states
    
    def __str__(self):
        return f"({self.theta1}, {self.vel1}) ({self.theta2}, {self.vel2})"


def DrawLine(surface, A, B):
    pygame.draw.line(surface, (0,0,0), (A.x, width-A.y), (B.x, width-B.y))

def DrawPoint(surface, A, radius=5):
    pygame.draw.circle(surface, (255,0,0), (A.x, width-A.y), radius)

def update_frame(surface):
    surface.fill((255,255,255))
    
    length = 100
    A = Vector2(width/2, width/2)
    B = A + PolarVector(currentState.theta1, length)
    C = B + PolarVector(currentState.theta2, length)

    DrawLine(surface, A, B)
    DrawLine(surface, B, C)
    DrawPoint(surface, B)
    DrawPoint(surface, C)

    pygame.display.update()

def get_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False     
    return True

def base_three(n):
  if n == 0:
    return "0"

  result = ""
  while n > 0:
    n, remainder = divmod(n, 3)
    result = str(remainder) + result

  return result

width = 500
def main():
    surface = pygame.display.set_mode((width, width), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    global dt, currentState, force, fear
    currentState = State(0, 0, 0, 0)

    running = True
    FPS = 30
    dt = 1 / FPS
    force = 25
    fear = .05
    depth = 3
    
    while running:
        clock.tick(FPS)

        states = []
        distances = []
        for i in np.arange(0, 9):
            id = base_three(i).rjust(2, "0")
            _state = currentState.Update((int(id[0])-1) * force, (int(id[1])-1) * force)
            states.append([_state])
            distances.append(_state.distance)

        for k in np.arange(0, depth):
            min_ind = np.argmin(distances)
            new_list = []
            for i in states[min_ind]:
                for j in i.Unfold():
                    if j.distance < distances[min_ind]:
                        distances[min_ind] = j.distance
                    new_list.append(j)
            states[min_ind] = copy.copy(new_list)

        id = base_three(np.argmin(distances)).rjust(2, "0")

        currentState = currentState.Update((int(id[0])-1) * force, (int(id[1])-1) * force)
        #Uncomment if you want to see the distances live
        #print(currentState.distance)
        running = get_events()
        update_frame(surface)
        

if __name__ == "__main__":
    main()