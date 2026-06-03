import random
import math

class LocalSearchBase:
    def __init__(self, world):
        self.world = world

    def evaluate(self, state):


        targets = self.world.get_targets()
        sensor_range = self.world.sensor_range

        uncovered_targets = 0

        for target in targets:
            is_covered = False
            for sensor in state:
                if (math.dist(target, sensor) <= sensor_range): #we use Euclidean Distance not Manhattan distance becuase sensor range follows direct distance
                    is_covered = True
                    break
            if not is_covered:
                uncovered_targets += 1
        
        w_targets = 1.0
        w_sensors = 0.5
        
        cost = w_targets * uncovered_targets + w_sensors * len(state)
        return cost

    def get_neighbor(self, state):
        current = list(state)
        used_positions = set(current)
        successors = [] #list of state candidates 

        #move existing sensors
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for i, (x, y) in enumerate(current):
            for dx, dy in directions:
                new_position = (x + dx, y + dy)

                if new_position in used_positions:
                    continue

                if not self.world.is_valid_position(*new_position):
                    continue

                new_state = current.copy()
                new_state[i] = new_position
                successors.append(new_state)

        #add a new sensor (if allowed)
        if len(current) < self.world.max_sensors:
            for pos in self._valid_positions():
                if pos not in used_positions:
                    successors.append(current + [pos])

        #remove an existing sensor
        for i in range(len(current)):
            new_state = current[:i] + current[i + 1:]
            successors.append(new_state)

        #return best neighbor
        if not successors:
            return current.copy()

        return successors
        #return random.choice(candidates)            for simulated_annealing
        #return min(candidates, key=self.evaluate)   for hill climbing
        # i think this is wrong to return just one state, should return all successors then algorithm decide which one to choose

    def initialize_state(self):
        """
        TODO: Generate a valid initial state.
        
        Create a starting configuration of sensors within the grid boundaries,
        respecting the maximum sensor limits and obstacle placements.
        
        Returns:
            initial_state (list of tuples): The starting coordinates of the sensors.
        """

        valid_positions = self._valid_positions()

        if not valid_positions:
            return []

        max_count = min(self.world.max_sensors, len(valid_positions))

        sensor_count = random.randint(1, max_count)

        return random.sample(valid_positions, sensor_count)

    def _valid_positions(self):
        positions = []
        for x in range(self.world.rows):
            for y in range(self.world.cols):
                if self.world.is_valid_position(x, y):
                    positions.append((x, y))
        return positions
