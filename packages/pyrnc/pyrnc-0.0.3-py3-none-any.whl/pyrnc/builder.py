from random import randrange
from typing import Iterable, NamedTuple, NewType, Union, Optional


class Lexeme(NamedTuple):
    word: Optional[str] = None
    gram: Optional[str] = None
    flags: Optional[str] = None
    sem: Optional[str] = None
    dist1: Optional[int] = None
    dist2: Optional[int] = None


class SeedParams(NamedTuple):
    sort: str
    out: str


class QueryBuilder:
    def __init__(self):
        self.start: str = "https://processing.ruscorpora.ru/search.xml?"
        self.default_parameters: str = "env=alpha&api=1.0"
        self.subcorpus_parameters: Union[str, None] = None
        self.current_lexeme: int = 1
        self.number_lexemes: int = 0
        self.final_url: str = ""
        self.lexemes_part: Union[str, None] = None
        self.current_page: int = 0
        self.stop_on_page: Union[int, None] = None
        self.seed: Optional[SeedParams] = None

    def build_subcorpus_start(self) -> str:
        if self.subcorpus_parameters is None:
            raise ValueError
        return self.start + self.default_parameters + self.subcorpus_parameters

    def build_end(self) -> str:
        return f"&p={self.current_page}"

    def next_page(self) -> None:
        if self.stop_on_page is not None and self.current_page == self.stop_on_page:
            raise StopIteration
        self.current_page += 1

    def build_lexeme_start(self, lexeme: Lexeme) -> str:
        return ""

    def build_lexeme_params(self, lexeme: Lexeme) -> str:
        return ""

    def add_lexeme(self, lexeme: Lexeme) -> None:
        if self.lexemes_part is None:
            self.lexemes_part = ""
        self.lexemes_part += self.build_lexeme_start(lexeme) + self.build_lexeme_params(lexeme)

    def lexemes_linear_adding(self, lexemes: Iterable[Lexeme]) -> None:
        for lexm in lexemes:
            self.add_lexeme(lexm)

    def add_seed(self, params: SeedParams, seed_id: Optional[int]=None):
        if seed_id is None:
            seed_id = randrange(1, 32767)
        self.seed = params
        seed_url = f"&sort={params.sort}&out={params.out}&seed={seed_id}&dpp=50&spd=50"
        self.default_parameters += seed_url
        return seed_id

    def build_query(self) -> str:
        if self.lexemes_part is None:
            raise ValueError
        self.final_url = self.build_subcorpus_start() + self.lexemes_part + self.build_end()
        return self.final_url


class MainCorpusLexGram(QueryBuilder):
    def __init__(self):
        super().__init__()
        self.subcorpus_parameters = "&mode=main&lang=ru&nodia=1&text=lexgramm"

    def build_lexeme_start(self, lexeme: Lexeme) -> str:
        n = self.number_lexemes + 1
        return f"&parent{n}=0&level{n}=0"

    def build_lexeme_params(self, lexeme: Lexeme) -> str:
        n = self.number_lexemes + 1
        lex_n = lexeme.word if lexeme.word else ""
        gramm_n = lexeme.gram if lexeme.gram else ""
        sem_n = lexeme.sem if lexeme.sem else ""
        flags_n = lexeme.flags if lexeme.flags else ""
        sem_mod_n = "sem"
        if lexeme.dist1 is None or lexeme.dist2 is None:
            raise ValueError
        return f"&lex{n}={lex_n}&gramm{n}={gramm_n}" +\
               f"&sem{n}={sem_n}&flags{n}={flags_n}&sem-mod{n}={sem_mod_n}" +\
               f"&min{n+1}={lexeme.dist1}&max{n+1}={lexeme.dist2}"

    def add_lexeme(self, lexeme: Lexeme) -> None:
        super().add_lexeme(lexeme)
        self.number_lexemes += 1


def safe_select_builder(name: str) -> QueryBuilder:
    if name == "MainCorpusLexGram":
        return MainCorpusLexGram
    else:
        raise ValueError
