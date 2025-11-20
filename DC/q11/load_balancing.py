import threading, time
from collections import deque



class Backend:
    def __init__(self, name):
        self.name = name
        self.conns = 0
        self.lock = threading.Lock()
    def handle(self, req):
        with self.lock:
            self.conns += 1
            cur = self.conns
        print(f"[{self.name}] handling {req} (conns={cur})")
        time.sleep(0.2)
        with self.lock:
            self.conns -= 1
            

def round_robin(backends, requests):
    q = deque(backends)
    for req in requests:
        b = q[0]; q.rotate(-1)
        threading.Thread(target=b.handle, args=(req,), daemon=True).start()
        time.sleep(0.05)


def least_connections(backends, requests):
    for req in requests:
        b = min(backends, key=lambda x: x.conns)
        threading.Thread(target=b.handle, args=(req,), daemon=True).start()
        time.sleep(0.05)
        
        

def simulate():
    backends = [Backend("B1"), Backend("B2"), Backend("B3")]
    reqs = [f"req{i}" for i in range(9)]
    print("=== Round Robin ===")
    round_robin(backends, reqs)
    time.sleep(2)
    print("\n=== Least Connections ===")
    least_connections(backends, reqs)
    time.sleep(2)

if __name__ == "__main__":
    simulate()
