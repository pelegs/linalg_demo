#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import sys
import numpy as np
import pygame


class point:
    def __init__(self, px, py, i, j):
        self.pos = np.array([px, py])
        self.i, self.j = i, j

    def make_neighbors(self, grid):
        neighbors_x = [grid.points[self.i+di][self.j]
                       for di in [-1, 1]
                       if 0 < self.i + di < grid.nx]
        neighbors_y = [grid.points[self.i][self.j+dj]
                       for dj in [-1, 1]
                       if 0 < self.j + dj < grid.ny]
        self.neighbors = neighbors_x + neighbors_y

    def draw_point(self, surface, center, r=2):
        pygame.draw.circle(screen, [0, 255, 150], (self.pos+center).astype(int), r, 0)

    def draw_lines(self, surface, center, w=1):
        for neighbor in self.neighbors:
            pygame.draw.line(screen, [100, 100, 100], (self.pos+center).astype(int), (neighbor.pos+center).astype(int), w)

    def transform(self, matrix):
        self.pos = np.dot(matrix, self.pos)

    def print_data(self):
        print(self.pos)


class Grid:
    def __init__(self, nx, ny, sx, sy):
        self.nx = nx
        self.ny = ny
        self.sx = sx
        self.sy = sy

        self.points = [[point(sx*(i-nx/2), sy*(j-ny/2), i, j)
                        for j in range(ny)]
                        for i in range(nx)]
        for row in self.points:
            for pnt in row:
                pnt.make_neighbors(self)

    def reset(self):
        self.points = [[point(self.sx*(i-self.nx/2), self.sy*(j-self.ny/2), i, j)
                        for j in range(self.ny)]
                        for i in range(self.nx)]
        for row in self.points:
            for pnt in row:
                pnt.make_neighbors(self)

    def draw_points(self, surface, center):
        for row in self.points:
            for pnt in row:
                pnt.draw_point(surface, center)

    def draw_lines(self, surface, center):
        for row in self.points:
            for pnt in row:
                pnt.draw_lines(surface, center)

    def transform(self, matrix):
        for row in self.points:
            for pnt in row:
                pnt.transform(matrix)

    def print_data(self):
        for row in self.points:
            for point in row:
                point.print_data()


def rotate(angle):
    s = np.sin(angle)
    c = np.cos(angle)
    return np.array([[c, -s],
                     [s,  c]])

def apply_matrix(M, grid, i, j, a):
    grid.reset()
    M[i, j] += a
    print(M)
    grid.transform(M)


g = Grid(25, 25, 40, 40)
a = 0.01
M = np.array([[1, 0],
              [0, 1]]).astype(np.float64)

pygame.init()
screen = pygame.display.set_mode((800, 800))
center = np.array([400, 400]).astype(int)

while True:
    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                apply_matrix(M, g, 0, 0, +0.1)
            if event.key == pygame.K_a:
                apply_matrix(M, g, 0, 0, -0.1)
            if event.key == pygame.K_w:
                apply_matrix(M, g, 0, 1, +0.1)
            if event.key == pygame.K_s:
                apply_matrix(M, g, 0, 1, -0.1)
            if event.key == pygame.K_e:
                apply_matrix(M, g, 1, 0, +0.1)
            if event.key == pygame.K_d:
                apply_matrix(M, g, 1, 0, -0.1)
            if event.key == pygame.K_r:
                apply_matrix(M, g, 1, 1, +0.1)
            if event.key == pygame.K_f:
                apply_matrix(M, g, 1, 1, -0.1)

    # Draw
    screen.fill([0, 0, 0])
    g.draw_lines(screen, center)
    g.draw_points(screen, center)

    # Update display
    pygame.display.update()
