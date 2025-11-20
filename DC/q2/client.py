from xmlrpc.client import ServerProxy

server = ServerProxy("http://127.0.0.1:8000/")

print("Remote Code Execution")


while True:
    code = input("\nEnter a task to execute (or 'exit'): ")

    if code == "exit":
        break

    result = server.run(code)
    print("Server Response:", result)