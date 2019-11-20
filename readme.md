## Onion Router Project

The contained code implements a sort of multiple hop process for getting a file from the web.

The file chainfile.txt or chaingang.txt contains the names of random hops ips and ports to take when retrieving the file.
```buildoutcfg
3
denver.cs.colostate.edu 8080
olympia.cs.colostate.edu 8080
nashville.cs.colostate.edu 8080
```

#### Dependencies

This program must be run with python3 as it uses type hints. Also note that the requests package
must be installed in order for the steppingstone.py to fetch files properly. The venv directory will be included
in the tar submission so that you can set up the python environment by using
```buildoutcfg
source ./venv/bin/activate
``` 

### Running the Program

#### steppingstone.py

The steppingstone can be run with the following command.
```
python3 steppingstone.py -p/--port <port-num>
```

#### awget.py

The awget can be run with the following command:
```
python3 awget.py <url> -c <chain-file>
```

### Running scripts

In the scripts directory there are a set of scripts for deploying the steppingstones to the 
lab machines. The ./deploy_routers.sh <chainfile.txt> should (if properly working) create a directory and clone the git repository
for this source code. It will then run the steppingstones using nohup. This script should initialize everything using the
chainfile. The kill_routers.sh <chainfile> should hop to every machine and kill the stepping stone processes by looking at the 
reported pids in the $host-steppingstone.pid files created by the deploy_routers script.