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

## Prerequisites

- Python 3.x
- `psutil` library

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the simulator and give a memory (GB) and CPU limit (cores):

```bash
python simulator.py --cpu 5 --memory 8.0
```

To stop the simulation, simply press `Ctrl+C` in the terminal.

## Important Notes

This tool allocates real physical memory. While it has safety checks,
using it on a system that is already under high load might lead to
performance degradation or application crashes. Use with care.

The simulation is not perfect:

It does nothing to simulate other differences, like SSD I/O, GPU, cooling,
USB speed, network speed, etc.

It only deals with CPU core counts, not with speed differences of the cores,
like super/performance/efficiency cores or just older/newer cores.
