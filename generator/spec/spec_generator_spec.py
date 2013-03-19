import sys
sys.path.append("/home/hudson/projetos/yakinduparser/generator")


from unittest import TestCase
from should_dsl import should, should_not
from spec_generator import SpecGenerator


class SpecGenerator_Spec(TestCase):

    def setUp(self):
        self.spec_generator = SpecGenerator('/home/hudson/projetos/yakinduparser/parser/spec/resources/refrigerator.odt')

    def test_there_are_at_least_two_states(self):
        states_list = []
        states_list = self.spec_generator._get_states_content()
        states_list |should_not| be_empty
        states_list |should| be_greater_than_or_equal_to(2)
        states_list |should| equal_to(['refrigeratordoorclosed', 'refrigeratordooropened'])

    def test_there_is_a_initial_state(self):
        initial_state_list = []
        initial_state_list = self.spec_generator._get_initial_state()
        initial_state_list |should_not| be_empty
        initial_state_list |should| be_greater_than_or_equal_to(1)
        initial_state_list |should| equal_to([['refrigerator', 'door', 'closed'],
                                              ['refrigerator', 'door', 'closed']])

    def test_sequence_transitions(self):
        sequence_transitions_list = []
        sequence_transitions_list = self.spec_generator._join_sequence_transitions()
        sequence_transitions_list |should_not| be_empty
        sequence_transitions_list |should| be_greater_than_or_equal_to(1)
        sequence_transitions_list |should| equal_to([['refrigeratordoorclosed', 'opendoor', 'refrigeratordooropened'],
                                                     ['refrigeratordooropened', 'closedoor', 'refrigeratordoorclosed']])

    def test_states_test_interface(self):
        self.spec_generator.create_states_test_interface() |should| equal_to("states_list = []\n"+\
        "states_list = self.spec_generator._get_states_content()\n"+\
        "states_list |should_not| be_empty\n"+\
        "states_list |should| be_greater_than_or_equal_to(2)\n"+\
        "states_list |should| equal_to(['refrigeratordoorclosed', 'refrigeratordooropened'])")