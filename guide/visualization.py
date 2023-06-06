
from cube import palette
from guide import status

import cv2


#------------------------------------------------------------------------------
# Printer
#------------------------------------------------------------------------------

class printer:
    _actions = {
        status.ACTION_NONE : "NONE",

        status.ACTION_MOVE_MX : "Rotate the cube away from you",
        status.ACTION_MOVE_PX : "Rotate the cube towards you",
        status.ACTION_MOVE_MY : "Rotate the cube to the left",
        status.ACTION_MOVE_PY : "Rotate the cube to the right",
        status.ACTION_MOVE_MZ : "Rotate the cube clockwise",
        status.ACTION_MOVE_PZ : "Rotate the cube counterclockwise",

        status.ACTION_TURN_MU : "Turn the top layer a quarter turn to the left",
        status.ACTION_TURN_PU : "Turn the top layer a quarter turn to the right",
        status.ACTION_TURN_MR : "Turn the right side a quarter turn away from you",
        status.ACTION_TURN_PR : "Turn the right side a quarter turn towards you",
        status.ACTION_TURN_MF : "Turn the front side a quarter turn to the right",
        status.ACTION_TURN_PF : "Turn the front side a quarter turn to the left",
        status.ACTION_TURN_MD : "Turn the bottom layer a quarter turn to the right",
        status.ACTION_TURN_PD : "Turn the bottom layer a quarter turn to the left",
        status.ACTION_TURN_ML : "Turn the left side a quarter turn towards you",
        status.ACTION_TURN_PL : "Turn the left side a quarter turn away from you",
        status.ACTION_TURN_MB : "TURN_MB",
        status.ACTION_TURN_PB : "TURN_PB",

        status.ACTION_INVALID : "INVALID",

        status.ACTION_ASK_WHITE  : "Show me the side with the white center",
        status.ACTION_ASK_RED    : "Show me the side with the red center",
        status.ACTION_ASK_GREEN  : "Show me the side with the green center",
        status.ACTION_ASK_YELLOW : "Show me the side with the yellow center",
        status.ACTION_ASK_ORANGE : "Show me the side with the orange center",
        status.ACTION_ASK_BLUE   : "Show me the side with the blue center",
    }

    _warn_top = {
        status.WARN_NONE : "",

        status.WARN_TOP_WHITE : "Make sure the side with the white center is up!",
        status.WARN_TOP_BLUE  : "Make sure the side with the blue center is up!",
        status.WARN_TOP_GREEN : "Make sure the side with the green center is up!",
    }

    _warn_extended = {
        status.WARN_NONE : "",

        status.WARN_MISMATCH_WHITE  : "The center looks white. Do you want to SCAN anyway?",
        status.WARN_MISMATCH_RED    : "The center looks red. Do you want to SCAN anyway?",
        status.WARN_MISMATCH_GREEN  : "The center looks green. Do you want to SCAN anyway?",
        status.WARN_MISMATCH_YELLOW : "The center looks yellow. Do you want to SCAN anyway?",
        status.WARN_MISMATCH_ORANGE : "The center looks orange. Do you want to SCAN anyway?",
        status.WARN_MISMATCH_BLUE   : "The center looks blue. Do you want to SCAN anyway?",

        status.WARN_SEEN_WHITE  : "I've scanned the white side.",
        status.WARN_SEEN_RED    : "I've scanned the red side.",
        status.WARN_SEEN_GREEN  : "I've scanned the green side.",
        status.WARN_SEEN_YELLOW : "I've scanned the yellow side.",
        status.WARN_SEEN_ORANGE : "I've scanned the orange side.",
        status.WARN_SEEN_BLUE   : "I've scanned the blue side.",
    }

    @staticmethod
    def split_text(text):
        return text.split("<br>")
    
    @staticmethod
    def trim_text(lines):
        return [line for line in lines if (line and not line.isspace())]

    @staticmethod
    def build_caption(top_state, state, step_index, step_count, action, warn, detected, auto_scan):
        if (top_state == 7):
            return "Say HELLO to start!<br> <br> <br> <br> "
        if (top_state == 0):
            return "Hello, I'm MARCuS.<br>My purpose is to help you solve rubik's cubes.<br>Grab a rubik's cube and settle in.<br>Let me know when you're READY to begin.<br> "
        if (top_state == 1):
            return "We're going to scan the cube now.<br>Hold the cube so the side with the white center is up<br>and the side with the red center is facing you.<br>Tell me when you're READY!<br> "
        if (top_state == 3 and state == 1):
            return "Scan complete! Now, we'll solve this cube together.<br>I'll be quiet while you handle the cube but feel free to<br>ask for HELP at any time.<br>Tell me when you're READY!<br> "
        if (top_state == 3 and state == 2):
            return "This cube is already solved!<br>Say RESET to start over.<br> <br> "

        if (state == 2):
            return "Well done, you solved the cube!<br>Say RESET to start over.<br> <br> "
        if (state == 3):
            return "Cube was scanned incorrectly!<br>Say RESET to start over.<br> <br> "
        
        warn_top = warn & 0x0300
        warn_extended = warn & 0xFC00

        if (action in printer._actions):
            str_action = printer._actions[action]
        elif (action == status.ACTION_ASK_RESCAN):
            return "Error detected!<br>Say RESET to start over.<br> <br> "
        elif (action == status.ACTION_WAIT):
            if (detected == 0):
                str_action = "Show me the cube"
            elif (warn_top == 0):
                str_action = "Analyzing... Keep the cube in view"
            else:
                str_action = "Bad orientation"

        str_action_modifier = " and tell me to SCAN." if ((state == 0) and (auto_scan == 0)) else "."

        str_warn_top = printer._warn_top[warn_top]
        str_warn_scan = printer._warn_extended[warn_extended]

        if (detected == 0):
            str_warn_scan = ""

        str_step = f"Steps completed: {step_index} of {step_count}." if (state == 1) else ""
        
        return str_warn_scan + "<br>" + str_action + str_action_modifier + "<br>" + str_warn_top + "<br>" + str_step + "<br> "
    
    @staticmethod
    def build_step(top_state, state, step_index, step_count, action, warn, detected, auto_scan):
        scan_order = ["red", "blue", "orange", "green", "white", "yellow"]
        colors = ["white", "red", "green", "yellow", "orange", "blue"]

        text = printer.build_caption(top_state, state, step_index, step_count, action, warn, detected, auto_scan)
        steps = printer.split_text(text)

        if (top_state == 7):
            return steps[0]
        if (top_state == 0):
            return steps[0] + "<br>" + steps[1] + "<br>" + steps[2] + "<br>" + steps[3]
        if (top_state == 1):
            return steps[0] + "<br>" + steps[1] + "<br>" + steps[2] + "<br>" + steps[3]
        if (top_state == 3 and state == 1):
            return steps[0] + "<br>" + steps[1] + "<br>" + steps[2] + "<br>" + steps[3]
        if (top_state == 3 and state == 2):
            return steps[0] + "<br>" + steps[1]

        if (state == 2 or state == 3 or action == status.ACTION_ASK_RESCAN):
            return steps[0] + "<br>" + steps[1]

        if (state == 0):
            if ((warn & 0x2000) != 0):
                return steps[1] + "<br>" + steps[2]

            if (detected == 0):
                return steps[1] + "<br>" + steps[2]
            
            if ((warn & 0x1C00) == 0):
                return steps[1] + "<br>" + steps[2]
            
            return "I asked you to show me the " + scan_order[step_index] + " side,<br>but this side looks " + colors[((warn >> 10) & 7) - 1] + ".<br>Do you want me to SCAN anyway?"
        
        return steps[1] + '<br>' + steps[2]

    @staticmethod
    def build_process(top_state, state):
        if (top_state == 7):
            return "Hello."
        if (top_state == 0):
            return "I'm waiting for you to get a rubik's cube before we begin.<br>Tell me when you're ready."
        if (top_state == 1):
            return "We're getting ready to scan the cube.<br>Tell me when you're ready."
        if (top_state == 2):
            return "I'm scanning the cube with your help.<br>I need to scan it to find the solution and help you solve it."
        if (top_state == 3):
            if (state == 1):
                return "We just finished scanning the cube and are going to solve it now.<br>Tell me when you're ready."
            if (state == 2):
                return "We just finished scanning the cube.<br>The cube is already solved.<br>Say reset if you wish to solve another cube."
            if (state == 3):
                return "We just finished scanning the cube.<br>The cube was scanned incorrectly, unfortunately.<br>For best results, please follow the instructions on screen carefully next time.<br>Say reset to try again!"
        if (top_state == 4):
            return "You're solving the cube with my help... hopefully.<br>Follow the instructions on screen carefully."
        if (top_state == 5):
            return "The cube has been solved.<br>Say reset if you wish to solve another cube."
    
    @staticmethod
    def print_guide(lines):
        name = "GUIDE:"
        for line in lines:
            print(f"{name} {line}")
            name = "      "

    @staticmethod
    def print_user(text):
        print(f"USER:  {text}")

    @staticmethod
    def normalize_text(text):
        text = printer.split_text(text)
        text = printer.trim_text(text)
        return text
    
    def __init__(self):
        self._current_caption = ['']

    def update(self, top_state, state, step_index, step_count, action, warn, detected, auto_scan):
        self._top_state = top_state
        self._state = state
        self._step_index = step_index
        self._step_count = step_count
        self._action = action
        self._warn = warn
        self._detected = detected
        self._auto_scan = auto_scan

    def get_caption(self):
        text = printer.build_caption(self._top_state, self._state, self._step_index, self._step_count, self._action, self._warn, self._detected, self._auto_scan)
        return printer.normalize_text(text)
    
    def get_step(self):
        text = printer.build_step(self._top_state, self._state, self._step_index, self._step_count, self._action, self._warn, self._detected, self._auto_scan)
        return printer.normalize_text(text)
    
    def get_process(self):
        text = printer.build_process(self._top_state, self._state)
        return printer.normalize_text(text)
    
    def print_caption(self):
        caption = self.get_caption()
        if (caption != self._current_caption):
            self._current_caption = caption
            printer.print_guide(self._current_caption)
        return self._current_caption
    
    def print_step(self):
        step = self.get_step()
        printer.print_guide(step)
        return step
    
    def print_process(self):
        process = self.get_process()
        printer.print_guide(process)
        return process


#------------------------------------------------------------------------------
# Painter
#------------------------------------------------------------------------------

class painter:
    STICKER_AREA_TILE_SIZE = 30
    STICKER_AREA_TILE_GAP = 4
    STICKER_AREA_OFFSET = 20
    MINI_STICKER_AREA_TILE_SIZE = 14
    MINI_STICKER_AREA_TILE_GAP = 2
    MINI_STICKER_AREA_OFFSET = 20
    LINK_COLOR = (255, 0, 255)
    LINK_THICKNESS = 3
    TEXT_COLOR = (255, 0, 255)
    CENTER_COLOR = (255, 0, 255)
    CENTER_RADIUS = 5

    _action_move_links = {
        status.ACTION_MOVE_MX : (3, (lambda i : i+6),             (lambda i : i)),
        status.ACTION_MOVE_MY : (3, (lambda i : 3*i+2),           (lambda i : 3*i)),
        status.ACTION_MOVE_MZ : (4, (lambda i : [6, 0, 7, 4][i]), (lambda i : [0, 2, 4, 5][i])),
    }

    _action_turn_links = {
        status.ACTION_TURN_MU : (1, (lambda i : 2),               (lambda i : 0)),
        status.ACTION_TURN_MR : (1, (lambda i : 8),               (lambda i : 2)),
        status.ACTION_TURN_MF : (4, (lambda i : [1, 5, 7, 3][i]), (lambda i : [5, 7, 3, 1][i])),
        status.ACTION_TURN_MD : (1, (lambda i : 6),               (lambda i : 8)),
        status.ACTION_TURN_ML : (1, (lambda i : 0),               (lambda i : 6)),
        status.ACTION_TURN_MB : (2, (lambda i : 8-2*i),           (lambda i : 2*i)),
    }

    _grid = {
        'white' : [1, 0],
        'orange': [0, 1],
        'green' : [1, 1],
        'red'   : [2, 1],
        'blue'  : [3, 1],
        'yellow': [1, 2],
    }
    
    @staticmethod
    def draw_centers(frame, cube_centers, radius=CENTER_RADIUS, color=CENTER_COLOR):
        for p in cube_centers:
            frame = cv2.circle(frame, p, radius, color, -1)
        return frame

    @staticmethod
    def draw_contour_link(frame, cube_centers, start, end, color=LINK_COLOR, thickness=LINK_THICKNESS):
        frame = cv2.arrowedLine(frame, cube_centers[start], cube_centers[end], color, thickness)
        return frame

    @staticmethod
    def draw_action_links(frame, cube_centers, action):
        base_action = action & ~status.ACTION_P
        if (base_action in painter._action_turn_links):
            n, link_start, link_end = painter._action_turn_links[base_action]
        elif (base_action in painter._action_move_links):
            n, link_start, link_end = painter._action_move_links[base_action]
        else:
            return frame        
        if ((action & status.ACTION_P) != 0):
            link_start, link_end = link_end, link_start
        for i in range(0, n):
            frame = painter.draw_contour_link(frame, cube_centers, link_start(i), link_end(i))
        return frame
    
    # From https://github.com/kkoomen/qbr with some modifications
    @staticmethod
    def draw_stickers(frame, stickers, offset_x, offset_y, tile_size, tile_gap):
        for row in range(3):
            for col in range(3):
                x1 = offset_x + (tile_size + tile_gap) * col
                y1 = offset_y + (tile_size + tile_gap) * row
                x2 = x1 + tile_size
                y2 = y1 + tile_size
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), -1)
                color = stickers[3*row+col]
                frame = cv2.rectangle(frame, (x1 + 1, y1 + 1), (x2 - 1, y2 - 1), palette.get_ideal_color(color) if (isinstance(color, str)) else color, -1)
        return frame

    # From https://github.com/kkoomen/qbr with some modifications
    @staticmethod
    def draw_preview_stickers(frame, stickers):
        return painter.draw_stickers(frame, stickers, painter.STICKER_AREA_OFFSET, painter.STICKER_AREA_OFFSET, painter.STICKER_AREA_TILE_SIZE, painter.STICKER_AREA_TILE_GAP)

    # From https://github.com/kkoomen/qbr with some modifications
    @staticmethod
    def draw_2d_cube_state(frame, result_state):
        side_offset = painter.MINI_STICKER_AREA_TILE_GAP * 3
        side_size   = painter.MINI_STICKER_AREA_TILE_SIZE * 3 + painter.MINI_STICKER_AREA_TILE_GAP * 2
        offset_x    = frame.shape[1] - (side_size * 4) - (side_offset * 3) - painter.MINI_STICKER_AREA_OFFSET
        offset_y    = painter.MINI_STICKER_AREA_OFFSET
        for side, (grid_x, grid_y) in painter._grid.items():
            frame = painter.draw_stickers(frame, result_state[side] if (side in result_state) else ['X']*9, offset_x + (side_size + side_offset) * grid_x, offset_y + (side_size + side_offset) * grid_y, painter.MINI_STICKER_AREA_TILE_SIZE, painter.MINI_STICKER_AREA_TILE_GAP)
        return frame
    
    @staticmethod
    def draw_text(frame, text, position, color=TEXT_COLOR):
        return cv2.putText(frame, text, position, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 1)

    @staticmethod
    def draw_text_block(frame, text_block):
        n = len(text_block)
        for i in range(0, n):
            frame = painter.draw_text(frame, text_block[i], (2, frame.shape[0] - 10 - (n-1-i)*20))
        return frame

    @staticmethod
    def draw_status(frame, caption, action, cube_centers, colors, cube_colors):
        if (cube_centers is not None):
            centers = [tuple([int(x), int(y)]) for (x, y) in cube_centers]
            frame = painter.draw_centers(frame, centers)
            frame = painter.draw_action_links(frame, centers, action)
        frame = painter.draw_preview_stickers(frame, colors)
        frame = painter.draw_2d_cube_state(frame, cube_colors)
        frame = painter.draw_text_block(frame, caption)
        return frame

