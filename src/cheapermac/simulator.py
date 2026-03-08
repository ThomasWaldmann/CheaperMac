import sys
import time
import psutil
from .cpu import start_cpu_simulation, stop_cpu_simulation
from .memory import get_libc, allocate_memory_in_chunks


class CheaperMac:
    def __init__(self, memory_gb, cpu_limit):
        self.memory_bytes = int(memory_gb * (1024**3))
        self.total_bytes = psutil.virtual_memory().total
        self.eat_bytes = self.total_bytes - self.memory_bytes
        self.allocated_memory = []

        self.cpu_limit = cpu_limit
        self.total_cores = psutil.cpu_count(logical=True)
        self.busy_cores = 0
        if cpu_limit is not None:
            self.busy_cores = max(0, self.total_cores - int(cpu_limit))
        self.cpu_processes = []

        # Load libc for memory locking (mlock)
        self.libc = get_libc()

        if self.eat_bytes <= 0 and self.busy_cores <= 0:
            print(
                f"Current resources (RAM: {self.total_bytes / (1024**3):.2f} GB, CPU: {self.total_cores} cores) are already within limits."
            )
            sys.exit(0)

    def allocate(self):
        if self.busy_cores > 0:
            print(f"System Total Cores: {self.total_cores}")
            print(f"CPU core limit to simulate: {self.cpu_limit}")
            print(
                f"Starting {self.busy_cores} busy loops to simulate core reduction..."
            )
            self.cpu_processes = start_cpu_simulation(self.busy_cores)
            print(f"CPU simulation started.")

        if self.eat_bytes > 0:
            print(f"System Total RAM: {self.total_bytes / (1024**3):.2f} GB")
            print(f"Memory limit to simulate: {self.memory_bytes / (1024**3):.2f} GB")
            print(
                f"Attempting to lock approximately {self.eat_bytes / (1024**3):.2f} GB of RAM into physical memory..."
            )

            try:
                self.allocated_memory = allocate_memory_in_chunks(
                    self.eat_bytes, self.libc
                )
            except KeyboardInterrupt:
                self.cleanup()
        else:
            print(
                f"Memory limit ({self.memory_bytes / (1024**3):.2f} GB) already met. No RAM will be locked."
            )

        print("Simulation is active.")
        print("Press Ctrl+C to stop the simulation and free resources.")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.cleanup()

    def cleanup(self):
        if self.busy_cores > 0:
            print("\nStopping CPU busy loops...")
            stop_cpu_simulation(self.cpu_processes)
            print("CPU processes stopped.")

        if self.allocated_memory:
            print("Releasing memory...")
            self.allocated_memory = []
            print("Memory released.")

        print("Exiting.")
        sys.exit(0)
