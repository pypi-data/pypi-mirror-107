# -*- coding: utf-8 -*-

"""String utilities."""

import re
import string as string_lib

from typing import Any, Optional

PRINTABLE_SET = frozenset(string_lib.printable)
NON_PRINTABLE_SET = frozenset(chr(i) for i in range(128)) - PRINTABLE_SET
NON_PRINTABLE_TANSLATE = {ord(character): None for character in NON_PRINTABLE_SET}
REGEX_WORD = re.compile(r"^\w+")


def to_str(string: Any, encoding: str = "utf-8") -> Optional[str]:
    """Safely returns either string or None."""

    string = (
        string
        if isinstance(string, str)
        else string.decode(encoding)
        if isinstance(string, bytes)
        else None
    )

    return string.translate(NON_PRINTABLE_TANSLATE) if string is not None else None


def normalize_space(item: Any, preserve_newline: bool = False) -> str:
    """Normalize space in a string."""

    item = to_str(item)

    if not item:
        return ""

    if preserve_newline:
        try:
            return "\n".join(
                normalize_space(line) for line in item.splitlines()
            ).strip()
        except Exception:
            return ""

    try:
        return " ".join(item.split())
    except Exception:
        return ""


def truncate(
    string: str,
    length: int,
    ellipsis: str = "[…]",
    respect_word: bool = False,
) -> str:
    """Truncates a string at given length."""

    if length < 0 or len(string) <= length + len(ellipsis):
        return string

    string_trunc = string[:length]

    if respect_word:
        match = REGEX_WORD.match(string[length:])
        if match:
            string_trunc += match.group(0)

    if string_trunc.rstrip().endswith(ellipsis):
        return string_trunc.rstrip()

    if not respect_word or not string_trunc or string_trunc[-1].isspace():
        return string_trunc + ellipsis

    return f"{string_trunc} {ellipsis}"
