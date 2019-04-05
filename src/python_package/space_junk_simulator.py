
import ctypes
import numpy
import glob
import os
from ctypes import *

class Object(ctypes.Structure):

    _fields_ = [('x', ctypes.POINTER(ctypes.c_double)),
                ('y', ctypes.POINTER(ctypes.c_double)),
                ('z', ctypes.POINTER(ctypes.c_double)),
                ('vx', ctypes.POINTER(ctypes.c_double)),
                ('vy', ctypes.POINTER(ctypes.c_double)),
                ('vz', ctypes.POINTER(ctypes.c_double)),
                ('size', ctypes.POINTER(ctypes.c_double)),
               ]

class space_simulator:
    def __init__(self, gpu = False):
        #print(os.getcwd())
        # cur_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        so_cpu_path = ('src/python_package/python_package_cpu.so')
        self.cpu_lib = ctypes.CDLL(so_cpu_path)
        self.cpu_lib.solve_cpu.argtypes = [numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # x
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # y
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # z
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vx
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vy
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vz
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # x_res
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # y_res
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # z_res
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vx_res
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vy_res
                                          numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vz_res
                                          c_size_t,
                                          c_double]

        self.cpu_lib.solve_cpu.restype = None
        print("Ok!")

        if gpu:
            so_gpu_path = ('/python_package_cpu.so')
            self.solver_gpu = ctypes.CDLL(cur_path + so_gpu_path)
            self.solver_gpu.main_.argtypes = [numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # x
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # y
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # z
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vx
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vy
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vz
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # x_res
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # y_res
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # z_res
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vx_res
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vy_res
                                              numpy.ctypeslib.ndpointer(dtype=numpy.float64, flags="C_CONTIGUOUS"),  # vz_res
                                              c_size_t,
                                              c_double]

            self.solver_gpu.main_.restype = None

    def run(self, x, y, z, vx, vy, vz, vzsteps=10, timestep = 1.0, gpu = False):
        x_res, y_res, z_res, vx_res, vy_res, vz_res = x, y, z, vx, vy, vz

        if gpu==False:
            self.cpu_lib.solve_cpu(x, y, z, vx, vy, vz, x_res, y_res, z_res, vx_res, vy_res, vz_res, vzsteps, timestep)
        else:
            self.solver_gpu.solve_gpu(x, y, z, vx, vy, vz, x_res, y_res, z_res, vx_res, vy_res, vz_res, vzsteps, timestep)

        print("run!")
        return x_res, y_res, z_res, vx_res, vy_res, vz_res



