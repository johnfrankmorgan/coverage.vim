import glob
import pynvim
import xml.etree.ElementTree as xml

@pynvim.plugin
class CoveragePlugin:
    def __init__(self, nvim: pynvim.Nvim):
        self.nvim = nvim

    @pynvim.command('CoverageDisplay')
    def display(self):
        coverage_patterns = self.nvim.vars.get('coverage_paths', 'cov.xml')
        if not isinstance(coverage_patterns, list):
            coverage_patterns = [coverage_patterns]

        current_file = self.nvim.funcs.expand('%')

        if not current_file:
            self.nvim.out_write('No file loaded!\n')
            return

        coverage_displayed = False

        for coverage_paths in coverage_patterns:
            for coverage_path in glob.iglob(coverage_paths):
                if self.try_display(current_file, coverage_path):
                    coverage_displayed = True
                    break

        if not coverage_displayed:
            self.nvim.out_write(f'Failed to find coverage for {current_file} in {coverage_paths}\n')

    def try_display(self, filepath, coverage_path):
        cov = xml.parse(coverage_path)

        for f in cov.getroot().findall('*/file'):
            if f.attrib['name'].endswith(filepath):
                self.do_display(filepath, f)
                return True

        return False

    def do_display(self, filepath, file_element: xml.Element):
        for line in file_element.findall('line'):
            if not int(line.attrib['count']):
                continue

            line_num = int(line.attrib['num'])
            self.nvim.current.buffer.add_highlight('CoveredLine', line_num - 1)

