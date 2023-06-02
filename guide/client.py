
import cv2
import ptg
import detector
import server
import visualization
import controller


# Settings --------------------------------------------------------------------

# HoloLens address
host = '192.168.1.7'

# Distance between cube centers in meters
scale = 0.01905 

# Guide parameters
pv_focus = 200
color_integration_length = 10
color_threshold = 10.0
auto_scan = True
scan_explore = True
fail_length = 15
bypass_first = False
bypass_start = False
bypass_scan = False
bypass_solve = False

#------------------------------------------------------------------------------

if (__name__ == '__main__'):
    ptg.cube_explorer.create_cubie_table()

    camera = server.camera(host, focus=pv_focus)
    ipc_umq = server.ipc_umq(host)
    ipc_vi = server.ipc_vi(host, controller.MASTER_LIST)

    ipc_umq.open()
    ipc_vi.open()

    ipc_umq.send_configure()
    
    talk_callback = lambda : ipc_umq.send_say_step()
    talk_done_callback = lambda : not ipc_umq.send_tts_busy()
    
    key_clear = True
    key_last = True

    while (True):
        if ((key_clear) or (key_last)):
            fsm = ptg.experience_fsm(color_threshold, color_integration_length, auto_scan, scan_explore, fail_length, 7 if (key_last) else 1)
            driver = ptg.driver_fsm(15 if (key_last) else 3)
            log = visualization.printer()
            key_first, key_start, key_scan, key_force_scan, key_solve, key_talk_step, key_talk_process, key_clear, key_last = controller.process(None, 0)
            enable = False
            
        valid, timestamp, frame, focal_length, principal_point, pose = camera.read()

        cube_detector = detector.RubiksOpenCV()
        ok = cube_detector.analyze(frame, 3)

        if (ok):
            cube_centers, colors = cube_detector.get_centers_and_colors()
        else:
            cube_centers = None
            colors = ['X']*9

        action, warn = fsm.step(colors if (ok) else None, enable, key_force_scan)

        top_state   = fsm.get_top_state()
        state       = fsm.get_state()
        step_index  = fsm.get_index()
        step_count  = fsm.get_count()
        cube_colors = fsm.get_state_cube()
        side_colors = fsm.get_colors()
        progress    = fsm.get_progress()

        ipc_umq.send_update(top_state, state, step_index, step_count, action, warn, cube_centers, scale, focal_length, principal_point, pose, progress, auto_scan, side_colors)

        log.update(top_state, state, step_index, step_count, action, warn, ok, auto_scan)
        caption = log.print_caption()

        frame = visualization.painter.draw_status(frame, caption, action, cube_centers, colors, cube_colors)
        cv2.imshow('Video', frame)
        key = cv2.waitKey(1) & 0xFF
        if (key == 27): # esc
            break

        enable = driver.step(top_state, step_index, talk_callback, talk_done_callback, key_first or bypass_first, key_start or bypass_start, key_scan or bypass_scan, key_solve or bypass_solve)

        if (driver.can_talk()):
            if (key_talk_step):
                ipc_umq.send_say_step()
                log.print_step()
            if (key_talk_process):
                ipc_umq.send_say_process()
                log.print_process()

        inputs = ipc_vi.pull()
        matches = list(inputs.keys())

        if (len(matches) > 0):
            ipc_umq.send_acknowledge_vi()
            vi = matches[-1]
            visualization.printer.print_user(vi)
        else:
            vi = None

        key_first, key_start, key_scan, key_force_scan, key_solve, key_talk_step, key_talk_process, key_clear, key_last = controller.process(vi, key)
        key_clear = key_clear and (top_state >= 2 and top_state <= 5)

    ipc_umq.close()
    ipc_vi.close()
    camera.release()

