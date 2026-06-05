from search.local_search_base import LocalSearchBase
import random


class GeneticAlgorithm(LocalSearchBase):

    def fitness(self, state):
        cost = self.evaluate(state)
        return 1 / (1 + cost)

    def selection(self, population):
        """
        Tournament Selection
        """
        tournament_size = min(3, len(population))

        candidates = random.sample(population, tournament_size)

        return min(candidates, key=self.evaluate)

    def crossover(self, parent1, parent2):
        """
        Combine two parents.
        """

        if not parent1:
            return parent2.copy()

        if not parent2:
            return parent1.copy()

        cut1 = random.randint(0, len(parent1))
        cut2 = random.randint(0, len(parent2))

        child = parent1[:cut1] + parent2[cut2:]

        # remove duplicates
        unique = []
        seen = set()

        for sensor in child:
            if sensor not in seen:
                unique.append(sensor)
                seen.add(sensor)

        child = unique

        # respect max sensors
        if len(child) > self.world.max_sensors:
            child = random.sample(child, self.world.max_sensors)

        return child

    def mutation(self, state, mutation_rate):
        """
        Move / Add / Remove sensor
        """

        child = list(state)

        if random.random() > mutation_rate:
            return child

        action = random.choice(["move", "add", "remove"])

        # move
        if action == "move" and child:

            idx = random.randrange(len(child))

            valid_positions = self._valid_positions()

            free_positions = [
                p for p in valid_positions
                if p not in child
            ]

            if free_positions:
                child[idx] = random.choice(free_positions)

        # add
        elif (
            action == "add"
            and len(child) < self.world.max_sensors
        ):

            valid_positions = self._valid_positions()

            free_positions = [
                p for p in valid_positions
                if p not in child
            ]

            if free_positions:
                child.append(random.choice(free_positions))

        # remove
        elif action == "remove" and len(child) > 1:

            idx = random.randrange(len(child))
            child.pop(idx)

        return child

    def run(self,
            initial_state,
            population_size=30,
            generations=100,
            mutation_rate=0.1):

        population = []

        # initial population
        population.append(list(initial_state))

        while len(population) < population_size:
            population.append(self.initialize_state())

        best_state = min(population, key=self.evaluate)
        best_cost = self.evaluate(best_state)

        evaluations = [best_cost]
        states_history = [best_state.copy()]

        for _ in range(generations):

            new_population = []

            while len(new_population) < population_size:

                parent1 = self.selection(population)
                parent2 = self.selection(population)

                child = self.crossover(parent1, parent2)

                child = self.mutation(
                    child,
                    mutation_rate
                )

                new_population.append(child)

            population = new_population

            generation_best = min(
                population,
                key=self.evaluate
            )

            generation_cost = self.evaluate(
                generation_best
            )

            if generation_cost < best_cost:
                best_cost = generation_cost
                best_state = generation_best.copy()

            evaluations.append(best_cost)
            states_history.append(best_state.copy())

        return (
            best_state,
            best_cost,
            evaluations,
            states_history
        )
