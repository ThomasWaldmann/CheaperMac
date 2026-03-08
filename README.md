# MacNeoSimulator - 8GB RAM Life Simulator

MacNeoSimulator is a tool designed to simulate the experience of living with restricted system resources (like 8GB RAM or fewer CPU cores) on a more powerful machine.

## How it works

- **Memory Simulation**: The tool calculates the difference between your total system RAM and a memory limit (defaulting to 8GB) and allocates that extra memory. It then uses `mlock` to lock it into physical RAM, preventing the operating system from swapping it out.
- **CPU Simulation**: The tool can simulate fewer CPU cores by spawning busy-loop processes that consume the extra cores, making them unavailable for other tasks.

This creates an environment where you can test workflows, develop software, or just browse the web under the constraints of a less powerful machine.

## Prerequisites

- Python 3.x
- `psutil` library

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the simulation with the default memory limit of 8GB:

```bash
python simulator.py
```

Specify a different memory limit (e.g., 4GB) and CPU limit (e.g., 4 cores):

```bash
python simulator.py --memory 4.0 --cpu 4
```

To stop the simulation and free the resources, simply press `Ctrl+C` in the terminal.

## Safety Features

- **Progressive Allocation**: Allocates memory in chunks to prevent sudden system spikes.
- **Memory Locking**: Uses `mlock` where available to ensure allocated memory stays in physical RAM and isn't swapped to disk.
- **CPU Isolation**: Uses separate processes for CPU busy-loops to ensure they effectively consume core capacity.
- **Safety Buffer**: Automatically stops memory allocation if available system memory drops below 500MB.
- **Graceful Cleanup**: Frees all allocated memory and terminates busy-loop processes upon exit.

## Important Note

This tool allocates real physical memory. While it has safety checks, using it on a system that is already under high load might lead to performance degradation or application crashes. Use with care.
