from pyrnc.builder import SeedParams
from typing import Callable, List, Optional, NamedTuple
import lxml.etree
import lxml.html
import re


class Item(NamedTuple):
    content: str
    selected: bool


class Match(NamedTuple):
    title: str
    text: List[Item]
    marked: Optional[bool]


class ParsedPage:
    def __init__(self, raw_data, seed: SeedParams):
        self.number_documents: Optional[int] = None  # add_stats
        self.number_matches: Optional[int] = None  # add_stats
        self.page_matches: Optional[List[Match]] = None
        self.seed: SeedParams = seed
        self.navigation_index: Optional[int] = None
        self.is_last_page: Optional[bool] = None  # last_page_checker
        self.raw_data = raw_data
        self.model = lxml.html.fromstring(self.raw_data)
        self.parse_data()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["model"]
        del state["raw_data"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def parse_data(self):
        self.last_page_checker()
        self.add_stats()
        try:
            self.parse_navigation()
        except IndexError:
            self.navigation_index = 0
        if self.seed.out == "kwic" and self.navigation_index:
            self.page_matches = [m for m in self.kwic_get_matches()]

    def last_page_checker(self):
        next_buttons = self.model.xpath("//*[text()='следующая страница']")
        self.is_last_page = not next_buttons

    def add_stats(self):
        stat_blocks = self.model.xpath("//*[@class='stat-number']/..")
        local_search = 1
        if len(stat_blocks) < 2:
            self.number_documents = 0
            self.number_matches = 0
        d, m = stat_blocks[local_search].xpath("./*[@class='stat-number']")
        self.number_documents = int(d.text.replace(" ", ""))
        self.number_matches = int(m.text.replace(" ", ""))

    def parse_navigation(self):
        self.navigation_index = int(self.model.xpath("//*[@class='pager']/b")[0].text)

    def kwic_get_matches(self):
        table = self.model.xpath("//*[contains(@class, 'g-em')]/ancestor::table")[0]
        td = table.xpath("tbody/tr/td")
        title = None
        items = []
        classif = re.compile('''
        (<\/span>|^) (?P<string>[^<>]+?) (?=<span|$)
        |
        <span [ ]+ class=" (?P<token_class>.+?)"[ ]*> (?P<token_body>.+?) (?=<\/span>)
        ''', re.X)

        def f(s): return re.sub(r'[\n\s\t]{2,}', ' ', s)

        for i in range(0, len(td)):
            content = lxml.etree.tostring(td[i].xpath(".//nobr")[0], encoding="unicode")
            content = re.sub(r'explain=".+?"', '', content)
            content = re.sub(r'</?nobr>', '', content)
            if i % 3 == 2:
                title = re.search(r'msg="(.+?)"', content).group(1)
                remove_expander = re.compile(r'\n.*?<!--\s*expand_context.+',
                                             flags=re.MULTILINE|re.DOTALL)
                content = re.sub(remove_expander, '', content)
            content = re.sub(r'<!--.+?-->', '', content)
            for item in re.finditer(classif, content):
                if item.group("string"):
                    items.append(Item(f(item.group("string")), False))
                elif item.group("token_class"):
                    sel = "g-em" in item.group("token_class")
                    items.append(Item(f(item.group("token_body")), sel))
            if i % 3 == 2:
                yield Match(title, items, marked=False)
                title = None
                items = []


class JointPages:
    def __init__(self, load_id: str, num_documents: int, num_matches: int):
        self.load_id = load_id
        self.number_documents: int = num_documents
        self.number_matches: int = num_matches
        self.joint_matches: List[Match] = []

    def add_list(self, jmatches: List[Match]):
        self.joint_matches += jmatches

    def filter(self, flt: Callable[[List[Match]], List[Match]]):
        self.joint_matches = flt(self.joint_matches)
