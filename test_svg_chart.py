from svg_chart import *


chart = Chart(node_width = 150, name="test_chart")

o = chart.add(Node(0,0,"Origin node"))

a = chart.add(Node(1,5,"A",rounded=True))

b = chart.add(Node(2,3,"This is node B", color="#d9ffe4"))

chart.add(Edge(o,b,"r->t0.1", "r->t0.1", color="green"))

chart.add(Edge(o,a,"b-->l", "b-->l",color="cyan"))

chart.add(Edge(b,a,"b<-->t0.9","b<-->t0.9",color="#97a1ff"))

chart.exportSvg("output.svg")
