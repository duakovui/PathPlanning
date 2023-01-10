import pygame
from Spot import *
import math
from queue import PriorityQueue

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def update_safe(draw, grid):
	max_safety = 0
	count = 1
	open_set = PriorityQueue()
	for rows in grid:
		for spot in rows:
			if spot.is_barrier():
				spot.safe = 0
				open_set.put((0, count, spot))
				count += 1

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		for neighbor in current.neighbors1:
			if not neighbor.is_open():
				if not neighbor.is_closed():
					neighbor.safe = current.safe + 1
					if max_safety < neighbor.safe:
						max_safety = neighbor.safe
					open_set.put((neighbor.safe, count, neighbor))
					count += 1
					neighbor.make_open()
		draw()
		if not current.is_barrier():
			current.make_closed()

	for row in grid:
		for spot in row:
			spot.safe = max_safety - spot.safe
def reconstruct_path_safe(draw, came_from, approved_set, path_safety, g_score, current):
	while current in came_from:
		tmp_current = current
		current = came_from[current]
		for neighbor in tmp_current.neighbors:
			if neighbor in approved_set:
				if path_safety[neighbor] < path_safety[current] and g_score[neighbor] <= g_score[current]:
					current = neighbor
		current.make_path()
		draw()

def reconstruct_path(draw, came_from, current):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

def algorithm_safe(draw, grid, start, end, anpha, beta, ganma):
	open_set = PriorityQueue()
	open_set.put((0, start.safe, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())
	path_safety = {spot: 0 for row in grid for spot in row}
	path_safety[start] = 0

	open_set_hash = {start}
	approved_set = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path_safe(draw, came_from, approved_set, path_safety, g_score, end)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			if g_score[neighbor] > temp_g_score:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = anpha*g_score[neighbor] + beta*h(neighbor.get_pos(), end.get_pos()) + ganma*neighbor.safe
				if neighbor not in open_set_hash:
					if not neighbor.is_closed():
						open_set.put((f_score[neighbor], neighbor.safe, neighbor))
						open_set_hash.add(neighbor)
						neighbor.make_open()
						path_safety[neighbor] = path_safety[current] + neighbor.safe
						if neighbor not in approved_set:
							approved_set.add(neighbor)
		draw()

		if current != start:
			current.make_closed()

	return False

def algorithm(draw, grid, start, end, anpha, beta):
	open_set = PriorityQueue()
	count = 0
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(draw, came_from, end)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1
			if g_score[neighbor] > temp_g_score:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = anpha*g_score[neighbor] + beta*h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		draw()
		if current != start:
			current.make_closed()

	return False