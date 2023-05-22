20230508-Ubuntu-Note

### Todo

* hibernate
    https://ubuntuhandbook.org/index.php/2021/08/enable-hibernate-ubuntu-21-10/

$ df -h
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           787M  2.1M  785M   1% /run
/dev/sda7       255G   45G  197G  19% /
tmpfs           3.9G  100M  3.8G   3% /dev/shm
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
/dev/sda2       256M   87M  170M  34% /boot/efi
tmpfs           787M  2.4M  785M   1% /run/user/1000

$ blkid
/dev/sda7: UUID="23063ca9-91bf-4d77-865f-4e8a2191c19e" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="44ef08aa-7eda-4c5f-a61d-e7e444a72890"

$ sudo filefrag -v /swapfile
[sudo] kazu のパスワード: 
Filesystem type is: ef53
File size of /swapfile is 2147483648 (524288 blocks of 4096 bytes)
 ext:     logical_offset:        physical_offset: length:   expected: flags:
   0:        0..   63487:      34816..     98303:  63488:            
   1:    63488..  126975:     100352..    163839:  63488:      98304:
   2:   126976..  190463:     165888..    229375:  63488:     163840:
   3:   190464..  253951:     231424..    294911:  63488:     229376:
   4:   253952..  481279:     296960..    524287: 227328:     294912:
   5:   481280..  524287:     557056..    600063:  43008:     524288: last,eof
/swapfile: 6 extents found

... secure boot をオフにすることが前提と書かれていた。

https://www.linuxuprising.com/2021/08/how-to-enable-hibernation-on-ubuntu.html

前半は、先のサイトと同様（SwapファイルのUUID,Offsetを設定してGrubをしなおす。
そのあと、以下（initramfsをアップデート）

/etc/initramfs-tools/conf.d/resume
-----
RESUME=UUID=23063ca9-91bf-4d77-865f-4e8a2191c19e resume_offset=34816
-----


sudo update-initramfs -c -k all

やはりsecure bootをオフにする。

https://itadminguide.com/disable-secure-boot-in-ubuntu/#:~:text=Disable%20Secure%20Boot%20in%20Ubuntu%201%20Identify%20if,Any%20key%20in%20Shim%20Signed%20Key%20Management%20

kazu@kazu-PC-GN246Y3A5 14:00:20 :~
$ sudo mokutil --sb-state
SecureBoot enabled
kazu@kazu-PC-GN246Y3A5 14:00:26 :~
$ sudo mokutil --disable-validation 
password length: 8~16
input password: 
input password again: 
kazu@kazu-PC-GN246Y3A5 14:00:48 :~
$ shutdown -r
Reboot scheduled for Tue 2023-05-09 14:02:13 JST, use 'shutdown -c' to cancel.
kazu@kazu-PC-GN246Y3A5 14:01:13 :~


-----------

Power off menuに追加

sudo vi /etc/polkit-1/localauthority/50-local.d/com.ubuntu.enable-hibernate.pkla

---
[Re-enable hibernate by default in upower]
Identity=unix-user:*
Action=org.freedesktop.upower.hibernate
ResultActive=yes

[Re-enable hibernate by default in logind]
Identity=unix-user:*
Action=org.freedesktop.login1.hibernate;org.freedesktop.login1.handle-hibernate-key;org.freedesktop.login1;org.freedesktop.login1.hibernate-multiple-sessions;org.freedesktop.login1.hibernate-ignore-inhibit
ResultActive=yes
---