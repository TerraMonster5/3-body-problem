import pygame
from pygame.math import Vector2, Vector3

G: float = 6.6743015e-11

class Body:
    def __init__(self, pos: tuple | Vector2, vel: tuple | Vector2, mass: float):
        self._pos: Vector2 = Vector2(pos)
        self._vel: Vector2 = Vector2(vel)
        self._acl: Vector2 = Vector2(0, 0)
        self._rfv: Vector2 = Vector2(0, 0)
        self._mass = mass

    def update(self):
        pass

    def render(self):
        pass

    def calcResultantForce(self, bodies):
        pass