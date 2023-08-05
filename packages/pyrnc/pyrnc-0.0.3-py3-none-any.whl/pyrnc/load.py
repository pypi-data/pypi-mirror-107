from pyrnc.builder import QueryBuilder
from pyrnc.parser import JointPages, Match, ParsedPage
from pathlib import Path
from typing import Callable, Dict, Iterator, List, Optional
import concurrent.futures
import os
import pickle
import requests
import time

default_path = os.path.join(str(Path.home()), "rnc_files")
error_handling_range = range(3)
max_for: Dict[str, Optional[int]] = {}
missed_of: Dict[str, List[int]] = {}


def error_handling_timeout(tm):
    return 1000 * (tm + 1)**3


def create_folder():
    Path(default_path).mkdir(parents=True, exist_ok=True)


def load_page_to_pickle(load_id: str, builder: QueryBuilder,
                        page: int, verbose: bool = False) -> None:
    create_folder()

    builder.current_page = page
    url = builder.build_query()

    status_code = None
    for tme in error_handling_range:
        if load_id in max_for and page >= max_for[load_id]:
            return
        r = requests.get(url)
        status_code = r.status_code
        if verbose:
            print(status_code)
        if status_code == 200:
            break
        else:
            sleeping = error_handling_timeout(tme)
            if verbose:
                print(f"Invalid response occured, attempts left:\
                {len(error_handling_range)-tme}, sleeping for {sleeping}ms")
            time.sleep(sleeping / 1000)
    if r.status_code != 200:
        raise ConnectionError("Status is not 200, not OK!")

    try:
        pp = ParsedPage(r.text, builder.seed)
    except IndexError:
        if load_id not in max_for or max_for[load_id] != -1:
            max_for[load_id] = -1
            print("No results found for the query!!")
        return

    if pp.navigation_index != page + 1:
        if verbose:
            print("Page limit exceeded!")
        max_for[load_id] = page

    file_name = f"{load_id}.{page}.p"
    if not os.path.exists(os.path.join(default_path, file_name)):
        with open(os.path.join(default_path, file_name), "wb") as pdump:
            pickle.dump(pp, pdump)
            pdump.close()
        if verbose:
            print(f"Pickle saved: {file_name}")
    elif verbose:
        print(f"Problem occured with {file_name}")

    if load_id in missed_of:
        missed_of[load_id].remove(page)

    return True


def run_loader(load_id: str, builder: QueryBuilder,
               page: int, verbose: bool):
    return load_page_to_pickle(load_id, builder, page, verbose)


def load_until(page_range: Iterator[int], load_id: str,
               builder: QueryBuilder, verbose: bool = False):
    missed_of[load_id] = [x for x in page_range]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        res = [executor.submit(run_loader, load_id,
                               builder, p, verbose) for p in page_range]
    concurrent.futures.wait(res)
    missed_of[load_id] = [x for x in missed_of[load_id] if load_id not in max_for
                                                        or x <= max_for[load_id]]
    if load_id in max_for and max_for[load_id] == -1:
        print("------------------------------")
        print("NO MATCHES FOUND FOR THE QUERY")
        print("------------------------------")


def full_load_until(page_range: Iterator[int], load_id: str,
                    builder: QueryBuilder, verbose: bool = False):
    load_until(page_range, load_id, builder, verbose)
    while missed_of[load_id]:
        load_until(missed_of[load_id], load_id, builder, verbose)


def join_by_load_id(load_id: str, verbose: bool = False, rm: bool = True):
    joint_pages = None
    for i in range(10**5):
        if os.path.exists(os.path.join(default_path, f"{load_id}.{i}.p")):
            pth = os.path.join(default_path, f"{load_id}.{i}.p")
            print(pth)
            page = pickle.load(open(pth, "rb"))
            if i == 0:
                joint_pages = JointPages(load_id, page.number_documents,
                                         page.number_matches)
            if page.page_matches:
                joint_pages.add_list(page.page_matches)
            if rm:
                os.remove(pth)
    if not os.path.exists(os.path.join(default_path, f"{load_id}.joint.p")):
        pickle.dump(joint_pages, open(os.path.join(default_path, f"{load_id}.joint.p"), "wb"))
    else:
        j = 1
        while os.path.exists(os.path.join(default_path, f"{load_id}.joint ({j}).p")):
            j += 1
        pickle.dump(joint_pages, open(os.path.join(default_path, f"{load_id}.joint ({j}).p"), "wb"))


def filter_joint(jname: str, flt: Callable[[List[Match]], List[Match]], rname: str):
    joint = pickle.load(open(os.path.join(default_path, jname), "rb"))
    joint.filter(flt)
    jname = jname.rstrip(".p")
    pickle.dump(joint, open(os.path.join(default_path, f"{jname} - {rname}.p"), "wb"))
    return True
