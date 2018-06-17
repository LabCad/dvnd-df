#!/usr/bin/env bash
# rsync -ravhz --progress --delete --exclude 'build' suggarC imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/

# rsync -ravhz --progress --delete ~/git/dvnd-df/code/dvnd-df imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/dvnd-df/code/
echo "--- Syncing DVNS src ---"
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '*.so' ~/git/dvnd-df/code/dvnd-df/src rodolfo@sol.ic.uff.br:/home/rodolfo/git/dvnd-df/code/dvnd-df/src

echo "--- Syncing SUCURI pyDF ---"
rsync -ravhz --progress --delete --exclude '*.pyc' ~/git/Sucuri/pyDF rodolfo@sol.ic.uff.br:/home/rodolfo/git/Sucuri/pyDF

echo "--- Syncing Simple-PyCUDA ---"
rsync -ravhz --progress --delete --exclude '*.pyc' ~/git/simple-pycuda rodolfo@sol.ic.uff.br:/home/rodolfo/git/simple-pycuda

echo "--- Syncing WAMCA2016 ---"
rsync -ravhz --progress --delete ~/git/wamca2016/source rodolfo@sol.ic.uff.br:/home/rodolfo/git/wamca2016/source

