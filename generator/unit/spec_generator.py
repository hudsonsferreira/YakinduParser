import os
from parser.yakindu_parser import YakinduParser

class SpecGenerator(YakinduParser):

    def __init__(self, path):
        YakinduParser.__init__(self, path)
        self.root_path = os.getcwd()
        self._indentation = 4 * ' '

    def create_states_test_interface(self):
        pharse = "\n\n{one}def test_there_are_at_least_two_states(self):\n"+\
        "{two}states_list = []\n"+\
        "{two}states_list = self.spec_generator._get_states_content()\n"+\
        "{two}states_list |should_not| be_empty\n"+\
        "{two}states_list |should| be_greater_than_or_equal_to(%d)\n"+\
        "{two}states_list |should| equal_to(%s)"
        
        states_list = []
        states_list = self._get_states_content()
        length = len(states_list)
        final_pharse = pharse.format(one=self._indentation, two=2*self._indentation) %(length, states_list)
        return final_pharse

    def create_initial_state_test_interface(self):
        pharse = "\n\n{one}def test_there_is_a_initial_state(self):\n"+\
        "{two}initial_state_list = []\n"+\
        "{two}initial_state_list = self.spec_generator._clean_initial_state()\n"+\
        "{two}initial_state_list |should_not| be_empty\n"+\
        "{two}initial_state_list |should| equal_to(%s)"

        initial_state_list = []
        initial_state_list = self._clean_initial_state()
        final_pharse = pharse.format(one=self._indentation, two=2*self._indentation) %(initial_state_list)
        return final_pharse

    def create_sequence_transitions_test_interface(self):
        pharse = "\n\n{one}def test_sequence_transitions(self):\n"+\
        "{two}sequence_transitions_list = []\n"+\
        "{two}sequence_transitions_list = self.spec_generator._join_sequence_transitions()\n"+\
        "{two}sequence_transitions_list |should_not| be_empty\n"+\
        "{two}sequence_transitions_list |should| be_greater_than_or_equal_to(%d)\n"+\
        "{two}sequence_transitions_list |should| equal_to(%s)"

        sequence_transitions_list = []
        sequence_transitions_list = self._join_sequence_transitions()
        length = len(sequence_transitions_list)
        final_pharse = pharse.format(one=self._indentation, two=2*self._indentation) %(length, sequence_transitions_list)
        return final_pharse

    def create_test_file(self):
        test_file_content = []
        first_constant = open(self.root_path + '/first_constant.txt', 'r')
        test_file_content.append(first_constant.read())

        test_file_content.append(self.create_states_test_interface())
        test_file_content.append(self.create_initial_state_test_interface())
        test_file_content.append(self.create_sequence_transitions_test_interface())
        
        second_constant = open(self.root_path + '/second_constant.txt', 'r')
        test_file_content.append(second_constant.read())

        test_file = open(self.root_path + '/factory_utils_spec.py', 'w')
        for content in test_file_content:
            test_file.write(str(content))
        test_file.close()