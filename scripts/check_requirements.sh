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