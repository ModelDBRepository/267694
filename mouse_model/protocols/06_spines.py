from Purkinje_morpho_1 import Purkinje_Morpho_1
from Purkinje_morpho_1_number import number_ind_1
from neuron import h,gui
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt

import random as rnd

#per disabilitare tutti i generatori random
seed = 123456
rnd.seed(seed)
h.use_mcell_ran4(1)
h.mcell_ran4_init(seed)

spines_on = 1 # Spine ON (1) ONLY


#fixed time step only
Fixed_step = h.CVode()
Fixed_step.active(0) #the model does not work with the variable time step!

#Instantiation of the cell template
cell = Purkinje_Morpho_1(spines_on) #only spines.

stimdata = dict()
stimdata['timeglobal'] =  2000



##Neuron control menu
h.nrncontrolmenu()

#Voltage graph
#h('load_file("vm.ses")')

#this code discover the number of cores available in a CPU and activate the multisplit to use them all.
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


synapsesdata = dict()

#Excitation
#parallel fiber

synapsesdata['syninterval'] = 10
synapsesdata['synnumber'] = 10
synapsesdata['synstart'] = 1000
synapsesdata['synnoise'] = 0


#new delay factor
synapsesdata['synpfdelay'] = 0

stim_xy = ([0, -0, -0, -0], #AA
            [-92.0, -79.0, 85.0, 102.0], #PF 
            [-0, -0, -0, -0], # AA_SC
            [-0, -0, -0, -0]) #PF_SC







for i in range(len(stim_xy)): #0,0 norrandom and no syn list
    if i == 1:
        cell.spine_heads_x_y(stim_xy[i][0], stim_xy[i][1], stim_xy[i][2], stim_xy[i][3]) 
        
        #percentage of active spine!!
        percentage_spines = 30 
        
        
        cell.activator(1, 1, 0, percentage_spines, 0, 0, 0) #30
        print('local_number_spine', len(cell.pfrand))

    
#print('len AA_1', len(cell.AAdendminmax))
print('len PF_1', len(cell.PFdendminmax))


#synapsesdata['naa'] = len(cell.AAdendminmax)
synapsesdata['npf'] = len(cell.PFdendminmax)


#PF bursts
spk_stim_pf = []
totalstim = int(stimdata['timeglobal']/  synapsesdata['synstart'])

for j in range(int(totalstim)):
    spk_stim = h.NetStim()
    spk_stim.interval=synapsesdata['syninterval']
    spk_stim.number=synapsesdata['synnumber']
    spk_stim.noise=synapsesdata['synnoise']
    spk_stim.start=(synapsesdata['synstart'] * (totalstim - j)) + synapsesdata['synpfdelay']
    
    spk_stim_pf.append(spk_stim)
    spk_nc_pfsyn = []
    j = j-1

print('len pf', len(cell.PFdendminmax))

for m in range(int(totalstim)):	
    spk_nc_pfsyn.append([h.NetCon(spk_stim_pf[m],PF.input,0,0.1,1) for PF in cell.PFdendminmax])
    

h.dt = 0.025
h.celsius = 32
h.tstop = stimdata['timeglobal'] 
h.v_init = -70

    
#initialization and run.    
def initialize():
    h.finitialize()
    h.run()
    
initialize()

if spines_on == 1:
    #save files
    np.savetxt('06_vm_soma_spines.txt', np.column_stack((np.array(cell.time_vector), np.array(cell.vm_soma))), delimiter = ' ')

    img = plt.plot(np.array(cell.time_vector), np.array(cell.vm_soma))
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig('06_vm_soma_spines.eps')
    plt.close()


quit()
