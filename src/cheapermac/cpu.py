import multiprocessing

def cpu_busy_loop():
    """Simple busy loop to consume CPU cycles."""
    try:
        while True:
            # Just some basic arithmetic to keep CPU busy
            _ = 1 * 1
    except KeyboardInterrupt:
        pass

def start_cpu_simulation(busy_cores):
    """Starts busy_cores amount of processes for CPU simulation."""
    cpu_processes = []
    for _ in range(busy_cores):
        p = multiprocessing.Process(target=cpu_busy_loop)
        p.daemon = True
        p.start()
        cpu_processes.append(p)
    return cpu_processes

def stop_cpu_simulation(cpu_processes):
    """Terminates all given CPU processes."""
    for p in cpu_processes:
        p.terminate()
