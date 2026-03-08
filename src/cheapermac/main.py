import argparse
import signal
import multiprocessing

from cheapermac import __version__
from cheapermac.simulator import CheaperMac


def main():
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser(
        description="cheapermac - simulate a Mac with restricted resources."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--memory", type=float, default=8.0, help="Memory limit in GB (default: 8.0 GB)"
    )
    parser.add_argument(
        "--cpu", type=int, default=5, help="CPU core limit (default: 5 cores)"
    )
    args = parser.parse_args()

    simulator = CheaperMac(args.memory, args.cpu)

    signal.signal(signal.SIGINT, lambda s, f: simulator.cleanup())
    signal.signal(signal.SIGTERM, lambda s, f: simulator.cleanup())

    simulator.allocate()


if __name__ == "__main__":
    main()
