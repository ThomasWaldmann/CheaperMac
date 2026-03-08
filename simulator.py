import ctypes
import ctypes.util
import argparse
import multiprocessing
import signal
import sys
import time

import psutil


def cpu_busy_loop():
    """Simple busy loop to consume CPU cycles."""
    try:
        while True:
            # Just some basic arithmetic to keep CPU busy
            _ = 1 * 1
    except KeyboardInterrupt:
        pass


class SmallMachineSimulator:
    def __init__(self, memory_gb, cpu_limit=None):
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
        self.libc = None
        try:
            libc_path = ctypes.util.find_library("c")
            if libc_path:
                self.libc = ctypes.CDLL(libc_path)
                if hasattr(self.libc, "mlock"):
                    self.libc.mlock.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
                    self.libc.mlock.restype = ctypes.c_int
        except Exception:
            # Fallback if ctypes or libc fails
            pass

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
            for _ in range(self.busy_cores):
                p = multiprocessing.Process(target=cpu_busy_loop)
                p.daemon = True
                p.start()
                self.cpu_processes.append(p)
            print(f"CPU simulation started.")

        if self.eat_bytes > 0:
            print(f"System Total RAM: {self.total_bytes / (1024**3):.2f} GB")
            print(f"Memory limit to simulate: {self.memory_bytes / (1024**3):.2f} GB")
            print(
                f"Attempting to lock approximately {self.eat_bytes / (1024**3):.2f} GB of RAM into physical memory..."
            )

            # We allocate in chunks of 100MB to avoid sudden spikes and allow graceful interruption
            chunk_size = 100 * 1024 * 1024
            chunks_needed = self.eat_bytes // chunk_size

            try:
                for i in range(chunks_needed):
                    # Allocate chunk and touch it to ensure it's in physical memory
                    chunk = bytearray(chunk_size)
                    # Touching memory is important so the OS actually commits it to RAM
                    for j in range(0, chunk_size, 4096):
                        chunk[j] = 1

                    # Use mlock to prevent OS from swapping this chunk out
                    if self.libc and hasattr(self.libc, "mlock"):
                        try:
                            # Get address of bytearray buffer
                            c_buf = (ctypes.c_byte * chunk_size).from_buffer(chunk)
                            addr = ctypes.addressof(c_buf)
                            # Lock the memory chunk
                            self.libc.mlock(addr, chunk_size)
                        except Exception:
                            # Fallback if locking fails, just continue with regular allocation
                            pass

                    self.allocated_memory.append(chunk)

                    if (i + 1) % 10 == 0 or (i + 1) == chunks_needed:
                        print(
                            f"Allocated: {(i + 1) * chunk_size / (1024**3):.2f} GB..."
                        )

                    # Check current available memory to avoid triggering swap or OOM killer
                    vm = psutil.virtual_memory()
                    if vm.available < (
                        500 * 1024 * 1024
                    ):  # Keep at least 500MB safety buffer
                        print(
                            "Safety limit reached: Stopping allocation to prevent system instability."
                        )
                        break
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
            for p in self.cpu_processes:
                p.terminate()
            print("CPU processes stopped.")

        if self.allocated_memory:
            print("Releasing memory...")
            self.allocated_memory = []
            print("Memory released.")

        print("Exiting.")
        sys.exit(0)


def signal_handler(sig, frame):
    # This will be handled by the KeyboardInterrupt in the loop
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulate living with restricted computer resources."
    )
    parser.add_argument(
        "--memory", type=float, default=8.0, help="Memory limit in GB (default: 8.0)"
    )
    parser.add_argument(
        "--cpu", type=int, default=None, help="CPU core limit (default: all cores)"
    )
    args = parser.parse_args()

    simulator = SmallMachineSimulator(args.memory, args.cpu)

    # Register signal for clean exit
    signal.signal(signal.SIGINT, lambda s, f: simulator.cleanup())
    signal.signal(signal.SIGTERM, lambda s, f: simulator.cleanup())

    simulator.allocate()
