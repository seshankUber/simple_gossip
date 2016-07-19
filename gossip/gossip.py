import sys
from core.gossip_node import GossipNode


def initiate_gossip(port, connection_nodes):
    gossip_node = GossipNode(port, connection_nodes)
    gossip_node.start_gossip()


if __name__ == "__main__":
    args = sys.argv
    port = int(args[1])
    connected_nodes = args[2:len(args)]
    print port, connected_nodes
    initiate_gossip(port, connected_nodes)
