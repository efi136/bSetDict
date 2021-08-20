from bloom_filter import BloomFilter
from collections import deque

class PrunBloomTree(object):

    ELEMENT_END = b'e'
    ELEMENT_START = b's'

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

    def get_bin_element(self, element):
        return b''.join([bin(a)[2:].zfill(8).encode() for a in element])

    def unbin_element(self, s):
        return bytes(int(s[i : i + 8], 2) for i in range(0, len(s), 8))

    def add(self, element):
        """
        adds the element to the set.
        The element should be of type bytes.
        """
        element = self.get_bin_element(element)
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
        element = self.get_bin_element(element)
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
            for b in [b'0', b'1']:
                cur_candidate = cur_element + b
                if self._prefix_exists(cur_candidate):
                    element_queue.appendleft(cur_candidate)
                if (len(cur_candidate) % 8 == 0) and self.exists(self.unbin_element(cur_candidate)):
                    elements.add(self.unbin_element(cur_candidate))
        return elements
