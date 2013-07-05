from os.path import exists
from unittest import TestCase
from should_dsl import should, should_not
from unit.spec_generator import SpecGenerator


class SpecGenerator_Spec(TestCase):

    def setUp(self):
        self.spec_generator = SpecGenerator('../../../YakinduParser/parser/spec/resources/refrigerator.odt')

    def test_there_are_at_least_two_states(self):
        states_list = []
        states_list = self.spec_generator._get_states_content()
        states_list |should_not| be_empty
        states_list |should| be_greater_than_or_equal_to(2)
        states_list |should| equal_to(['refrigeratordoorclosed', 'refrigeratordooropened'])

    def test_there_is_a_initial_state(self):
        initial_state_list = []
        initial_state_list = self.spec_generator._clean_initial_state()
        initial_state_list |should_not| be_empty
        initial_state_list |should| equal_to(set(['refrigeratordoorclosed']))

    def test_sequence_transitions(self):
        sequence_transitions_list = []
        sequence_transitions_list = self.spec_generator._join_sequence_transitions()
        sequence_transitions_list |should_not| be_empty
        sequence_transitions_list |should| be_greater_than_or_equal_to(2)
        sequence_transitions_list |should| equal_to([['refrigeratordoorclosed', 'opendoor', 'refrigeratordooropened'],
                                                     ['refrigeratordooropened', 'closedoor', 'refrigeratordoorclosed']])

    def test_states_test_interface(self):
        self.spec_generator.create_states_test_interface() |should| equal_to("\n\n    def test_there_are_at_least_two_states(self):\n"+\
        "        states_list = []\n"+\
        "        states_list = self.spec_generator._get_states_content()\n"+\
        "        states_list |should_not| be_empty\n"+\
        "        states_list |should| be_greater_than_or_equal_to(2)\n"+\
        "        states_list |should| equal_to(['refrigeratordoorclosed', 'refrigeratordooropened'])")

    def test_initial_state_test_interface(self):
        self.spec_generator.create_initial_state_test_interface() |should| equal_to("\n\n    def test_there_is_a_initial_state(self):\n"+\
        "        initial_state_list = []\n"+\
        "        initial_state_list = self.spec_generator._clean_initial_state()\n"+\
        "        initial_state_list |should_not| be_empty\n"+\
        "        initial_state_list |should| equal_to(set(['refrigeratordoorclosed']))")

    def test_sequence_transitions_test_interface(self):
        self.spec_generator.create_sequence_transitions_test_interface() |should| equal_to("\n\n    def test_sequence_transitions(self):\n"+\
        "        sequence_transitions_list = []\n"+\
        "        sequence_transitions_list = self.spec_generator._join_sequence_transitions()\n"+\
        "        sequence_transitions_list |should_not| be_empty\n"+\
        "        sequence_transitions_list |should| be_greater_than_or_equal_to(2)\n"+\
        "        sequence_transitions_list |should| equal_to([['refrigeratordoorclosed', 'opendoor', 'refrigeratordooropened'], "+\
                                                     "['refrigeratordooropened', 'closedoor', 'refrigeratordoorclosed']])")

    def test_if_file_was_created(self):
        self.spec_generator.create_test_file()
        exists("../../../YakinduParser/generator/unit/factory_utils_spec.py") |should| equal_to(True)