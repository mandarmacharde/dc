from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import threading

class ThreadedServer(ThreadingMixIn,SimpleXMLRPCServer):
    pass

def execute_code(code):
    try:
        allowed = {"__builtins__": {"sum": sum, "sorted": sorted, "len": len}}
        result = eval(code, allowed)
        print(result)
        return f"result: {result}"
    except Exception as e:
        return f"Error: {e}"
    
class RCEngine:
    def run(self, code):
        print(f"Executing: {code} (Thread: {threading.current_thread().name})")
        return execute_code(code)

if __name__ == "__main__":
    server = ThreadedServer(("127.0.0.1", 8000), allow_none=True)
    server.register_instance(RCEngine())

    print("Remote Code Execution Server Running on port 8000...")
    server.serve_forever()
