#!/bin/bash


# echo

md5_str=$1

for i in $(seq 1 30);do
 
    ssh_pid=`ps -ef |grep $md5_str |grep -v grep |grep -v session_tracker.sh |grep -v sshpass |awk '{print $2}'`
    echo "ssh session pid:$ssh_pid"
    if [ "$ssh_pid" = "" ];then
       continue
   else

      today=`date "+%Y_%m_%d"`
      today_audit_dir="logs/audit/$today"

      echo "today_audit_dir:$today_audit_dir"
      if [ -d $today_audit_dir ]
      then
          echo "-----start log------"
       else
         echo "dir not exist"
         echo "today  dir: $today_audit_dir"
         sudo mkdir -p $today_audit_dir
       fi;
      echo 123456 | sudo -S /usr/bin/strace -ttt -p $ssh_pid -o "$today_audit_dir/$md5_str.log"
      break
   fi;


done;
