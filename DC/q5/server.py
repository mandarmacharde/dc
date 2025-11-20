from xmlrpc.server import SimpleXMLRPCServer

def add(a,b):
    return a+b
def subtract(a,b):
    return a-b
def multiply(a,b):
    return a*b


server = SimpleXMLRPCServer(("localhost", 8001))
server.register_introspection_functions()

server.register_function(add, 'add')
server.register_function(subtract,'subtract')
server.register_function(multiply,'multiply')

server.serve_forever()