import numpy as np

def roomba_path(room_size: tuple, starting_point: tuple, litter_list: list, diagonal: bool = False):
    """
    Finds path for the roomba to clean a room with the given litter list.
    """
    grid = initialize_potential(room_size, litter_list)
    initial_grid = grid.copy()

    whole_path = [starting_point]
    current_position = starting_point

    print("Current position: ", current_position)
    print("Sources: ", litter_list)
    while len(litter_list) > 0:
        
        
        path = climb_hill(grid, current_position, diagonal)
        print("Climbed to ", path[-1])
        whole_path += path

        current_position = path[-1]
        grid = remove_source_and_update_potential(grid, current_position)
        litter_list.remove(current_position)
    print('Area clear!')
    return whole_path, initial_grid


def climb_hill(potential: np.ndarray, start_pos: tuple, diagonal: bool = False):
    """
    Climbs the potential hill starting from the given position.
    Maybe I could implement a gradient ascend?
    """


    current_x, current_y = start_pos
    current_height = potential[current_x, current_y]

    # Keep track of the path
    path = [(start_pos[0], start_pos[1])]

    if diagonal:
        directions = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1),           (0, 1),
                    (1, -1),  (1, 0),  (1, 1)]
    else:
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Climbing loop
    while True:
        neighbors = []
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < potential.shape[0] and 0 <= ny < potential.shape[1]:
                neighbors.append((nx, ny))
        
        # Find the neighbor with the highest height
        max_height = current_height
        next_pos = (current_x, current_y)
        for nx, ny in neighbors:
            neighbor_height = potential[nx, ny]
            if neighbor_height > max_height:
                max_height = neighbor_height
                next_pos = (nx, ny)
        
        # Move to the neighbor if it's higher
        if max_height > current_height:
            current_x, current_y = next_pos
            current_height = max_height
            path.append((current_x, current_y))
        else:
            # Local maximum reached
            break

    return path


def initialize_potential(grid_shape: tuple, sources: list):
    """
    Calculates the potential grid based on the sources
    """

    potential_grid = np.zeros((grid_shape[0], grid_shape[1]))

    for i in range(grid_shape[0]):
        for j in range(grid_shape[1]):
            potential = 0
            for source in sources:
                r = L1_distance((i, j), source)
                if r == 0:
                    potential += 2  # Source point itself. Value is arbitrary but must be > 1
                else:
                    potential += 1 / r  # Additive potential from source
            potential_grid[i, j] = potential
    
    return potential_grid


def remove_source_and_update_potential(potential_grid: np.ndarray, removed_source: tuple):
    """
    Recalculates the potential grid after removing a source from it by subtracting
    the contribution of the removed source from the current potential grid.
    """
    
    # Loop through all points in the grid and subtract the potential from the removed source
    for i in range(potential_grid.shape[0]):
        for j in range(potential_grid.shape[1]):
            r = L1_distance((i, j), removed_source)
            if r == 0:
                potential_grid[i, j] -= 2  # The removed source point itself
            else:
                potential_grid[i, j] -= 1 / r  # Subtract the source's potential

    return potential_grid


def L1_distance(p1, p2):
    """
    Calculates L1 distance between two points
    """
    return np.abs(p1[0] - p2[0]) + np.abs(p1[1] - p2[1])
