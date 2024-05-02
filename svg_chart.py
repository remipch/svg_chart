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

class EdgeShape(Enum):
    STRAIGHT = 0
    CURVE_BEFORE= 1
    CURVE_BETWEEN= 2
    CURVE_AFTER= 3

class Border(Enum):
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3

class Node:
    def __init__(self, chart, col, row, text="", color="white", rounded=False):
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

    def getBorderCenter(self, border):
        if border==Border.LEFT:
            return (self.col * self.chart.horizontal_step - self.chart.node_width/2, self.row * self.chart.vertical_step)
        if border==Border.TOP:
            return (self.col * self.chart.horizontal_step, self.row * self.chart.vertical_step - self.chart.node_height/2)
        if border==Border.RIGHT:
            return (self.col * self.chart.horizontal_step + self.chart.node_width/2, self.row * self.chart.vertical_step)
        if border==Border.BOTTOM:
            return (self.col * self.chart.horizontal_step, self.row * self.chart.vertical_step + self.chart.node_height/2)

    def getEdgePointOnBorder(self, border, edge):
        (x, y) = self.getBorderCenter(border)
        if border==Border.LEFT:
            y = y + (self.chart.node_height / 2) - (self.chart.node_height * (self.getEdgeIndex(border, edge) + 1) / (self.getEdgeCount(border) + 1))
        if border==Border.TOP:
            x = x + self.chart.node_width * (self.getEdgeIndex(border, edge) + 1) / (self.getEdgeCount(border) + 1) - self.chart.node_width / 2
        if border==Border.RIGHT:
            y = y + self.chart.node_height * (self.getEdgeIndex(border, edge) + 1) / (self.getEdgeCount(border) + 1) - self.chart.node_height / 2
        if border==Border.BOTTOM:
            x = x + (self.chart.node_width / 2) - (self.chart.node_width * (self.getEdgeIndex(border, edge) + 1) / (self.getEdgeCount(border) + 1))

        return (x, y)

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

        if self.text != "":
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
    def __init__(self, chart, node_a, node_b, edge_string="-", text="", color="black", layout=EdgeLayout.AUTO, shape=EdgeShape.STRAIGHT):
        assert(node_a is not None)
        assert(node_b is not None)
        (self.dashed, node_a_arrow, node_b_arrow) = parseEdgeString(edge_string)

        self.text = text
        self.color = color
        self.layout = layout
        self.shape = shape
        if layout==EdgeLayout.AUTO:
            self.shape = EdgeShape.STRAIGHT
            # VERTICAL by default, fallback to HORIZONTAL only if nodes are on the same row
            if node_a.row == node_b.row:
                self.layout = EdgeLayout.HORIZONTAL
            else:
                self.layout = EdgeLayout.VERTICAL
        if layout==EdgeLayout.VERTICAL and shape==EdgeShape.STRAIGHT:
            assert(node_a.row != node_b.row)
        if layout==EdgeLayout.HORIZONTAL and shape==EdgeShape.STRAIGHT:
            assert(node_a.col != node_b.col)

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
            if shape==EdgeShape.STRAIGHT or shape==EdgeShape.CURVE_BETWEEN:
                self.left_node_border = Border.RIGHT
                self.right_node_border = Border.LEFT
            elif shape==EdgeShape.CURVE_BEFORE:
                self.left_node_border = Border.LEFT
                self.right_node_border = Border.LEFT
            elif shape==EdgeShape.CURVE_AFTER:
                self.left_node_border = Border.RIGHT
                self.right_node_border = Border.RIGHT
            (self.left_node_x, self.left_node_y) = self.left_node.getBorderCenter(self.left_node_border)
            (self.right_node_x, self.right_node_y) = self.right_node.getBorderCenter(self.right_node_border)
            self.yc = (self.left_node_y + self.right_node_y) / 2
            if shape==EdgeShape.STRAIGHT or shape==EdgeShape.CURVE_BETWEEN:
                self.xc = (self.left_node_x + self.right_node_x) / 2
            elif shape==EdgeShape.CURVE_BEFORE:
                self.xc = self.left_node_x  - abs(self.left_node_y - self.right_node_y)/2
            elif shape==EdgeShape.CURVE_AFTER:
                self.xc = self.right_node_x  + abs(self.left_node_y - self.right_node_y)/2

            # WARNING: using only edge slope leads to incorrect edge ordering on border in case of multiple curved edges on the same border
            left_node_edge_slope = (self.left_node_y - self.yc) / (self.left_node_x - self.xc)
            self.left_node.addEdge(self.left_node_border, left_node_edge_slope, self)
            right_node_edge_slope = (self.right_node_y - self.yc) / (self.right_node_x - self.xc)
            self.right_node.addEdge(self.right_node_border, right_node_edge_slope, self)

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
            if shape==EdgeShape.STRAIGHT or shape==EdgeShape.CURVE_BETWEEN:
                self.top_node_border = Border.BOTTOM
                self.bottom_node_border = Border.TOP
            elif shape==EdgeShape.CURVE_BEFORE:
                self.top_node_border = Border.TOP
                self.bottom_node_border = Border.TOP
            elif shape==EdgeShape.CURVE_AFTER:
                self.top_node_border = Border.BOTTOM
                self.bottom_node_border = Border.BOTTOM
            (self.top_node_x, self.top_node_y) = self.top_node.getBorderCenter(self.top_node_border)
            (self.bottom_node_x, self.bottom_node_y) = self.bottom_node.getBorderCenter(self.bottom_node_border)
            self.xc = (self.top_node_x + self.bottom_node_x) / 2
            if shape==EdgeShape.STRAIGHT or shape==EdgeShape.CURVE_BETWEEN:
                self.yc = (self.top_node_y + self.bottom_node_y) / 2
            elif shape==EdgeShape.CURVE_BEFORE:
                self.yc = self.top_node_y  - abs(self.top_node_x - self.bottom_node_x)/4
            elif shape==EdgeShape.CURVE_AFTER:
                self.yc = self.bottom_node_y  + abs(self.top_node_x - self.bottom_node_x)/4

            top_node_edge_angle = math.atan2(self.top_node_y - self.yc, self.top_node_x - self.xc)
            self.top_node.addEdge(self.top_node_border, top_node_edge_angle, self)
            bottom_node_edge_angle = math.atan2(self.bottom_node_y - self.yc, self.bottom_node_x - self.xc)
            self.bottom_node.addEdge(self.bottom_node_border, bottom_node_edge_angle, self)

        self.chart = chart
        chart.addEdge(self)
        print(F"New edge '{text}' : '{node_a.text}' '{edge_string}' '{node_b.text}'")

    def getRect(self):
        if self.layout == EdgeLayout.HORIZONTAL:
            (x1, y1) = self.left_node.getEdgePointOnBorder(self.left_node_border, self)
            (x2, y2) = self.right_node.getEdgePointOnBorder(self.right_node_border, self)
        elif self.layout==EdgeLayout.VERTICAL:
            (x1, y1) = self.top_node.getEdgePointOnBorder(self.top_node_border, self)
            (x2, y2) = self.bottom_node.getEdgePointOnBorder(self.bottom_node_border, self)

        return Rect(min(x1,self.xc,x2), max(x1,self.xc,x2), min(y1,self.yc,y2), max(y1,self.yc,y2))

    def draw(self, drawing):
        arrow_length = 8
        arrow = draw.Marker(-arrow_length, -5, 2, 5, orient='auto-start-reverse')
        arrow.append(draw.Lines(-arrow_length, 3, -arrow_length, -3, 2, 0, fill=self.color, close=True))

        if self.layout == EdgeLayout.HORIZONTAL:
            (x1, y1) = self.left_node.getEdgePointOnBorder(self.left_node_border, self)
            (x2, y2) = self.right_node.getEdgePointOnBorder(self.right_node_border, self)
            origin_arrow = self.left_arrow
            destination_arrow = self.right_arrow

        elif self.layout==EdgeLayout.VERTICAL:
            (x1, y1) = self.top_node.getEdgePointOnBorder(self.top_node_border, self)
            (x2, y2) = self.bottom_node.getEdgePointOnBorder(self.bottom_node_border, self)
            origin_arrow = self.top_arrow
            destination_arrow = self.bottom_arrow

        if self.shape==EdgeShape.STRAIGHT:
            # Recompute center with actual edge border points
            self.xc = (x1+x2)/2
            self.yc = (y1+y2)/2
            drawing.append(draw.Line(x1, y1, x2, y2,
                                     stroke=self.color,
                                     stroke_width=2,
                                     stroke_dasharray="7,4" if self.dashed else None,
                                     fill='none',
                                     marker_start=arrow if origin_arrow else None,
                                     marker_end=arrow if destination_arrow else None))

        else:
            path = draw.Path(stroke=self.color,
                             stroke_width=2,
                             stroke_dasharray="7,4" if self.dashed else None,
                             fill='none',
                             marker_start=arrow if origin_arrow else None,
                             marker_end=arrow if destination_arrow else None)
            if self.layout == EdgeLayout.HORIZONTAL:
                if self.shape==EdgeShape.CURVE_BEFORE:
                    drawing.append(path.M(x1, y1).L(x1-arrow_length, y1).Q(self.xc, y1, self.xc, self.yc).Q(self.xc, y2, x1-arrow_length, y2).L(x2, y2))
                elif self.shape==EdgeShape.CURVE_BETWEEN:
                    drawing.append(path.M(x1, y1).L(x1+arrow_length, y1).Q(self.xc, y1, self.xc, self.yc).Q(self.xc, y2, x2-arrow_length, y2).L(x2, y2))
                elif self.shape==EdgeShape.CURVE_AFTER:
                    drawing.append(path.M(x1, y1).L(x2+arrow_length, y1).Q(self.xc, y1, self.xc, self.yc).Q(self.xc, y2, x2+arrow_length, y2).L(x2, y2))
            else:
                if self.shape==EdgeShape.CURVE_BEFORE:
                    drawing.append(path.M(x1, y1).L(x1, y1-arrow_length).Q(x1, self.yc, self.xc, self.yc).Q(x2, self.yc, x2, y1-arrow_length).L(x2, y2))
                elif self.shape==EdgeShape.CURVE_BETWEEN:
                    drawing.append(path.M(x1, y1).L(x1, y1+arrow_length).Q(x1, self.yc, self.xc, self.yc).Q(x2, self.yc, x2, y2-arrow_length).L(x2, y2))
                elif self.shape==EdgeShape.CURVE_AFTER:
                    drawing.append(path.M(x1, y1).L(x1, y2+arrow_length).Q(x1, self.yc, self.xc, self.yc).Q(x2, self.yc, x2, y2+arrow_length).L(x2, y2))

        if self.text == "":
            return

        drawing.append(draw.Text(self.text,
                                 self.chart.font_size,
                                 self.xc,
                                 self.yc,
                                 text_anchor='middle',
                                 dominant_baseline='middle',
                                 font_family='Arial',
                                 fill='white',
                                 stroke='white',
                                 stroke_width=4))
        drawing.append(draw.Text(self.text,
                                 self.chart.font_size,
                                 self.xc,
                                 self.yc,
                                 text_anchor='middle',
                                 dominant_baseline='middle',
                                 font_family='Arial',
                                 fill=self.color))

class Cluster:
    def __init__(self, chart, children, text="", color="none", rounded=False):
        assert(len(children)>0)
        self.children = children
        self.text = text
        self.color = color
        self.rounded = rounded

        self.chart = chart
        chart.addCluster(self)
        print(F"New cluster '{text}'")

    def getRect(self):
        englobing_rect = Rect(math.inf,-math.inf,math.inf,-math.inf)
        for child in self.children:
            englobing_rect.englobe(child.getRect())
        top_margin = self.chart.cluster_margin
        if self.text!="":
            top_margin = top_margin + self.chart.font_size
        englobing_rect.enlarge(self.chart.cluster_margin, top_margin, self.chart.cluster_margin, self.chart.cluster_margin)
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

    def enlarge(self, left, top, right, bottom):
        self.min_x = self.min_x - left
        self.max_x = self.max_x + right
        self.min_y = self.min_y - top
        self.max_y = self.max_y + bottom

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
                 vertical_node_space = 30,
                 cluster_margin = 15):
        self.font_size  = font_size
        self.node_width  = node_width
        self.node_height  = node_height
        self.horizontal_node_space  = horizontal_node_space
        self.vertical_node_space  = vertical_node_space
        self.cluster_margin  = cluster_margin

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
        for child in self.all_clusters+self.all_edges+self.all_nodes:
            englobing_rect.englobe(child.getRect())
        englobing_rect.enlarge(self.horizontal_node_space, self.vertical_node_space, self.horizontal_node_space, self.vertical_node_space)
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

        # Draw all elements (order is important to not hide children by their parent elements)
        for cluster in self.all_clusters:
            cluster.draw(d)
        for edge in self.all_edges:
            edge.draw(d)
        for node in self.all_nodes:
            node.draw(d)

        # Finally save
        d.save_svg(filename)
