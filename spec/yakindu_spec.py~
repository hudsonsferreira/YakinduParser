from os.path import basename, dirname, exists
from os import system
from unittest import TestCase
from should_dsl import should, should_not
from yakindu_parser import YakinduParser


class Yakindu_Spec(TestCase):

    def setUp(self):
        self.parser = YakinduParser('spec/resources/geladeira.odt')
    
    def test_if_file_exists(self):
        (YakinduParser, 'spec/resources/geladeira.odt') |should_not| throw(NameError)

    def test_if_file_not_exists(self):
        (YakinduParser, 'spec/resources/not_exist') |should| throw(NameError)
    
    def test_if_file_is_valid(self):
        (YakinduParser, 'spec/resources/trabalho-fsi.pdf') |should| throw(NameError)
    
    def test_if_file_was_unziped(self):
        self.parser._unzip_odt()
        exists(self.parser._content_directory + '/content.xml') |should| equal_to(True)

    def test_if_content_was_extracted(self):
        self.parser._clean_content() |should| equal_to('initially the initial_state refrigerator door is closed end , consequently the  specification  light is off end  and the specification  thermostat power is minimum end  . when one  transition  opens the door end  , the  state  door is opened end  , the  specification  light turns on end  and the specification  thermostat power changes to maximum. when one  transition  closes the door end  , the  state  refrigerator door is closed end  .')
    
    def test_if_content_was_tokenized(self):
        self.parser._tokenize_content() |should| equal_to([['initially', 'initial_state', 'refrigerator', 'door', 'closed', 'end', 'specification', 'light', 'off', 'end', 'specification', 'thermostat', 'power', 'minimum', 'end'], ['transition', 'opens', 'door', 'end', 'state', 'door', 'opened', 'end', 'specification', 'light', 'turns', 'on', 'end', 'specification', 'thermostat', 'power', 'maximum'], ['transition', 'closes', 'door', 'end', 'state', 'refrigerator', 'door', 'closed', 'end']])
    
    def test_if_tags_was_ordered_by_sent(self):
        self.parser._order_tags_by_sent() |should| equal_to ([['initial_state', 'end', 'specification'], ['transition', 'end', 'state', 'specification'], ['transition', 'end', 'state']])
    
    def test_if_tmp_file_was_removed(self):
        exists(self.parser._content_directory + '/content.xml') |should_not| equal_to(True)

if __name__ == '__main__':
    unittest.main()

