# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['condorcet']

package_data = \
{'': ['*']}

install_requires = \
['pytest-mock>=3.6.1,<4.0.0']

setup_kwargs = {
    'name': 'condorcet',
    'version': '0.1.1',
    'description': 'Condorcet is a utility for evaluating votes using the condorcet method',
    'long_description': '# Condorcet\n\nCondorcet is a Python library for evaluating votes using [the condorcet method](https://en.wikipedia.org/wiki/Condorcet_method#Summary).\n\n\n## Installation\n\n```\npip install condorcet\n```\n\n\n## Synopsis\n\nThe library exposes a class `CondorcetEvaluator` which is called with a list of candidates and a list of votes in order to instantiate an evaluator.\n\n```python\n# Attention! This is pseudo-code!!\nCondorcetEvaluator : List[Candidates], List[Votes] -> CondorcetEvaluator\n```\n\nThis instantiated evaluator has a method `get_n_winners` which takes a (non-negative) integer, n, and returns a list containing __at most__ the first n winners in order, along with a table of pairwise wins and losses for __the remainder__ of the candidates (the ones who are not in the list of winners).\n\n__At most__, because some times there may not be that many winners &mdash; a cycle might exist among a set of candidates. This is one of the motivations for returning a table of pairwise wins and losses along with the list of winners.\n\n```python\n# Attention! This is pseudo-code!!\nCondorcetEvaluator.get_n_winners : int -> List[Candidates], WinsAndLossesTable\n```\n\nAnd that is that for that!\n\n\n## Quick Start: Rochambeau Games\n\nThis years\' edition of the Rochambeau Games had seven people ranking four candidates &mdash Rock, Paper, Scissors, and the relatively unknown Dynamite &mdash from 1 to 4, where candidate 1 on someone\'s ballot would be their most prefered candidate, and 4, the less preferred.\n\nAs the election officer you are to evaluate their votes according to the Condorcet method and announce the result.\n\nYou have the following data:\n\n```python\ncandidates = ["Rock", "Paper", "Scissors", "Dynamite"]\nvotes = [\n    {"Rock": 1, "Scissors": 2, "Dynamite": 3, "Paper": 4},\n    {"Rock": 1, "Dynamite": 2, "Scissors": 3, "Paper": 4},\n    {"Dynamite": 1, "Paper": 2, "Rock": 3, "Scissors": 4},\n    {"Paper": 1, "Dynamite": 2, "Rock": 3, "Scissors": 4},\n    {"Scissors": 1, "Paper": 2, "Dynamite": 3, "Rock": 4},\n    {"Scissors": 1, "Dynamite": 2, "Paper": 3, "Rock": 4},\n    {"Rock": 1, "Paper": 2, "Dynamite": 3, "Scissors": 4},\n]\n```\n\nYou want to announce how the four candidates fared with respect to each other. So, you instantiate a condorcet evaluator using the list of candidates and list of votes, and ask it to produce four winners as shown below:\n\n```python\nimport condorcet\n\nevaluator = condorcet.CondorcetEvaluator(candidates=candidates, votes=votes)\nwinners, rest_of_table = evaluator.get_n_winners(4)\n```\n\nPrint out the list of winners.\n\n```python\nprint(winners)\n\n# [\'Dynamite\']\n```\n\nFour winners were asked for, but only one was returned. Studying the table of wins and losses for the rest of the candidates will throw light on the underlying issue.\n\n```python\nprint(rest_of_table)\n\n# {\n#  \'Paper\': {\n#      \'losses\': [\'Scissors\'],\n#      \'wins\': [\'Rock\']\n#   },\n#  \'Rock\': {\n#      \'losses\': [\'Paper\'],\n#      \'wins\': [\'Scissors\']\n#  },\n#  \'Scissors\': {\n#      \'losses\': [\'Rock\'],\n#      \'wins\': [\'Paper\']\n#  }\n# }\n```\n\nThe wins and losses table for the rest of the candidates shows that no winner could be picked among them, as each one has lost to at least one of the other.\n\n\n## Contributing\n\nCondorcet is happy to receive contributions. Please submit a PR/MR containing your contribution (including tests if it\'s a code contribution) and bug the maintainer to review and merge.\n\nDon\'t forget to add yourself to CONTRIBUTORS.txt\n',
    'author': 'Mfon Eti-mfon',
    'author_email': 'mfonetimfon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/a-thousand-juniors/condorcet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
