import threading, time

class Replica:
    
    def __init__(self,name):
        self.name = name;
        self.store={}
    def put(self, k, v):
        self.store[k]=v
        print(f"[{self.name}] PUT {k}={v}")
    def get(self, k):
        return self.store[k]
    def merge_from(self, other):
        for k,v in other.store.items():
            self.store[k] = v
        print(f"[{self.name}] merged from {other.name}")
        
        
def simulate():
    r1, r2, r3 = Replica('r1'), Replica('r2'), Replica('r3')
    for r in (r1,r2,r3):
        r.put("x","1")
    r2.put("x","2")
    print("Immediate reads:", r1.get("x"), r2.get("x"), r3.get("x"))
    def propagate():
        time.sleep(1.0)
        r1.merge_from(r2)
        r3.merge_from(r2)
        print("After propagation reads:", r1.get("x"), r2.get("x"), r3.get("x"))
    threading.Thread(target=propagate).start()
    

if __name__ == "__main__":
    simulate()
    time.sleep(2.0)

        