This is the README for Human and mouse Purkinje cell models for the paper:

> Human Purkinje cells outperform mouse Purkinje cells in dendritic complexity and computational capacity
>
> Stefano Masoli, Diana Sanchez-Ponce, Nora Vrieler, Karin Abu-Haya, Vitaly Lerner, Tal
Shahar, Hermina Nedelescu, Martina Francesca Rizza, Ruth Benavides-Piccione, Javier
DeFelipe, Yosef Yarom, Alberto Munoz, Egidio D’Angelo. *Nature Comunication Biology*, 2024.
[https://doi.org/10.1038/s42003-023-05689-y](https://doi.org/10.1038/s42003-023-05689-y)

Purkinje cells in the cerebellum are among the largest neurons in the brain and have been
extensively investigated in rodents. However, their morphological and physiological properties
remain poorly understood in humans. In this study, we utilized high-resolution morphological
reconstructions and unique electrophysiological recordings of human Purkinje cells
ex vivo to generate computational models and estimate computational capacity. An interspecies
comparison showed that human Purkinje cell had similar fractal structures but were
larger than those of mouse Purkinje cells. Consequently, given a similar spine density (2/μm),
human Purkinje cell hosted approximately 7.5 times more dendritic spines than those of mice.
Moreover, human Purkinje cells had a higher dendritic complexity than mouse Purkinje cells
and usually emitted 2–3 main dendritic trunks instead of one. Intrinsic electro-responsiveness
was similar between the two species, but model simulations revealed that the dendrites could
process ~6.5 times (n = 51 vs. n = 8) more input patterns in human Purkinje cells than in
mouse Purkinje cells. Thus, while human Purkinje cells maintained spike discharge properties
similar to those of rodents during evolution, they developed more complex dendrites,
enhancing computational capacity.


Models built by Stefano Masoli in Python3/Neuron8. Stefano.masoli@unipv.it

## Requirement

- The models was implemented in Python3 and NEURON 8
- NEURON 8.2.2 runs the models without issues but the models do not run on NEURON 9, yet.
- Both mouse and human models require a fast CPU. 

The model uses NEURON multisplit to distribute automatically the calculation on all the available cores.

The mouse model is limited to 16 cores and the human model to 32 cores.

## Mouse no spines
A typical 20s simulation takes about 2 and half minutes on an AMD 5950x 16cores/32thread CPU

## Mouse with spines
A typical 20s simulation takes about 28 minutes on an AMD 5950x 16cores/32thread CPU

## Human no spines
A typical 10s simulation takes about 7m on an AMD 5950x 16cores/32thread CPU

## Human with spines
The speed can vary. The normal runtime taken avout 1m time = 100ms simulation on an AMD 5950x 16cores/32thread CPU.



## Usage instructions

Download and extract the archive.

### Under Linux/Unix
Change directory to `Purkinje_human_mice_2023` folder. 
Run `nrnivmodl ./mod_files` to compile the mod files.

To switch between no spine and spine there is a variable in each protocol except for the protocols 03, 05 and 06.

Run `nrngui -python ./protocols/0x_protocol` with `0x_protocol` the name of the Python file in the protocols directory. 


The model is provided with seven protocols able to reproduce:
- 01 - spontaneuos firing
- 02 - Positive current injections
- 03 - Ramp current injection

The number of synapses, types, bursts frequency can be set in the dictionary at the start of the protocol.
- 04 - Random synaptic locations - burst/pause
- 05 - Fixed synaptic locations - burst/pause

- 06 - Spine fixed location - burst/pause

## Attention
The model does not work with the variable time step!

Not tested under NEURON for windows or MAC OS.
