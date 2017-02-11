import gensim
import string



class CuisineParser(object):
    THRESHOLD = 0.20

    def __init__(self, look_ahead=5, reference_file_name='../Word2VecData.bin'):
        print 'Loading Word2Vec model'
        self.model = gensim.models.Word2Vec.load_word2vec_format(reference_file_name, binary=True)
        print 'Done!'

    def parse_food_tags(self, text):

        tags = {}

        for word in text.replace('\n', ' ').translate(None, string.punctuation).split(' '):

            if word in self.model.vocab:
                sim = self.model.similarity('bread', word)
                if sim > self.THRESHOLD:
                    tags[word] = sim

        return tags
