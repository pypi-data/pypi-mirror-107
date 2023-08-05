from collections import defaultdict


def evaluate_votes_for_candidate_pair(candidate_0, candidate_1, votes):
    candidate_0_score = 0
    candidate_1_score = 0
    for vote in votes:
        if vote[candidate_0] < vote[candidate_1]:
            candidate_0_score += 1
        elif vote[candidate_1] < vote[candidate_0]:
            candidate_1_score += 1

    return {candidate_0: candidate_0_score, candidate_1: candidate_1_score}


def tabulate_pairwise_results(pairwise_results):
    table = defaultdict(lambda: defaultdict(list))
    for result in pairwise_results:
        if len(set(result.values())) == 1:
            continue
        looser, winner = sorted(
            result.keys(), key=lambda k: result[k]  # pylint: disable=cell-var-from-loop
        )  # noqa: W0640
        table[winner]["wins"].append(looser)
        table[looser]["losses"].append(winner)

    return _get_normalized_table(table)


def get_winner_from_result_table(result_table):
    try:
        return next(
            candidate
            for candidate in result_table
            if len(result_table[candidate]["losses"]) == 0
        )
    except StopIteration:
        return None


def get_n_winners_from_result_table(n, result_table):
    iteration = n
    winners = []
    pruned_table = _get_normalized_table(result_table)
    while iteration > 0:
        next_winner = get_winner_from_result_table(pruned_table)
        if next_winner is None:
            break
        winners.append(next_winner)
        pruned_table = drop_candidate_from_result_table(next_winner, pruned_table)
        iteration -= 1

    return winners, pruned_table


def drop_candidate_from_result_table(candidate, result_table):
    return {
        person: {
            ws_or_ls: [opp for opp in opponents if opp != candidate]
            for ws_or_ls, opponents in wins_and_losses.items()
        }
        for person, wins_and_losses in result_table.items()
        if person != candidate
    }


def _get_normalized_table(table):
    return {
        person: {"wins": wins_and_losses["wins"], "losses": wins_and_losses["losses"]}
        for person, wins_and_losses in table.items()
    }
