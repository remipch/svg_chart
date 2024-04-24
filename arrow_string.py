from enum import Enum
import unittest

class AnchorBorder(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

def toAnchorBorder(char):
    if char == "l" or char=="L":
        return AnchorBorder.LEFT
    elif char == "r" or char=="R":
        return AnchorBorder.RIGHT
    elif char == "t" or char=="T":
        return AnchorBorder.TOP
    elif char == "b" or char=="B":
        return AnchorBorder.BOTTOM
    else:
        raise ValueError("Unknown arrow anchor border")

def parseArrowString(arrow_string):
    parts = arrow_string.split("-")

    # Line dash depends on the number of '-' :
    # one '-' means plain line
    # two '-' means dashed line
    # other are incorrect
    if len(parts)==2:
        dashed=False
    elif len(parts)==3:
        dashed=True
    else:
        print(F"Incorrect arrow_string")
        print(F"parts: '{parts}'")
        return None

    origin_arrow_string = parts[0]
    destination_arrow_string = parts[-1]

    # '<' before '-' and '>' after '-' define the arrows at the origin or destination
    origin_arrow = origin_arrow_string.endswith("<")
    if origin_arrow:
        origin_arrow_string = origin_arrow_string[:-1]
    destination_arrow = destination_arrow_string.startswith(">")
    if destination_arrow:
        destination_arrow_string = destination_arrow_string[1:]

    # 'l', 'r', 't', 'b', define the anchor border
    origin_anchor_border = toAnchorBorder(origin_arrow_string[0])
    destination_anchor_border = toAnchorBorder(destination_arrow_string[0])
    origin_arrow_string = origin_arrow_string[1:]
    destination_arrow_string = destination_arrow_string[1:]

    # The remaining number defines the relative position on the border
    if len(origin_arrow_string)==0:
        origin_arrow_position = 0.5
    else:
        origin_arrow_position = float(origin_arrow_string)

    if len(destination_arrow_string)==0:
        destination_arrow_position = 0.5
    else:
        destination_arrow_position = float(destination_arrow_string)

    return {
        'dashed': dashed,
        'origin_arrow': origin_arrow,
        'origin_anchor_border': origin_anchor_border,
        'origin_arrow_position': origin_arrow_position,
        'destination_arrow': destination_arrow,
        'destination_anchor_border': destination_anchor_border,
        'destination_arrow_position': destination_arrow_position,
    }



class TestParseArrowString(unittest.TestCase):
    def test_plain_line_with_one_arrow(self):
        self.assertEqual(
            parseArrowString("l->t"),
            {
                'stroke_dasharray': "1",
                'origin_arrow': False,
                'origin_anchor_border': AnchorBorder.LEFT,
                'origin_arrow_position': 0.5,
                'destination_arrow': True,
                'destination_anchor_border': AnchorBorder.TOP,
                'destination_arrow_position': 0.5,
            })

    def test_dashed_line_without_arrow(self):
        self.assertEqual(
            parseArrowString("t-->r0.3"),
            {
                'stroke_dasharray': "9,5",
                'origin_arrow': False,
                'origin_anchor_border': AnchorBorder.TOP,
                'origin_arrow_position': 0.5,
                'destination_arrow': True,
                'destination_anchor_border': AnchorBorder.RIGHT,
                'destination_arrow_position': 0.3,
            })

    def test_plain_line_with_two_arrows(self):
        self.assertEqual(
            parseArrowString("b0<->l"),
            {
                'stroke_dasharray': "1",
                'origin_arrow': True,
                'origin_anchor_border': AnchorBorder.BOTTOM,
                'origin_arrow_position': 0,
                'destination_arrow': True,
                'destination_anchor_border': AnchorBorder.LEFT,
                'destination_arrow_position': 0.5,
            })

if __name__ == '__main__':
    unittest.main()
