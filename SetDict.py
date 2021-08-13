class bSetDict(object):

    HASH_INDEX_ADDITION = b'\\7e'

    def __init__(self, L, d):
        self.L = L
        self.d = d
        self.set_array = [set() for _ in range(L)]
        self.flows = set()

    def get_hash(self, value, i):
        return hash(value + i*self.HASH_INDEX_ADDITION) % self.L

    def add_element(self, flow_id, element):
        self.flows.add(flow_id)
        for i in range(self.d):
            index = self.get_hash(flow_id, i)
            self.set_array[index].add(element)

    def query_element_in_set(self, flow_id, element):
        if flow_id not in self.flows:
            return False
        for i in range(self.d):
            index = self.get_hash(flow_id, i)
            if element not in self.set_array[index]:
                return False
        return True

    def get_estimated_set_for_flow(self, flow_id):
        intersection = self.set_array[self.get_hash(flow_id, 0)]
        for i in range(1, self.d):
            index = self.get_hash(flow_id, i)
            intersection = intersection.intersection(self.set_array[index])
        return intersection

    def get_size(self):
        total_size = len(self.flows) + self.L
        for i in range(self.L):
            total_size += len(self.set_array[i])
        return total_size

    def get_keys(self):
        return self.flows
        

class SetDict(object):

    def __init__(self):
        self.flows_sets = dict()

    def add_element(self, flow_id, element):
        if flow_id not in self.flows_sets:
            self.flows_sets[flow_id] = set()
        self.flows_sets[flow_id].add(element)

    def query_element_in_set(self, flow_id, element):
        if flow_id not in self.flows_sets:
            return False
        return element in self.flows_sets[flow_id]
        
    def get_estimated_set_for_flow(self, flow_id):
        if flow_id not in self.flows_sets:
            return set()
        return self.flows_sets[flow_id]

    def get_size(self):
        total_size = len(self.flows_sets)
        for key in self.flows_sets:
            total_size += len(self.flows_sets[key])
        return total_size

    def get_keys(self):
        return self.flows_set.keys()