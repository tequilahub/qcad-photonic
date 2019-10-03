"""
If you did not add the location of the code for OpenVQE and Photonic
to your PYTHONPATH you have to do it here
uncomment the line below and add the correct paths
You need to change the paths of course
"""
#import sys
#sys.path.append("/home/jsk/projects/OpenVQE/")
#sys.path.append("/home/jsk/projects/photonic-qc/code/")

from photonic import PhotonicSetup
from openvqe.simulator.simulator_qiskit import SimulatorQiskit
from openvqe.simulator.simulator_cirq import SimulatorCirq

"""
Here we create a parity sort setup from BeamSplitter and DovePrism

I assume that the Trotter decomposition can be improved to get better results (currently the two target states
are asymetric)

Count will differ from run to run and by how you set samples and trotter step
"""

if __name__ == "__main__":
    """
    Set The Parameters here:
    """
    S = 1                           # Modes will run from -S ... 0 ... +S
    qpm = 2                         # Qubits per mode
    trotter_steps = 10              # number of trotter steps for the BeamSplitter
    samples = 100                   # number of samples to simulate
    istate = "|100>_a|000>_b"       # initial state for this test
    # the state is denoted in occupation numbers |occ(mode(-S)) ... 0 ... occ(mode(S))>_path
    # i.e. |100>_a|100>b means: 1 photon in mode -1 in path a, and the same for path b
    # note that the initial state has to be denoted consistently with S
    # so if S=2 the same state would be |01000>_a|01000>
    simulator = SimulatorQiskit()   # Pick the Simulator
    # Alternatives
    # SimulatorCirq: Googles simulator
    # SimulatorQiskit: IBM simulator
    # SimulatorPyquil: Rigettis simulator, the quantum virtual machine needs to run in the background
    # Pyquil is broken currently ... Sorry

    """
    Here comes the actual code
    """

    setup = PhotonicSetup(pathnames=['a', 'b'], S=S, qpm=qpm)
    setup.BeamSplitter(path_a='a', path_b='b', t=0.25, steps=trotter_steps)
    setup.DovePrism(path='a', mode=0, t=1.0)
    setup.BeamSplitter(path_a='a', path_b='b', t=0.25, steps=trotter_steps)
    counts=setup.run(initial_state=istate, samples=samples, simulator=simulator)
    counts.plot(title="Parity Sort: Initial state was " + istate)
