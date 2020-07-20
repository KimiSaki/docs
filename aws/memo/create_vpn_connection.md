
* VPCの作成
* サブネットの作成
* ルートテーブルの作成
* 仮想プライベートゲートウェイの作成
* Transit Gatewayの作成
* Transit Gateway Attachmentの作成
  * カスタマーゲートウェイ
  * VPN接続
  
* ローカルネットワークのゲートウェイ機器に設定を登録
  * configをVPN接続画面からDL
  * configを編集
  * ルータのconfigをbackup
  * ルータのconfigを更新
    * コマンド投入(BGPを除く)->ルータは通信中になった!->IPSEC IS UP -> ステータスはダウン
    * BGPのコマンド投入->ステータスアップになった!
    * Ping, tracertがタイムアウトする->Transit GatewayにVPCをアタッチ、ルートテーブルにTransit Gatewayを追加
* 導通確認

https://docs.google.com/presentation/d/1XBAlyTMyPH-CnN6qgTUoyyYt45Dir6nYjaW7WdJjUBM/edit#slide=id.g216ae9a80d_0_0

https://tech.guitarrapc.com/entry/2013/10/06/171650#fn1

https://dev.classmethod.jp/cloud/aws/reinvent2018-transit-gateway-via-vpn/



* [X] ~~*内部からSSHでログインできること*~~ [2019-11-01]
  * ホストに接続できません->ネットワークACLとセキュリティグループにCREiST devからのssh接続を許可
* [X] ~~*踏み台->1号機にsshで接続できること*~~ [2019-11-01]
  * Connection timed out->環境変数に設定されているIPアドレスが違う(IPアドレスでssh接続できる)
  * .esl_envのIPアドレスを変更->環境変数指定でssh接続できた!
* [X] ~~*.ssh配下のpem(鍵ファイル)を変更*~~ [2019-11-07]

* [X] ~~*外部からログインできること*~~ [2019-11-06]
    * Elastic IP(EIP)の割り当て
    * EIPをENIに紐づけ
      * Network vpc- is not attached to any internet gateway
      * igwを作成し、VPCにアタッチ
      * ルートテーブルにigwを追加
      * Pingは通る sshで接続できない(ホストに接続できません)
      * セキュリティグループ、ネットワークACLにcreistのip(153.156.81.66/32)を登録
    * https://aws.amazon.com/jp/getting-started/projects/scalable-wordpress-website/01/04/