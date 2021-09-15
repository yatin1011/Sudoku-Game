import pygame
import requests

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
buffer = 5

response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

def insert(win, position):
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    i, j = position[1], position[0]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if grid_original[i-1][j-1] != 0:
                    return
                if event.key == 48:  # Checking for 0
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - buffer*2, 50 - buffer*2))
                    pygame.display.update()
                    return
                if 0 < event.key - 48 < 10:  # Checking for valid input
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - buffer*2, 50 - buffer*2))
                    value = myfont.render(str(event.key - 48), True, (0,0,0))
                    win.blit(value, (position[0]*50 + 20, position[1]*50 + 15))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(0, 10):
        if i%3 == 0:
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4)
        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2)

    for i in range(len(grid[0])):
        for j in range(len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j+1)*50 + 20, (i+1)*50 + 15))
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return

main()

print(grid)