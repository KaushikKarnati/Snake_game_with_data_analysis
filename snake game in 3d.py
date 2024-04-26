import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

def draw_cube(position):
    """ Draws a cube at the given position """
    glPushMatrix()
    glTranslate(*position)  # Move to the right position
    glBegin(GL_QUADS)

    # Define the 6 faces of the cube
    vertices = (
        (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
        (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1),
        (1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1),
        (-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1),
        (-1, 1, -1), (1, 1, -1), (1, 1, 1), (-1, 1, 1),
        (-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)
    )
    # Normal vectors for each face
    normals = (
        (0, 0, -1), (0, 0, 1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)
    )
    # Define vertices for each face
    for i in range(6):
        glNormal3dv(normals[i])
        for j in range(4):
            glVertex3fv(vertices[i * 4 + j])
    glEnd()
    glPopMatrix()

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    # Game settings
    snake_positions = [(0, 0, 0)]
    apple_position = (random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5))
    direction = (1, 0, 0)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    direction = (-1, 0, 0)
                if keys[pygame.K_RIGHT]:
                    direction = (1, 0, 0)
                if keys[pygame.K_UP]:
                    direction = (0, 1, 0)
                if keys[pygame.K_DOWN]:
                    direction = (0, -1, 0)
                if keys[pygame.K_PAGEUP]:
                    direction = (0, 0, 1)
                if keys[pygame.K_PAGEDOWN]:
                    direction = (0, 0, -1)

        # Move the snake
        new_head = tuple(map(sum, zip(snake_positions[0], direction)))
        snake_positions.insert(0, new_head)
        if new_head != apple_position:
            snake_positions.pop()
        else:
            apple_position = (random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glColor3f(1, 0, 0)
        draw_cube(apple_position)
        glColor3f(0, 1, 0)
        for pos in snake_positions:
            draw_cube(pos)

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
