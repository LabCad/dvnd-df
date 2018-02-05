#!/bin/bash
./runexp.sh 1 1 4 rvnd > rvnd_n1w1g4.out
./runexp.sh 1 1 4 dvnd > dvnd_n1w1g4.out
./runexp.sh 1 2 4 rvnd > rvnd_n1w2g4.out
./runexp.sh 1 2 4 dvnd > dvnd_n1w2g4.out
./runexp.sh 1 3 4 rvnd > rvnd_n1w3g4.out
./runexp.sh 1 3 4 dvnd > dvnd_n1w3g4.out
./runexp.sh 1 4 4 rvnd > rvnd_n1w4g4.out
./runexp.sh 1 4 4 dvnd > dvnd_n1w4g4.out

# Remover
#./runexp.sh 1 4 1 rvnd > rvnd_n1w4g1.out
#./runexp.sh 1 4 1 dvnd > dvnd_n1w4g1.out
