import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8001/")

num1, num2 = 15, 7

result_add = proxy.add(num1,num2)
result_subtract = proxy.subtract(num1,num2)
result_multiply= proxy.multiply(num1,num2)

print(result_add, result_multiply, result_subtract)