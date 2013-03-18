import sys
sys.path.append("/home/hudson/projetos/yakinduparser/generator")


from unittest import TestCase
from should_dsl import should, should_not
from spec_generator import SpecGenerator


class SpecGenerator_Spec(TestCase):

    def setUp(self):
        self.spec_generator = SpecGenerator('/home/hudson/projetos/yakinduparser/parser/spec/resources/refrigerator.odt')

    def test_if_there_are_at_least_two_states(self):
        states_list = []
        states_list = self.spec_generator._get_states_content()
        states_list |should_not| be_empty
        states_list |should| be_greater_than_or_equal_to(2)

    def test_if_there_are_a_initial_state(self):
        initial_state_list = []
        initial_state_list = self.spec_generator._get_initial_state()
        initial_state_list |should_not| be_empty
        initial_state_list |should| be_greater_than_or_equal_to(1)