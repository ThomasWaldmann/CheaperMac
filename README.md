# MacNeoSimulator - 8GB RAM Life Simulator

MacNeoSimulator is a tool designed to simulate the experience of living with restricted system memory (like 8GB on a new MacBook) on a more powerful machine with more RAM.

## How it works

The simulator calculates the difference between your total system RAM and a memory limit (defaulting to 8GB) and allocates that extra memory. It then uses `mlock` to lock it into physical RAM, preventing the operating system from swapping it out and making it truly unavailable for other applications.

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

Specify a different memory limit (e.g., 4GB):

```bash
python simulator.py --memory 4.0
```

To stop the simulation and free the memory, simply press `Ctrl+C` in the terminal.

## Safety Features

- **Progressive Allocation**: Allocates memory in chunks to prevent sudden system spikes.
- **Memory Locking**: Uses `mlock` where available to ensure allocated memory stays in physical RAM and isn't swapped to disk.
- **Safety Buffer**: Automatically stops allocation if available system memory drops below 500MB to prevent crashing or heavy swapping.
- **Graceful Cleanup**: Frees all allocated memory upon exit (via Ctrl+C or SIGTERM).

## Important Note

This tool allocates real physical memory. While it has safety checks, using it on a system that is already under high load might lead to performance degradation or application crashes. Use with care.
