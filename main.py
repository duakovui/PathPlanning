import pygame
import Astar
import Grid
from Spot import *
import os


WIDTH = 750
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

def fileCount(folder):
    "count the number of files in a directory"

    count = 0

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        if os.path.isfile(path):
            count += 1

    return count

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def main(win, width):
	number_of_maps = fileCount("map")
	current_map = 0
	ROWS = 50
	grid = Grid.make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		Grid.draw(win, grid, ROWS, width)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_s:
					number_of_maps += 1
					f = open("map\map"+str(number_of_maps)+".txt","a+")
					for row in grid:
						for spot in row:
							if spot.is_barrier():
								f.write("1")
							else:
								f.write("0")
						f.write("\n")
					f.close()

				if event.key == pygame.K_LEFT:
					if current_map > 1:
						current_map -= 1
					else: current_map = number_of_maps
					f = open("map\map"+str(current_map)+".txt", "r")
					data = f.readlines()
					reset_grid(grid)
					for i in range(ROWS):
						for j in range(ROWS):
							spot = grid[i][j]
							if data[i][j] == "1":
								spot.make_barrier()
					f.close()
					Grid.draw(win, grid, ROWS, width)

				if event.key == pygame.K_RIGHT:
					if current_map < number_of_maps:
						current_map += 1
					else: current_map = 1
					f = open("map\map"+str(current_map)+".txt", "r")
					data = f.readlines()
					reset_grid(grid)
					for i in range(ROWS):
						for j in range(ROWS):
							spot = grid[i][j]
							if data[i][j] == "1":
								spot.make_barrier()
					f.close()
					Grid.draw(win, grid, ROWS, width)

				if event.key == pygame.K_u:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					Astar.update_safe(lambda: Grid.draw(win, grid, ROWS, width), grid)

				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
							if spot != start and spot != end and not spot.is_barrier():
								spot.reset()

					Astar.algorithm_safe(lambda: Grid.draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_a and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
							if spot != start and spot != end and not spot.is_barrier():
								spot.reset()
					Astar.algorithm(lambda: Grid.draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = Grid.make_grid(ROWS, width)

				if event.key == pygame.K_ESCAPE:
					run = False

	pygame.quit()

main(WIN, WIDTH)