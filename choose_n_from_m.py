import random


def get_random_list_without_repetition(m, n):
    results = []
    while len(results) < n:
        s = random.randint(0, m)
        if s not in results:
            results.append(s)
    return results
