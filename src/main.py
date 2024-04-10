from __future__ import annotations

import pygame
from pygame.math import Vector2

from math import sqrt

pygame.init()

CLOCK = pygame.time.Clock()
def dt() -> float: return CLOCK.get_time()/100

SCREEN: pygame.Surface = pygame.display.set_mode((800, 800))

G: float = 6.6743015e-11

class Body:
    def __init__(self, pos: tuple | Vector2, vel: tuple | Vector2, mass: float) -> None:
        self._pos: Vector2 = Vector2(pos)
        self._vel: Vector2 = Vector2(vel)
        self._acc: Vector2 = Vector2(0, 0)
        self._rfv: Vector2 = Vector2(0, 0)
        self._mass = mass

    def update(self) -> None:
        self._acc.x = self._rfv.x/self._mass
        self._acc.y = self._rfv.y/self._mass

        self._pos.x += self._vel.x*dt()+0.5*self._acc.x*((dt())**2)
        self._pos.y += self._vel.y*dt()+0.5*self._acc.y*((dt())**2)

        self._vel.x += self._acc.x*dt()
        self._vel.y += self._acc.y*dt()

    def render(self) -> None:
        pygame.draw.circle(SCREEN, (255, 0, 0), self._pos, 10)

    def calcResultantForce(self, bodies: list[Body]) -> None:
        self._rfv.x = self._rfv.y = 0
        for body in bodies:
            r = self._pos.distance_to(body.getPos())
            f = (G*self._mass*body.getMass())/(r**2)

            x = "eq" if self._pos.x == body.getPos().x else "lt" if self._pos.x > body.getPos().x else "gt"
            y = "eq" if self._pos.y == body.getPos().y else "lt" if self._pos.y > body.getPos().y else "gt"

            h = sqrt(((self._pos.x-body.getPos().x)**2)+((self._pos.y-body.getPos().y)**2))

            match (x, y):
                case ("eq", "lt"):
                    self._rfv.y -= f
                case ("eq", "gt"):
                    self._rfv.y += f
                case ("lt", "eq"):
                    self._rfv.x -= f
                case ("gt","eq"):
                    self._rfv.x += f
                case ("lt", "lt"):
                    self._rfv.x -= (abs(self.pos.x-body.getPos().x)/h)*f
                    self._rfv.y -= (abs(self.pos.y-body.getPos().y)/h)*f
                case ("lt", "gt"):
                    self._rfv.x -= (abs(self.pos.x-body.getPos().x)/h)*f
                    self._rfv.y += (abs(self.pos.y-body.getPos().y)/h)*f
                case ("gt", "lt"):
                    self._rfv.x += (abs(self.pos.x-body.getPos().x)/h)*f
                    self._rfv.y -= (abs(self.pos.y-body.getPos().y)/h)*f
                case ("gt", "gt"):
                    self._rfv.y += (abs(self.pos.y-body.getPos().y)/h)*f
                    self._rfv.x += (abs(self.pos.x-body.getPos().x)/h)*f

    def getPos(self) -> Vector2:
        return self._pos

    def getMass(self) -> float:
        return self._mass

BODIES: list[Body] = [Body((50, 100), (0, 0), 100), Body((200, 500), (0, 0), 100), Body((400, 700), (0, 0), 100)]

running = True
while running:
    if pygame.QUIT in map(lambda x: x.type, pygame.event.get()):
        running = False
    
    for body in BODIES:
        SCREEN.fill((0, 0, 0))
        body.calcResultantForce(BODIES)
        body.update()
        body.render()
        pygame.display.update()
        CLOCK.tick()