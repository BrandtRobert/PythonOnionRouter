GITURL=https://github.com/BrandtRobert/PythonOnionRouter.git
STEPPINGSTONEDIR=~/OnionRouter/
PORT=$1

cd $STEPPINGSTONEDIR/PythonOnionRouter || exit
kill `cat $HOSTNAME-steppingstone.pid`
#rm $HOSTNAME-steppingstone.pid
#rm $HOSTNAME-steppingstone.log