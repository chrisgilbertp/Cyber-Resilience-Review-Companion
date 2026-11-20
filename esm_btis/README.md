# Online Resource 1

**Energy efficiency in neuromorphic computing and spiking neural networks at scale**  
*Brain Theory and Intelligence Science*

Chris Gilbert, Duah Jeremiah Leakpor, Kwitee D. Gaylah, John K. Constance, Maxwell Dorgbefu Jnr, and Mercy A. Gilbert

**Correspondence**  
Chris Gilbert, Department of Computer Science and Engineering, College of Engineering and Technology, William V. S. Tubman University, Harper, Maryland County, Liberia.  
cabilimi@tubmanu.edu.lr

## Contents

- Fig. 1 is a schematic of a workload boundary and the event-processing pathway.
- Fig. 2 is a deterministic sensitivity calculation using illustrative inputs.
- Fig. 3 compares two published matrix–vector operating modes on one PCM chip.
- Fig. 4 compares reported energy per inference on an ESP32-C6 microcontroller.

`break_even_assumptions.csv` contains the illustrative parameters in Section 6.2.  
The normalized fixed and dense-event costs are 0.10 and 0.24. The state costs are 0.0125, 0.025, and 0.05 per timestep. The reference energy is set to one. The calculation treats one decision horizon as a fixed number of integer steps. Only the plot clips the break-even curve to the admissible range of 0 to 100%.

`pcm_operating_modes.csv` transcribes published point values for 8-bit-input, 8-bit-output matrix–vector operations. Internal read precision differs between the four-phase and one-phase modes. Source: Le Gallo et al. (2023), *Nature Electronics* 6:680–693.  
https://doi.org/10.1038/s41928-023-01010-1

`microcontroller_inference.csv` transcribes the four energy values reported in the abstract of Hansert, Gechter, and Offermann (2026), *International Journal of Neural Systems*. The conventional network has no simulation-step setting. The spiking network was tested at 1, 3, and 10 steps with the same task and device. The derived percentage reductions use the reported ANN point as the denominator.  
https://doi.org/10.1142/S0129065727500092

`reproduce.py` regenerates the numerical results and figures from the CSV inputs.

## Run

```bash
python3 reproduce.py
```

Requires Python 3 and Matplotlib for figure generation. All calculations use the values transcribed from the cited sources or the illustrative parameters stated in the manuscript.
