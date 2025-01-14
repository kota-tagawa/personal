#!/bin/bash
#PBS -q wEduq
#PBS -l select=1:ncpus=1
#PBS -v DOCKER_IMAGE=prg-env:latest

ulimit -c 0
source /etc/profile
. /common/intel-2022/compiler/latest/env/vars.sh
. /common/intel-2022/mkl/latest/env/vars.sh

export OMP_NUM_THREADS=4
cd $PBS_O_WORKDIR
icx -qopenmp e06_223337.c -o e06.x
./e06.x