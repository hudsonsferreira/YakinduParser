import sys
sys.path.append("/home/hudson/projetos/yakinduparser/parser")

from yakindu_parser import YakinduParser

class SpecGenerator(YakinduParser):

    def __init__(self, path):
       YakinduParser.__init__(self, path)

    def create_states_test_interface(self):
        pharse = "states_list = []\n"+\
        "states_list = self.spec_generator._get_states_content()\n"+\
        "states_list |should_not| be_empty\n"+\
        "states_list |should| be_greater_than_or_equal_to(%d)\n"+\
        "states_list |should| equal_to(%s)"
        
        states_list = []
        states_list = self._get_states_content()
        length = len(states_list)
        final_pharse = pharse %(length, states_list)
        return final_pharse

    def create_initial_state_test_interface(self):
        pharse = "initial_state_list = []\n"+\
        "initial_state_list = self.spec_generator._clean_initial_state()\n"+\
        "initial_state_list |should_not| be_empty\n"+\
        "initial_state_list |should| equal_to(%s)"

        initial_state_list = []
        initial_state_list = self._clean_initial_state()
        final_pharse = pharse %(initial_state_list)
        return final_pharse