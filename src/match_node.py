import re
from enum import Enum


class MatchType(Enum):
    CODE="code"
    BULLET="bullet_list"
    BULLET_END="bullet_list_end"
    NUM_LIST="num_list"
    NUM_LIST_END="num_list_end"

class MatchNode():
    def __init__(self, match: "Match", match_type: MatchType) -> None:
        self.start = match.start()
        self.result = match.group(0)
        self.raw_result = match.group(0)
        self.match_type: MatchType = match_type

    def __eq__(self, other: "MatchNode") -> bool:
        return self.start == other.start

    def __lt__(self, other: "MatchNode") -> bool:
        return self.start < other.start

class MatchList():
    def __init__(self) -> None:
        self.match_list: "MatchNode" = []

    def __iter__(self) -> "MatchNode":
        for m in self.match_list:
            yield m

    def __bool__(self) -> bool:
        if self.match_list:
            return True
        return False

    def extend(self, match_list: list["Match"], match_type: MatchType) -> None:
        extension: list["MatchNode"] = []
        for match in match_list:
            match_node = MatchNode(match, match_type)
            if match_type == MatchType.CODE:
                code_lang = re.search(r'(?<=```).*', match_node.result)[0]
                match_node.result = match_node.result.replace(code_lang, "", 1)
            elif match_type in [MatchType.BULLET_END, MatchType.NUM_LIST_END]:
                match_node.result = match_node.result.replace("\n", "\n\n")
            self.match_list.append(match_node)
    
    def sort(self) -> None:
        self.quick_sort(0, len(self.match_list) - 1)

    def partition(self, low: int, high: int) -> int:
        j = low - 1
        for i in range(low, high):
            if self.match_list[i] < self.match_list[high]:
                j += 1
                self.match_list[i], self.match_list[j] = self.match_list[j], self.match_list[i]
        j += 1
        self.match_list[high], self.match_list[j] = self.match_list[j], self.match_list[high]       
        return j

    def quick_sort(self, low: int, high: int) -> None:
        if low >= high:
            return
        pivot = self.partition(low, high)
        self.quick_sort(low, pivot - 1)
        self.quick_sort(pivot + 1, high)