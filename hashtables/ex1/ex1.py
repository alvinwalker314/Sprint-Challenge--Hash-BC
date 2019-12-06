#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)
    l = 0
    r = 1
    if length != 1:
        while l != length:
            while r != length:
                if weights[l] + weights[r] == limit:
                    if l > r:
                        return [l, r]
                    else:
                        return [r, l]
                else:
                    r += 1
            l += 1
            r = l + 1
    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
