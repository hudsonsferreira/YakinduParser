from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize
from nltk.util import clean_html, bigrams, trigrams
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.data import load
from nltk.probability import FreqDist
from string import punctuation
from stopwords import STOPWORDS
from os.path import join, basename, dirname, exists
from os import system
from re import sub
from OrderedSet import OrderedSet
from itertools import izip, chain
from magic import from_file
from shutil import rmtree
from tempfile import mkdtemp
from nltk.stem import WordNetLemmatizer
from groupby import modified_groupby


class YakinduParser(object):
    
    def __init__(self, path):
        if not exists(path) or not self._valid_mimetype(path):
            raise NameError("Invalid file")
        else:
            self._name = basename(path)
            self._path = dirname(path)
            self._tags = ['initial_state', 'state', 'final_state', 'transition', 'end', 'choice', 'synchronization', 'specification']
        self._content_directory = mkdtemp(prefix="YakinduDirectory")
        self._file_name = self._content_directory + '/content.xml'
        self._indentation = 4 * ' '

    def _valid_mimetype(self, path):
        return from_file(path, mime=True) == 'application/vnd.oasis.opendocument.text'

    def _unzip_odt(self):
        system('unzip %s/%s -d %s content.xml >>/dev/null' %(self._path, self._name, self._content_directory))

    def _clean_content(self):
        self._unzip_odt()
        extracted_doc_name = 'content.xml'
        raw_content_text = PlaintextCorpusReader(self._content_directory, extracted_doc_name).raw()
        cleaned_text = clean_html(raw_content_text)
        raw_content = sub(r'\w+ \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2} ', '', cleaned_text)
        tiny_raw_content = raw_content.lower()
        return tiny_raw_content

    def _remove_directory(self):
        rmtree(self._content_directory)
    
    def _tokenize_content(self):
        tokenized_content = []
        raw_content = self._clean_content()
        content_sents = sent_tokenize(raw_content)
        content_words_by_sents = map(lambda sent: word_tokenize(sent), content_sents)
        stopwords = regexp_tokenize(STOPWORDS, "[\w']+")
        extra_puncts = ['),', ').', '%),', '%).', '):', '()', '://', '>.', '.;', '...', '/>.']
        puncts = list(punctuation) + extra_puncts
        stopwords.extend(puncts)
        for sent in content_words_by_sents:
            clean_sent = [word for word in sent if word not in stopwords]
            tokenized_content.append(clean_sent)
        return tokenized_content

    def _order_tags_by_sent(self):
        self.tokenized_content = self._tokenize_content()
        tags_into_tokenized_content = []
        bigrams_of_tags_by_sent = []
        ordered_tags_by_sent = []
        for sent in self.tokenized_content:
            tags_into_tokenized_content.append([tag for tag in sent if tag in self._tags])
        for tags_by_sent in tags_into_tokenized_content:
            bigrams_of_tags_by_sent.append(bigrams(tags_by_sent))
            ordered_tags_by_sent.append(list(OrderedSet(tags_by_sent)))
        return ordered_tags_by_sent

    def _indexes_of_process_intersections(self):
        ordered_tags_by_sent = self._order_tags_by_sent()
        indexes_of_ordered_tags_by_process = []
        for i in range(len(ordered_tags_by_sent)):
            indexes_of_ordered_tags_by_process.append([])
        for i in range(len(ordered_tags_by_sent)):
            for tag in ordered_tags_by_sent[i]:
                indexes_of_ordered_tags_by_process[i].extend([index for index, label in enumerate(self.tokenized_content[i]) if label == tag])
        return indexes_of_ordered_tags_by_process
        
    def _sort_tag_indexes_bigrams(self):
        sorted_tag_indexes_bigrams_by_process = []
        for process_indexes_bigrams in self._indexes_of_process_intersections():
            sorted_tag_indexes_bigrams_by_process.append(bigrams(sorted(process_indexes_bigrams)+[None]))
        return sorted_tag_indexes_bigrams_by_process
        
    def _cut_tag_content_tuples_from_sent(self, index_set_from_sent, process):
        tag_content_tuples_from_sent = []
        for indexed_tuple in index_set_from_sent:
            tag_content_tuples_from_sent.append(list(process[indexed_tuple[0]:indexed_tuple[1]]))
        while [] in tag_content_tuples_from_sent:
            tag_content_tuples_from_sent.remove([])
        return tag_content_tuples_from_sent
    
    def _take_tagged_content(self, indexes, content):
        tagged_content = []
        for index_set, cont in izip(indexes, content):
            tagged_content.append(self._cut_tag_content_tuples_from_sent(index_set, cont))
        return tagged_content
        
    def _create_lean_content(self):
        lean_content = []
        tagged_content = self._take_tagged_content(self._sort_tag_indexes_bigrams(), self.tokenized_content)
        for sent_tagged_content in tagged_content:
            lean_content.append([tag_content_tuple for tag_content_tuple in sent_tagged_content if tag_content_tuple != ['end',]])
        while [] in lean_content:
            lean_content.remove([])
        return lean_content

    def _pos_tag_lean_content(self):
        pos_tagged_content = []
        tagger = load("/taggers/conll2000_aubt.pickle")
        for sent in self._create_lean_content():
            pos_tagged_content.append(tagger.batch_tag(sent))
        return pos_tagged_content
        
    def _clean_pos_tagged_content(self, pos_tagged_sent):
        cleaned_pos_tagged_content = []
        lemmatizer = WordNetLemmatizer()
        verb_tags = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        for chunk in pos_tagged_sent:
            if chunk[0][0] == 'specification':
                cleaned_pos_tagged_content.append([w for (w, t) in chunk if t not in verb_tags])
            else:
                if chunk[0][0] == 'transition':
                    cleaned_pos_tagged_content.append([lemmatizer.lemmatize(w) if t in verb_tags else w for (w, t) in chunk])
                else:
                    cleaned_pos_tagged_content.append([w for (w, t) in chunk])
        return cleaned_pos_tagged_content

    def _create_cleaned_content(self):
        cleaned_content = []
        for sent in self._pos_tag_lean_content():
            cleaned_content.append(self._clean_pos_tagged_content(sent))
        return cleaned_content
    
    def exchange_states(self):
        self._remove_directory()
        content = []
        state_tags = ['state', 'final_state']
        final_content = self._create_cleaned_content()
        for sent in final_content:
            content.append(map(lambda x: tuple(x[1:]), sent))
            fd_content = FreqDist(list(chain(*content)))
            for chunk in sent:
                if chunk[0] in state_tags and fd_content[tuple(chunk[1:])] > 1:
                    chunk[0] = 'initial_state'
                for word in chunk:
                    if word == 'true':
                        chunk[chunk.index(word)] = True
                    elif word == 'false':
                        chunk[chunk.index(word)] = False
        return final_content

    def _convert_to_yakindu_type(self, term):
        python_types = ['int', 'float', 'bool', 'str', 'NoneType']
        yakindu_types = ['integer', 'real', 'boolean', 'string', 'void']
        types_dict = dict(izip(python_types, yakindu_types))
        return types_dict[term]

    def _create_objects_interface(self):
        formated_objects_interface = []
        specification = []
        for sent in self.exchange_states():
             for chunk in sent:
                 if chunk[0] == 'specification':
                     specification.append(trigrams([chunk[1], chunk[-2], self._convert_to_yakindu_type(type(chunk[-1]).__name__)]))
        default_specification = list(OrderedSet(chain(*specification)))
        objects_specification = modified_groupby(default_specification, key=lambda obj: obj[0])
        for obj, specification_chunks in objects_specification.items():
            formated_objects_interface.append('\n\ninterface ' + obj + ':')
            for chunk in specification_chunks:
                 formated_objects_interface.append('\nvar ' + chunk[-2] + ':' + chunk[-1])               
        return ''.join(formated_objects_interface)

    def _create_events_interface(self):
        transition_events_interface = []
        flat_final_content = list(chain(*self.exchange_states()))
        sub_sent = [chunk for chunk in flat_final_content if chunk[0] == 'transition']
        events_interface = modified_groupby(sub_sent, key=lambda chunk: chunk[0])
        for k, transition_chunks in events_interface.items():
            for chunk in transition_chunks:
                transition_events_interface.append(chunk[1:])
        formated_transition_events_interface = map(lambda event: '\nin event ' + ''.join(event), transition_events_interface)
        return '\n\ninterface:' + ''.join(formated_transition_events_interface)

    def create_default_specification(self):
        set_specification_method = 2 * self._indentation + 'statechart.setSpecification('
        objects_interface = self._create_objects_interface()
        events_interface = self._create_events_interface()
        set_specification_content = '"' + objects_interface + events_interface + '"'
        return '%s%s%s' % (set_specification_method, repr(set_specification_content)[1:-1], ');\n\n    ')

    def _get_states_content(self):
        state_tags = ['initial_state', 'state', 'final_state']
        states_interface = []
        states_interface_capitalized = []
        for sent in self.exchange_states():
            for chunk in sent:
                if chunk[0] in state_tags:
                    states_interface.append(''.join(chunk[1:]))
        joined_states = list(OrderedSet(states_interface))      
        return joined_states

    def create_states_specification(self):
        states = []
        specification = []
        states_specification_content = []
        for sent in self.exchange_states():
            specification.append([list(chain(*trigrams([chunk[1] + '{0}', chunk[-2] + ' {1} ', str(chunk[-1]).lower() + '{2}{3}']))) for chunk in sent if chunk[0] == 'specification'])
        while [] in specification:
            specification.remove([])
        for spec in specification:
            spec[0].insert(0, 'entry/\n')
            spec[-1][-1] = spec[-1][-1].rstrip('{2}{3}')
        states_specification = dict(izip(self._get_states_content(), specification))
        for state, specification in states_specification.items():
            states_specification[state] = list(chain(*specification))
            states_specification[state].insert(0, '"')
            states_specification[state].append('"')
        for state, specification in states_specification.items():
            states_specification[state] = ''.join(specification).format('.', '=', ';', '\n')
        return states_specification


    def create_states_specification_interface(self):
        states_specification_interface = self.create_states_specification()
        specification_interface_process = '{1}State %s = SGraphFactory.eINSTANCE.createState();\n{1}%s.setName("%s"); \n{1}%s.setSpecification({0}); \n{1}region.getVertices().add(%s); \n{1}Node %sNode = ViewService.createNode(\n{1}getRegionCompartmentView(regionView), %s,\n{1}SemanticHints.STATE, preferencesHint);\n{1}setStateViewLayoutConstraint(%sNode);\n\n'
        for joined_state, specific_set_specification_content in states_specification_interface.items():
            states_specification_interface[joined_state] = specification_interface_process.format(repr(specific_set_specification_content)[1:-1], 2 * self._indentation) % ((joined_state,)*8)
        return states_specification_interface

   #import ipdb; ipdb.set_trace()   

    def create_states_layout_methods(self):
        states = self._get_states_content()
        layout_method_process = "{1}private static void setStateViewLayoutConstraint%s(Node %sNode) {\nBounds bounds = NotationFactory.eINSTANCE.createBounds(); \n{1}bounds.setX(%d); \n{1}bounds.setY(%d); \n{1}%sNode.setLayoutConstraint(bounds);\n{1}}".format(2 * self._indentation) %(((state,)*2), counter_x, counter_y, state)
        counter_x = 0
        counter_y = 0
        states_layout_list = []
        for state in states:
            counter_x += 100
            counter_y += 250
            #construction

    def _get_initial_state(self):
        initial_state_list = []
        for sent in self.exchange_states():
            for chunk in sent:
                if chunk[0] == 'initial_state':
                    initial_state_list.append(chunk[1:])
        return initial_state_list

    def create_initial_state_interface(self):
        formated_initial_state_interface = []
        initial_state_joined = []
        initial_state_cleaned = []
        states_selected = self._get_initial_state()
        for state in states_selected:
            initial_state_joined.append(''.join(state))
        initial_state_cleaned = set(initial_state_joined)
        for state in initial_state_cleaned:
            formated_initial_state_interface.append('{0}Transition transition = SGraphFactory.eINSTANCE.createTransition();\n{0}transition.setSource(initialState);\n{0}transition.setTarget(%s);\n{0}initialState.getOutgoingTransitions().add(transition);\n{0}ViewService.createEdge(initialStateView, %sNode, transition,\n{0}SemanticHints.TRANSITION, preferencesHint);\n'.format(2 * self._indentation) %((state,)*2))
        return formated_initial_state_interface

    def _get_sequence_transitions(self):
        state_tags = ['initial_state', 'state', 'final_state']
        list_sequence = []
        list_transitions = []
        for sent in self.exchange_states():
            for chunk in sent:
                if chunk[0] in state_tags or chunk[0] == 'transition':
                    list_sequence.append(chunk[1:])
        for i in range(2, len(list_sequence), 2):
            list_transitions.append(list_sequence[i-2:i+1])
        return list_transitions

    def _join_sequence_transitions(self):
        sequence_joined = []
        interface_transitions_joined = []
        for sequence in self._get_sequence_transitions():
            for word in sequence:
                sequence_joined.append(''.join(word))
        for i in range(2, len(sequence_joined), 3): 
            interface_transitions_joined.append(list(sequence_joined[i-2:i+1]))
        return interface_transitions_joined

    def create_transitions_interface(self):
        formated_transition_interface = []
        for item in self._join_sequence_transitions():
            formated_transition_interface.append('{0}Transition %s = SGraphFactory.eINSTANCE.createTransition();\n{0}%s.setSpecification("%s");\n{0}%s.setSource(%s);\n{0}%s.setTarget(%s);\n\n'.format(2 * self._indentation) %(item[1], item[1], item[1], item[1], item[0], item[1], item[2]))
        return formated_transition_interface
    
    def create_class_factory_utils(self):
        class_content = []
        first_constant = open('../yakindu-parser/src/first_constant.txt', 'r')
        second_constant = open('../yakindu-parser/src/second_constant.txt', 'r')
        third_constant = open('../yakindu-parser/src/third_constant.txt', 'r')
        class_content.append(first_constant.read())
        class_content.append(self.create_default_specification())
        class_content.append(second_constant.read())
        states_specification_interface = self.create_states_specification_interface()
        for state, specification in states_specification_interface.items():
            class_content.append(states_specification_interface[state])
        for transition in self.create_transitions_interface():
            class_content.append(transition)
        for initial_state in self.create_initial_state_interface():
            class_content.append(initial_state)
        class_content.append(third_constant.read())
        class_factory_utils = open('../yakindu-parser/src/FactoryUtils.java', 'w')
        for content in class_content:
            class_factory_utils.write(str(content))
        class_factory_utils.close()
