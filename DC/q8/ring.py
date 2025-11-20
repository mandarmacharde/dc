class Node:
    def __init__(self, nid ):
        self.nid = nid
        self.next = None
        self.alive = True
    def set_next(self, nxt):
        self.next = nxt
    def fail(self):
        self.alive = False
        print(f"Node {self.nid} has failed")
    def initiate(self):
        print(f"Node {self.nid} initiates election")
        candidates = [self.nid]
        curr = self.next
        while curr != self:
            if curr.alive:
                candidates.append(curr.nid)
            curr = curr.next
        leader =  max(candidates)
        print(f"Ring election candidates: {candidates} -> leader {leader}")
        return leader
    
def simulate():
    N=5
    nodes = [Node(i+1) for i in range(N)]
    for i in range(N):
        nodes[i].set_next(nodes[(i+1)%N])
    nodes[-1].fail()
    leader = nodes[1].initiate()

if __name__ == "__main__":
    simulate()

        