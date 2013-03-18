import sys

sys.path.append("/home/hudson/projetos/yakinduparser/parser")

from yakindu_parser import YakinduParser

class SpecGenerator(YakinduParser):

    def __init__(self, path):
       YakinduParser.__init__(self, path)

    def take_states(self):
        states_list = []
        states_list = self._get_states_content()