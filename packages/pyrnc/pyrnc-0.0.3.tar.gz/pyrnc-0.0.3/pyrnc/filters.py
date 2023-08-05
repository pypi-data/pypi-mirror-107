from pyrnc.parser import Match
from typing import Callable, Dict, Iterable, List, NamedTuple, NewType
import re

Language = NewType("Language", str)
Desc = NewType("Desc", str)


class Filter(NamedTuple):
    name: str
    description: Dict[Language, Desc]
    function: Callable[..., Callable[[List[Match]], List[Match]]]


def y_quota_sampling(year_ranges: List[Iterable[int]]) -> Callable[[List[Match]], List[Match]]:
    def srt(j_old: List[Match]) -> List[Match]:
        j_new = []
        rng_list = [list() for _ in year_ranges]
        for x, rng in enumerate(year_ranges):
            for match in j_old:
                yrm = re.search(r'(\d{4})(?!.*\d{4}).*?$', match.title)
                year = int(yrm.group(1)) if yrm else None
                if year and year in rng:
                    rng_list[x].append(match)
        quota = min([len(l) for l in rng_list])
        for lst in rng_list:
            j_new.extend(lst[:quota])
        return j_new
    return srt


YearQuotaSampling = Filter(
    name = "Quota Sampling by Year Ranges",
    description = {
        "en": "arranges equal groups of matches (as many as possible) in the "
              "order corresponding to the order of the argument ranges"
    },
    function = y_quota_sampling
)
