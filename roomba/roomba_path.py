import numpy as np


class PotentialGrid:
    """
    Represents the potential grid of a room with sources.

    This class creates and manages a potential field for a room, where each point
    in the room has a potential value calculated by the distance to the nearest source.

    Attributes:
        room_shape (tuple): The dimensions of the room (height, width).
        potential_mask (numpy.ndarray): A 2D array representing the potential field.
        sources (dict): A dictionary of potential sources with their positions as keys.
        allow_diagonal (bool): If True, allows diagonal movements in potential calculations.
    """
    def __init__(self, room_shape: tuple):
        """
        Initialize the PotentialGrid.

        Args:
            room_shape (tuple): The dimensions of the room (height, width).
        """
        self.room_shape = room_shape
        self.potential_mask = None
        self.sources = {}  # Dict of potential sources with their positions as keys
        self.allow_diagonal = False

    def initialize_potential_mask(self):
        """
        Calculates the potential mask for the given grid shape.

        The mask is used to calculate the potential grid for the room. It creates
        a potential field that decreases with distance from the center.
        """
        # Initialize the potential mask with zeros
        self.potential_mask = np.zeros((2*self.room_shape[0], 2*self.room_shape[1]))

        # Calculate the center of the mask
        center_x, center_y = self.room_shape[0] - 1, self.room_shape[1] - 1

        # Iterate through each point in the mask
        for i in range(2*self.room_shape[0]):
            for j in range(2*self.room_shape[1]):
                if self.allow_diagonal:
                    r = np.sqrt((i - center_x)**2 + (j - center_y)**2)  # L2 distance (Euclidean)
                else:
                    r = np.abs(i - center_x) + np.abs(j - center_y)  # L1 distance (Manhattan)
                
                if r == 0:
                    self.potential_mask[i, j] = 2  # Center point has maximum potential
                else:
                    self.potential_mask[i, j] = 2 / (1 + r)  # Potential decays with 1/r from center

    def calculate_potential_in_point(self, point: tuple):
        """
        Calculates the potential at a given point by summing the potentials from all sources.
        Uses the potential.

        Args:
            point (tuple): The (x, y) coordinates of the point to calculate potential for.

        Returns:
            float: The total potential at the given point.
        """
        if not self.sources:
            return 0
        
        potential = 0
        for source_pos in self.sources:
            if self.sources[source_pos]:  # If the source is active
                # Calculate the relative position in the potential mask
                mask_x = self.room_shape[0] + point[0] - source_pos[0] - 1
                mask_y = self.room_shape[1] + point[1] - source_pos[1] - 1
                potential += self.potential_mask[mask_x, mask_y]
        return potential


def roomba_path(starting_point: tuple, potential_grid: PotentialGrid = None):
    """
    Finds path for the roomba to clean a room with the given litter list (in potential_grid.sources).

    Args:
        starting_point (tuple): The initial (x, y) position of the Roomba.
        potential_grid (PotentialGrid): The potential grid representing the room and litter.

    Returns:
        list: A list of (x, y) coordinates representing the path taken by the Roomba.
    """
    whole_path = [starting_point]
    current_position = starting_point

    print("Current position: ", current_position)
    print("Sources: ", [source for source in potential_grid.sources])

    # Continue cleaning while there are still active sources
    while any([potential_grid.sources[source] for source in potential_grid.sources]):
        # Find path to the highest potential point (likely a dirt source)
        path = climb_hill(current_position, potential_grid)
        print("Climbed to ", path[-1])
        whole_path += path
        current_position = path[-1]
        print("Removing source at ", current_position)
        # Mark the source as cleaned
        potential_grid.sources[current_position] = False

    print('Area clear!')
    return whole_path


def climb_hill(start_pos: tuple, potential_grid: PotentialGrid = None):
    """
    Climbs the potential hill starting from the given position.

    Args:
        start_pos (tuple): The (x, y) starting position for the hill climb.
        potential_grid (PotentialGrid): The potential grid representing the room.

    Returns:
        list: A list of (x, y) coordinates representing the path to the highest potential point.
    """
    current_x, current_y = start_pos
    current_height = potential_grid.calculate_potential_in_point([current_x, current_y])

    # Keep track of the path
    path = [(start_pos[0], start_pos[1])]

    # Define possible movement directions
    if potential_grid.allow_diagonal:
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
    else:
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    # Climbing loop
    while True:
        neighbors = []
        # Find valid neighboring positions
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < potential_grid.room_shape[0] and 0 <= ny < potential_grid.room_shape[1]:
                neighbors.append((nx, ny))
        
        # Find the neighbor with the highest potential
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
            # Local maximum reached, end the climb
            break

    return path
