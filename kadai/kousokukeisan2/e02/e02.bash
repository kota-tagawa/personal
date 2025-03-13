#!/bin/bash
#PBS -q wEduq
#PBS -l select=1:ncpus=4
#PBS -v DOCKER_IMAGE=prg-env:latest

ulimit -c 0
source /etc/profile
. /common/intel-2022/compiler/latest/env/vars.sh
. /common/intel-2022/mkl/latest/env/vars.sh

export OMP_NUM_THREADS=4
cd $PBS_O_WORKDIR
gcc -O0 -o e02.x 223337_e02.c
./e02.x