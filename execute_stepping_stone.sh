GITURL=https://github.com/BrandtRobert/PythonOnionRouter.git
STEPPINGSTONEDIR=~/OnionRouter/

echo "Checking for $STEPPINGSTONEDIR"

if [ ! -d "$STEPPINGSTONEDIR" ]
then
  echo "$STEPPINGSTONEDIR does not exist creating"
  mkdir "$STEPPINGSTONEDIR"
fi

cd ~/OnionRouter || exit

echo "Checking for OnionRouter src"
if [ ! -d "./PythonOnionRouter" ]
then
  echo "Source does not exist cloning from $GITURL"
  git clone $GITURL
fi

cd ./PythonOnionRouter || exit

nohup python3 ./steppingstone.py -p9977 > steppingstone.log 2>&1 & echo $! > steppingstone.pid

#ssh root@MachineB 'bash -s' < local_script.sh
