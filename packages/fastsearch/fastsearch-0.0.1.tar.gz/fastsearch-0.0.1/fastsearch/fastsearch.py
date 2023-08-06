import ahocorasick
import re

class FastSearch:
    def __init__(self, delim_pattern, ngram_length):
        self.delim_pattern = delim_pattern
        self.ngram_length = ngram_length
        self.A = ahocorasick.Automaton()

    def add_sentence(self, sentence, descriptor, selection_start=0, selection_end=0):
        words = self.delim_pattern.split(sentence)
        for word in words:
            if len(word) >= self.ngram_length:
                for i in range(selection_start, len(word) - self.ngram_length + 1 - selection_end):
                    ngram = word[i: i + self.ngram_length]
                    self.A.add_word(ngram, descriptor)
    
    def fit(self):
        self.A.make_automaton()

    def lookup(self, text, one_match=False):
        for end_index, descriptor in self.A.iter(text):
            start_index = end_index - self.ngram_length + 1
            print(text, start_index, descriptor)
            if one_match:
                break

if __name__ == '__main__':
    delim_pattern = re.compile('\+')
    search = FastSearch(delim_pattern, 3)
    search.add_sentence('1234+56789+abcdefg', {'fun': 1})
    search.add_sentence('bbbb+cccc+ddd', {'fun': 2})
    search.fit()
    search.lookup('aaaaa12aaaa', one_match=True)
    search.lookup('aaaadefaaa', one_match=True)
    search.lookup('aaaad234aaa', one_match=True)
    search.lookup('aaaad34aaa', one_match=True)
    search.lookup('aaaa89abaa', one_match=True)
    search.lookup('aaaa89ddds', one_match=True)
