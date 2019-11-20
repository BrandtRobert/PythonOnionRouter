GITURL=https://github.com/BrandtRobert/PythonOnionRouter.git
STEPPINGSTONEDIR=~/OnionRouter/
PORT=$1

cd ./$STEPPINGSTONEDIR/PythonOnionRouter || exit

kill -9 `cat steppingstone.pid`
