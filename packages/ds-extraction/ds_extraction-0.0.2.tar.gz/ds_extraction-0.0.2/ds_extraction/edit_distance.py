from fuzzywuzzy import fuzz
from ds_extraction.utils.preprocess import PreProcess

class Distance:
    def __init__(self):
        self.preprocess = PreProcess()

    def compare_word(self,token_rule,sentence):
        """
        compare 2 char
        params:
            character a, character b, threshold
        return:
            boolean, True if pass thresshold
        """
        partial_ratio = fuzz.partial_ratio(self.preprocess.remove_accent(token_rule),self.preprocess.remove_accent(sentence))
        token_set_ratio = fuzz.token_set_ratio(self.preprocess.remove_accent(token_rule),self.preprocess.remove_accent(sentence))

        partial_ratio = float(partial_ratio)/100
        token_set_ratio = float(token_set_ratio)/100
        return {"partial":partial_ratio,"token_set":token_set_ratio}