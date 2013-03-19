from package org.yakindu.sct.ui.editor.factories import FactoryUtils.java
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
        initial_state_list = self.spec_generator._clean_initial_state()
        initial_state_list |should_not| be_empty
        initial_state_list |should| equal_to(set(['refrigeratordoorclosed']))

    def test_sequence_transitions(self):
        sequence_transitions_list = []
        sequence_transitions_list = self.spec_generator._join_sequence_transitions()
        sequence_transitions_list |should_not| be_empty
        sequence_transitions_list |should| be_greater_than_or_equal_to(2)
        sequence_transitions_list |should| equal_to([['refrigeratordoorclosed', 'opendoor', 'refrigeratordooropened'], ['refrigeratordooropened', 'closedoor', 'refrigeratordoorclosed']])


if __name__ == "__main__":
    unittest.main()