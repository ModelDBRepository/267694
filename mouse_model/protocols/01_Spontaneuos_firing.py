from Purkinje_morpho_1 import Purkinje_Morpho_1
from neuron import h,gui
import multiprocessing
from Purkinje_morpho_1_number import number_ind_1
import numpy as np
import matplotlib.pyplot as plt

Hines = h.CVode()
Hines.active(0)

spines_on = 0 # switch between 0 (no spines) and 1 (spines)

stimdata = dict()
stimdata['timeglobal'] = 20000

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
print(cpu)

h.dt = 0.025
h.celsius = 32
h.tstop = stimdata['timeglobal']
h.v_init = -65

def initialize():
    h.finitialize()
    h.run()

initialize()

if spines_on == 0:
    #save files
    np.savetxt('01_vm_soma_no_spines.txt', np.column_stack((np.array(cell.time_vector), np.array(cell.vm_soma))), delimiter = ' ')

    img = plt.plot(np.array(cell.time_vector), np.array(cell.vm_soma))
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig('01_vm_soma_nospines.eps')
    plt.close()
if spines_on == 1:
    #save files
    np.savetxt('01_vm_soma_spines.txt', np.column_stack((np.array(cell.time_vector), np.array(cell.vm_soma))), delimiter = ' ')

    img = plt.plot(np.array(cell.time_vector), np.array(cell.vm_soma))
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig('01_vm_soma_spines.eps')
    plt.close()
quit()

