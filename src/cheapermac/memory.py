import ctypes
import ctypes.util
import psutil


def get_libc():
    """Tries to find and load libc for mlock."""
    libc = None
    try:
        libc_path = ctypes.util.find_library("c")
        if libc_path:
            libc = ctypes.CDLL(libc_path)
            if hasattr(libc, "mlock"):
                libc.mlock.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
                libc.mlock.restype = ctypes.c_int
    except Exception:
        # Fallback if ctypes or libc fails
        pass
    return libc


def lock_memory_chunk(libc, chunk, chunk_size):
    """Locks a chunk of memory using mlock if available."""
    if libc and hasattr(libc, "mlock"):
        try:
            # Get address of bytearray buffer
            c_buf = (ctypes.c_byte * chunk_size).from_buffer(chunk)
            addr = ctypes.addressof(c_buf)
            # Lock the memory chunk
            libc.mlock(addr, chunk_size)
        except Exception:
            # Fallback if locking fails, just continue with regular allocation
            pass


def allocate_memory_in_chunks(eat_bytes, libc):
    """Allocates memory in chunks and returns a list of allocated chunks."""
    allocated_memory = []
    # We allocate in chunks of 100MB to avoid sudden spikes and allow graceful interruption
    chunk_size = 100 * 1024 * 1024
    chunks_needed = int(eat_bytes // chunk_size)

    for i in range(chunks_needed):
        # Allocate chunk and touch it to ensure it's in physical memory
        chunk = bytearray(chunk_size)
        # Touching memory is important so the OS actually commits it to RAM
        for j in range(0, chunk_size, 4096):
            chunk[j] = 1

        # Use mlock to prevent OS from swapping this chunk out
        lock_memory_chunk(libc, chunk, chunk_size)

        allocated_memory.append(chunk)

        if (i + 1) % 10 == 0 or (i + 1) == chunks_needed:
            print(f"Allocated: {(i + 1) * chunk_size / (1024**3):.2f} GB...")

        # Check current available memory to avoid triggering swap or OOM killer
        vm = psutil.virtual_memory()
        if vm.available < (500 * 1024 * 1024):  # Keep at least 500MB safety buffer
            print(
                "Safety limit reached: Stopping allocation to prevent system instability."
            )
            break

    return allocated_memory
