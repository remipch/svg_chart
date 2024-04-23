from svg_chart import *


chart = Chart(node_width = 150, name="test_chart")

o = chart.add(Node(0,0,"Origin node"))

a = chart.add(Node(1,2,"A"))

b = chart.add(Node(2,2,"This is node B", color="#d9ffe4"))

chart.add(Edge(o,a,"->",color="green"))

chart.exportSvg("output.svg")
