def show(name, vc):
    print(f"{name}: {vc}")
    
class Proc:
    def __init__(self, pid, n):
        self.pid = pid
        self.n = n
        self.vc = [0]*n
    def internal(self):
        self.vc[self.pid]+=1
        show(f"P{self.pid} internal", self.vc)
    def send(self):
        self.vc[self.pid]+=1
        show(f"P{self.pid} send", self.vc)
        return list(self.vc)
    def receive(self, msg_vc, from_pid):
        self.vc = [max(self.vc[i], msg_vc[i]) for i in range(self.n)]
        self.vc[self.pid] += 1
        show(f"P{self.pid} recv from P{from_pid}", self.vc)
    
    

def main():
    n=3
    p = [Proc(i,n) for i in range(n)]
    p[0].internal()
    m1 = p[0].send()
    p[1].receive(m1, 0)
    p[2].internal()
    m2 = p[1].send()
    p[2].receive(m2,1)
    m3 = p[2].send()
    p[0].receive(m3,2)

if __name__ == "__main__":
    main()
