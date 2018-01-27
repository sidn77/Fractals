"""
Initiator, generator and production rule.
Mandelbrot: z sub(n + 1) = F(z sub n)
Julia: F = f + ig

First we create an infinite sequence of numbers according to
the following pattern:
We start with 0.
Every new number is the previous number squared, plus c.
In mathematical notation, we have a sequence (zn), where zn+1 = zn2 + c.
If this sequence of numbers always increases and tends to infinity (it
diverges), we colour the point white.
However if the sequence does not increase beyond a certain
limit (if it is bounded), we colour the point black

We repeat this process for every point in the coordinate system.
The collection of all the black points is the Mandelbrot set.
Move the blue pin below to explore what happens at various points

TODO: Able to watch the fractal to be drawn.
"""
import pygame
from pygame.locals import *
import cmath
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1),
    )

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
    )

faces = (
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
    )

colors = (
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    )


def m_brot():
    epsilon = 0.04
    x_range = np.arange(-2, 2, epsilon)
    max_it = 10
    print len(x_range)

    glBegin(GL_LINES)

    for x in x_range:
        for y in x_range:
            it = 0
            z = complex(0, 0)
            c = complex(x, y)
            while abs(z) < 2 and it < max_it:
                z = (z ** 2) + c
                it += 1
            glVertex3fv((x, y, 0))
            glColor3fv(colors[12 % it])
    glEnd()


def cube():
    glBegin(GL_QUADS)

    for face in faces:
        x = 0
        for vertex in face:
            x += 1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])

    glEnd()

    glBegin(GL_LINES)

    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display,
                            DOUBLEBUF | OPENGL)  # what is doublebuf

    gluPerspective(45, (display[0] / display[1]),
                   0.1, 50.0)  # last args are z-near and z-far

    glTranslatef(0.0, 0.0, -10)

    #         speed, x, y, z
    glRotatef(  1,   1, 0, 0)
    n = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.5, 0, 0)
                if event.key == pygame.K_RIGHT:
                    glTranslatef(0.5, 0, 0)
                if event.key == pygame.K_UP:
                    glTranslatef(0, 0.5, 0)
                if event.key == pygame.K_DOWN:
                    glTranslatef(0, -0.5, 0)
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        glTranslatef(0, 0, 1)
                    if event.button == 5:
                        glTranslatef(0, 0, -1)

        # glRotatef(1, 1, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        m_brot()
        pygame.display.flip()  # use flip() why not update
        pygame.time.wait(10)  # 10 miliseconds


main()
