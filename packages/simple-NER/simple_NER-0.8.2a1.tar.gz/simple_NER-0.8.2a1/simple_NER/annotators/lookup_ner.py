from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from os import listdir
from os.path import join, dirname
from quebra_frases import find_spans


class LookUpNER(NERWrapper):
    def __init__(self, lang="en-us"):
        super().__init__()
        self.entities = {}
        self.load_entities(join(dirname(dirname(__file__)), "res", lang))
        self.add_detector(self.annotate)

    def load_entities(self, folder):
        # TODO make a decent list, this is just a POC
        for entity_file in listdir(folder):
            if not entity_file.endswith(".entity"):
                continue
            with open(join(folder, entity_file)) as f:
                self.entities[entity_file.replace(".entity", "")] = f.read().lower().split("\n")

    def annotate(self, text):
        for label in self.entities:
            for start, end, word in find_spans(text, self.entities[label]):
                if not word:
                    continue
                yield Entity(word, label, spans=[(start, end)],
                             source_text=text)
