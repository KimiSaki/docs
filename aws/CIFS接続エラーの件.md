

# CIFS接続エラーの件

## 事象

それぞれ異なるサブネットのインスタンス3台のうち、
1台だけCIFS接続でエラーとなる

## 原因

### 原因１

接続できないインスタンスが所属しているサブネットのネットワークACLだけ、
ほかのサブネットと異なるネットワークACLを参照していた。

### 原因２

CIFS接続できないネットワークACLのインバウンドルートのうち、
TCP/UDPの1024 - 65535ポートが開いていなかった


## 1号機(NG)

```
[centos@ip-10-194-8-8 ~]$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/xvda1      31445996 4337860  27108136  14% /
devtmpfs         1916580       0   1916580   0% /dev
tmpfs            1939436       0   1939436   0% /dev/shm
tmpfs            1939436   32988   1906448   2% /run
tmpfs            1939436       0   1939436   0% /sys/fs/cgroup
tmpfs             387888       0    387888   0% /run/user/1000
[centos@ip-10-194-8-8 ~]$ mount -t cifs //192.168.2.99/esl$/eairecv/ /mnt/test/ -o username=ESLusr,password=ESL_3048,vers=3.0
mount: only root can use "--options" option
[centos@ip-10-194-8-8 ~]$ sudo mount -t cifs //192.168.2.99/esl$/eairecv/ /mnt/t
est/ -o username=ESLusr,password=ESL_3048,vers=3.0
mount: mount //192.168.2.99/esl$/eairecv/ on /mnt/test failed: Operation now in progress
[centos@ip-10-194-8-8 ~]$ sudo mount -t cifs //192.168.2.99/esl$/eairecv/ /mnt/test/ -o username=ESLusr,password=ESL_3048,vers=3.0
[centos@ip-10-194-8-8 ~]$ ls -l /mnt/test
total 14552
-rwxr-xr-x 1 root root 14901115 Oct 16 15:25 ECI_ESL_M571_20191112221510.csv
[centos@ip-10-194-8-8 ~]$ umount /mnt/test
umount: /mnt/test: umount failed: Operation not permitted
[centos@ip-10-194-8-8 ~]$ sudo umount /mnt/test
[centos@ip-10-194-8-8 ~]$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/xvda1      31445996 4339296  27106700  14% /
devtmpfs         1916580       0   1916580   0% /dev
tmpfs            1939436       0   1939436   0% /dev/shm
tmpfs            1939436   32988   1906448   2% /run
tmpfs            1939436       0   1939436   0% /sys/fs/cgroup
tmpfs             387888       0    387888   0% /run/user/1000
[centos@ip-10-194-8-8 ~]$
```


## 2号機(OK)


```
[centos@ip-10-194-8-24 ~]$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/xvda1      31445996 4565976  26880020  15% /
devtmpfs         1916580       0   1916580   0% /dev
tmpfs            1939436       0   1939436   0% /dev/shm
tmpfs            1939436   32956   1906480   2% /run
tmpfs            1939436       0   1939436   0% /sys/fs/cgroup
tmpfs             387888       0    387888   0% /run/user/1000
[centos@ip-10-194-8-24 ~]$ mount -t cifs //192.168.2.99/esl$/eairecv/ /mnt/test/ -o username=ESLusr,password=ESL_3048,vers=3.0
mount: only root can use "--options" option
[centos@ip-10-194-8-24 ~]$ su
Password:
[centos@ip-10-194-8-24 ~]$ sudo mount -t cifs //192.168.2.99/esl$/eairecv/ /mnt/
test/ -o username=ESLusr,password=ESL_3048,vers=3.0
[centos@ip-10-194-8-24 ~]$ df
Filesystem                   1K-blocks     Used Available Use% Mounted on
/dev/xvda1                    31445996  4566036  26879960  15% /
devtmpfs                       1916580        0   1916580   0% /dev
tmpfs                          1939436        0   1939436   0% /dev/shm
tmpfs                          1939436    32956   1906480   2% /run
tmpfs                          1939436        0   1939436   0% /sys/fs/cgroup
tmpfs                           387888        0    387888   0% /run/user/1000
//192.168.2.99/esl$/eairecv/ 120829948 57940976  62888972  48% /mnt/test
[centos@ip-10-194-8-24 ~]$ ls -l /mnt/test
total 14552
-rwxr-xr-x 1 root root 14901115 Oct 16 15:25 ECI_ESL_M571_20191112221510.csv
[centos@ip-10-194-8-24 ~]$ sudo umount /mnt/test
[centos@ip-10-194-8-24 ~]$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/xvda1      31445996 4565540  26880456  15% /
devtmpfs         1916580       0   1916580   0% /dev
tmpfs            1939436       0   1939436   0% /dev/shm
tmpfs            1939436   32956   1906480   2% /run
tmpfs            1939436       0   1939436   0% /sys/fs/cgroup
tmpfs             387888       0    387888   0% /run/user/1000
```

## 3号機(OK)

```
[centos@ip-10-194-8-41 ~]$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/xvda1      31445996 4565140  26880856  15% /
devtmpfs         1916580       0   1916580   0% /dev
tmpfs            1939436       0   1939436   0% /dev/shm
tmpfs            1939436   33012   1906424   2% /run
tmpfs            1939436       0   1939436   0% /sys/fs/cgroup
tmpfs             387888       0    387888   0% /run/user/1000
tmpfs             387888       0    387888   0% /run/user/0
[centos@ip-10-194-8-41 ~]$ sudo mount -t cifs //192.168.2.99/esl$/eairecv/ /mnt/test/ -o username=ESLusr,password=ESL_3048,vers=3.0
[centos@ip-10-194-8-41 ~]$ df
Filesystem                   1K-blocks     Used Available Use% Mounted on
/dev/xvda1                    31445996  4565124  26880872  15% /
devtmpfs                       1916580        0   1916580   0% /dev
tmpfs                          1939436        0   1939436   0% /dev/shm
tmpfs                          1939436    33012   1906424   2% /run
tmpfs                          1939436        0   1939436   0% /sys/fs/cgroup
tmpfs                           387888        0    387888   0% /run/user/1000
tmpfs                           387888        0    387888   0% /run/user/0
//192.168.2.99/esl$/eairecv/ 120829948 57942180  62887768  48% /mnt/test
[centos@ip-10-194-8-41 ~]$ ls -l /mnt/test
total 14552
-rwxr-xr-x 1 root root 14901115 Oct 16 15:25 ECI_ESL_M571_20191112221510.csv
[centos@ip-10-194-8-41 ~]$ sudo umount /mnt/test
[centos@ip-10-194-8-41 ~]$ df
Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/xvda1      31445996 4565104  26880892  15% /
devtmpfs         1916580       0   1916580   0% /dev
tmpfs            1939436       0   1939436   0% /dev/shm
tmpfs            1939436   33012   1906424   2% /run
tmpfs            1939436       0   1939436   0% /sys/fs/cgroup
tmpfs             387888       0    387888   0% /run/user/1000
tmpfs             387888       0    387888   0% /run/user/0
```

## 考察


## おまけ。CIFSのコマンド
df
mount -t cifs //192.168.2.99/esl$/eairecv/ /mnt/test/ -o username=ESLusr,password=ESL_3048,vers=3.0
df
ls -l /mnt/test
umount /mnt/test
df
