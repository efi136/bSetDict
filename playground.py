'''
#%%
import dpkt

counter=0
ipcounter=0
tcpcounter=0
udpcounter=0

filename='./samples/sample.pcap'

#%%
reader = dpkt.pcap.Reader(open(filename,'rb'))
(t, pkt) = reader.next()
eth=dpkt.ethernet.Ethernet(pkt)
#%%
for ts, pkt in reader:

    counter+=1
    eth=dpkt.ethernet.Ethernet(pkt)
    if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
       continue

    ip=eth.data
    ipcounter+=1

    if ip.p==dpkt.ip.IP_PROTO_TCP: 
       tcpcounter+=1

    if ip.p==dpkt.ip.IP_PROTO_UDP:
       udpcounter+=1

print("Total number of packets in the pcap file: ", counter)
print("Total number of ip packets: ", ipcounter)
print("Total number of tcp packets: ", tcpcounter)
print("Total number of udp packets: ", udpcounter)
'''
# %%
from PruneBloomTree import PrunBloomTree

a = PrunBloomTree(10000, 0.01)
a.add(b'123')
a.add(b'234')
print(a.get_elements_in_set())
# %%
