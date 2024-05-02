# MIT License
#
# Copyright (c) 2024 remipch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import drawsvg as draw
import math
from enum import Enum

class EdgeLayout(Enum):
    AUTO = 0
    VERTICAL = 1
    HORIZONTAL = 2

class Border(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

class Node:
    def __init__(self, chart, col, row, text, color="white", rounded=False):
        self.col = col
        self.row = row
        self.text = text
        self.color = color
        self.rounded = rounded
        self.edges = {Border.LEFT: [], Border.TOP: [], Border.RIGHT: [], Border.BOTTOM: []}

        self.chart = chart
        chart.addNode(self)
        print(F"New node '{text}'")

    def addEdge(self, border, angle, edge):
        self.edges[border].append((angle, edge))

        # Sort edges by angle
        self.edges[border] = sorted(self.edges[border], key=lambda x: x[0])

    def getEdgeCount(self, border):
        return len(self.edges[border])

    def getEdgeIndex(self, border, edge):
        for i, angle_and_edge in enumerate(self.edges[border]):
            if angle_and_edge[1] == edge:
                return i
        return None

    def getRect(self):
        return Rect((self.col * self.chart.horizontal_step) - self.chart.node_width/2,
                    (self.col * self.chart.horizontal_step) + self.chart.node_width/2,
                    (self.row * self.chart.vertical_step) - self.chart.node_height/2,
                    (self.row * self.chart.vertical_step) + self.chart.node_height/2)

    def draw(self, drawing):
        rx = self.chart.node_height/2 if self.rounded else 0
        rect = self.getRect()
        drawing.append(draw.Rectangle(rect.min_x,
                                      rect.min_y,
                                      rect.getWidth(),
                                      rect.getHeight(),
                                      fill=self.color,
                                      stroke='black',
                                      stroke_width=2,
                                      rx=rx))
        drawing.append(draw.Text(self.text,
                      self.chart.font_size,
                      self.col * self.chart.horizontal_step,
                      self.row * self.chart.vertical_step,
                      text_anchor='middle',
                      dominant_baseline='middle',
                      font_family='Arial'))


# edge_string format : [<]-[-][>]
def parseEdgeString(edge_string):
    node_a_arrow = edge_string.startswith("<")
    node_b_arrow = edge_string.endswith(">")
    dashed = "--" in edge_string

    return (dashed, node_a_arrow, node_b_arrow)

class Edge:
    def __init__(self, chart, node_a, node_b, edge_string="-", text="", color="black", layout=EdgeLayout.AUTO):
        assert(node_a is not None)
        assert(node_b is not None)
        (self.dashed, node_a_arrow, node_b_arrow) = parseEdgeString(edge_string)

        self.text = text
        self.color = color
        if layout==EdgeLayout.AUTO:
            # VERTICAL by default, fallback to HORIZONTAL only if nodes are on the same row
            if node_a.row == node_b.row:
                self.layout = EdgeLayout.HORIZONTAL
            else:
                self.layout = EdgeLayout.VERTICAL
        elif layout==EdgeLayout.VERTICAL:
            assert(node_a.row != node_b.row)
            self.layout = EdgeLayout.VERTICAL
        elif layout==EdgeLayout.HORIZONTAL:
            assert(node_a.col != node_b.col)
            self.layout = EdgeLayout.HORIZONTAL

        if self.layout == EdgeLayout.HORIZONTAL:
            if node_a.col < node_b.col:
                self.left_node = node_a
                self.right_node = node_b
                self.left_arrow = node_a_arrow
                self.right_arrow = node_b_arrow
            else:
                self.left_node = node_b
                self.right_node = node_a
                self.left_arrow = node_b_arrow
                self.right_arrow = node_a_arrow
            self.x1 = self.left_node.col * chart.horizontal_step + chart.node_width/2
            self.y1 = self.left_node.row * chart.vertical_step
            self.x2 = self.right_node.col * chart.horizontal_step - chart.node_width/2
            self.y2 = self.right_node.row * chart.vertical_step
            edge_angle = math.atan2(self.y2 - self.y1, self.x2 - self.x1)
            self.left_node.addEdge(Border.RIGHT, edge_angle, self)
            self.right_node.addEdge(Border.LEFT, -edge_angle, self)
        elif self.layout==EdgeLayout.VERTICAL:
            if node_a.row < node_b.row:
                self.top_node = node_a
                self.bottom_node = node_b
                self.top_arrow = node_a_arrow
                self.bottom_arrow = node_b_arrow
            else:
                self.top_node = node_b
                self.bottom_node = node_a
                self.top_arrow = node_b_arrow
                self.bottom_arrow = node_a_arrow
            self.x1 = self.top_node.col * chart.horizontal_step
            self.y1 = self.top_node.row * chart.vertical_step + chart.node_height/2
            self.x2 = self.bottom_node.col * chart.horizontal_step
            self.y2 = self.bottom_node.row * chart.vertical_step - chart.node_height/2
            edge_angle = math.atan2(self.y2 - self.y1, self.x2 - self.x1)
            self.top_node.addEdge(Border.BOTTOM, -edge_angle, self)
            self.bottom_node.addEdge(Border.TOP, edge_angle, self)

        self.chart = chart
        chart.addEdge(self)
        print(F"New edge '{text}' : '{node_a.text}' '{edge_string}' '{node_b.text}'")

    def draw(self, drawing):
        if self.layout == EdgeLayout.HORIZONTAL:
            dy_left = self.chart.node_height * (self.left_node.getEdgeIndex(Border.RIGHT, self) + 1) / (self.left_node.getEdgeCount(Border.RIGHT) + 1) - self.chart.node_height / 2
            dy_right = self.chart.node_height * (self.right_node.getEdgeIndex(Border.LEFT, self) + 1) / (self.right_node.getEdgeCount(Border.LEFT) + 1) - self.chart.node_height / 2

            x1 = self.x1
            y1 = self.y1 + dy_left
            x2 = self.x2
            y2 = self.y2 + dy_right
            origin_arrow = self.left_arrow
            destination_arrow = self.right_arrow

        elif self.layout==EdgeLayout.VERTICAL:
            dx_top = self.chart.node_width * (self.top_node.getEdgeIndex(Border.BOTTOM, self) + 1) / (self.top_node.getEdgeCount(Border.BOTTOM) + 1) - self.chart.node_width / 2
            dx_bottom = self.chart.node_width * (self.bottom_node.getEdgeIndex(Border.TOP, self) + 1) / (self.bottom_node.getEdgeCount(Border.TOP) + 1) - self.chart.node_width / 2

            x1 = self.x1 + dx_top
            y1 = self.y1
            x2 = self.x2 + dx_bottom
            y2 = self.y2
            origin_arrow = self.top_arrow
            destination_arrow = self.bottom_arrow

        arrow = draw.Marker(-9, -5, 2, 5, orient='auto-start-reverse')
        arrow.append(draw.Lines(-9, 3, -9, -3, 2, 0, fill=self.color, close=True))

        drawing.append(draw.Line(x1, y1, x2, y2,
                                 stroke=self.color,
                                 stroke_width=2,
                                 stroke_dasharray="7,4" if self.dashed else None,
                                 fill='none',
                                 marker_start=arrow if origin_arrow else None,
                                 marker_end=arrow if destination_arrow else None))
        drawing.append(draw.Text(self.text,
                                 self.chart.font_size,
                                 (x1 + x2) / 2,
                                 (y1 + y2) / 2,
                                 text_anchor='middle',
                                 dominant_baseline='middle',
                                 font_family='Arial',
                                 fill='white',
                                 stroke='white',
                                 stroke_width=4))
        drawing.append(draw.Text(self.text,
                                 self.chart.font_size,
                                 (x1 + x2) / 2,
                                 (y1 + y2) / 2,
                                 text_anchor='middle',
                                 dominant_baseline='middle',
                                 font_family='Arial',
                                 fill=self.color))

class Cluster:
    # Warning: nodes append order defines the paint order (last nodes will hide first ones)
    def __init__(self, chart, nodes, text="", margin_x=15, margin_y=15, color="none", rounded=False):
        assert(len(nodes)>0)
        self.nodes = nodes
        self.text = text
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.color = color
        self.rounded = rounded

        self.chart = chart
        chart.addCluster(self)
        print(F"New cluster '{text}'")

    def getRect(self):
        englobing_rect = Rect(math.inf,-math.inf,math.inf,-math.inf)
        for node in self.nodes:
            englobing_rect.englobe(node.getRect())
        englobing_rect.enlarge(self.margin_x, self.margin_y)
        return englobing_rect

    def draw(self, drawing):
        englobing_rect = self.getRect()

        rx = self.chart.node_height/2 if self.rounded else 0
        drawing.append(draw.Rectangle(englobing_rect.min_x,
                                      englobing_rect.min_y,
                                      englobing_rect.getWidth(),
                                      englobing_rect.getHeight(),
                                      fill=self.color,
                                      stroke='black',
                                      stroke_width=2,
                                      rx=rx))

        drawing.append(draw.Text(self.text,
                                 self.chart.font_size,
                                 englobing_rect.min_x,
                                 englobing_rect.min_y,
                                 text_anchor='start',
                                 dominant_baseline='text-after-edge',
                                 font_family='Arial',
                                 font_weight='bold'))

class Rect:
    def __init__(self, min_x, max_x, min_y, max_y):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def enlarge(self, margin_x, margin_y):
        self.min_x = self.min_x - margin_x
        self.max_x = self.max_x + margin_x
        self.min_y = self.min_y - margin_y
        self.max_y = self.max_y + margin_y

    def englobe(self, other):
        self.min_x = min(self.min_x, other.min_x)
        self.max_x = max(self.max_x, other.max_x)
        self.min_y = min(self.min_y, other.min_y)
        self.max_y = max(self.max_y, other.max_y)

    def getWidth(self):
        return self.max_x - self.min_x

    def getHeight(self):
        return self.max_y - self.min_y

class Chart:
    def __init__(self,
                 font_size = 20,
                 node_width = 150,
                 node_height = 40,
                 horizontal_node_space = 50,
                 vertical_node_space = 30):
        self.font_size  = font_size
        self.node_width  = node_width
        self.node_height  = node_height
        self.horizontal_node_space  = horizontal_node_space
        self.vertical_node_space  = vertical_node_space

        self.all_nodes = []
        self.all_edges = []
        self.all_clusters = []

        self.horizontal_step = node_width + horizontal_node_space
        self.vertical_step = node_height + vertical_node_space

        print(F"New chart")

    def addNode(self, node):
        self.all_nodes.append(node)

    def addEdge(self, edge):
        self.all_edges.append(edge)

    def addCluster(self, cluster):
        self.all_clusters.append(cluster)

    def exportSvg(self, filename):
        # Compute drawing size by iterating all nodes and clusters
        englobing_rect = Rect(math.inf,-math.inf,math.inf,-math.inf)
        for node in self.all_nodes:
            englobing_rect.englobe(node.getRect())
        for cluster in self.all_clusters:
            englobing_rect.englobe(cluster.getRect())
        englobing_rect.enlarge(self.horizontal_node_space, self.vertical_node_space)
        print(F"Chart englobing_rect: {englobing_rect.min_x},{englobing_rect.max_x},{englobing_rect.min_y},{englobing_rect.max_y} ")

        # Create a new drawing
        d = draw.Drawing(englobing_rect.max_x-englobing_rect.min_x,
                         englobing_rect.max_y-englobing_rect.min_y,
                         origin=(englobing_rect.min_x,englobing_rect.min_y))

        # Draw englobing white rect
        d.append(draw.Rectangle(englobing_rect.min_x,
                                      englobing_rect.min_y,
                                      englobing_rect.getWidth(),
                                      englobing_rect.getHeight(),
                                      fill='white',
                                      stroke='none'))

        # Draw all elements
        for cluster in self.all_clusters:
            cluster.draw(d)
        for edge in self.all_edges:
            edge.draw(d)
        for node in self.all_nodes:
            node.draw(d)

        # Finally save
        d.save_svg(filename)
