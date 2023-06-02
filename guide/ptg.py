
from cube import cube_solver
from experimental import cube_explorer
from guide import status, scan_guide, solve_guide, filter


#------------------------------------------------------------------------------
# Guide (FSM - L0 - S1A2M3)
#------------------------------------------------------------------------------

class guide_fsm:
    def __init__(self, threshold, size, auto, explore):
        self._scanner = scan_guide(threshold, size, auto)
        self._scanner.load()
        self._state = 0
        self._state_cube = {}
        self._index = 0
        self._total = len(scan_guide.ORDER)
        self._progress = 0.0
        self._colors = self._scanner.get_colors()
        self._size = size
        self._auto = auto
        self._explore = explore

    def step(self, colors, trigger):
        if (self._state == 0):
            action, warn = self._scanner.assess(colors, trigger)
            self._progress = self._scanner.get_count() / self._size
            if (action == status.ACTION_NONE):
                if (not self._scanner.next(colors)):
                    self._state_cube = self._scanner.get_state_translated()
                    algorithm = cube_solver(self._state_cube).solve()
                    if (self._explore and (algorithm is None)):
                        print('DEBUG: bad scan, exploring...')
                        explorer = cube_explorer(self._state_cube)
                        explorer.explore()
                        schemas = explorer.get_schemas()
                        algorithms = []
                        states = []
                        print(f'DEBUG: found {len(schemas)} candidate(s).')
                        for schema in schemas:
                            algorithm = cube_solver(schema).solve()
                            if (algorithm is not None):
                                algorithms.append(algorithm)
                                states.append(schema)
                        if (len(algorithms) == 1):
                            self._state_cube = states[0]
                            algorithm = algorithms[0]
                            print('DEBUG: unique solution found.')
                        else:
                            print('DEBUG: no unique solution, abort...')
                            algorithm = None
                    if (algorithm is None):
                        self._state = 3
                        self._progress = 0.0
                    elif (len(algorithm) <= 0):
                        self._state = 2
                        self._progress = 1.0
                    else:
                        self._guide = solve_guide(self._state_cube, algorithm)
                        self._total = len(self._guide.get_algorithm())
                        self._index = self._guide.get_sim_index()
                        self._state = 1
                        self._progress = 0.0
                else:
                    action, warn = self._scanner.assess(colors, trigger)
                    self._state_cube = self._scanner.get_state()
                    self._index = self._scanner.get_index()
                self._colors = self._scanner.get_colors()
        if (self._state == 1):
            colors = self._scanner.translate(colors)
            action, warn = self._guide.assess(colors)
            if (action == status.ACTION_NONE):
                self._state_cube = self._guide.get_sim_cube()
                if (not self._guide.next()):
                    self._state = 2
                    self._progress = 1.0
                    self._scanner.save()
                else:
                    action, warn = self._guide.assess(colors)
                    self._index = self._guide.get_sim_index()
                    self._progress = self._index / self._total
        if (self._state == 2):
            action = status.ACTION_NONE
            warn = status.WARN_NONE
        if (self._state == 3):
            action = status.ACTION_ASK_RESCAN
            warn = status.WARN_NONE
        return action, warn
    
    def get_state(self):
        return self._state
    
    def get_state_cube(self):
        return self._state_cube
    
    def get_index(self):
        return self._index
    
    def get_count(self):
        return self._total
    
    def get_progress(self):
        return self._progress
    
    def get_colors(self):
        return self._colors


#------------------------------------------------------------------------------
# Experience (FSM - TOP - L1 - I1I2I3)
#------------------------------------------------------------------------------

class experience_fsm(guide_fsm):
    def __init__(self, threshold, size, auto, explore, hold, override_state=0):
        super().__init__(threshold, size, auto, explore)
        self._low_pass = filter(hold)
        self._experience_state = override_state
        self._action, self._warn = super().step([(255, 255, 255)]*9, False)        

    def step(self, colors, select, trigger):
        if (self._experience_state == 0): # Welcome
            if (select):
                self._experience_state = 1
            return self._action, self._warn
        if (self._experience_state == 1): # Pre-Scan
            if (select):
                self._experience_state = 2
            return self._action, self._warn
        if (self._experience_state == 2): # Scan
            if (colors is not None):
                self._action, self._warn = super().step(colors, trigger)
                if (self.get_state() != 0):
                    self._experience_state = 3
            return self._action, self._warn
        if (self._experience_state == 3): # Post-Scan -> Solving, Solved, Bad
            if (select and self.get_state() == 1):
                self._experience_state = 4
                self._low_pass.assess(status.ACTION_NONE)
            self._action = status.ACTION_WAIT
            self._warn = status.WARN_NONE
            return self._action, self._warn
        if (self._experience_state == 4): # Solving
            if (colors is not None):
                self._action, self._warn = super().step(colors, False)
                if (self.get_state() == 2):
                    self._experience_state = 5
                else:
                    self._action = self._low_pass.assess(self._action)
            return self._action, self._warn
        if (self._experience_state == 5): # Done
            return self._action, self._warn
        if (self._experience_state == 7): # Wait
            if (select):
                self._experience_state = 0
            return self._action, self._warn


    def get_top_state(self):
        return self._experience_state


#------------------------------------------------------------------------------
# Driver (FSM - BRIDGE - L0)
#------------------------------------------------------------------------------

class driver_fsm:
    _talk_allowed = [2, 5, 6, 9, 10, 11, 12, 15]

    def __init__(self, override_state=0):
        self._state = override_state

    def step(self, top_state, top_index, talk, talk_done, first_trigger, start_trigger, scan_trigger, solve_trigger):
        enable = False
        if (self._state == 0 and top_state == 0):
            talk()
            self._state = 1
        if (self._state == 1): 
            if (talk_done()):
                self._state = 2
        if (self._state == 2): # Allow User Input (Welcome)
            enable = start_trigger
            if (enable):
                self._state = 3
        if (self._state == 3 and top_state == 1):
            talk()
            self._state = 4
        if (self._state == 4):
            if (talk_done()):
                self._state = 5
        if (self._state == 5): # Allow User Input (Pre-Scan)
            enable = scan_trigger
            if (enable):
                self._state = 6
                self._last_scan_step = -1
        if (self._state == 6 and top_state == 2): # Allow User Input (Force-Scan)
            if (self._last_scan_step != top_index):
                talk()
            self._last_scan_step = top_index
            if (top_index == 5):
                self._state = 7
        if (self._state == 7 and top_state == 3):
            talk()
            self._state = 8
        if (self._state == 8):
            if (talk_done()):
                self._state = 9
        if (self._state == 9): # Allow User Input (Post-Scan)
            enable = solve_trigger
            if (enable):
                self._state = 10
        if (self._state == 10 and top_state == 4):
            # Placeholder
            self._state = 11
        if (self._state == 11 and top_state == 5):
            talk()
            self._state = 12
        if (self._state == 15 and top_state == 7):
            enable = first_trigger
            if (enable):
                self._state = 0
        return enable

    def get_state(self):
        return self._state
    
    def can_talk(self):
        return self._state in driver_fsm._talk_allowed

