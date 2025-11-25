from operator import truediv
import pygame
import sys

pygame.init()

width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Lab1-Grafica 2D cu Pygame")

alb = (255, 255, 255)
rosu = (220, 20, 60)
verde = (0, 128, 0)
albastru = (0, 191, 255)
gri = (211, 211, 211)
maro=(128,0,0)
galben=(240,230,140)


x = 900
y = 600
radius = 80
speed = 0.5

rect_w=100
rect_h=80

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x += speed
    if x - radius <= 0 or x + radius >= width:
        speed = -speed

    mx,my=pygame.mouse.get_pos()
    screen.fill(gri)
    pygame.draw.circle(screen, albastru, (x, y), radius)
    pygame.draw.rect(screen,verde,(mx-rect_w,my-rect_h,rect_w,rect_h))
    pygame.draw.line(screen, rosu, (0, 0), (1000, 800), 5)

    pygame.draw.rect(screen, galben, (250, 250, 300, 250))
    pygame.draw.polygon(screen, rosu, [ (250, 250),(400, 150),(550, 250)])
    pygame.draw.rect(screen, maro, (365, 350, 70, 150))
    pygame.draw.rect(screen, albastru, (280, 330, 80, 60))
    pygame.draw.rect(screen, albastru, (440, 330, 80, 60))
    pygame.draw.circle(screen, alb, (365 + 60, 425), 8)

    pygame.display.flip()

pygame.quit()
sys.exit()
