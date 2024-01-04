from Purkinje_morpho_1 import Purkinje_Morpho_1
from neuron import h,gui
import multiprocessing
from Purkinje_morpho_1_number import number_ind_1
import numpy as np
import matplotlib.pyplot as plt

from toolbox_pc import *

Hines = h.CVode()
Hines.active(0)

spines_on = 0 #Simulated only without spines

stimdata = dict()

stimdata['timeglobal'] = 2000

cell = Purkinje_Morpho_1(spines_on)

h('load_file("vm.ses")')
h.nrncontrolmenu()
    
cpu = multiprocessing.cpu_count()
h.load_file("parcom.hoc")
p = h.ParallelComputeTool()
if spines_on == 0:
    p.change_nthread(cpu,1)
    print('spines_off')
else:    
    p.change_nthread(16,1)
    print('spines_on')
p.multisplit(1)

stim = [h.IClamp(0.5,sec=cell.soma[0])]

stim[0].delay = 0
stim[0].dur = 2000
stim[0].amp = 0

v = vec_inject(0.025,2000,1.6,[500, 500, 500, 500])
v.play(stim[0]._ref_amp, 0.025)

h.dt = 0.025
h.celsius = 32
h.tstop = stimdata['timeglobal']
h.v_init = -65 

indiv_number = number_ind_1['indiv']

def initialize():
    h.finitialize()
    h.run()
    
initialize()


#save files
np.savetxt('03_vm_soma_no_spines.txt', np.column_stack((np.array(cell.time_vector), np.array(cell.vm_soma))), delimiter = ' ')

img = plt.plot(np.array(cell.time_vector), np.array(cell.vm_soma))
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.savefig('03vm_soma_nospines.eps')
plt.close()

quit()
