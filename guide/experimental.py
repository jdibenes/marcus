
from cube import cube_simulator


#------------------------------------------------------------------------------
# Cube Explorer
#------------------------------------------------------------------------------

class cube_explorer(cube_simulator):
    _chain = {
        'white'  : 'red',
        'red'    : 'green',
        'green'  : 'yellow',
        'yellow' : 'orange',
        'orange' : 'blue',
        'blue'   : None,
    }

    _color2flag = {
        'white'  : 0x20,
        'red'    : 0x10,
        'green'  : 0x08,
        'yellow' : 0x04,
        'orange' : 0x02,
        'blue'   : 0x01,
        'X'      : 0x00,
    }

    START = 'white'

    START_CORNERS = {
        _color2flag['white']  | _color2flag['red']    | _color2flag['green'],  # URF
        _color2flag['white']  | _color2flag['red']    | _color2flag['blue'],   # URB
        _color2flag['white']  | _color2flag['green']  | _color2flag['orange'], # UFL
        _color2flag['white']  | _color2flag['orange'] | _color2flag['blue'],   # ULB
        _color2flag['red']    | _color2flag['green']  | _color2flag['yellow'], # RFD
        _color2flag['red']    | _color2flag['yellow'] | _color2flag['blue'],   # RDB
        _color2flag['green']  | _color2flag['yellow'] | _color2flag['orange'], # FDL
        _color2flag['yellow'] | _color2flag['orange'] | _color2flag['blue'],   # DLB
    }

    START_SIDES = {
        _color2flag['white']  | _color2flag['red'],    # UR
        _color2flag['white']  | _color2flag['green'],  # UF
        _color2flag['white']  | _color2flag['orange'], # UL
        _color2flag['white']  | _color2flag['blue'],   # UB
        _color2flag['red']    | _color2flag['green'],  # RF
        _color2flag['red']    | _color2flag['yellow'], # RD
        _color2flag['red']    | _color2flag['blue'],   # RB
        _color2flag['green']  | _color2flag['yellow'], # FD
        _color2flag['green']  | _color2flag['orange'], # FL
        _color2flag['yellow'] | _color2flag['orange'], # DL
        _color2flag['yellow'] | _color2flag['blue'],   # DB
        _color2flag['orange'] | _color2flag['blue'],   # LB
    }

    @staticmethod
    def cubie_mode_U(U, R, F, D, L, B):
        # U
        # U = U
        # D = D
        F, R, B, L = L, F, R, B
        return U, R, F, D, L, B

    @staticmethod
    def cubie_mode_R(U, R, F, D, L, B):
        # R
        # R = R
        # L = L
        F, D, B, U = U, F, D, B
        return U, R, F, D, L, B

    @staticmethod
    def cubie_mode_F(U, R, F, D, L, B):
        # F
        # F = F
        # B = B
        R, U, L, D = D, R, U, L
        return U, R, F, D, L, B
    
    @staticmethod
    def cubie_to_int(U, R, F, D, L, B):
        return (cube_explorer._color2flag[U] << 40) | (cube_explorer._color2flag[R] << 32) | (cube_explorer._color2flag[F] << 24) | (cube_explorer._color2flag[D] << 16) | (cube_explorer._color2flag[L] << 8) | cube_explorer._color2flag[B]

    _cubie_table = set()

    @staticmethod
    def create_cubie_entry(U, R, F, D, L, B):
        for _ in range(0, 4):
            for _ in range(0, 4):
                for _ in range(0, 4):
                    cube_explorer._cubie_table.add(cube_explorer.cubie_to_int(U, R, F, D, L, B))
                    U, R, F, D, L, B = cube_explorer.cubie_mode_F(U, R, F, D, L, B)
                U, R, F, D, L, B = cube_explorer.cubie_mode_R(U, R, F, D, L, B)
            U, R, F, D, L, B = cube_explorer.cubie_mode_U(U, R, F, D, L, B)

    @staticmethod
    def create_cubie_table():
        cube_explorer.create_cubie_entry('white', 'red', 'green',      'X',      'X', 'X')
        cube_explorer.create_cubie_entry('white', 'red',     'X',      'X',      'X', 'blue')
        cube_explorer.create_cubie_entry('white',   'X', 'green',      'X', 'orange', 'X')
        cube_explorer.create_cubie_entry('white',   'X',     'X',      'X', 'orange', 'blue')
        cube_explorer.create_cubie_entry(    'X', 'red', 'green', 'yellow',      'X', 'X')
        cube_explorer.create_cubie_entry(    'X', 'red',     'X', 'yellow',      'X', 'blue')
        cube_explorer.create_cubie_entry(    'X',   'X', 'green', 'yellow', 'orange', 'X')
        cube_explorer.create_cubie_entry(    'X',   'X',     'X', 'yellow', 'orange', 'blue')

        cube_explorer.create_cubie_entry('white', 'red',     'X',      'X',      'X', 'X')
        cube_explorer.create_cubie_entry('white',   'X', 'green',      'X',      'X', 'X')
        cube_explorer.create_cubie_entry('white',   'X',     'X',      'X', 'orange', 'X')
        cube_explorer.create_cubie_entry('white',   'X',     'X',      'X',      'X', 'blue')
        cube_explorer.create_cubie_entry(    'X', 'red', 'green',      'X',      'X', 'X')
        cube_explorer.create_cubie_entry(    'X', 'red',     'X', 'yellow',      'X', 'X')
        cube_explorer.create_cubie_entry(    'X', 'red',     'X',      'X',      'X', 'blue')
        cube_explorer.create_cubie_entry(    'X',   'X', 'green', 'yellow',      'X', 'X')
        cube_explorer.create_cubie_entry(    'X',   'X', 'green',      'X', 'orange', 'X')
        cube_explorer.create_cubie_entry(    'X',   'X',     'X', 'yellow', 'orange', 'X')
        cube_explorer.create_cubie_entry(    'X',   'X',     'X', 'yellow',      'X', 'blue')
        cube_explorer.create_cubie_entry(    'X',   'X',     'X',      'X', 'orange', 'blue')

    @staticmethod
    def _evaluate_corner(U, R, F, D, L, B):
        return cube_explorer.cubie_to_int(U, R, F, D, L, B) in cube_explorer._cubie_table

    def _evaluate_adjacent(self, side, remaining_corners:set, remaining_sides:set):
        if (side == 'white'):
            corners = []
            sides = []

            return remaining_corners.issuperset(corners) and remaining_sides.issuperset(sides), remaining_corners.difference(corners), remaining_sides.difference(sides)
        if (side == 'red'):
            white = self._state['white']
            red = self._state['red']

            # evaluate white-red side
            f_wr = cube_explorer._color2flag[white[5]] | cube_explorer._color2flag[red[1]]
            if (not cube_explorer._evaluate_corner(white[5], red[1], 'X', 'X', 'X', 'X')):
                return False, None, None

            corners = []
            sides = [f_wr]
            return remaining_corners.issuperset(corners) and remaining_sides.issuperset(sides), remaining_corners.difference(corners), remaining_sides.difference(sides)
        if (side == 'green'):
            white = self._state['white']
            red = self._state['red']
            green = self._state['green']

            # evaluate white-red-green corner
            f_wrg = cube_explorer._color2flag[white[8]] | cube_explorer._color2flag[red[0]] | cube_explorer._color2flag[green[2]]
            if (not cube_explorer._evaluate_corner(white[8], red[0], green[2], 'X', 'X', 'X')):
                return False, None, None

            # evaluate red-green side
            f_rg = cube_explorer._color2flag[red[3]] | cube_explorer._color2flag[green[5]]
            if (not cube_explorer._evaluate_corner('X', red[3], green[5], 'X', 'X', 'X')):
                return False, None, None

            # evaluate white-green side
            f_wg = cube_explorer._color2flag[white[7]] | cube_explorer._color2flag[green[1]]
            if (not cube_explorer._evaluate_corner(white[7], 'X', green[1], 'X', 'X', 'X')):
                return False, None, None

            corners = [f_wrg]
            sides = [f_rg, f_wg]
            return remaining_corners.issuperset(corners) and remaining_sides.issuperset(sides), remaining_corners.difference(corners), remaining_sides.difference(sides)
        if (side == 'yellow'):
            red = self._state['red']
            green = self._state['green']
            yellow = self._state['yellow']

            # evaluate red-green-yellow corner
            f_rgy = cube_explorer._color2flag[red[6]] | cube_explorer._color2flag[green[8]] | cube_explorer._color2flag[yellow[2]]
            if (not cube_explorer._evaluate_corner('X', red[6], green[8], yellow[2], 'X', 'X')):
                return False, None, None

            # evaluate green-yellow side
            f_gy = cube_explorer._color2flag[green[7]] | cube_explorer._color2flag[yellow[1]]
            if (not cube_explorer._evaluate_corner('X', 'X', green[7], yellow[1], 'X', 'X')):
                return False, None, None

            # evaluate red-yellow side
            f_ry = cube_explorer._color2flag[red[7]] | cube_explorer._color2flag[yellow[5]]
            if (not cube_explorer._evaluate_corner('X', red[7], 'X', yellow[5], 'X', 'X')):
                return False, None, None

            corners = [f_rgy]
            sides = [f_gy, f_ry]
            return remaining_corners.issuperset(corners) and remaining_sides.issuperset(sides), remaining_corners.difference(corners), remaining_sides.difference(sides)
        if (side == 'orange'):
            white = self._state['white']
            green = self._state['green']
            yellow = self._state['yellow']
            orange = self._state['orange']

            # evaluate white-green-orange corner
            f_wgo = cube_explorer._color2flag[white[6]] | cube_explorer._color2flag[green[0]] | cube_explorer._color2flag[orange[2]]
            if (not cube_explorer._evaluate_corner(white[6], 'X', green[0], 'X', orange[2], 'X')):
                return False, None, None

            # evaluate green-yellow-orange corner
            f_gyo = cube_explorer._color2flag[green[6]] | cube_explorer._color2flag[yellow[0]] | cube_explorer._color2flag[orange[8]]
            if (not cube_explorer._evaluate_corner('X', 'X', green[6], yellow[0], orange[8], 'X')):
                return False, None, None

            # evaluate white-orange side
            f_wo = cube_explorer._color2flag[white[3]] | cube_explorer._color2flag[orange[1]]
            if (not cube_explorer._evaluate_corner(white[3], 'X', 'X', 'X', orange[1], 'X')):
                return False, None, None

            # evaluate green-orange side
            f_go = cube_explorer._color2flag[green[3]] | cube_explorer._color2flag[orange[5]]
            if (not cube_explorer._evaluate_corner('X', 'X', green[3], 'X', orange[5], 'X')):
                return False, None, None

            # evaluate yellow-orange side
            f_yo = cube_explorer._color2flag[yellow[3]] | cube_explorer._color2flag[orange[7]]
            if (not cube_explorer._evaluate_corner('X', 'X', 'X', yellow[3], orange[7], 'X')):
                return False, None, None

            corners = [f_wgo, f_gyo]
            sides = [f_wo, f_go, f_yo]
            return remaining_corners.issuperset(corners) and remaining_sides.issuperset(sides), remaining_corners.difference(corners), remaining_sides.difference(sides)
        if (side == 'blue'):
            white = self._state['white']
            red = self._state['red']
            yellow = self._state['yellow']
            orange = self._state['orange']
            blue = self._state['blue']

            # evaluate white-red-blue corner
            f_wrb = cube_explorer._color2flag[white[2]] | cube_explorer._color2flag[red[2]] | cube_explorer._color2flag[blue[0]]
            if (not cube_explorer._evaluate_corner(white[2], red[2], 'X', 'X', 'X', blue[0])):
                return False, None, None

            # evaluate red-yellow-blue corner
            f_ryb = cube_explorer._color2flag[red[8]] | cube_explorer._color2flag[yellow[8]] | cube_explorer._color2flag[blue[6]]
            if (not cube_explorer._evaluate_corner('X', red[8], 'X', yellow[8], 'X', blue[6])):
                return False, None, None

            # evaluate yellow-orange-blue corner
            f_yob = cube_explorer._color2flag[yellow[6]] | cube_explorer._color2flag[orange[6]] | cube_explorer._color2flag[blue[8]]
            if (not cube_explorer._evaluate_corner('X', 'X', 'X', yellow[6], orange[6], blue[8])):
                return False, None, None

            # evaluate white-orange-blue corner
            f_wob = cube_explorer._color2flag[white[0]] | cube_explorer._color2flag[orange[0]] | cube_explorer._color2flag[blue[2]]
            if (not cube_explorer._evaluate_corner(white[0], 'X', 'X', 'X', orange[0], blue[2])):
                return False, None, None

            # evaluate white-blue side
            f_wb = cube_explorer._color2flag[white[1]] | cube_explorer._color2flag[blue[1]]
            if (not cube_explorer._evaluate_corner(white[1], 'X', 'X', 'X', 'X', blue[1])):
                return False, None, None

            # evaluate red-blue side
            f_rb = cube_explorer._color2flag[red[5]] | cube_explorer._color2flag[blue[3]]
            if (not cube_explorer._evaluate_corner('X', red[5], 'X', 'X', 'X', blue[3])):
                return False, None, None

            # evaluate yellow-blue side
            f_yb = cube_explorer._color2flag[yellow[7]] | cube_explorer._color2flag[blue[7]]
            if (not cube_explorer._evaluate_corner('X', 'X', 'X', yellow[7], 'X', blue[7])):
                return False, None, None

            # evaluate orange-blue side
            f_ob = cube_explorer._color2flag[orange[3]] | cube_explorer._color2flag[blue[5]]
            if (not cube_explorer._evaluate_corner('X', 'X', 'X', 'X', orange[3], blue[5])):
                return False, None, None
            
            corners = [f_wrb, f_ryb, f_yob, f_wob]
            sides = [f_wb, f_rb, f_yb, f_ob]
            return remaining_corners.issuperset(corners) and remaining_sides.issuperset(sides), remaining_corners.difference(corners), remaining_sides.difference(sides)

    def explore(self, side=START, remaining_corners=START_CORNERS, remaining_sides=START_SIDES):
        if (side is None):
            self._valid += 1
            self._solutions.append(self.get_state())
            return True
        if (side == cube_explorer.START):
            U = self.get_orientation_candidates('white')[1]
            R = self.get_orientation_candidates('red')[1]
            F = self.get_orientation_candidates('green')[1]
            D = self.get_orientation_candidates('yellow')[1]
            L = self.get_orientation_candidates('orange')[1]
            B = self.get_orientation_candidates('blue')[1]
            self._range = {
                'white'  : 4 if (U == 0) else U,
                'red'    : 4 if (R == 0) else R,
                'green'  : 4 if (F == 0) else F,
                'yellow' : 4 if (D == 0) else D,
                'orange' : 4 if (L == 0) else L,
                'blue'   : 4 if (B == 0) else B
            }

            self._valid = 0
            self._solutions = []

        for _ in range(0, self._range[side]):
            ok, next_corners, next_sides = self._evaluate_adjacent(side, remaining_corners, remaining_sides)
            if (ok):
                ok = self.explore(cube_explorer._chain[side], next_corners, next_sides)
                if (ok):
                    pass
            self.partial_turn_face(side, cube_simulator.DIRECTION_RIGHT)

        return False
    
    def get_schemas(self):
        return self._solutions
    
