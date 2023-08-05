"""
Execute the profiler
"""
from gr_lora_sdr_profiler import main
import sys

def run():
    main.main(sys.argv[1:])
run()