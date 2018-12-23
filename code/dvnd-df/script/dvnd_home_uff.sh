#!/usr/bin/env bash
# rsync -ravhz --progress --delete --exclude 'build' suggarC imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/

# rsync -ravhz --progress --delete ~/git/dvnd-df/code/dvnd-df imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/dvnd-df/code/
echo "--- Syncing DVND src ---"
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '*.so' --exclude '.git' ~/git/dvnd-df/code/dvnd-df/src/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/dvnd-df/code/dvnd-df/src
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '*.so' --exclude '.git' ~/git/dvnd-df/code/dvnd-df/test/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/dvnd-df/code/dvnd-df/test
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '*.so' --exclude '.git' ~/git/dvnd-df/code/dvnd-df/script/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/dvnd-df/code/dvnd-df/script
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '*.so' --exclude '.git' --exclude '.idea' ~/git/dvnd-df/code/dvnd-df/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/dvnd-df/code/dvnd-df/

echo "--- Syncing SUCURI pyDF ---"
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '.git' ~/git/Sucuri/pyDF/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/Sucuri/pyDF

echo "--- Syncing Simple-PyCUDA ---"
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '.git' ~/git/simple-pycuda/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/simple-pycuda

echo "--- Syncing WAMCA2016 ---"
rsync -ravhz --progress --delete --exclude '.git' ~/git/wamca2016/source/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/wamca2016/source
rsync -ravhz --progress --delete --exclude '.git' ~/git/wamca2016/instances/ rodolfo@sol.ic.uff.br:/home/rodolfo/git/wamca2016/instances

