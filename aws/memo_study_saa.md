# これだけでOK！AWS認定ソリューションアーキテクト-アソシエイト試験突破講座

## 5.EC2

### Bashコマンドによる設定

* インスタンス作成時、ユーザーデータを設定することでインスタンス起動時に自動的に設定された内容が実行される
* ユーザーデータはbashなどのシェルスクリプトで記述することができる

```sh
sed -i 's/^HOSTNAME=[a-zA-Z0-9¥.¥-]*$/HOSTNAME=udemy-bash/g'
/etc/sysconfig/network hostname 'udemy-bash'
cp /usr/share/zoneinfo/Japan /etc/localtime
sed -i 's|^ZONE=[a-zA-Z0-9¥.¥-¥"]*$|ZONE="Azia/Tokyo"|g' /etc/sysconfig/clock
echo "LANG=ja_JP.UTF-8" > /etc/sysconfig/i18n
sudo yum update -y
sudo install httpd -y
sudo chkconfig httpd on
```

ssh -i ~/.ssh/handson-key-kimisaki.pem ec2-user@18.183.194.195

### EBS

* 実態はネットワーク接続型ストレージ
* 1GB ~ 16GB
* セキュリティグループによる通信制御対象外
* データは永続的に保存
* ボリュームデータはAZ内で複数HWに冗長化されている
* snapshotでバックアップ（s3に保存
* 2世代目以降は増分バックアップ
* AMIにはsnapshotも含まれている

