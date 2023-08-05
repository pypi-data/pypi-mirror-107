from typing import Any, Sequence

from click import style


def list2str(seq: Sequence[Any]) -> str:
    # Source: https://stackoverflow.com/a/53981846

    # seq = [str(s) for s in seq]
    seq = [style(str(s), underline=True) for s in seq]

    if len(seq) < 3:
        return " and ".join(seq)

    return ", ".join(seq[:-1]) + ", and " + seq[-1]
