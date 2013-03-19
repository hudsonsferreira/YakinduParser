import sys
sys.path.append("/home/hudson/projetos/yakinduparser/parser")

from yakindu_parser import YakinduParser

class SpecGenerator(YakinduParser):

    def __init__(self, path):
       YakinduParser.__init__(self, path)
       self._indentation = 4 * ' '

    def create_states_test_interface(self):
        pharse = "states_list = []\n"+\
        "states_list = self.spec_generator._get_states_content()\n"+\
        "states_list |should_not| be_empty\n"+\
        "states_list |should| be_greater_than_or_equal_to(%d)\n"+\
        "states_list |should| equal_to(['%s', '%s'])"
        
        states_list = []
        states_list = self._get_states_content()
        length = len(states_list)
        final_pharse = pharse %(length, states_list[length-2], states_list[length-1])
        return final_pharse