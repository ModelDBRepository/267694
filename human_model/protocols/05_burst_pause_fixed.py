from Purkinje_morpho_1 import Purkinje_Morpho_1
from Purkinje_morpho_1_number import number_ind_1
from neuron import h,gui
import numpy as np
import multiprocessing
import matplotlib.pyplot as plt

from toolbox_pc import *
import random as rnd

spines_on = 0 # This protocols works without spines for speed and sections coordinates

#per disabilitare tutti i generatori random
seed = 123456
rnd.seed(seed)
h.use_mcell_ran4(1)
h.mcell_ran4_init(seed)


#fixed time step only
Fixed_step = h.CVode()
Fixed_step.active(0) #the model does not work with the variable time step!

#Instantiation of the cell template
cell = Purkinje_Morpho_1(spines_on)

stimdata = dict()
stimdata['timeglobal'] =  35500

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
    p.change_nthread(32,1)
    print('spines_on')
p.multisplit(1)
print(cpu)


synapsesdata = dict()

#Excitation
#parallel fiber

synapsesdata['syninterval'] = 5
synapsesdata['synnumber'] = 5
synapsesdata['synstart'] = 1000
synapsesdata['synnoise'] = 0

#ascending axon
synapsesdata['synaainterval'] = 5
synapsesdata['synaanumber'] = 5
synapsesdata['synaastart'] = 1000
synapsesdata['synaanoise'] = 0

#Inhibition
#Stellate on parallel fiber
synapsesdata['synpfstlinterval'] = 7
synapsesdata['synpfstlnumber'] = 3
synapsesdata['synpfstlstart'] = 1000
synapsesdata['synpfstlnoise'] = 0

#new delay factor
synapsesdata['synpfdelay'] = 0
synapsesdata['synaadelay'] = 0
synapsesdata['synpfstldelay'] = 4



#ok
stim_xy = ([30, 180, -410, -270, 1],
            [100, 150, -330, -300, 2],
            [0, 30, -450, -250, 0]) #101 syn
branchPF = "first_branch" 


#stim_xy  = ([130, 250, -210, -50, 1],
            #[200, 235, -190, -150, 2],
            #[140, 250, 0, 10, 0]) #50
#branchPF = "central_branch_50/25" 

#stim_xy = ([370, 500, -380, -200, 1],
            #[450, 500, -300, -200, 2],
            #[500, 600, -400, -250, 0]) #101 syn
#branchPF = "third_branch" 
        
for i in range(0, len(stim_xy)): #0,0 norrandom and no syn list
    cell.dendrites_xy_nospine(stim_xy[i][0], stim_xy[i][1], stim_xy[i][2], stim_xy[i][3], stim_xy[i][4])

print('len AA_1', len(cell.AAdendminmax))
print('len PF_1', len(cell.PFdendminmax))
print('len SC_1', len(cell.SCdendminmax))


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
    

#AA syn
spk_stim_aa = []
totalstim = int(stimdata['timeglobal']/  synapsesdata['synaastart'])

for j in range(int(totalstim)):
    spk_stim_AA = h.NetStim()
    spk_stim_AA.interval=synapsesdata['synaainterval']
    spk_stim_AA.number=synapsesdata['synaanumber']
    spk_stim_AA.noise=synapsesdata['synaanoise']
    spk_stim_AA.start=(synapsesdata['synaastart'] * (totalstim - j)) + synapsesdata['synaadelay']
    
    spk_stim_aa.append(spk_stim_AA)
    spk_nc_aasyn = []
    j = j-1

print('len aa', len(cell.AAdendminmax))

for m in range(int(totalstim)):	
    spk_nc_aasyn.append([h.NetCon(spk_stim_aa[m],aa.input,0,0.1,1) for aa in cell.AAdendminmax])



#SC
spk_stim_SC_complete = []
totalstim_SC = int(stimdata['timeglobal']/  synapsesdata['synpfstlstart'])

for j in range(int(totalstim_SC)):
    spk_stim_SC = h.NetStim()
    spk_stim_SC.interval=synapsesdata['synpfstlinterval']
    spk_stim_SC.number=synapsesdata['synpfstlnumber']
    spk_stim_SC.noise=synapsesdata['synpfstlnoise']
    spk_stim_SC.start=(synapsesdata['synpfstlstart'] * (totalstim_SC - j)) + synapsesdata['synpfstldelay']
    
    spk_stim_SC_complete.append(spk_stim_SC)
    j = j-1

print('len SC', len(cell.SCdendminmax))
spk_nc_SCsyn = []
for m in range(int(totalstim_SC)):	
    spk_nc_SCsyn.append([h.NetCon(spk_stim_SC_complete[m],stl.input,0,0.1,1) for stl in cell.SCdendminmax])


indiv_number = number_ind_1['indiv']
#Basic properties of the simulation. dt, temperature, sim duration and initial voltage


h.dt = 0.025
h.celsius = 32
h.tstop = stimdata['timeglobal']
h.v_init = -70

    
#initialization and run.    
def initialize():
    h.finitialize()
    h.run()
    
initialize()

if spines_on == 0:
    #save files
    np.savetxt('05_vm_soma_no_spines.txt', np.column_stack((np.array(cell.time_vector), np.array(cell.vm_soma))), delimiter = ' ')

    img = plt.plot(np.array(cell.time_vector), np.array(cell.vm_soma))
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig('05_vm_soma_nospines.eps')
    plt.close()





quit()
