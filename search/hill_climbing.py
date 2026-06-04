from search.local_search_base import LocalSearchBase


class HillClimbing(LocalSearchBase):
    def run(self, initial_state, **kwargs):
        """
        TODO: Implement the Hill Climbing algorithm.
        
        Parameters
        ----------
        initial_state : list of tuples
            The initial configuration of sensors.
        **kwargs : 
            Define and add any other parameters you might need for the algorithm 

        Returns
        -------
        best_state : list of tuples
            The best configuration found.
        best_cost : int or float
            The cost of the best configuration.
        evaluations : list
            List of costs at each iteration (used for plotting).
        states_history : list of lists
            List of states at each iteration (used for animation).
        """
        max_iterations = kwargs.get("max_iterations", 100)

        current = list(initial_state)
        current_cost = self.evaluate(current)

        evaluations = [current_cost]
        states_history = [current.copy()]

        for _ in range(max_iterations):
            neighbor = min(self.get_neighbor(current), key=self.evaluate)
            neighbor_cost = self.evaluate(neighbor)

            if neighbor_cost >= current_cost:
                return current, current_cost, evaluations, states_history

            current = neighbor
            current_cost = neighbor_cost

            evaluations.append(current_cost)
            states_history.append(current.copy())

        return current, current_cost, evaluations, states_history
