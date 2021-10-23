import numpy as np
from trie import Trie

def dp_levenshtein_trie(x, trie, th):
    results = {}
    n = trie.get_num_states()
    m = len(x)
    prev = np.zeros(n, dtype=np.uint64)
    current = np.zeros(n, dtype=np.uint64)
    for i in range(1, n):
        prev[i] = prev[trie.get_parent(i)] + 1

    for col in range(1, m + 1):
        current[0] = col
        for fil in range(1, n):
            cost = not x[col-1] == trie.get_label(fil)
            current[fil] = min(prev[fil] + 1,
                           current[trie.get_parent(fil)] + 1,
                           prev[trie.get_parent(fil)] + cost)
        if min(current) > th:
            return {}
        prev, current = current, prev

    for i in range(n):
        if trie.is_final(i):
            if prev[i] <= th:
                results[trie.get_output(i)] = prev[i]
    return results


def dp_restricted_damerau_trie(x, trie, th):
    results = {}
    n = trie.get_num_states()
    m = len(x)
    prev1 = np.zeros(n, dtype=np.uint64)
    prev2 = np.zeros(n, dtype=np.uint8)
    current = np.arange(n, dtype=np.uint8)

    for j in range(1, m+1):
        prev1, current, prev2 = current, prev1, prev1
        current[0] = prev1[0] + 1

        for i in range(1, n):
            erase = current[trie.get_parent(i)] + 1
            ins = prev1[i] + 1
            mod = prev1[trie.get_parent(i)]+ (not x[j-1] == trie.get_label(i))

            if i > 1 and j > 1 and x[j-2] == trie.get_label(i) and x[j-1] == trie.get_label(trie.get_parent(i)):
                current[i] = min(erase, ins, mod, prev2[trie.get_parent(i)])
            else:
                current[i] = min(erase, ins, mod)



    for i in range(n+1):
        if trie.is_final(i):
            if current[i] <= th:
                results[trie.get_output(i)] = current[i]
           

    return results


def dp_intermediate_damerau_trie(x, trie, th):
    results = {}
    n = trie.get_num_states()
    m = len(x)
    prev1 = np.zeros(n, dtype=np.uint64)
    prev2 = np.zeros(n, dtype=np.uint8)
    prev3 = np.zeros(n, dtype=np.uint8)
    current = np.arange(n, dtype=np.uint8)

    for j in range(1, m+1):
        prev3, prev2, prev1, current = current, prev3, current, prev3
        current[0] = prev1[0] + 1

        for i in range(1, n):
            erase = current[trie.get_parent(i)] + 1
            ins = prev1[i] + 1
            mod = prev1[trie.get_parent(i)]+ (not x[j-1] == trie.get_label(i))

            if i > 1 and j > 1 and x[j-2] == trie.get_label(i) and x[j-1] == trie.get_label(trie.get_parent(i)):
                current[i] = min(erase, ins, mod, prev2[trie.get_parent(i)])
            elif i > 2 and j > 1 and x[j-2] == trie.get_label(i) and x[j-1] == trie.get_label(trie.get_parent(trie.get_parent(i))):
                current[i] = min(erase, ins, mod, prev3[trie.get_parent(i)])
            elif i > 2 and j > 1 and x[j-3] == trie.get_label(i) and x[j-1] == trie.get_label(trie.get_parent(i)):
                current[i] = min(erase, ins, mod, prev3[trie.get_parent(i)])
            else:
                current[i] = min(erase, ins, mod)

    for i in range(n+1):
        if trie.is_final(i):
            if current[i] <= th:
                results[trie.get_output(i)] = current[i]
           

    return results


words = ["algortimo", "algortximo",
         "lagortimo", "agaloritom", "algormio", "ba"]
words.sort()
trie = Trie(words)

test = ["algoritmo", "acb"]
thrs = range(1, 4)

for th in thrs:
    print(f"threshols: {th:3}")
    for x in test:
        for dist, name in (
            (dp_levenshtein_trie, "levenshtein"),
            (dp_restricted_damerau_trie, "restricted"),
            (dp_intermediate_damerau_trie, "intermediate"),
        ):
            print(f"\t{x:12} \t{name}\t", end="")
            print(dist(x, trie, th))

"""
Salida del programa:

threshols:   1
	algoritmo    	levenshtein	[]
	algoritmo    	restricted	[('algortimo', 1)]
	algoritmo    	intermediate	[('algortimo', 1)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[]
threshols:   2
	algoritmo    	levenshtein	[('algortimo', 2)]
	algoritmo    	restricted	[('algortimo', 1), ('lagortimo', 2)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 2)]
	acb          	levenshtein	[]
	acb          	restricted	[]
	acb          	intermediate	[('ba', 2)]
threshols:   3
	algoritmo    	levenshtein	[('algormio', 3), ('algortimo', 2), ('algortximo', 3)]
	algoritmo    	restricted	[('algormio', 3), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 3)]
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('agaloritom', 3), ('algortximo', 2)]
	acb          	levenshtein	[('ba', 3)]
	acb          	restricted	[('ba', 3)]
	acb          	intermediate	[('ba', 2)]

"""
