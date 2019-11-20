#ssh root@MachineB 'bash -s' < local_script.sh
username=brandtr

ssh $username@"olympia.cs.colostate.edu" "bash -s" < check_requirements.sh

sed 1d "$1" | while IFS= read -r line
do
  echo "$line"
  splitarr=($line)
  host=${splitarr[0]}
  port=${splitarr[1]}
  ssh $username@"$host" "bash -s -- $port" < execute_stepping_stone.sh &
done