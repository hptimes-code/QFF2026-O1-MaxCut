# Routing Metrics and SWAP Count

The submission reports compiled circuit depth and native CX count for each processor, together with excess depth/CX relative to an all-to-all compilation reference. Since the final basis is `rz,sx,x,cx`, any SWAP may be decomposed into native gates. Thus zero explicit final `swap` instructions does **not** prove zero inserted routing SWAPs. The current code does not independently measure routing-stage SWAP insertions. See `results/tables/all_architecture.csv` after running the experiments for the quantitative results.
