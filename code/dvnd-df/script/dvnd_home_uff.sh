# rsync -ravhz --progress --delete --exclude 'build' suggarC imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/

# rsync -ravhz --progress --delete ~/git/dvnd-df/code/dvnd-df imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/dvnd-df/code/
echo "--- Syncing DVNS src ---"
rsync -ravhz --progress --delete --exclude '*.pyc' --exclude '*.so' ~/git/dvnd-df/code/dvnd-df/src imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/src

echo "--- Syncing SUCURI pyDF ---"
rsync -ravhz --progress --delete --exclude '*.pyc' ~/git/Sucuri/pyDF imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/pyDF

echo "--- Syncing Simple-PyCUDA ---"
rsync -ravhz --progress --delete --exclude '*.pyc' ~/git/simple-pycuda imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/dvnd-df/code/dvnd-df/simple-pycuda

echo "--- Syncing WAMCA2016 ---"
rsync -ravhz --progress --delete ~/git/wamca2016/source imcoelho@sol.ic.uff.br:/home/imcoelho/Rodolfo/wamca2016/source/

