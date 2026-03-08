import argparse
import signal
import multiprocessing
from cheapermac.simulator import CheaperMac


def main():
    multiprocessing.freeze_support()
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

    simulator = CheaperMac(args.memory, args.cpu)

    # Register signal for clean exit
    signal.signal(signal.SIGINT, lambda s, f: simulator.cleanup())
    signal.signal(signal.SIGTERM, lambda s, f: simulator.cleanup())

    simulator.allocate()


if __name__ == "__main__":
    main()
