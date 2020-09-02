import re
from typing import List


def get_options(help_str: str) -> List[str]:
    """
    Options:
      --env [development|production]  [required]
      --is-test                       [required]
      --age INTEGER                   [required]
      --name TEXT                     [required]
      -h, --help                      Show this message and exit.
    """
    options_found = False
    res: List[str] = []
    for line in help_str.splitlines():
        if line.startswith('Options'):
            options_found = True
            continue
        if options_found:
            if line.startswith('  '):
                m = re.search(r'^  --([\w-]+)', line)
                if m is None:
                    continue
                option_name = m.group(1)
                res.append(option_name)
            else:
                options_found = False
    return res
