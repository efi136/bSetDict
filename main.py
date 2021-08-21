import itercap
import sqlite3
import random
import os
from PruneBloomTree import PrunBloomTree


class Result(object):
    def __init__(self, max_size, base_error_rate, number_of_elements, number_of_destinations, number_of_sources):
        self.max_size = max_size
        self.base_error_rate = base_error_rate
        self.number_of_elements = number_of_elements
        self.number_of_destinations = number_of_destinations
        self.number_of_sources = number_of_sources

    def get_dict_from_set(self, s):
        d = dict()
        for src_dst in s:
            src = src_dst[:4]
            dst = src_dst[4:]
            if src not in d:
                d[src] = set()
            d[src].add(dst)
        return d

    def calculate_error(self, real_set, bloom_tree):
        """
        The errors
        """
        errors = dict()
        real_flows_sets = self.get_dict_from_set(real_set)
        bloom_flows_sets = self.get_dict_from_set(bloom_tree.get_elements_in_set())
        for flow in real_flows_sets:
            real_flow_set = real_flows_sets[flow]
            estimated_flow_set = bloom_flows_sets[flow]
            errors[flow] = (len(estimated_flow_set) - len(real_flow_set), len(real_flow_set))
        return errors
    
    def calculate_avarage_error(self, errors):
        errors = [float(t[0]) / float(t[1]) for t in errors.values()]
        return sum(errors) / len(errors), max(errors)

    def save_result_to_db(self, conn, real_set, bloom_tree):
        errors = self.calculate_error(real_set, bloom_tree)
        avarage_error, maximum_error = self.calculate_avarage_error(errors)
        conn.execute('insert into results (max_size, error_rate, number_of_flows, number_of_destinations, number_of_sources, avarage_error, maximum_error) values (?,?,?,?,?,?,?)',
        (self.max_size, self.base_error_rate, self.number_of_elements, self.number_of_destinations, self.number_of_sources, avarage_error, maximum_error,))
        conn.commit()


def create_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE IF NOT EXISTS results (max_size INTEGER, error_rate REAL, number_of_flows INTEGER, number_of_destinations INTEGER, number_of_sources INTEGER, avarage_error REAL, maximum_error REAL);')
    return conn

def compare_performance_on_random(conn, max_size, base_error_rate, number_of_elements, number_of_destinations, number_of_sources):
    result_set = set()
    bloom_tree = PrunBloomTree(max_size, base_error_rate)
    srcs = [os.urandom(4) for _ in range(number_of_sources)]
    dsts = [os.urandom(4) for _ in range(number_of_destinations)]
    for _ in range(number_of_elements):
        src_ip = random.choice(srcs)
        dst_ip = random.choice(dsts)
        element = src_ip + dst_ip
        bloom_tree.add(element)
        result_set.add(element)
    r = Result(max_size, base_error_rate, number_of_elements, number_of_destinations, number_of_sources)
    r.save_result_to_db(conn, result_set, bloom_tree)


number_of_elements_values = [100, 1000]
number_of_destinations_values = [100, 1000, 10000]
number_of_sources_values = [100, 1000, 10000]
base_error_rate_values = [0.2, 0.3, 0.4, 0.5]
size_ratio_values = [5,6,7,8,9]

def random_results():
    conn = create_db('./random_results.db')
    for base_error_rate in base_error_rate_values:
        print(base_error_rate)
        for e in number_of_elements_values:
            print(e)
            for srcs in number_of_sources_values:
                for dsts in number_of_destinations_values:
                    for size_ratio in size_ratio_values:
                        print("Running...")
                        compare_performance_on_random(conn, e*size_ratio, base_error_rate, e, dsts, srcs)
    conn.close()

def main():
    random_results()

main()