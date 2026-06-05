from search.local_search_base import LocalSearchBase
import random


class GeneticAlgorithm(LocalSearchBase):

    def fitness(self, state):
        return 1.0 / (1.0 + self.evaluate(state))

    def reproduce(self, parent1, parent2):
        if len(parent1) == 0:
            return parent2.copy()

        if len(parent2) == 0:
            return parent1.copy()

        c = random.randint(
            1,
            min(len(parent1), len(parent2))
        )

        child = (
            parent1[:c]
            + parent2[c:]
        )

        # حذف سنسورهای تکراری
        child = list(dict.fromkeys(child))

        # رعایت محدودیت تعداد سنسورها
        child = child[:self.world.max_sensors]

        # جلوگیری از حالت خالی
        if len(child) == 0:
            child.append(
                random.choice(
                    self._valid_positions()
                )
            )

        return child

    def mutate(self, state):
        state = state.copy()

        if len(state) == 0:
            return state

        valid_positions = self._valid_positions()

        idx = random.randrange(len(state))

        state[idx] = random.choice(valid_positions)

        state = list(dict.fromkeys(state))

        return state
    
            # ---------- Initial Population ----------

    def run(self, initial_state, population_size=30, generations=100, mutation_rate=0.1):

        population = [list(initial_state)]

        while len(population) < population_size:
            population.append(
                self.initialize_state()
            )

        best_state = min(
            population,
            key=self.evaluate
        )

        best_cost = self.evaluate(best_state)

        evaluations = [best_cost]
        states_history = [best_state.copy()]

        # ---------- Main Loop ----------

        for _ in range(generations):

            fitnesses = [
                self.fitness(individual)
                for individual in population
            ]

            population2 = []

            for _ in range(population_size):

                # WEIGHTED_RANDOM_CHOICES

                parent1 = random.choices(
                    population,
                    weights=fitnesses,
                    k=1
                )[0]

                parent2 = random.choices(
                    population,
                    weights=fitnesses,
                    k=1
                )[0]

                # REPRODUCE

                child = self.reproduce(
                    parent1,
                    parent2
                )

                # MUTATE

                if random.random() < mutation_rate:
                    child = self.mutate(child)

                population2.append(child)

            population = population2

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
