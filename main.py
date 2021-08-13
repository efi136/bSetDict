import itercap
from SetDict import bSetDict, SetDict


def compare_performance_on_sample(sample, L, d):
    set_dict = SetDict()
    b_set_dict = bSetDict(L, d)
    for packet in itercap.iter_eth_packets(sample):
        src_ip = itercap.get_src_ip(packet)
        dst_ip = itercap.get_dst_ip(packet)
        set_dict.add_element(src_ip,  dst_ip)
        b_set_dict.add_element(src_ip, dst_ip)
    return set_dict.get_size(), b_set_dict.get_size()

def main():
    print(compare_performance_on_sample('./samples/sample.pcap', 1000, 5))

main()