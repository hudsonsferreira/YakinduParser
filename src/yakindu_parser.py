from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize
from nltk.util import clean_html, bigrams
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

    def _valid_mimetype(self, path):
        return from_file(path, mime=True) == 'application/vnd.oasis.opendocument.text'

    def _unzip_odt(self):
        system('unzip %s/%s -d %s content.xml >>/dev/null' %(self._path, self._name, self._content_directory))

    def _clean_content(self):
        self._unzip_odt()
        extracted_doc_name = 'content.xml'
        raw_content_text = PlaintextCorpusReader(self._content_directory, extracted_doc_name).raw()
        cleaned_text = clean_html(raw_content_text)
        #import ipdb; ipdb.set_trace()
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
        initial_state_sent = list(chain(*[sent for sent in self.exchange_states() if sent[0][0] == 'initial_state']))
        sub_sent = [chunk for chunk in initial_state_sent if chunk[0] == 'specification']
        objects_specification = modified_groupby(sub_sent, key=lambda chunk: chunk[1])
        for k, specification_chunks in objects_specification.items():
            formated_objects_interface.append('\n\ninterface ' + k + ':')
            for chunk in specification_chunks:
                 formated_objects_interface.append('\nvar ' + chunk[-2] + ':' + self._convert_to_yakindu_type(type(chunk[-1]).__name__))
        return ''.join(formated_objects_interface)

    def _create_events_interface(self):
        transition_events_interface = []
        flat_final_content = list(chain(*self.exchange_states()))
        sub_sent = [chunk for chunk in flat_final_content if chunk[0] == 'transition']
        events_interface = modified_groupby(sub_sent, key=lambda chunk: chunk[0])
        for k, transition_chunks in events_interface.items():
            for chunk in transition_chunks:
                transition_events_interface.append(chunk[1:])
        formated_transition_events_interface = map(lambda x: '\nin event ' + ' '. join(x), transition_events_interface)
        return '\n\ninterface:' + ''.join(formated_transition_events_interface)

    def create_set_specification(self):
        set_specification_method = 'statechart.setSpecification(' + '"'
        return "%s%s%s%s" % (set_specification_method, self._create_objects_interface(), self._create_events_interface(), '");')
    
    def _delete_duplicate_states(self, states):
        final_states = set()
        for state in states:
            if state[0] not in final_states:
                yield state
                final_states.add(state[0])

    def _get_states_content(self):
        state_tags = ['initial_state', 'state', 'final_state']
        states_interface = []
        states_interface_capitalized = []
        for sent in self.exchange_states():
            for chunk in sent:
                if chunk[0] in state_tags:
                    states_interface.append(chunk[1:])
        return states_interface

    def create_states_interface(self):
        formated_states_interface = []
        states_joined = []
        states_selected = self._get_states_content()
        for state in self._delete_duplicate_states(states_selected):
            states_joined.append(''.join(state))
        for state in states_joined:
            formated_states_interface.append('State %s = SGraphFactory.eINSTANCE.createState();\n %s.setName("%s"); \n%s.setSpecification("entry/\nlight.off = true;\nthermostat.minimum = true;\nlight.on = false;\nthermostat.maximum = false"); \nregion.getVertices().add(%s); \nNode %sNode = ViewService.createNode(\ngetRegionCompartmentView(regionView), %s,\nSemanticHints.STATE, preferencesHint);\nsetStateViewLayoutConstraint(%sNode);\n\n' %((state,)*8))
        return formated_states_interface

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
        states_selected = self._get_initial_state()
        for state in self._delete_duplicate_states(states_selected):
            initial_state_joined.append(''.join(state))
        for state in initial_state_joined:
            formated_initial_state_interface.append('Transition transition = SGraphFactory.eINSTANCE.createTransition();\ntransition.setSource(initialState);\ntransition.setTarget(%s);\ninitialState.getOutgoingTransitions().add(transition);\nViewService.createEdge(initialStateView, %sNode, transition,\nSemanticHints.TRANSITION, preferencesHint);' %((state,)*2))
        return formated_initial_state_interface

    def _get_sequence_transitions(self):
        state_tags = ['initial_state', 'state', 'final_state']
        list_sequence = []
        list_transitions = []
        for sent in self.exchange_states():
            for chunk in sent:
                if chunk[0] in state_tags or chunk[0] == 'transition':
                    list_sequence.append(chunk[1:])
        #import ipdb; ipdb.set_trace()
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
            formated_transition_interface.append('Transition %s = SGraphFactory.eINSTANCE.createTransition();\n%s.setSpecification("%s");\n %s.setSource(%s);\n%s.setTarget(%s);' %(item[1], item[1], item[1], item[1], item[0], item[1], item[2]))
        return formated_transition_interface
        

#OBS: falta tratar e incrementar as specifications dos states, esta foi feita na mao
