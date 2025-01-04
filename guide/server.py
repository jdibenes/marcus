
import multiprocessing as mp
import numpy as np
import struct
import cv2
import hl2ss_imshow
import hl2ss
import hl2ss_lnm
import hl2ss_mp
import hl2ss_3dcv


#------------------------------------------------------------------------------
# Camera
#------------------------------------------------------------------------------

class camera:
    CONFIGURATIONS = [
        (1952, 1100, 30), #  0
        (1920, 1080, 30), #  1
        (1504,  846, 30), #  2
        (1280,  720, 30), #  3
        (1128,  636, 30), #  4
        ( 960,  540, 30), #  5
        ( 760,  428, 30), #  6
        ( 640,  360, 30), #  7
        ( 500,  282, 30), #  8
        ( 424,  240, 30), #  9

        (1952, 1100, 15), # 10
        (1920, 1080, 15), # 11
        (1504,  846, 15), # 12
        (1280,  720, 15), # 13
        (1128,  636, 15), # 14
        ( 960,  540, 15), # 15
        ( 760,  428, 15), # 16
        ( 640,  360, 15), # 17
        ( 500,  282, 15), # 18
        ( 424,  240, 15), # 19

        (1952, 1100, 60), # 20
        (1504,  846, 60), # 21
        (1504,  846,  5), # 22
    ]

    FORMATS = [
        ('bgr24', 3), # 0
        ('bgra',  4), # 1
    ]

    def __init__(self, host, configuration_index=6, format_index=0, buffer_size=10, profile=hl2ss.VideoProfile.H265_MAIN, factor=1/100, focus=hl2ss.PV_FocusValue.Min):
        self._host = host
        self._width, self._height, self._framerate = camera.CONFIGURATIONS[configuration_index]
        self._divisor = 1
        self._profile = profile
        self._bitrate = hl2ss_lnm.get_video_codec_bitrate(self._width, self._height, self._framerate, self._divisor, factor)
        self._count = self._framerate*buffer_size
        self._format, self._channels = camera.FORMATS[format_index]

        hl2ss_lnm.start_subsystem_pv(self._host, hl2ss.StreamPort.PERSONAL_VIDEO)

        ipc_rc = hl2ss_lnm.ipc_rc(self._host, hl2ss.IPCPort.REMOTE_CONFIGURATION)
        ipc_rc.open()
        ipc_rc.pv_wait_for_subsystem(True)
        ipc_rc.pv_set_video_temporal_denoising(hl2ss.PV_VideoTemporalDenoisingMode.Off)
        ipc_rc.pv_set_focus(hl2ss.PV_FocusMode.Manual, hl2ss.PV_AutoFocusRange.Normal, hl2ss.PV_ManualFocusDistance.Infinity, focus, hl2ss.PV_DriverFallback.Disable)
        ipc_rc.close()

        producer = hl2ss_mp.producer()
        producer.configure(hl2ss.StreamPort.PERSONAL_VIDEO, hl2ss_lnm.rx_pv(self._host, hl2ss.StreamPort.PERSONAL_VIDEO, width=self._width, height=self._height, framerate=self._framerate, divisor=self._divisor, profile=self._profile, bitrate=self._bitrate, decoded_format=self._format))
        producer.initialize(hl2ss.StreamPort.PERSONAL_VIDEO, self._count)
        producer.start(hl2ss.StreamPort.PERSONAL_VIDEO)

        consumer = hl2ss_mp.consumer()
        sink = consumer.create_sink(producer, hl2ss.StreamPort.PERSONAL_VIDEO, mp.Manager(), None)
        _ = sink.get_attach_response()

        self._producer = producer
        self._consumer = consumer
        self._sink = sink

        self._timestamp = 0
        self._image = np.zeros((self._height, self._width, self._channels), dtype=np.uint8)
        self._focal_length = np.ones((2,), dtype=np.float32)
        self._principal_point = np.zeros((2,), dtype=np.float32)
        self._pose = np.eye(4, 4, dtype=np.float32)
        
    def set(self, prop, value):
        pass

    def get(self, prop):
        if (prop == cv2.CAP_PROP_FRAME_WIDTH):
            return self._width
        if (prop == cv2.CAP_PROP_FRAME_HEIGHT):
            return self._height
        
    def read(self):
        _, data = self._sink.get_most_recent_frame()
        if ((data is not None) and (data.payload.image.size > 0)):
            self._timestamp = data.timestamp
            self._image = data.payload.image
            self._focal_length = data.payload.focal_length
            self._principal_point = data.payload.principal_point
            self._pose = data.pose
            valid = True
        else:
            valid = False
        return valid, self._timestamp, self._image, self._focal_length, self._principal_point, self._pose
    
    def release(self):
        self._sink.detach()
        self._producer.stop(hl2ss.StreamPort.PERSONAL_VIDEO)
        hl2ss_lnm.stop_subsystem_pv(self._host, hl2ss.StreamPort.PERSONAL_VIDEO)


#------------------------------------------------------------------------------
# IPC Command Buffer
#------------------------------------------------------------------------------

class ipc_command_buffer(hl2ss.umq_command_buffer):
    @staticmethod
    def centers_2d_to_unity_3d(cube_centers, scale, focal_length, principal_point, pose):
        intrinsics = hl2ss.create_pv_intrinsics(focal_length, principal_point)
        extrinsics = np.eye(4, 4, dtype=np.float32)
        intrinsics, extrinsics = hl2ss_3dcv.pv_fix_calibration(intrinsics, extrinsics)
        image2camera = hl2ss_3dcv.image_to_camera(intrinsics)
        camera2world = hl2ss_3dcv.camera_to_rignode(extrinsics) @ hl2ss_3dcv.reference_to_world(pose)
        centers = np.zeros((9, 3), dtype=np.float32)
        for i in range(0, 9):
            x, y = cube_centers[i]
            centers[i, :] = hl2ss_3dcv.transform(np.array([x, y, 1], dtype=np.float32).reshape((1, 3)), image2camera)
        l = 0.0
        for i in [0, 1, 3, 4, 6, 7]:
            l += np.linalg.norm(centers[i, :] - centers[i+1, :])
        for i in [0, 1, 2, 3, 4, 5]:
            l += np.linalg.norm(centers[i, :] - centers[i+3, :])
        l /= 12.0
        depth = scale / l if (l != 0) else 0.0
        centers = hl2ss_3dcv.transform(centers * depth, camera2world)
        centers[:, 2] = -centers[:, 2]
        return centers

    def update(self, top_state, state, step_index, step_count, action, warn, cube_centers, scale, focal_length, principal_point, pose, progress, auto_scan, scan_colors):
        detected, centers = (1, ipc_command_buffer.centers_2d_to_unity_3d(cube_centers, scale, focal_length, principal_point, pose).tobytes()) if (cube_centers is not None) else (0, b'')
        data = bytearray()
        data.extend(struct.pack('<BBHHHff', (top_state << 2) | state, (int(auto_scan) << 7) | detected, step_index, step_count, action | warn, scale, progress))
        for color in scan_colors:
            data.extend(struct.pack('<BBBB', color[0], color[1], color[2], color[3]))
        data.extend(centers)
        self.add(0x00000000, bytes(data))

    def configure(self, show_contours, arrow_color, head_factor, thickness, font_size, text_color):
        data = struct.pack('<BBBBfffBBB', int(show_contours), arrow_color[0], arrow_color[1], arrow_color[2], head_factor, thickness, font_size, text_color[0], text_color[1], text_color[2])
        self.add(0x00000001, data)

    def say_step(self):
        self.add(0x00000002, b'')

    def say_process(self):
        self.add(0x00000003, b'')

    def tts_busy(self):
        self.add(0x00000004, b'')

    def acknowledge_vi(self):
        self.add(0x00000005, b'')


#------------------------------------------------------------------------------
# IPC Unity Message Queue
#------------------------------------------------------------------------------

class ipc_umq:
    def __init__(self, host, drain_rate=256):
        self._drain_rate = drain_rate
        self._ipc_umq = hl2ss_lnm.ipc_umq(host, hl2ss.IPCPort.UNITY_MESSAGE_QUEUE)        
        self._pushes = 0

    def open(self):
        self._ipc_umq.open()

    def _get(self):
        data = self._ipc_umq.pull_n(self._pushes)
        self._pushes = 0
        return data

    def _drain(self):
        return self._get() if (self._pushes >= self._drain_rate) else None

    def _push(self, icb):
        self._ipc_umq.push(icb)
        self._drain()
        self._pushes += 1

    def send_update(self, top_state, state, step_index, step_count, action, warn, cube_centers, scale, focal_length, principal_point, pose, progress, auto_scan, scan_colors):
        icb = ipc_command_buffer()
        icb.update(top_state, state, step_index, step_count, action, warn, cube_centers, scale, focal_length, principal_point, pose, progress, auto_scan, scan_colors)
        self._push(icb)

    def send_configure(self, show_contours=False, arrow_color=(255, 0, 255), head_factor=1.0/5.0, thickness=0.002, font_size=0.1, text_color=(255, 255, 255)):
        icb = ipc_command_buffer()
        icb.configure(show_contours, arrow_color, head_factor, thickness, font_size, text_color)
        self._push(icb)

    def send_say_step(self):
        icb = ipc_command_buffer()
        icb.say_step()
        self._push(icb)

    def send_say_process(self):
        icb = ipc_command_buffer()
        icb.say_process()
        self._push(icb)

    def send_tts_busy(self):
        icb = ipc_command_buffer()
        icb.tts_busy()
        self._push(icb)
        return self._get()[-1] != 0
    
    def send_acknowledge_vi(self):
        icb = ipc_command_buffer()
        icb.acknowledge_vi()
        self._push(icb)

    def close(self):
        self._ipc_umq.close()


#------------------------------------------------------------------------------
# IPC Voice Input
#------------------------------------------------------------------------------

class ipc_vi:
    def __init__(self, host, commands):
        self._commands = commands
        self._ipc_vi = hl2ss_lnm.ipc_vi(host, hl2ss.IPCPort.VOICE_INPUT)

    def open(self):
        self._ipc_vi.open()
        self._ipc_vi.start(self._commands)

    def pull(self, confidence=hl2ss.VI_SpeechRecognitionConfidence.Medium):
        events = self._ipc_vi.pop()
        for event in events:
            event.unpack()
        return {self._commands[event.index] : event for event in events if (event.confidence <= confidence)}

    def close(self):
        self._ipc_vi.stop()
        self._ipc_vi.close()

