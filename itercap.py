import dpkt

def iter_eth_packets(cap_path):
    with open(cap_path,'rb') as capfile:
        reader = dpkt.pcap.Reader(capfile)
        (t, pkt) = reader.next()
        eth=dpkt.ethernet.Ethernet(pkt)
        for ts, pkt in reader:
            eth=dpkt.ethernet.Ethernet(pkt)
            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
                continue
            yield eth

def get_src_ip(packet):
    """
    Gets the src ip from eth packet.
    """
    return packet.data.src

def get_dst_ip(packet):
    return packet.data.dst
