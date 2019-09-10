UL_CORNER_RECT = [[0, 0], [150, 100]]
LL_CORNER_RECT = [[0, 140], [150, 240]]
UR_CORNER_RECT = [[170, 0], [320, 100]]
LR_CORNER_RECT = [[170, 140], [320, 240]]

corners = {
    'UL': UL_CORNER_RECT,
    'LL': LL_CORNER_RECT,
    'UR': UR_CORNER_RECT,
    'LR': LR_CORNER_RECT
}

import cv2

def draw_bounds(frame):
    cv2.rectangle(frame, tuple(UL_CORNER_RECT[0]), tuple(UL_CORNER_RECT[1]), (255, 0, 0), 1)
    cv2.rectangle(frame, tuple(LL_CORNER_RECT[0]), tuple(LL_CORNER_RECT[1]), (255, 0, 0), 1)
    cv2.rectangle(frame, tuple(UR_CORNER_RECT[0]), tuple(UR_CORNER_RECT[1]), (255, 0, 0), 1)
    cv2.rectangle(frame, tuple(LR_CORNER_RECT[0]), tuple(LR_CORNER_RECT[1]), (255, 0, 0), 1)

def in_bounds(midpoint, cmds):
    x, y = midpoint
    for cmd_name, cmd in cmds.items():
        corner_bounds = cmd.box
        if corner_bounds:
            if corner_bounds[0][0] <= x <= corner_bounds[1][0] and \
                corner_bounds[0][1] <= y <= corner_bounds[1][1]:
                    return cmd_name
    return None
