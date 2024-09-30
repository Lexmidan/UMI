import numpy as np


class PotentialGrid:
    """
    Represents the potential grid of a room with sources.
    """
    def __init__(self, room_shape: tuple):
        self.room_shape = room_shape
        self.potential_mask = None
        self.sources = {} #Dict of potential sources with their positions as keys
        self.allow_diagonal = False

    def initialize_potential_mask(self):
        """
        Calculates the potential mask for the given grid shape. The mask is used to
        calculate the potential grid for the room.
        """

        self.potential_mask = np.zeros((2*self.room_shape[0], 2*self.room_shape[1]))

        center_x, center_y = self.room_shape[0] - 1, self.room_shape[1] - 1
        for i in range(2*self.room_shape[0]):
            for j in range(2*self.room_shape[1]):
                if self.allow_diagonal:
                    r = np.sqrt((i - center_x)**2 + (j - center_y)**2)  # L2 distance
                else:
                    r = np.abs(i - center_x) + np.abs(j - center_y)  # L1 distance
                
                if r == 0:
                    self.potential_mask[i, j] = 2  # Center point
                else:
                    self.potential_mask[i, j] = 2 / (1 + r)  # Decay with 1/r from center


    def calculate_potential_in_point(self, point: tuple):
        """
        Calculates the potential in the given point by summing the potentials
        from all sources.
        """
        if not self.sources:
            return 0
        
        potential = 0
        for source_pos in self.sources:
            if self.sources[source_pos]:
                mask_x = self.room_shape[0] + point[0] - source_pos[0] - 1
                mask_y = self.room_shape[1] + point[1] - source_pos[1] - 1
                potential += self.potential_mask[mask_x, mask_y]
        return potential


def roomba_path(starting_point: tuple,  potential_grid: PotentialGrid = None):
    """
    Finds path for the roomba to clean a room with the given litter list.
    """
    whole_path = [starting_point]
    current_position = starting_point

    print("Current position: ", current_position)
    print("Sources: ", [source for source in potential_grid.sources])

    # while any source is active
    while any([potential_grid.sources[source] for source in potential_grid.sources]):
        
        path = climb_hill(current_position, potential_grid)
        print("Climbed to ", path[-1])
        whole_path += path
        current_position = path[-1]
        print("Removing source at ", current_position)
        potential_grid.sources[current_position] = False

    print('Area clear!')
    return whole_path


def climb_hill(start_pos: tuple, potential_grid: PotentialGrid = None):
    """
    Climbs the potential hill starting from the given position.
    Maybe I could implement a gradient ascend?
    """


    current_x, current_y = start_pos
    current_height = potential_grid.calculate_potential_in_point([current_x, current_y])

    # Keep track of the path
    path = [(start_pos[0], start_pos[1])]

    if potential_grid.allow_diagonal:
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
            if 0 <= nx < potential_grid.room_shape[0] and 0 <= ny < potential_grid.room_shape[1]:
                neighbors.append((nx, ny))
        
        # Find the neighbor with the highest height
        max_height = current_height
        next_pos = (current_x, current_y)
        for nx, ny in neighbors:
            neighbor_height = potential_grid.calculate_potential_in_point((nx, ny))
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
