# -*- coding: utf-8 -*-
import re
from collections import Counter
import numpy as np
import time


from trie import Trie

from test_tarea2 import dp_levenshtein_threshold
from test_tarea2 import dp_restricted_damerau_threshold
from test_tarea2 import dp_intermediate_damerau_threshold


class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """

        self.vocabulary = self.build_vocab(
            vocab_file_path, tokenizer=re.compile("\W+"))

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding='utf-8') as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard('')  # por si acaso
            return sorted(vocab)

    def suggest(self, term, distance="levenshtein", threshold=2):
        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate"]
        results = {}  # diccionario termino:distancia
        function = {
            "levenshtein": dp_levenshtein_threshold,
            "restricted": dp_restricted_damerau_threshold,
            "intermediate": dp_intermediate_damerau_threshold
        }

        for vocab_term in self.vocabulary:
            if (abs(len(term) - len(vocab_term)) <= threshold):
                dist = function[distance](term, vocab_term, threshold)
                if dist <= threshold:
                    results[vocab_term] = dist

        return results

    def suggest_opt(self, term, distance="levenshtein", threshold=2):
        """Método para sugerir palabras similares siguiendo la tarea 3.

                A completar.

                Args:
                    term (str): término de búsqueda.
                    distance (str): algoritmo de búsqueda a utilizar
                        {"levenshtein", "restricted", "intermediate"}.
                    threshold (int): threshold para limitar la búsqueda
                        puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                        o filtrando la salida de las distancias de la tarea 2
                """
        assert distance in ["levenshtein", "restricted", "intermediate"]
        results = {}  # diccionario termino:distancia
        function = {
            "levenshtein": dp_levenshtein_threshold,
            "restricted": dp_restricted_damerau_threshold,
            "intermediate": dp_intermediate_damerau_threshold
        }

        for vocab_term in self.vocabulary:
            if (abs(len(term) - len(vocab_term)) <= threshold):
                vocabulary = list(term+vocab_term)
                vx = dict.fromkeys(vocabulary)
                vy = dict.fromkeys(vocabulary)
                
                for l in vx:
                    vx[l] = term.count(l)
                    vy[l] = vocab_term.count(l)
            
                v = np.subtract(list(vx.values()), list(vy.values()))
            
                dif = max(np.sum(v[v>0]), -np.sum(v[v<0]))
                if dif <= threshold:
                    dist = function[distance](term, vocab_term, threshold)
                    if dist <= threshold:
                        results[vocab_term] = dist

        return results

    def test(self, spellsuggester, words, thresholds):
        # bucle de palabras separadas por tabulación en filas
        # casa	1	31
        with open("resuls.txt", "w", encoding='utf-8') as text_file:
            for word in words:
                text_file.write(word + "\t" + threshold + "\t")
                for threshold in thresholds:
                    results = spellsuggester.suggest(
                        word, "levenshtein", threshold)
                    for my_word in results:
                        return 0


class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    
    """
    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)


if __name__ == "__main__":
    spellsuggester = TrieSpellSuggester("./corpora/quijote.txt")
    start = time.time()
    print("hello")
    spellsuggester.suggest_opt("suggest")
    end = time.time()
    print(end - start)
    start2 = time.time()
    print("hello")
    spellsuggester.suggest("suggest")
    end2 = time.time()
    print(end2 - start2)
    # spellsuggester.test(spellsuggester, "hola",2)
    # cuidado, la salida es enorme print(suggester.trie)
