# CheaperMac - living with a cheaper, less powerful Mac.

CheaperMac is a tool designed to simulate the experience of living
with a less powerful Mac than the machine running the simulator:

- fewer CPU cores
- less memory (RAM)

## How it works

- **CPU Simulation**: The tool can simulate fewer CPU cores by spawning
  busy-loop processes that consume the extra cores, making them unavailable 
  for other tasks.
- **Memory Simulation**: The tool calculates the difference between your total
  system RAM and a memory target and allocates that extra memory. It then uses
  `mlock` to lock it into physical RAM, preventing the operating system from 
  swapping it out.

## Installation

Either download the binary from Github releases page or
use ``pip install cheapermac`` to install it from PyPI.

## Usage (CLI)

Run the `cheapermac` command in a terminal window:

```bash
cheapermac  # use the defaults (same as shown below)
cheapermac --cpu 5 --memory 8.0  # leave 5 cores and 8 GB free to use
```

To stop the simulation, simply press `Ctrl+C` in the terminal.

The defaults are similar to the resources offered on a Macbook Neo 2026.

## Important Notes

This tool allocates real physical memory. While it has safety checks,
using it on a system that is already under high load might lead to
performance degradation or application crashes. Use with care.

The simulation is not perfect:

It does nothing to simulate other differences, like SSD I/O, GPU, cooling,
USB speed, network speed, etc.

It only deals with CPU core counts, not with speed differences of the cores,
like super/performance/efficiency cores or just older/newer cores.

While the simulation is running, it keeps the excess CPU cores busy.
This causes a higher than usual power consumption, more heat and potentially
more fan activity. You need to ignore these side effects, they won't happen
on the cheaper Mac.

## Demo
```bash
# Running on a Macbook Pro M3 Pro with 12 cores and 18 GB of RAM:
tw@MacBook-Pro Downloads % ./cheapermac          
System Total Cores: 12
CPU core limit to simulate: 5
Starting 7 busy loops to simulate core reduction...
CPU simulation started.
System Total RAM: 18.00 GB
Memory limit to simulate: 8.00 GB
Attempting to lock approximately 10.00 GB of RAM into physical memory...
Allocated: 0.98 GB...
Allocated: 1.95 GB...
Allocated: 2.93 GB...
Allocated: 3.91 GB...
Allocated: 4.88 GB...
Allocated: 5.86 GB...
Allocated: 6.84 GB...
Allocated: 7.81 GB...
Allocated: 8.79 GB...
Allocated: 9.77 GB...
Allocated: 9.96 GB...
Simulation is active.
Press Ctrl+C to stop the simulation and free resources.
^C
Stopping CPU busy loops...
CPU processes stopped.
Releasing memory...
Memory released.
Exiting.
```
