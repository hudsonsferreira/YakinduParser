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
        self.parser._clean_content() |should| equal_to('initially the initial_state refrigerator door is closed end , consequently the  specification  light off is true end  and the  specification  light on is false end  ; the specification  thermostat power minimum is true  end  and the  specification  thermostat power maximum is false end  . when one  transition  opens the door end  , the  state  door is opened end  , the  specification  light on is true end  and the  specification  light off is false  end  ; the specification  thermostat power maximum is true end  and the  specification  thermostat power minimum is false end  . when one  transition  closes the door end  , the  state  refrigerator door is closed end  .')
    
    def test_if_content_was_tokenized(self):
        self.parser._tokenize_content() |should| equal_to([['initially', 'initial_state', 'refrigerator', 'door', 'closed', 'end', 'specification', 'light', 'off', 'true', 'end', 'specification', 'light', 'on', 'false', 'end', 'specification', 'thermostat', 'power', 'minimum', 'true', 'end', 'specification', 'thermostat', 'power', 'maximum', 'false', 'end'], ['transition', 'opens', 'door', 'end', 'state', 'door', 'opened', 'end', 'specification', 'light', 'on', 'true', 'end', 'specification', 'light', 'off', 'false', 'end', 'specification', 'thermostat', 'power', 'maximum', 'true', 'end', 'specification', 'thermostat', 'power', 'minimum', 'false', 'end'], ['transition', 'closes', 'door', 'end', 'state', 'refrigerator', 'door', 'closed', 'end']])
    
    def test_if_tags_was_ordered_by_sent(self):
        self.parser._order_tags_by_sent() |should| equal_to([['initial_state', 'end', 'specification'], ['transition', 'end', 'state', 'specification'], ['transition', 'end', 'state']])
    
    def test_if_indexes_were_acquired(self):
        self.parser._indexes_of_process_intersections() |should| equal_to([[1, 5, 10, 15, 21, 27, 6, 11, 16, 22], [0, 3, 7, 12, 17, 23, 29, 4, 8, 13, 18, 24], [0, 3, 8, 4]])
    
    def test_if_indexes_were_sorted_by_bigrams(self):
        self.parser._sort_tag_indexes_bigrams() |should| equal_to([[(1, 5), (5, 6), (6, 10), (10, 11), (11, 15), (15, 16), (16, 21), (21, 22), (22, 27), (27, None)], [(0, 3), (3, 4), (4, 7), (7, 8), (8, 12), (12, 13), (13, 17), (17, 18), (18, 23), (23, 24), (24, 29), (29, None)], [(0, 3), (3, 4), (4, 8), (8, None)]] )
    
    def test_if_tags_content_tuples_were_cut_by_sent(self):
        indexes = [(0, 0), (0, 1), (1, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 8), (8, 9), (9, 10), (10, 12), (12, 13), (13, 14), (14, None)]
        content = ['initial_state', 'refrigerator', 'door', 'closed', 'end', 'specification', 'light', 'off', 'end', 'specification', 'thermostat', 'power', 'minimum', 'end']
        second_indexes = [(0, 0), (0, 1), (1, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 8), (8, 9), (9, 10), (10, 12), (12, 13), (13, 14), (14, None)]
        second_content = ['transition', 'opens', 'door', 'end', 'state', 'door', 'opened', 'end', 'specification', 'light', 'turns', 'on', 'end', 'specification', 'thermostat', 'power', 'maximum']
        third_indexes = [(0, 0), (0, 1), (1, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 8), (8, 9), (9, 10), (10, 12), (12, 13), (13, 14), (14, None)]
        third_content = ['transition', 'closes', 'door', 'end', 'state', 'refrigerator', 'door', 'closed', 'end']
        self.parser._cut_tag_content_tuples_from_sent(indexes, content) |should| equal_to([['initial_state'], ['refrigerator', 'door'], ['closed'], ['end'], ['specification'], ['light'], ['off'], ['end'], ['specification'], ['thermostat', 'power'], ['minimum'], ['end']])
        self.parser._cut_tag_content_tuples_from_sent(second_indexes, second_content) |should| equal_to([['transition'], ['opens', 'door'], ['end'], ['state'], ['door'], ['opened'], ['end'], ['specification'], ['light'], ['turns', 'on'], ['end'], ['specification'], ['thermostat', 'power', 'maximum']])
        self.parser._cut_tag_content_tuples_from_sent(third_indexes, third_content) |should| equal_to([['transition'], ['closes', 'door'], ['end'], ['state'], ['refrigerator'], ['door'], ['closed'], ['end']])

    def test_if_content_was_tagged(self):
        sorted_indexes_tags = self.parser._sort_tag_indexes_bigrams()
        tokenized_content = self.parser._tokenize_content()
        self.parser._take_tagged_content(sorted_indexes_tags, tokenized_content)|should| equal_to([[['initial_state', 'refrigerator', 'door', 'closed'], ['end'], ['specification', 'light', 'off', 'true'], ['end'], ['specification', 'light', 'on', 'false'], ['end'], ['specification', 'thermostat', 'power', 'minimum', 'true'], ['end'], ['specification', 'thermostat', 'power', 'maximum', 'false'], ['end']], [['transition', 'opens', 'door'], ['end'], ['state', 'door', 'opened'], ['end'], ['specification', 'light', 'on', 'true'], ['end'], ['specification', 'light', 'off', 'false'], ['end'], ['specification', 'thermostat', 'power', 'maximum', 'true'], ['end'], ['specification', 'thermostat', 'power', 'minimum', 'false'], ['end']], [['transition', 'closes', 'door'], ['end'], ['state', 'refrigerator', 'door', 'closed'], ['end']]])

    def test_if_lean_content_was_created(self):
        self.parser._create_cleaned_content() |should| equal_to([[['initial_state', 'refrigerator', 'door', 'closed'], ['specification', 'light', 'off', 'true'], ['specification', 'light', 'on', 'false'], ['specification', 'thermostat', 'power', 'minimum', 'true'], ['specification', 'thermostat', 'power', 'maximum', 'false']], [['transition', 'open', 'door'], ['state', 'door', 'opened'], ['specification', 'light', 'on', 'true'], ['specification', 'light', 'off', 'false'], ['specification', 'thermostat', 'power', 'maximum', 'true'], ['specification', 'thermostat', 'power', 'minimum', 'false']], [['transition', 'close', 'door'], ['state', 'refrigerator', 'door', 'closed']]])
    
    def test_if_content_was_classified(self):
        self.parser._pos_tag_lean_content() |should| equal_to([[[('initial_state', 'NN'), ('refrigerator', 'NN'), ('door', 'NN'), ('closed', 'VBD')], [('specification', 'NN'), ('light', 'NN'), ('off', 'IN'), ('true', 'JJ')], [('specification', 'NN'), ('light', 'NN'), ('on', 'IN'), ('false', 'JJ')], [('specification', 'NN'), ('thermostat', 'NNP'), ('power', 'NN'), ('minimum', 'JJ'), ('true', 'JJ')], [('specification', 'NN'), ('thermostat', 'NNP'), ('power', 'NN'), ('maximum', 'JJ'), ('false', 'JJ')]], [[('transition', 'NN'), ('opens', 'VBZ'), ('door', 'NN')], [('state', 'NN'), ('door', 'NN'), ('opened', 'VBD')], [('specification', 'NN'), ('light', 'NN'), ('on', 'IN'), ('true', 'JJ')], [('specification', 'NN'), ('light', 'NN'), ('off', 'IN'), ('false', 'JJ')], [('specification', 'NN'), ('thermostat', 'NNP'), ('power', 'NN'), ('maximum', 'JJ'), ('true', 'JJ')], [('specification', 'NN'), ('thermostat', 'NNP'), ('power', 'NN'), ('minimum', 'JJ'), ('false', 'JJ')]], [[('transition', 'NN'), ('closes', 'VBZ'), ('door', 'NN')], [('state', 'NN'), ('refrigerator', 'NN'), ('door', 'NN'), ('closed', 'VBD')]]])
    
    def test_if_the_term_specification_was_removed_from_content(self):
        first_sent = [[('initial_state', None), ('refrigerator', 'NN')], [('door', 'NN')], [('closed', 'VBD')], [('specification', None)], [('light', 'JJ')], [('off', 'RP')], [('specification', None), ('thermostat', None)], [('power', 'NN')], [('minimum', 'JJ')]]
        second_sent = [[('transition', 'NN')], [('opens', 'VBZ'), ('door', 'NN')], [('state', 'NN')], [('door', 'NN')], [('opened', 'VBD')], [('specification', None)], [('light', 'JJ')], [('turns', 'VBZ'), ('on', 'IN')], [('specification', None)], [('thermostat', None), ('power', 'NN'), ('maximum', 'NN')]]
        third_sent = [[('transition', 'NN')], [('closes', None), ('door', 'NN')], [('state', 'NN')], [('refrigerator', 'NN')], [('door', 'NN')], [('closed', 'VBD')]]
        self.parser._clean_pos_tagged_content(first_sent) |should| equal_to([['initial_state', 'refrigerator'], ['door'], ['closed'], ['specification'], ['light'], ['off'], ['specification', 'thermostat'], ['power'], ['minimum']])
        self.parser._clean_pos_tagged_content(second_sent) |should| equal_to([['transition'], ['opens', 'door'], ['state'], ['door'], ['opened'], ['specification'], ['light'], ['turns', 'on'], ['specification'], ['thermostat', 'power', 'maximum']])
        self.parser._clean_pos_tagged_content(third_sent) |should| equal_to([['transition'], ['closes', 'door'], ['state'], ['refrigerator'], ['door'], ['closed']])

    def test_if_content_cleaned(self):
        self.parser._create_cleaned_content() |should| equal_to([[['initial_state', 'refrigerator', 'door', 'closed'], ['specification', 'light', 'off', 'true'], ['specification', 'light', 'on', 'false'], ['specification', 'thermostat', 'power', 'minimum', 'true'], ['specification', 'thermostat', 'power', 'maximum', 'false']], [['transition', 'open', 'door'], ['state', 'door', 'opened'], ['specification', 'light', 'on', 'true'], ['specification', 'light', 'off', 'false'], ['specification', 'thermostat', 'power', 'maximum', 'true'], ['specification', 'thermostat', 'power', 'minimum', 'false']], [['transition', 'close', 'door'], ['state', 'refrigerator', 'door', 'closed']]])
    
    def test_if_states_were_exchanged(self):
        self.parser.exchange_states() |should| equal_to([[['initial_state', 'refrigerator', 'door', 'closed'], ['specification', 'light', 'off', 'true'], ['specification', 'light', 'on', 'false'], ['specification', 'thermostat', 'power', 'minimum', 'true'], ['specification', 'thermostat', 'power', 'maximum', 'false']], [['transition', 'open', 'door'], ['state', 'door', 'opened'], ['specification', 'light', 'on', 'true'], ['specification', 'light', 'off', 'false'], ['specification', 'thermostat', 'power', 'maximum', 'true'], ['specification', 'thermostat', 'power', 'minimum', 'false']], [['transition', 'close', 'door'], ['initial_state', 'refrigerator', 'door', 'closed']]])
        
    def test_if_tmp_file_was_removed(self):
        exists(self.parser._content_directory + '/content.xml') |should_not| equal_to(True)
    
    def test_if_standard_patch_was_generated(self):
        pass
if __name__ == '__main__':
    unittest.main()

