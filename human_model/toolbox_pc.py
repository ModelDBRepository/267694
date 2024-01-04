# -*- coding: utf-8 -*-

import numpy as np
import scipy.io as io
from neuron import h

def vec_inject(dt,tstop,peak_injection,steps,plot=0):

    steps =np.cumsum(np.array(steps))
    time_vec = np.arange(0,tstop,dt)
    v_inj = np.zeros(time_vec.shape)

    time_rise = time_vec[np.bitwise_and(time_vec>steps[0],time_vec<steps[1])]
    time_fall = time_vec[np.bitwise_and(time_vec>=steps[1],time_vec<steps[2])]

    v_inj[np.bitwise_and(time_vec>steps[0],time_vec<steps[1])] = (time_rise - steps[0])/(steps[1]-steps[0])*peak_injection
    v_inj[np.bitwise_and(time_vec>=steps[1],time_vec<steps[2])] = -(time_fall - steps[2])/(steps[2]-steps[1])*peak_injection

        
    v = h.Vector()
    for x in v_inj:
        v.append(x)

    return v
