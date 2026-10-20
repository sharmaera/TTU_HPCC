#!/bin/bash

#SBATCH -J dmtcp_job
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH -p nocona
#SBATCH --export=ALL
#SBATCH --time=48:00:00

# Load DMTCP
module load gcc/14.2.0 dmtcp/4.0.0

# Directory for checkpoint files
export DMTCP_CHECKPOINT_DIR=$PWD/dmtcp_checkpoints

mkdir -p "$DMTCP_CHECKPOINT_DIR"

# Coordinator configuration
export DMTCP_COORD_HOST=$(hostname)
export DMTCP_COORD_PORT=7779

echo "Checkpoint directory: $DMTCP_CHECKPOINT_DIR"
echo "Coordinator host: $DMTCP_COORD_HOST"
echo "Coordinator port: $DMTCP_COORD_PORT"

# Start DMTCP coordinator
dmtcp_coordinator \
    --daemon \
    --port $DMTCP_COORD_PORT

# IMPORTANT:
# Python must be launched THROUGH dmtcp_launch
dmtcp_launch \
    --join-coordinator \
    --coord-host $DMTCP_COORD_HOST \
    --coord-port $DMTCP_COORD_PORT \
    python testing_dmtcp2.py
