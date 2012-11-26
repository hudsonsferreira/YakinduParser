from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize
from nltk.util import clean_html, bigrams
from nltk.corpus.reader import PlaintextCorpusReader
from nltk.tag import UnigramTagger
from nltk.corpus import treebank
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
#        import ipdb; ipdb.set_trace()
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
#        while [] in tag_content_tuples_from_sent:
#            tag_content_tuples_from_sent.remove([])
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
        train_sents = treebank.tagged_sents()[:3000]
        tagger = UnigramTagger(train_sents)
        for sent in self._create_lean_content():
            pos_tagged_content.append(tagger.batch_tag(sent))
        return pos_tagged_content
        
    def _clean_pos_tagged_content(self, pos_tagged):
        cleaned_pos_tagged_content = []
        for sent in pos_tagged:
            if sent[0][0] != 'specification':
                cleaned_pos_tagged_content.append([w for (w, t) in sent])
            else:
                cleaned_pos_tagged_content.append([w for (w, t) in sent if t!='VBZ' and t!='VBD'])
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
        return final_content
