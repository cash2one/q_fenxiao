__author__ = 'binpo'
import Queue
q = Queue.Queue(maxsize = 10)

print dir(q)
a={'id':10,'name':20,'tt':30}
for i in xrange(20):
    q.put_nowait(a)
print q.qsize()
