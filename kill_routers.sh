#ssh root@MachineB 'bash -s' < local_script.sh
username=brandtr
hosts=$1
while IFS= read -r line
do
  echo "$line"
  splitarr=($line)
  host=${splitarr[0]}
  port=${splitarr[1]}
  ssh $username@"$host".cs.colostate.edu 'bash -s' < kill_ss.sh &
done < "$hosts"