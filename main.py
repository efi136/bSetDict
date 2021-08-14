import itercap
import sqlite3
import random
import os
from SetDict import bSetDict, SetDict


class Result(object):
    def __init__(self, L, d, set_dict, b_set_dict):
        self.L = L
        self.d = d
        self.number_of_flows = len(set_dict.flows_sets)
        self.number_of_elements = len(set_dict.element_set)
        self.set_dict_size = set_dict.get_size()
        self.b_set_dict_size = b_set_dict.get_size()
        self.errors = self.calculate_error(set_dict, b_set_dict)
        self.avarage_error, self.maximum_error = self.calculate_avarage_error()

    def calculate_error(self, set_dict, b_set_dict):
        """
        The errors
        """
        errors = dict()
        for flow in set_dict.flows_sets:
            real_flow_set = set_dict.flows_sets[flow]
            estimated_flow_set = b_set_dict.get_estimated_set_for_flow(flow)
            errors[flow] = (len(estimated_flow_set) - len(real_flow_set), len(real_flow_set))
        return errors
    
    def calculate_avarage_error(self):
        errors = [float(t[0]) / float(t[1]) for t in self.errors.values()]
        return sum(errors) / len(errors), max(errors)

    def save_result_to_db(self, conn):
        conn.execute('insert into results (L, d, number_of_flows, number_of_elements, set_dict_size, b_set_dict_size, avarage_error, maximum_error) values (?,?,?,?,?,?,?,?)',
        (self.L, self.d, self.number_of_flows, self.number_of_elements, self.set_dict_size, self.b_set_dict_size, self.avarage_error, self.maximum_error,))
        conn.commit()


def create_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.execute('CREATE TABLE IF NOT EXISTS results (L INTEGER, d INTEGER, number_of_flows INTEGER, number_of_elements INTEGER, set_dict_size INTEGER, b_set_dict_size INTEGER, avarage_error REAL, maximum_error REAL);')
    return conn


def compare_performance_on_sample(sample, L, d, conn, set_dict_cache=None):
    set_dict = SetDict()
    b_set_dict = bSetDict(L, d)
    for packet in itercap.iter_eth_packets(sample):
        src_ip = itercap.get_src_ip(packet)
        dst_ip = itercap.get_dst_ip(packet)
        if set_dict_cache is None:
            set_dict.add_element(src_ip,  dst_ip)
        b_set_dict.add_element(src_ip, dst_ip)
    if set_dict_cache is not None:
        set_dict = set_dict_cache
    r = Result(L, d, set_dict, b_set_dict)
    r.save_result_to_db(conn)
    return set_dict


def compare_performance_on_random(L, d, conn, number_of_elements, number_of_destinations, number_of_sources):
    set_dict = SetDict()
    b_set_dict = bSetDict(L, d)
    srcs = [os.urandom(4) for _ in range(number_of_sources)]
    dsts = [os.urandom(4) for _ in range(number_of_destinations)]
    for _ in range(number_of_elements):
        src_ip = random.choice(srcs)
        dst_ip = random.choice(dsts)
        set_dict.add_element(src_ip,  dst_ip)
        b_set_dict.add_element(src_ip, dst_ip)
    r = Result(L, d, set_dict, b_set_dict)
    r.save_result_to_db(conn)

L_values = [100, 1000, 2000, 4000, 5000, 10000]
d_values = [2, 3, 5, 10, 20]

def sample_results():
    conn = create_db('./sample_results.db')
    set_dict = None
    for L in L_values:
        for d in d_values:
            set_dict = compare_performance_on_sample('./samples/sample.pcap', L, d, conn, set_dict_cache=set_dict)
    conn.close()

number_of_elements_values = [100, 1000, 10000, 100000, 1000000]
number_of_destinations_values = [100, 1000, 10000]
number_of_sources_values = [100, 1000, 10000]

def random_results():
    conn = create_db('./random_results.db')
    for L in L_values:
        for d in d_values:
            for e in number_of_elements_values:
                for s in number_of_sources_values:
                    for dsts in number_of_destinations_values:
                        compare_performance_on_random(L, d, conn, e, dsts, s)
    conn.close()

def main():
    sample_results()
    random_results()

main()