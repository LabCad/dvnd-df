#!/bin/bash
./runexp.sh 1 1 3 rvnd > rvnd_n1w1g3.out
./runexp.sh 1 1 3 dvnd > dvnd_n1w1g3.out
./runexp.sh 1 2 3 rvnd > rvnd_n1w2g3.out
./runexp.sh 1 2 3 dvnd > dvnd_n1w2g3.out
./runexp.sh 1 3 3 rvnd > rvnd_n1w3g3.out
./runexp.sh 1 3 3 dvnd > dvnd_n1w3g3.out
./runexp.sh 1 4 3 rvnd > rvnd_n1w4g3.out
./runexp.sh 1 4 3 dvnd > dvnd_n1w4g3.out

# Remover
#./runexp.sh 1 2 1 dvnd > dvnd_n1w2g1.out
#./runexp.sh 1 3 1 rvnd > rvnd_n1w3g1.out
#./runexp.sh 1 3 1 dvnd > dvnd_n1w3g1.out

