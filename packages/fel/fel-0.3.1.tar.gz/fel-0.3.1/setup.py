# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fel']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.14,<4.0.0',
 'PyGithub>=1.55,<2.0',
 'PyYAML>=5.4.1,<6.0.0',
 'yaspin>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['fel = fel.__main__:main']}

setup_kwargs = {
    'name': 'fel',
    'version': '0.3.1',
    'description': 'A tool for submitting and landing stacked diffs to GitHub',
    'long_description': '# Fel\nFel is a tool for submitting [stacked diffs](https://medium.com/@kurtisnusbaum/stacked-diffs-keeping-phabricator-diffs-small-d9964f4dcfa6)\nto GitHub. Fel takes care of all the busy work of submitting multiple commits as\na stack of PRs and lets you focus on keeping your diffs reviewable and lets reviewers\nfocus on understanding your code. When your stack is ready to land, Fel handles merging\nall your PRs through GitHub, producing a commit history that looks like you rebased\nthe whole stack at once, without polluting your history with extra merge commits,\nor requiring the upstream project to use an external tool to land diffs to master.\n\n# Demo\n![Fel Demo GIF](https://raw.githubusercontent.com/Zabot/fel/master/.images/demo.gif)\n\nFel even generates graphs for your PRs to indicate all of the diffs in your stack\nand how they relate.\n\n> This diff is part of a [fel stack](https://github.com/zabot/fel)\n> <pre>\n> * <a href="75">#75 Bugfixes in file 4</a>\n> * <a href="74">#74 Added file4</a>\n> | * <a href="73">#73 New line in third file</a>\n> |/  \n> * <a href="72">#72 Third new file</a>\n> * <a href="71">#71 Line 1 in new file</a>\n> * master\n> </pre>\n\n\n# Usage\nFel requires a GitHub oauth token to create and merge PRs on your behalf. Generate\none [here](https://github.com/settings/tokens). Once you have your token, add it\nto the Fel configuration file (default `~/.fel.yml`).\n\n```yaml\ngh_token: <your_token_here>\n```\n\nNow create a new branch and start writing some diffs. Working with stacked diffs\nrequires a different way of thinking, think of each commit as an atomic unit of\nchange. Commit early into the development of each diff and amend often. Leave \ndetailed commit bodies, they\'ll become the contents of your PRs when you submit\nyour stack for review.\n\nOnce your stack is ready, run `fel submit`. Fel will generate a PR for each commit\nin the stack, basing the first PR against `origin/master`, and then each subsequent\nPR against the previous PR in the stack. If multiple stacks overlap, Fel will\ncreate a single PR for the common diffs, and base the diverging diffs on the common\nbase.\n\nWhen your diffs are reviewed and ready to land, checkout the top of your stack\nand run `fel land`. Fel will merge the PRs on GitHub in order by rebasing onto\nthe base branch, without creating the ladder of merge commits associated\nwith a manual stacked PR workflow. After your commits are landed, fel cleans up\nthe branches it generated and leaves you on a fresh checkout of the upstream branch,\nwith all of your diffs landed.\n\n',
    'author': 'Zach Anderson',
    'author_email': 'zach.inbox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zabot/fel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
