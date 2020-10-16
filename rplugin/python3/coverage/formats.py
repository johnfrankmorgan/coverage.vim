import json
import xml.etree.ElementTree as xml
from abc import ABC, abstractmethod
from typing import Union, List


class Format(ABC):
    def __init__(self, filepath: str, coverage: str):
        self.filepath = filepath
        self.coverage = coverage
        self.init()

    def init(self):
        pass

    @abstractmethod
    def lines(self) -> Union[List[int], None]:
        return None

    @classmethod
    def from_file(cls, filepath: str, coverage_path: str) -> "Format":
        with open(coverage_path) as f:
            return cls(filepath, f.read())


class CoveragePyJson(Format):
    def init(self):
        self.json: dict = json.loads(self.coverage)

    def lines(self) -> Union[List[int], None]:
        """
        >>> c = CoveragePyJson("t/t", '{"files": {"t": {"executed_lines": [1, 2, 3]}}}')
        >>> c.lines()
        [1, 2, 3]
        """
        for localpath, details in self.json["files"].items():
            if not self.filepath.endswith(localpath):
                continue

            return details["executed_lines"]

        return None


class CoverageCloverXml(Format):
    def init(self):
        self.xml = xml.fromstring(self.coverage)

    def lines(self) -> Union[List[int], None]:
        """
        >>> c = CoverageCloverXml("t", '<root><p><file name="t"><line num="1" count="1" /></file></p></root>')
        >>> c.lines()
        [1]
        """
        for f in self.xml.findall("*/file"):
            if not f.attrib["name"].endswith(self.filepath):
                continue

            lines = []

            for line in f.findall("line"):
                if int(line.attrib["count"]):
                    lines.append(int(line.attrib["num"]))

            return lines

        return None
