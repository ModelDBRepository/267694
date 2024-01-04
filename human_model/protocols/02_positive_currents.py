from Purkinje_morpho_1 import Purkinje_Morpho_1
from neuron import h
import multiprocessing
from Purkinje_morpho_1_number import number_ind_1
import numpy as np
import matplotlib.pyplot as plt

Hines = h.CVode()
Hines.active(0)

spines_on = 0 # switch between 0 (no spines) and 1 (spines)

stimdata = dict()
stimdata['stim0del'] = 300
stimdata['stim0dur'] = 1000
stimdata['stim0amp'] = 0.3

stimdata['stim1del'] = 1300
stimdata['stim1dur'] = 1000
stimdata['stim1amp'] = 0.6

stimdata['stim2del'] = 2300
stimdata['stim2dur'] = 1000
stimdata['stim2amp'] = 0.9

stimdata['stim3del'] = 3300
stimdata['stim3dur'] = 1000
stimdata['stim3amp'] = 1.2

stimdata['stim4del'] = 4300
stimdata['stim4dur'] = 1000
stimdata['stim4amp'] = 1.5

stimdata['stim5del'] = 5300
stimdata['stim5dur'] = 1000
stimdata['stim5amp'] = 1.8

stimdata['stim6del'] = 6300
stimdata['stim6dur'] = 1000
stimdata['stim6amp'] = 2.1

stimdata['stim7del'] = 7300
stimdata['stim7dur'] = 1000
stimdata['stim7amp'] = 2.4

stimdata['stim8del'] = 8300
stimdata['stim8dur'] = 1000
stimdata['stim8amp'] = 2.7

stimdata['stim9del'] = 9300
stimdata['stim9dur'] = 1000
stimdata['stim9amp'] = 3

stimdata['stim10del'] = 10300
stimdata['stim10dur'] = 1000
stimdata['stim10amp'] = 3.3

stimdata['stim11del'] = 11300
stimdata['stim11dur'] = 1000
stimdata['stim11amp'] = 3.6

stimdata['stim12del'] = 12300
stimdata['stim12dur'] = 1000
stimdata['stim12amp'] = 3.9

stimdata['stim13del'] = 13300
stimdata['stim13dur'] = 1000
stimdata['stim13amp'] = 4.2

stimdata['stim14del'] = 14300
stimdata['stim14dur'] = 1000
stimdata['stim14amp'] = 4.5

stimdata['timeglobal'] = 15300

cell = Purkinje_Morpho_1(spines_on)

cpu = multiprocessing.cpu_count()
h.load_file("parcom.hoc")
p = h.ParallelComputeTool()
if spines_on == 0:
    p.change_nthread(cpu,1)
    print('spines_off')
else:    
    p.change_nthread(32,1)
    print('spines_on')
p.multisplit(1)
print(cpu)

h('load_file("vm.ses")')
h.nrncontrolmenu()

stim = [h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0]), h.IClamp(0.5,sec=cell.soma[0])] 

stim[0].delay = stimdata['stim0del']
stim[0].dur = stimdata['stim0dur']
stim[0].amp = stimdata['stim0amp'] 

stim[1].delay = stimdata['stim1del']
stim[1].dur = stimdata['stim1dur']
stim[1].amp = stimdata['stim1amp'] 

stim[2].delay = stimdata['stim2del']
stim[2].dur = stimdata['stim2dur']
stim[2].amp = stimdata['stim2amp'] 

stim[3].delay = stimdata['stim3del']
stim[3].dur = stimdata['stim3dur']
stim[3].amp = stimdata['stim3amp'] 

stim[4].delay = stimdata['stim4del']
stim[4].dur = stimdata['stim4dur']
stim[4].amp = stimdata['stim4amp'] 

stim[5].delay = stimdata['stim5del']
stim[5].dur = stimdata['stim5dur']
stim[5].amp = stimdata['stim5amp'] 

stim[6].delay = stimdata['stim6del']
stim[6].dur = stimdata['stim6dur']
stim[6].amp = stimdata['stim6amp'] 

stim[7].delay = stimdata['stim7del']
stim[7].dur = stimdata['stim7dur']
stim[7].amp = stimdata['stim7amp'] 

stim[8].delay = stimdata['stim8del']
stim[8].dur = stimdata['stim8dur']
stim[8].amp = stimdata['stim8amp'] 

stim[9].delay = stimdata['stim9del']
stim[9].dur = stimdata['stim9dur']
stim[9].amp = stimdata['stim9amp'] 

stim[10].delay = stimdata['stim10del']
stim[10].dur = stimdata['stim10dur']
stim[10].amp = stimdata['stim10amp'] 

stim[11].delay = stimdata['stim11del']
stim[11].dur = stimdata['stim11dur']
stim[11].amp = stimdata['stim11amp'] 

stim[12].delay = stimdata['stim12del']
stim[12].dur = stimdata['stim12dur']
stim[12].amp = stimdata['stim12amp'] 

stim[13].delay = stimdata['stim13del']
stim[13].dur = stimdata['stim13dur']
stim[13].amp = stimdata['stim13amp'] 

stim[14].delay = stimdata['stim14del']
stim[14].dur = stimdata['stim14dur']
stim[14].amp = stimdata['stim14amp'] 

h.dt = 0.025
h.celsius = 32
h.tstop = stimdata['timeglobal']
h.v_init = -65

indiv_number = number_ind_1['indiv']

def initialize():
    h.finitialize()
    h.run()
    
initialize()

if spines_on == 0:
    #save files
    np.savetxt('02_vm_soma_no_spines.txt', np.column_stack((np.array(cell.time_vector), np.array(cell.vm_soma))), delimiter = ' ')

    img = plt.plot(np.array(cell.time_vector), np.array(cell.vm_soma))
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig('02_vm_soma_nospines.eps')
    plt.close()
if spines_on == 1:
    #save files
    np.savetxt('02_vm_soma_spines.txt', np.column_stack((np.array(cell.time_vector), np.array(cell.vm_soma))), delimiter = ' ')

    img = plt.plot(np.array(cell.time_vector), np.array(cell.vm_soma))
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig('02_vm_soma_spines.eps')
    plt.close()
quit()
