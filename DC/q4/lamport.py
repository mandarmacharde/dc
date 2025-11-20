import threading, time, random, queue

class LogEvent:
    def __init__(self, server_id, local_ts, msg, lamport):
        self.server_id = server_id
        self.local_ts = local_ts
        self.msg = msg
        self.lamport = lamport
        
    def __repr__(self):
         return f"[S{self.server_id} local={self.local_ts} L={self.lamport}] {self.msg}"

class Server(threading.Thread):
    global_lamport = 0
    global_lock = threading.Lock()
    def __init__(self, sid, outq):
        super().__init__(daemon=True)
        self.sid = sid
        self.outq = outq
        self.local = 0
    def run(self):
        for i in range(6):
            time.sleep(0.1 + random.random()*0.2)
            self.local += 1
            with Server.global_lock:
                Server.global_lamport += 1
                L = Server.global_lamport
            e = LogEvent(self.sid, self.local, f"event-{i}", L)
            self.outq.put(e)
            print(f"[S{self.sid}] generated {e}")
            
            
            
def central_collector(outq, total):
    collected = []
    while len(collected) < total:
        try:
            e = outq.get(timeout=1)
            collected.append(e)
        except:
            pass
    collected.sort(key=lambda x: (x.lamport, x.server_id))
    print("\nCentralized logs ordered by Lamport:")
    for e in collected:
        print(e)

def main():
    N=3
    outq = queue.Queue()
    servers = [Server(i+1, outq) for i in range(N)]
    for s in servers: s.start()
    central_collector(outq, N*6)

if __name__ == "__main__":
    main()

        
        