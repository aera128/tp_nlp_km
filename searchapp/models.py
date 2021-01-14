import numpy
import spacy
# Create your models here.
from nltk.corpus import wordnet


class SynonymGetter:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")

    @staticmethod
    def wordnet_sim(syn1, syn2, lemma, sim_type='path'):
        if sim_type == "path":
            sim = syn1.path_similarity(syn2)
        elif sim_type == "wup":
            sim = syn1.wup_similarity(syn2)
        elif sim_type == "lch":
            sim = syn1.lch_similarity(syn2)
        else:
            sim = []
        return sim

    def search_syns(self, query):
        synonyms = []
        syn_candidates = []
        doc = self.nlp(query)
        for tok in doc:
            from searchapp.utils import get_wordnet_pos
            tok.pos_ = get_wordnet_pos(tok.tag_)
            if tok.pos_ != '':
                try:
                    syn_candidates = wordnet.synsets(
                        tok.text,
                        pos=eval("wordnet.{}".format(tok.pos_))
                    )
                    if len(syn_candidates) == 0:
                        word_morphed = wordnet.morphy(tok.text)
                        syn_candidates = wordnet.synsets(
                            word_morphed,
                            pos=eval("wordnet.{}".format(tok.pos_))
                        )
                except Exception as e:
                    print(e)
            try:
                for syn in syn_candidates:
                    for lemma in syn.lemmas():
                        sim = self.wordnet_sim(syn, syn_candidates[0], lemma, "path")
                        if sim and sim >= 0.1 and lemma.name().replace("_", " ").lower() != tok.text:
                            synonyms.append(lemma.name().replace("_", " "))
                        # print("Synonym : ", lemma.name().replace("_", " "), " - ", sim * 100, "%")

            except Exception as e:
                print(e)

        return synonyms
