#ssh root@MachineB 'bash -s' < local_script.sh
username=brandtr
sed 1d "$1" | while IFS= read -r line
do
  echo "$line"
  splitarr=($line)
  host=${splitarr[0]}
  port=${splitarr[1]}
  ssh $username@"$host" 'bash -s' < kill_ss.sh &
done