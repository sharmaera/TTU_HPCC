#!/bin/bash
#SBATCH -J dmtcp_restart
#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH -o %x.%j.out
#SBATCH -e %x.%j.err
#SBATCH -p nocona
#SBATCH --export=ALL

# Load the SAME dmtcp/gcc versions used to create the checkpoint
module load gcc/14.2.0 dmtcp/4.0.0

# Go to where the checkpoint files and restart script live
cd /lustre/scratch/ersharma/dataset/dmtcp/blast/dmtcp_checkpoints

chmod +x dmtcp_restart_script.sh

# Coordinator will run on whichever node this job lands on —
# override the old coord-host (cpu-26-18) baked into the script
./dmtcp_restart_script.sh \
    --coord-host $(hostname) \
    --coord-port 7779
