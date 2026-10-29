# Custom Phase 1 Processor Topologies

The Phase 1 Master Guide treats coupling maps as *reference architectures only* and explicitly permits teams to design alternative valid maps. The below are participant-designed graphs, not official hardware calibrations.

Processor A: 5 qubits, branching tree with edges `(0,1), (0,2), (0,3), (3,4)`.

Processor B: 9 qubits, 12 edges `(0,1), (0,2), (1,3), (1,4), (2,3), (3,4), (3,5), (3,8), (4,5), (4,6), (5,7), (6,7)`.

Edge connections are modeled bidirectionally. Basis: `rz`, `sx`, `x`, `cx`; same Master Guide synthetic noise rates apply to both. Exact physical connectivity and qubit placement can affect compiled circuit metrics.
