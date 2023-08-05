'''
File: autd.py
Project: pyautd
Created Date: 11/02/2020
Author: Shun Suzuki
-----
Last Modified: 24/05/2021
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2020 Hapis Lab. All rights reserved.

'''

import ctypes
from ctypes import c_void_p, byref, c_double
import math
import numpy as np
from functools import singledispatch

from .native_methods import Nativemethods

NATIVE_METHODDS = Nativemethods()


class Gain:
    def __init__(self):
        self.gain_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.autd3capi.AUTDDeleteGain(self.gain_ptr)

    @staticmethod
    def adjust_amp(amp):
        d = math.asin(amp) / math.pi
        return int(510.0 * d)

    @staticmethod
    def grouped(gain_pairs):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDGroupedGain(byref(gain.gain_ptr))
        for (id, gp) in gain_pairs:
            NATIVE_METHODDS.autd3capi.AUTDGroupedGainAdd(gain.gain_ptr, id, gp.gain_ptr)
        return gain

    @singledispatch
    def focal_point(pos, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDFocalPointGain(byref(gain.gain_ptr), pos[0], pos[1], pos[2], duty)
        return gain

    @focal_point.register
    def _(pos, amp: float = 1.0):
        return Gain.focal_point(pos, Gain.adjust_amp(amp))

    @singledispatch
    def bessel_beam(pos, dir, theta_z, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDBesselBeamGain(byref(gain.gain_ptr), pos[0], pos[1], pos[2], dir[0], dir[1], dir[2], theta_z, duty)
        return gain

    @bessel_beam.register
    def _(pos, dir, theta_z, amp: float = 1.0):
        return Gain.bessel_beam(pos, dir, theta_z, Gain.adjust_amp(amp))

    @singledispatch
    def plane_wave(pos, dir, duty: int = 255):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDPlaneWaveGain(byref(gain.gain_ptr), pos[0], pos[1], pos[2], dir[0], dir[1], dir[2], duty)
        return gain

    @plane_wave.register
    def _(pos, dir, amp: float = 1.0):
        duty = Gain.adjust_amp(amp)
        return Gain.plane_wave(pos, dir, duty)

    @staticmethod
    def custom(data):
        size = len(data)
        data = np.array(data).astype(np.uint16)
        data = np.ctypeslib.as_ctypes(data)

        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDCustomGain(byref(gain.gain_ptr), data, size)
        return gain

    @staticmethod
    def __pack_foci(foci):
        size = len(foci)
        foci_array = np.zeros([size * 3]).astype(np.float64)
        for i, focus in enumerate(foci):
            foci_array[3 * i] = focus[0]
            foci_array[3 * i + 1] = focus[1]
            foci_array[3 * i + 2] = focus[2]
        foci_array = np.ctypeslib.as_ctypes(foci_array)
        return foci_array

    def __pack_amps(amps):
        amps = np.array(amps).astype(np.float64)
        amps = np.ctypeslib.as_ctypes(amps)
        return amps

    @staticmethod
    def holo_sdp(foci, amps, alpha: float = 1e-3, lambda_: float = 0.9, repeat: int = 100, normalize: bool = False):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDHoloGainSDP(byref(gain.gain_ptr), backend, foci_array, amps, size, alpha, lambda_, repeat, normalize)
        return gain

    @staticmethod
    def holo_evd(foci, amps, gamma: float = 1, normalize: bool = False):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDHoloGainEVD(byref(gain.gain_ptr), backend, foci_array, amps, size, gamma, normalize)
        return gain

    @staticmethod
    def holo_gs(foci, amps, repeat: int = 100):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDHoloGainGS(byref(gain.gain_ptr), backend, foci_array, amps, size, repeat)
        return gain

    @staticmethod
    def holo_gspat(foci, amps, repeat: int = 100):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDHoloGainGSPAT(byref(gain.gain_ptr), backend, foci_array, amps, size, repeat)
        return gain

    @staticmethod
    def holo_naive(foci, amps):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDHoloGainNaive(byref(gain.gain_ptr), backend, foci_array, amps, size)
        return gain

    @staticmethod
    def holo_lm(foci, amps, eps1: float = 1e-8, eps2: float = 1e-8, tau: float = 1e-3, k_max: int = 5, initial=None):
        size = len(foci)
        foci_array = Gain.__pack_foci(foci)
        amps = Gain.__pack_amps(amps)

        backend = c_void_p()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDEigen3Backend(byref(backend))

        gain = Gain()
        NATIVE_METHODDS.autd3capi_holo_gain.AUTDHoloGainLM(
            byref(
                gain.gain_ptr),
            backend,
            foci_array,
            amps,
            size,
            eps1,
            eps2,
            tau,
            k_max,
            initial,
            0 if initial is None else len(initial))
        return gain

    @staticmethod
    def transducer_test(idx: int, duty: int, phase: int):
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDTransducerTestGain(byref(gain.gain_ptr), idx, duty, phase)
        return gain

    @staticmethod
    def null():
        gain = Gain()
        NATIVE_METHODDS.autd3capi.AUTDNullGain(byref(gain.gain_ptr))
        return gain


class Modulation:
    def __init__(self):
        self.modulation_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.autd3capi.AUTDDeleteModulation(self.modulation_ptr)

    @staticmethod
    def static(amp=255):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDStaticModulation(byref(mod.modulation_ptr), amp)
        return mod

    @staticmethod
    def custom(data):
        size = len(data)
        data = np.array(data).astype(np.uint8)
        data = np.ctypeslib.as_ctypes(data)

        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDSineModulation(byref(mod.modulation_ptr), data, size)
        return mod

    @staticmethod
    def sine(freq: int, amp=1.0, offset=0.5):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDSineModulation(byref(mod.modulation_ptr), freq, amp, offset)
        return mod

    @staticmethod
    def saw(freq: int):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDSawModulation(byref(mod.modulation_ptr), freq)
        return mod

    @staticmethod
    def square(freq: int, low: int = 0, high: int = 255):
        mod = Modulation()
        NATIVE_METHODDS.autd3capi.AUTDSquareModulation(byref(mod.modulation_ptr), freq, low, high)
        return mod


class Sequence:
    def __init__(self):
        self.seq_ptr = c_void_p()

    def __del__(self):
        NATIVE_METHODDS.autd3capi.AUTDDeleteSequence(self.seq_ptr)

    @staticmethod
    def sequence():
        seq = Sequence()
        NATIVE_METHODDS.autd3capi.AUTDSequence(byref(seq.seq_ptr))
        return seq

    @staticmethod
    def circum(center, normal, radius, num_points):
        seq = Sequence()
        NATIVE_METHODDS.autd3capi.AUTDCircumSequence(
            byref(
                seq.seq_ptr),
            center[0],
            center[1],
            center[2],
            normal[0],
            normal[1],
            normal[2],
            radius,
            num_points)
        return seq

    def add_point(self, point):
        NATIVE_METHODDS.autd3capi.AUTDSequenceAddPoint(self.seq_ptr, point[0], point[1], point[2])

    def add_points(self, points):
        size = len(points)
        points_array = np.zeros([size * 3]).astype(np.float64)
        for i, p in enumerate(points):
            points_array[3 * i] = p[0]
            points_array[3 * i + 1] = p[1]
            points_array[3 * i + 2] = p[2]
        points_array = np.ctypeslib.as_ctypes(points_array)

        NATIVE_METHODDS.autd3capi.AUTDSequenceAddPoints(self.seq_ptr, points_array, size)

    def set_frequency(self, freq: float):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSetFreq(self.seq_ptr, freq)

    def frequency(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceFreq(self.seq_ptr)

    def sampling_frequency(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSamplingFreq(self.seq_ptr)

    def sampling_frequency_div(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSamplingFreqDiv(self.seq_ptr)

    def period(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequencePeriod(self.seq_ptr)

    def sampling_period(self):
        return NATIVE_METHODDS.autd3capi.AUTDSequenceSamplingPeriod(self.seq_ptr)


class Link:
    def __init__(self):
        self.link_ptr = c_void_p()

    @staticmethod
    def enumerate_adapters():
        NATIVE_METHODDS.init_autd3capi_soem_link()
        res = []
        handle = c_void_p()
        size = NATIVE_METHODDS.autd3capi_soem_link.AUTDGetAdapterPointer(byref(handle))

        for i in range(size):
            sb_desc = ctypes.create_string_buffer(128)
            sb_name = ctypes.create_string_buffer(128)
            NATIVE_METHODDS.autd3capi_soem_link.AUTDGetAdapter(handle, i, sb_desc, sb_name)
            res.append([sb_name.value.decode('utf-8'), sb_desc.value.decode('utf-8')])

        NATIVE_METHODDS.autd3capi_soem_link.AUTDFreeAdapterPointer(handle)

        return res

    @staticmethod
    def soem_link(ifname, dev_num):
        NATIVE_METHODDS.init_autd3capi_soem_link()
        link = Link()
        NATIVE_METHODDS.autd3capi_soem_link.AUTDSOEMLink(byref(link.link_ptr), ifname.encode('utf-8'), dev_num)
        return link

    @staticmethod
    def twincat_link():
        link = Link()
        NATIVE_METHODDS.autd3capi_twincat_link.AUTDTwinCATLink(byref(link.link_ptr))
        return link


class AUTD:
    def __init__(self):
        self.p_cnt = c_void_p()
        NATIVE_METHODDS.autd3capi.AUTDCreateController(byref(self.p_cnt))
        self.__disposed = False

    def __del__(self):
        self.dispose()

    def last_error():
        size = NATIVE_METHODDS.autd3capi.AUTDGetLastError(None)
        err = ctypes.create_string_buffer(size)
        NATIVE_METHODDS.autd3capi.AUTDGetLastError(err)
        return err.value.decode('utf-8')

    def open(self, link: Link):
        return NATIVE_METHODDS.autd3capi.AUTDOpenController(self.p_cnt, link.link_ptr)

    def firmware_info_list(self):
        res = []
        handle = c_void_p()
        size = NATIVE_METHODDS.autd3capi.AUTDGetFirmwareInfoListPointer(self.p_cnt, byref(handle))

        for i in range(size):
            sb_cpu = ctypes.create_string_buffer(128)
            sb_fpga = ctypes.create_string_buffer(128)
            NATIVE_METHODDS.autd3capi.AUTDGetFirmwareInfo(handle, i, sb_cpu, sb_fpga)
            res.append([sb_cpu.value.decode('utf-8'), sb_fpga.value.decode('utf-8')])

        NATIVE_METHODDS.autd3capi.AUTDFreeFirmwareInfoListPointer(handle)

        return res

    def dispose(self):
        if not self.__disposed:
            self.close()
            self._free()
            self.__disposed = True

    def add_device(self, pos, rot, group_id=0):
        return NATIVE_METHODDS.autd3capi.AUTDAddDevice(self.p_cnt, pos[0], pos[1], pos[2], rot[0], rot[1], rot[2], group_id)

    def add_device_quaternion(self, pos, q, group_id=0):
        return NATIVE_METHODDS.autd3capi.AUTDAddDeviceQuaternion(self.p_cnt, pos[0], pos[1], pos[2], q[0], q[1], q[2], q[3], group_id)

    def synchronize(self, mod_sampling_div: int = 10, mod_buf_size: int = 4000):
        return NATIVE_METHODDS.autd3capi.AUTDSynchronize(self.p_cnt, mod_sampling_div, mod_buf_size)

    def stop(self):
        return NATIVE_METHODDS.autd3capi.AUTDStop(self.p_cnt)

    def close(self):
        return NATIVE_METHODDS.autd3capi.AUTDCloseController(self.p_cnt)

    def clear(self):
        return NATIVE_METHODDS.autd3capi.AUTDClear(self.p_cnt)

    def update_ctrl_flags(self):
        return NATIVE_METHODDS.autd3capi.AUTDUpdateCtrlFlags(self.p_cnt)

    def _free(self):
        NATIVE_METHODDS.autd3capi.AUTDFreeController(self.p_cnt)

    @property
    def is_open(self):
        return NATIVE_METHODDS.autd3capi.AUTDIsOpen(self.p_cnt)

    @property
    def silent_mode(self):
        return NATIVE_METHODDS.autd3capi.AUTDIsSilentMode(self.p_cnt)

    @silent_mode.setter
    def silent_mode(self, value: bool):
        return NATIVE_METHODDS.autd3capi.AUTDSetSilentMode(self.p_cnt, value)

    @property
    def wavelength(self):
        return NATIVE_METHODDS.autd3capi.AUTDWavelength(self.p_cnt)

    @wavelength.setter
    def wavelength(self, wavelength: float):
        NATIVE_METHODDS.autd3capi.AUTDSetWavelength(self.p_cnt, wavelength)

    def reads_fpga_info(self, value: bool):
        NATIVE_METHODDS.autd3capi.AUTDSetReadFPGAInfo(self.p_cnt, value)

    @property
    def fpga_info(self):
        infos = np.zeros([self.num_devices()]).astype(np.ubyte)
        pinfos = np.ctypeslib.as_ctypes(infos)
        NATIVE_METHODDS.autd3capi.AUTDSetReadFPGAInfo(self.p_cnt, pinfos)
        return infos

    def set_output_delay(self, delays):
        size = len(delays)
        delays_ = np.zeros([size]).astype(np.ushort)
        for i, p in enumerate(delays):
            delays_[i] = delays[0]
        delays_ = np.ctypeslib.as_ctypes(delays_)
        return NATIVE_METHODDS.autd3capi.AUTDSetOutputDelay(self.p_cnt, delays_)

    def num_devices(self):
        return NATIVE_METHODDS.autd3capi.AUTDNumDevices(self.p_cnt)

    def num_transducers(self):
        return NATIVE_METHODDS.autd3capi.AUTDNumTransducers(self.p_cnt)

    def send(self, gain: Gain, mod: Modulation):
        return NATIVE_METHODDS.autd3capi.AUTDSendGainModulation(self.p_cnt, gain.gain_ptr, mod.modulation_ptr)

    def send_gain(self, gain: Gain):
        return NATIVE_METHODDS.autd3capi.AUTDSendGain(self.p_cnt, gain.gain_ptr)

    def send_modulation(self, mod: Modulation):
        return NATIVE_METHODDS.autd3capi.AUTDSendModulation(self.p_cnt, mod.modulation_ptr)

    def send_seq(self, seq: Sequence):
        return NATIVE_METHODDS.autd3capi.AUTDSendSequence(self.p_cnt, seq.seq_ptr)

    def add_stm_gain(self, gain: Gain):
        NATIVE_METHODDS.autd3capi.AUTDAddSTMGain(self.p_cnt, gain.gain_ptr)

    def start_stm(self, freq: float):
        return NATIVE_METHODDS.autd3capi.AUTDStartSTM(self.p_cnt, freq)

    def stop_stm(self):
        return NATIVE_METHODDS.autd3capi.AUTDStopSTM(self.p_cnt)

    def finish_stm(self):
        return NATIVE_METHODDS.autd3capi.AUTDFinishSTM(self.p_cnt)

    def device_idx_for_trans_idx(self, idx: int):
        return NATIVE_METHODDS.autd3capi.AUTDDeviceIdxForTransIdx(self.p_cnt, idx)

    def trans_pos_global(self, idx: int):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDTransPositionByGlobal(self.p_cnt, idx, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])

    def trans_pos_local(self, dev_idx: int, trans_idx_local):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDTransPositionByGlobal(self.p_cnt, dev_idx, trans_idx_local, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])

    def device_direction_x(self, dev_idx: int):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDDeviceXDirection(self.p_cnt, dev_idx, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])

    def device_direction_y(self, dev_idx: int):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDDeviceYDirection(self.p_cnt, dev_idx, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])

    def device_direction_z(self, dev_idx: int):
        x = c_double(0.0)
        y = c_double(0.0)
        z = c_double(0.0)
        NATIVE_METHODDS.autd3capi.AUTDDeviceZDirection(self.p_cnt, dev_idx, byref(x), byref(y), byref(z))
        return np.array([x.value, y.value, z.value])
