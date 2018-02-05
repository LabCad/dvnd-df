#!/bin/bash
./runexp.sh 1 1 2 rvnd > rvnd_n1w1g2.out
./runexp.sh 1 1 2 dvnd > dvnd_n1w1g2.out
./runexp.sh 1 2 2 rvnd > rvnd_n1w2g2.out
./runexp.sh 1 2 2 dvnd > dvnd_n1w2g2.out
./runexp.sh 1 3 2 rvnd > rvnd_n1w3g2.out
./runexp.sh 1 3 2 dvnd > dvnd_n1w3g2.out
./runexp.sh 1 4 2 rvnd > rvnd_n1w4g2.out
./runexp.sh 1 4 2 dvnd > dvnd_n1w4g2.out

# Remover
#./runexp.sh 1 1 1 rvnd > rvnd_n1w1g2.out
#./runexp.sh 1 1 1 dvnd > dvnd_n1w1g2.out
#./runexp.sh 1 2 1 rvnd > rvnd_n1w2g2.out

