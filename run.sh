#!/bin/Bash
# shellcheck disable=SC2164
cd Vcdwavedir
python -m pytest ../TestBench/sdramtest.py --dump-vcd
echo "generate vcd file successful"
# pytest command
# -s
# -tb
# -x
# -v
# -