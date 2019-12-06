#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length
    for ticket in tickets:
        if ticket.source == "NONE":
            hash_table_insert(hashtable, 'NONE', ticket.destination)
        elif ticket.destination == "NONE":
            hash_table_insert(hashtable, ticket.source, 'NONE')
        else:
            hash_table_insert(hashtable, ticket.source, ticket.destination)
    current_key = 'NONE'
    for num in range(length):
        location = hash_table_retrieve(hashtable, current_key)
        route[num] = location
        current_key = location
    return route
