import re
from typing import Dict, List


def get_values(output_str: str) -> Dict[str, str]:
    """
    Get the dictionary representing actual value passed to the function
    """
    res_d = {}
    for line in output_str.splitlines():
        m = re.match(r'(\w+)=(.+)', line.strip())
        assert m is not None
        res_d[m.group(1)] = m.group(2)
    return res_d


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
