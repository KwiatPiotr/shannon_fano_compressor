s = b''.join([bytes([i]) for i in range(255)])
f = open('test_bytes', 'wb')

f.write(s)
f.close()

