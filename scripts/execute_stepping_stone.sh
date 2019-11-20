PORT=$1
cd ~/OnionRouter || exit
cd ./PythonOnionRouter || exit
source ./venv/bin/activate
echo "$PORT" > port.txt
nohup python3 ./steppingstone.py -p $PORT > $HOSTNAME-steppingstone.log 2>&1 & echo $! > $HOSTNAME-steppingstone.pid

