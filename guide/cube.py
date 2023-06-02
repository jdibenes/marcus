
import os
import json
import skimage
import kociemba
import pyciede2000


#------------------------------------------------------------------------------
# Palette
#------------------------------------------------------------------------------

class palette:
    COLORS = [
        'white',
        'red',
        'green',
        'yellow',
        'orange',
        'blue',        
    ]

    _ideal_color_palette = {        
        'white' : (255, 255, 255),
        'red'   : (  0,   0, 255),
        'green' : (  0, 255,   0),
        'yellow': (  0, 255, 255),
        'orange': (  0, 128, 255),
        'blue'  : (255,   0,   0),
        'X'     : (128, 128, 128),
    }

    def __init__(self):
        self._bgr_palette = {}
        self._lab_palette = {}
        for color in palette.COLORS:
            self.set_color(color, palette._ideal_color_palette[color])
        
    @staticmethod
    def get_ideal_color(name):
        return palette._ideal_color_palette[name]
    
    @staticmethod
    def bgr2lab(bgr):
        return skimage.color.rgb2lab((bgr[2] / 255, bgr[1] / 255, bgr[0] / 255))
    
    @staticmethod
    def compare(lab1, lab2):
        return pyciede2000.ciede2000(lab1, lab2)['delta_E_00']
    
    def get_color(self, name):
        return self._bgr_palette[name]
    
    def set_color(self, name, bgr):
        self._bgr_palette[name] = bgr
        self._lab_palette[name] = palette.bgr2lab(bgr)

    def translate(self, bgr):
        source = palette.bgr2lab(bgr)
        return min([(name, palette.compare(source, lab)) for name, lab in self._lab_palette.items()], key=lambda item: item[1])[0]

    def translate_batch(self, colors):
        return [self.translate(color) for color in colors]


#------------------------------------------------------------------------------
# Cube
#------------------------------------------------------------------------------

class cube:
    def __init__(self, state={}):
        self.set_state(state)

    @staticmethod
    def clone_state(state):
        r = {}
        for side, colors in state.items():
           r[side] = list(colors)
        return r

    def set_state(self, state):
        self._state = self.clone_state(state)

    def get_state(self):
        return cube.clone_state(self._state)
    
    def has_side(self, side):
        return side in self._state
    
    def set_side(self, side, colors):
        self._state[side] = list(colors)

    def get_side(self, side):
        return list(self._state[side])
    
    def is_ready(self):
        return len(self._state.keys()) >= 6


#------------------------------------------------------------------------------
# Cube Solver
#------------------------------------------------------------------------------

class cube_solver(cube):
    _absolute2relative = { 
        'F' : { 'F' : 'F', 'L' : 'L', 'R' : 'R', 'B' : 'B', 'U' : 'U', 'D' : 'D', },
        'R' : { 'F' : 'L', 'L' : 'B', 'R' : 'F', 'B' : 'R', 'U' : 'U', 'D' : 'D', },
        'B' : { 'F' : 'B', 'L' : 'R', 'R' : 'L', 'B' : 'F', 'U' : 'U', 'D' : 'D', },
        'L' : { 'F' : 'R', 'L' : 'F', 'R' : 'B', 'B' : 'L', 'U' : 'U', 'D' : 'D', },
        'U' : { 'F' : 'D', 'L' : 'L', 'R' : 'R', 'B' : 'U', 'U' : 'F', 'D' : 'B', },
        'D' : { 'F' : 'U', 'L' : 'L', 'R' : 'R', 'B' : 'D', 'U' : 'B', 'D' : 'F', },
    }

    _color2notation = {
        'white' : 'U',
        'red'   : 'R',
        'green' : 'F',
        'yellow': 'D',
        'orange': 'L',
        'blue'  : 'B',
    }

    _notation2color = {
        'U' : 'white',
        'R' : 'red',
        'F' : 'green',
        'D' : 'yellow',
        'L' : 'orange',
        'B' : 'blue',
    }

    _invert = {
        ''   : '\'',
        '2'  : '2',
        '\'' : ''
    }

    @staticmethod
    def absolute_to_relative(front, absolute):
        return cube_solver._absolute2relative[front][absolute]

    @staticmethod
    def color_to_notation(name):
        return cube_solver._color2notation[name]
    
    @staticmethod
    def notation_to_color(name):
        return cube_solver._notation2color[name]
    
    @staticmethod
    def invert_step(step):
        return step[0] + cube_simulator._invert[step[1:]]
    
    @staticmethod
    def atomize(algorithm):
        atomized = []
        for step in algorithm:
            atomized.extend([step[0], step[0]] if (step[1:] == '2') else [step])
        return atomized
    
    def update(self, colors):
        self.set_side(colors[4], colors)

    def is_solved(self):
        if (not self.is_ready()):
            return False
        for side, colors in self._state.items():
            for color in colors:
                if (color != side):
                    return False
        return True
    
    def solve(self):
        if (self.is_solved()):
            return []
        state_string = ''
        for side in ['white', 'red', 'green', 'yellow', 'orange', 'blue']:
            state_string += ''.join([cube_solver.color_to_notation(color) for color in self._state[side]])
        try:
            algorithm = kociemba.solve(state_string)
        except:
            return None        
        return algorithm.split(' ')


#------------------------------------------------------------------------------
# Cube Simulator
#------------------------------------------------------------------------------

class cube_simulator(cube_solver):
    DIRECTION_RIGHT = 0
    DIRECTION_LEFT  = 1

    _groups = ((0, 1, 2), (2, 5, 8), (8, 7, 6), (6, 3, 0), (3, 4, 5), (1, 4, 7))

    _adjacent = {
        'white'  : (('blue',  0), ('red',    0), ('green',  0), ('orange', 0)),
        'red'    : (('white', 1), ('blue',   3), ('yellow', 1), ('green',  1)),
        'green'  : (('white', 2), ('red',    3), ('yellow', 0), ('orange', 1)),
        'yellow' : (('green', 2), ('red',    2), ('blue',   2), ('orange', 2)),
        'orange' : (('white', 3), ('green',  3), ('yellow', 3), ('blue',   1)),
        'blue'   : (('white', 0), ('orange', 3), ('yellow', 2), ('red',    1)),
    }

    _modifier = {
        ''   : (DIRECTION_RIGHT, 1),
        '2'  : (DIRECTION_RIGHT, 2),
        '\'' : (DIRECTION_LEFT,  1),
    }

    @staticmethod
    def _move(source, destination, A, ga, B, gb, direction):
        S, D, s, d = (A, B, cube_simulator._groups[ga], cube_simulator._groups[gb]) if (direction == cube_simulator.DIRECTION_RIGHT) else (B, A, cube_simulator._groups[gb], cube_simulator._groups[ga])
        for i in range(0, 3):
            destination[D][d[i]] = source[S][s[i]]

    @staticmethod
    def _operation_turn_adjacent(source, destination, side, direction):
        steps = cube_simulator._adjacent[side]
        for i in range(0, 4):
            side1, g1 = steps[i]
            side2, g2 = steps[(i+1)&3]
            cube_simulator._move(source, destination, side1, g1, side2, g2, direction)

    @staticmethod
    def _operation_turn_face(source, destination, side, direction):
        for i in range(0, 3):
            side1, g1 = side, 2*i
            side2, g2 = side, 2*i+1
            cube_simulator._move(source, destination, side1, g1, side2, g2, direction)

    @staticmethod
    def _operation_turn(source, destination, side, direction):
        cube_simulator._operation_turn_adjacent(source, destination, side, direction)
        cube_simulator._operation_turn_face(source, destination, side, direction)

    def _operate(self, operation, side, direction):
        next_state = self.get_state()
        operation(self._state, next_state, side, direction)
        self._state = next_state

    def partial_turn_adjacent(self, side, direction):
        self._operate(cube_simulator._operation_turn_adjacent, side, direction)

    def partial_turn_face(self, side, direction):
        self._operate(cube_simulator._operation_turn_face, side, direction)

    def turn(self, side, direction):
        self._operate(cube_simulator._operation_turn, side, direction)

    def evaluate(self, step):
        side = cube_solver.notation_to_color(step[0])
        direction, times = cube_simulator._modifier[step[1:]]
        for _ in range(0, times):
            self.turn(side, direction)

    def get_orientation_candidates(self, color):
        reference_cube = cube_simulator(self.get_state())
        candidates = []
        for _ in range(0, 4):
            reference_cube.partial_turn_face(color, cube_simulator.DIRECTION_RIGHT)
            candidates.append(reference_cube.get_side(color))
        source = candidates[0]
        for i in [1, 2, 3, 0]:
            if (source == candidates[i]):
                return candidates, i


#------------------------------------------------------------------------------
# Cube Scanner
#------------------------------------------------------------------------------

class cube_scanner(cube):
    def __init__(self, state={}, calibration_path=os.path.join('.', 'calibration.json')):
        super().__init__(state)
        self._calibration_path = calibration_path
        self._palette = palette()
        
    def load(self):
        try:
            with open(self._calibration_path, 'r') as calibration_file:
                calibration = json.loads(calibration_file.read())
        except:
            calibration = {}
        for color in palette.COLORS:
            if (color in calibration):
                self._palette.set_color(color, tuple(calibration[color]))

    def save(self):
        calibration = {color : self._palette.get_color(color) for color in palette.COLORS}
        try:            
            with open(self._calibration_path, 'w') as calibration_file:
                json.dump(calibration, calibration_file)
        except:
            pass
        
    def update(self, side, colors):
        self.set_side(side, colors)
        self._palette.set_color(side, colors[4])

    def translate(self, colors):
        return self._palette.translate_batch(colors)
    
    def get_state_translated(self):
        state = {}
        for side, colors in self._state.items():
            state[side] = self.translate(colors)
        return state
    
    def get_name(self, colors):
        return self._palette.translate(colors[4])


#------------------------------------------------------------------------------
# Cube Integrator
#------------------------------------------------------------------------------

class cube_integrator(cube_scanner):
    def __init__(self, threshold, size):
        super().__init__()
        self._threshold = threshold
        self._size = size
        self._previous = palette.bgr2lab((0, 0, 0))
        self._count = 0
        
    def is_stable(self, colors):
        current = palette.bgr2lab(colors[4])
        delta = palette.compare(self._previous, current)
        self._previous = current
        if (delta > self._threshold):
            self._count = 0
            return False
        if (self._count >= self._size):
            return True
        self._count += 1
        return False
    
    def is_registered(self, colors):
        for side, registered in self._state.items():
            delta = palette.compare(palette.bgr2lab(registered[4]), palette.bgr2lab(colors[4]))
            if (delta <= self._threshold):
                return side
        return None
    
    def get_count(self):
        return self._count

