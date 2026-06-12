import pygame

pygame.init()
pygame.mixer.init()

HEIGHT,WIDTH=500,900
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First game")

WHITE=(255,255,55)
FPS=60
def draw_window():
    WIN.fill(WHITE)
    pygame.display.update()

def main():
    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            print(event.type)
            if event.type==pygame.QUIT:
                run=False
        draw_window()
    pygame.quit()


if __name__=='__main__':
    main()