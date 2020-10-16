import glob
import pynvim
import xml.etree.ElementTree as xml


@pynvim.plugin
class CoveragePlugin:
    def __init__(self, nvim: pynvim.Nvim):
        self.nvim = nvim
        self.color: dict = None
        self.covered = None

    @property
    def highlight_group(self):
        return self.color.get("highlight", "CoveredLine")

    @property
    def ctermbg(self):
        return self.color.get("ctermbg", None)

    @property
    def guibg(self):
        return self.color.get("guibg", None)

    def create_highlight(self):
        colors = []

        if self.ctermbg:
            colors.append(f"ctermbg={self.ctermbg}")

        if self.guibg:
            colors.append(f"guibg={self.guibg}")

        if not colors:
            return

        cmd = " ".join([f"highlight {self.highlight_group}"] + colors)
        self.nvim.command(cmd)

    @pynvim.command("CoverageDisplay")
    def display(self):
        coverage_patterns = self.nvim.vars.get("coverage_paths", "cov.xml")
        if not isinstance(coverage_patterns, list):
            coverage_patterns = [coverage_patterns]

        self.color = self.nvim.vars.get("coverage_color", {})
        self.create_highlight()

        current_file = self.nvim.funcs.expand("%")

        if not current_file:
            self.nvim.out_write("No file loaded!\n")
            return

        coverage_displayed = False

        for coverage_paths in coverage_patterns:
            for coverage_path in glob.iglob(coverage_paths):
                if self.try_display(current_file, coverage_path):
                    coverage_displayed = True
                    break

        if not coverage_displayed:
            self.nvim.out_write(
                f"Failed to find coverage for {current_file} in {coverage_paths}\n"
            )

    def try_display(self, filepath, coverage_path):
        cov = xml.parse(coverage_path)

        for f in cov.getroot().findall("*/file"):
            if f.attrib["name"].endswith(filepath):
                self.do_display(filepath, f)
                return True

        return False

    def do_display(self, filepath, file_element: xml.Element):
        covered = []

        for line in file_element.findall("line"):
            if not int(line.attrib["count"]):
                continue

            covered.append(int(line.attrib["num"]))

        self.covered = self.nvim.funcs.matchaddpos(self.highlight_group, covered)

    @pynvim.command("CoverageHide")
    def hide(self):
        if not self.covered:
            return

        self.nvim.out_write(f"{self.covered}\n")
        self.nvim.funcs.matchdelete(self.covered)
        self.covered = None
