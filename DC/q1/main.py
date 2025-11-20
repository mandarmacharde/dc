import threading
import time

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.leader = None
        self.lamport = 0
        self.seq = 0
        self.accounts = {}
        self.active = True
        
    def tick(self, r=None):
        self.lamport = max(self.lamport, r if r else self.lamport) + 1
        return self.lamport
    
    def election(self, nodes):
        
        print(f"[Node {self.id}] Starting Election")
        higher = [n for n in nodes if n.id>self.id and n.active]
        
        if not higher:
            self.leader = self.id
            print(f"[Node {self.id} I AM LEADER NOW]")
            for n in nodes:
                n.leader = self.id
            return
        
        for h in higher:
            print(f"[Node {self.id} Sending election to {h.id}]")
            h.election(nodes)
            
    def apply(self, acc, op, amt):
        if acc not in self.accounts:
            self.accounts[acc] = 0
        if op=="deposit":
            self.accounts[acc]+=amt
        elif op=="withdraw" and self.accounts[acc] >= amt:
            self.accounts[acc] -=amt
            
    def transaction(self, nodes, acc, op, amt):
        self.tick()
        leader_node = [n for n in nodes if n.id==self.leader][0]
        
        if leader_node.id !=self.id:
            return leader_node.transaction(nodes, acc, op, amt)
        
        self.seq+=1
        print(f"[Leader {self.id} TXN seq={self.seq}: {acc} {op} {amt}]")
        
        # Apply to all nodes
        for n in nodes:
            n.apply(acc, op, amt)

        return "OK"

def heartbeat(nodes):
    while True:
        time.sleep(2)
        for n in nodes:
            if not n.active:
                continue
            if n.leader is None or not any(x.id == n.leader and x.active for x in nodes):
                print(f"[Node {n.id}] Leader dead → starting election")
                n.election(nodes)
                
                
nodes = [Node(1), Node(2), Node(3)]

threading.Thread(target=heartbeat,args=(nodes,),daemon=True).start()

nodes[0].election(nodes);
time.sleep(1)

nodes[0].transaction(nodes,"Alice",'deposit',500)

print("\nAccount Balances:")
for n in nodes:
    print(f"Node {n.id} → {n.accounts}")
    
nodes[2].active=False
time.sleep(3)



print("\n--- Transaction After New Leader ---")
nodes[1].transaction(nodes, "Alice", "withdraw", 50)

for n in nodes:
    print(f"Node {n.id} → {n.accounts}")