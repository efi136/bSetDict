from bloom_filter import BloomFilter
from collections import deque

class PrunBloomTree(object):

    ELEMENT_END = b'#!element_end'
    ELEMENT_START = b'#!element_start'

    def __init__(self, max_size, error_rate):
        """
        max_size is the expected number of elements the set will hold.
        error_rate is the wanted error rate. 
        """
        self.bloom_filters = []
        self.max_size = max_size
        self.error_rate = error_rate

    def _get_ith_bloom(self, i):
        number_of_elements = self.max_size
        return BloomFilter(max_elements=number_of_elements, error_rate=self.error_rate)

    def add(self, element):
        """
        adds the element to the set.
        The element should be of type bytes.
        """
        for i in range(len(element)):
            cur_substring = self.ELEMENT_START + element[:i]
            if len(self.bloom_filters) <= i:
                self.bloom_filters.append(self._get_ith_bloom(i))
            self.bloom_filters[i].add(cur_substring)
        if len(self.bloom_filters) <= len(element):
            self.bloom_filters.append(self._get_ith_bloom(len(element)))
        self.bloom_filters[len(element)].add(element + self.ELEMENT_END)

    def exists(self, element):
        """
        Returns True if the element is in the set.
        The element should be of type bytes.
        """
        if len(self.bloom_filters) <= len(element):
            return False
        return (element + self.ELEMENT_END) in self.bloom_filters[len(element)]

    def _prefix_exists(self, prefix):
        """
        Retuns True if the prefix exists
        """
        if len(self.bloom_filters) <= len(prefix):
            return False
        return (self.ELEMENT_START + prefix) in self.bloom_filters[len(prefix)]

    def get_elements_in_set(self):
        """
        Returns all of the elements in the set + some false positives.
        """
        elements = set()
        element_queue = deque()
        element_queue.appendleft(b'')
        if self.exists(b''):
            elements.add(b'')
        while len(element_queue) != 0:
            cur_element = element_queue.pop()
            for b in range(256):
                cur_candidate = cur_element + bytes([b])
                if self._prefix_exists(cur_candidate):
                    element_queue.appendleft(cur_candidate)
                if self.exists(cur_candidate):
                    elements.add(cur_candidate)
        return elements
