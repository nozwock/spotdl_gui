import regex


class Splitter:
    def __init__(self, delim: str = ",", escape: str = "\\"):
        self.delim = regex.escape(delim)
        self.escape = regex.escape(escape)
        self._split_pat = regex.compile(
            f"(?<!{self.escape})(?:{self.escape*2})*\K{self.delim}"
        )
        self._escape_pat = regex.compile(f"({self.escape*2})|({self.escape})")

    def split(self, txt: str, *args, **kwargs) -> list[str]:
        ret = self._split_pat.split(txt, *args, **kwargs)
        self._resolve_escape(ret)
        return ret

    def _resolve_escape(self, seq: list[str]) -> None:
        for i, s in enumerate(seq):
            e: regex.Match
            for e in self._escape_pat.finditer(s):
                s = s[: e.start()] + s[e.end() :]

            seq[i] = s


if __name__ == "__main__":
    splitter = Splitter()
    assert splitter.split("So\, does escaping work?, Another item, and another") == [
        "So, does escaping work?",
        " Another item",
        " and another",
    ]
