class Node:
    def __init__(self, node_id, priority):
        self.node_id = node_id
        self.priority = priority
        self.alive = True
        self.coordinator = None
        self.all_nodes = []
    def set_nodes(self, nodes):
        self.all_nodes = nodes
    def fail(self):
        self.alive=False
        print(f"Node {self.node_id} has failed")
    def start_election(self):
        print(f"Node {self.node_id} starts election")
        higher = [n for n in self.all_nodes if n.priority>self.priority and n.alive]
        
        if not higher:
            self.become_coordinator()
            self.announce()
        else:
            for h in higher:
                print(f"  Node {self.node_id} -> sending ELECTION to Node {h.node_id}")
            for h in higher:
                h.start_election()
    def become_coordinator(self):
        self.coordinator = self.node_id
        print(f"Node {self.node_id} becomes coordinator")
    def announce(self):
        print(f"Node {self.node_id} broadcasting COORDINATOR")
        for n in self.all_nodes:
            if n.alive:
                n.coordinator = self.node_id
                print(f"  Node {n.node_id} sets coordinator={n.coordinator}")
                
                
def simulate():
    nodes = [Node(i+1,i+1) for i in range(4)]
    for n in nodes: n.set_nodes(nodes)
    nodes[-1].become_coordinator(); nodes[-1].announce()
    nodes[-1].fail()
    nodes[1].start_election()
    print("Final coordinators:")
    for n in nodes:
        print(f"Node {n.node_id} alive={n.alive} coordinator={n.coordinator}")

if __name__ == "__main__":
    simulate()