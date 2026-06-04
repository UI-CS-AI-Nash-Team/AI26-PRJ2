from search.local_search_base import LocalSearchBase
import math
import random


class SimulatedAnnealing(LocalSearchBase):

    def schedule(self, temperature, cooling_rate, cooling_type):
        if cooling_type == "linear":
            return temperature - cooling_rate
        else:  # default: exponential
            return temperature * cooling_rate


    def run(self, initial_state, max_iterations=100,
            initial_temperature=100.0,
            cooling_rate=0.95,
            cooling_type="linear"):

        current = list(initial_state)
        current_cost = self.evaluate(current)

        best_state = current.copy()
        best_cost = current_cost

        evaluations = [current_cost]
        states_history = [current.copy()]

        temperature = initial_temperature

        for _ in range(max_iterations):
            if temperature <= 0:
                break

            neighbor = random.choice(self.get_neighbor(current))
            neighbor_cost = self.evaluate(neighbor)

            delta = current_cost - neighbor_cost

            if delta > 0 or random.random() < math.exp(delta / temperature):
                current = neighbor
                current_cost = neighbor_cost

            if current_cost < best_cost:
                best_state = current.copy()
                best_cost = current_cost

            evaluations.append(current_cost)
            states_history.append(current.copy())

            temperature = self.schedule(temperature, cooling_rate, cooling_type)

        return best_state, best_cost, evaluations, states_history