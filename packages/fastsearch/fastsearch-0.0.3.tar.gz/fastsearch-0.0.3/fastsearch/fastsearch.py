import ahocorasick

class FastSearch:
    def __init__(self, delim_pattern, ngram_length):
        self.delim_pattern = delim_pattern
        self.ngram_length = ngram_length
        self.A = ahocorasick.Automaton()

    def add_sentence(self, sentence, descriptor, selection_start=0, selection_end=None):
        words = self.delim_pattern.split(sentence)
        selection_end = len(words) if not selection_end else selection_end
        for word in words[selection_start: selection_end]:
            if len(word) >= self.ngram_length:
                for i in range(0, len(word) - self.ngram_length + 1):
                    ngram = word[i: i + self.ngram_length]
                    self.A.add_word(ngram, descriptor)
    
    def fit(self):
        self.A.make_automaton()

    def lookup(self, text, one_match=False):
        matches = []
        for end_index, descriptor in self.A.iter(text):
            start_index = end_index - self.ngram_length + 1
            # print(text, start_index, descriptor)
            matches.append(descriptor)
            if one_match:
                break
        return matches


