import itertools

from . import utils


class CondorcetEvaluator:
    def __init__(self, *, candidates, votes):
        self.result_table = self._compute_result_table(candidates, votes)

    @staticmethod
    def _compute_result_table(candidates, votes):
        pairwise_combos = itertools.combinations(candidates, 2)
        return utils.tabulate_pairwise_results(
            [
                utils.evaluate_votes_for_candidate_pair(*combo, votes)
                for combo in pairwise_combos
            ]
        )

    def get_n_winners(self, n):
        return utils.get_n_winners_from_result_table(n, self.result_table)
