import sys
import Pyro4
import re

listinstance = sys.argv[1]
listinstance = re.findall('(fs[1-9]+)', listinstance)
instances = []
for i in range(0, listinstance.__len__()):
    instances.append(listinstance[i])

p = None

for i in instances:
    p = Pyro4.Proxy("PYRONAME:{}@localhost:50001" . format(i))
    p.set_identifier(i)
    for j in instances:
        if i != j:
            q = Pyro4.Proxy("PYRONAME:{}@localhost:50001" . format(j))
            p.add_peer(q)