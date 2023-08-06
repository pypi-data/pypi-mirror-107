#!/bin/sh

set -e

cp /repo/MDI_Mechanic/docker/ssh/config /home/mpiuser/.ssh/config
cp /repo/MDI_Mechanic/docker/ssh/id_rsa.mpi /home/mpiuser/.ssh/id_rsa
cp /repo/MDI_Mechanic/docker/ssh/id_rsa.mpi.pub /home/mpiuser/.ssh/id_rsa.pub
cp /repo/MDI_Mechanic/docker/ssh/id_rsa.mpi.pub /home/mpiuser/.ssh/authorized_keys

chmod 600 /home/mpiuser/.ssh/*
chown -R mpiuser:mpiuser /home/mpiuser/.ssh

exec "$@"
