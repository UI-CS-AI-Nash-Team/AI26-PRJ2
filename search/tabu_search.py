from search.local_search_base import LocalSearchBase


class TabuSearch(LocalSearchBase):
    def run(self, initial_state, max_iterations=100):

        best_solution = (initial_state, self.evaluate(initial_state))
        tabu_list = []
        tabu_size = 10

        current_state = initial_state

        evaluations = [self.evaluate(current_state)]
        states_history = [current_state.copy()]

        for _ in range(max_iterations):

            successors = self.get_neighbor(current_state)

            # actually it's not possible to don't have any successor, but we let be here
            if not successors:
                break

            admissibles =  []
            for successor in successors:
                if not self._is_tabu(current_state, successor, tabu_list) or self._satisfies_aspiration(successor, best_solution):
                    admissibles.append(successor)

            if admissibles:
                next_state = min(admissibles, key=self.evaluate)
                self._add_to_tabu(tabu_list, tabu_size, self._extract_move(current_state, next_state))
                current_state = next_state

                evaluations.append(self.evaluate(current_state))
                states_history.append(current_state.copy())

                #fallback
            else:
                next_state = min(successors, key=self.evaluate)
                self._add_to_tabu(tabu_list, tabu_size, self._extract_move(current_state, next_state))
                current_state = next_state

                evaluations.append(self.evaluate(current_state))
                states_history.append(current_state.copy())

            if self.evaluate(current_state) < self.evaluate(best_solution[0]):
                best_solution = (current_state, self.evaluate(current_state))

        best_cost = best_solution[1]
        best_state = best_solution[0]
        
        return best_state, best_cost, evaluations, states_history


    def _add_to_tabu(self, tabu_list, tabu_size, move):
        if move not in tabu_list:
            if len(tabu_list) >= tabu_size:
                tabu_list.pop(0)
            tabu_list.append(move)


    def _extract_move(self, initial_state, successor_state):
        """
        Returns the move that transforms initial_state into successor_state.
        Possible move types:
            - ("move", old_position, new_position)
            - ("add", new_position)
            - ("remove", removed_position)
        """
    
        initial_set = set(initial_state)
        successor_set = set(successor_state)
    
        # Case 1: Sensor Added
        if len(successor_state) == len(initial_state) + 1:
            added = successor_set - initial_set
            if added:
                return ("add", added.pop())
    
        # Case 2: Sensor Removed
        if len(successor_state) == len(initial_state) - 1:
            removed = initial_set - successor_set
            if removed:
                return ("remove", removed.pop())
    
        # Case 3: Sensor Moved
        if len(successor_state) == len(initial_state):
            removed = initial_set - successor_set
            added = successor_set - initial_set
    
            if len(removed) == 1 and len(added) == 1:
                return ("move", removed.pop(), added.pop())
    
        return ("unknown", None)


    def _is_tabu(self, initial_state, successor_state, tabu_list):
        """
        Returns True if the move from initial_state to successor_state
        is tabu (including reverse operations).
        """

        move = self._extract_move(initial_state, successor_state)

        if move[0] == "move":
            _, old_pos, new_pos = move
            reverse_move = ("move", new_pos, old_pos)

            return move in tabu_list or reverse_move in tabu_list

        elif move[0] == "add":
            _, pos = move
            reverse_move = ("remove", pos)

            return move in tabu_list or reverse_move in tabu_list

        elif move[0] == "remove":
            _, pos = move
            reverse_move = ("add", pos)

            return move in tabu_list or reverse_move in tabu_list

        return False

    def _satisfies_aspiration(self, successor_state, best_solution):
        """
        Returns True if successor_state satisfies the aspiration criterion.
        That is, its cost is better than the global best cost.
        """

        _, best_cost = best_solution
        successor_cost = self.evaluate(successor_state)

        return successor_cost < best_cost