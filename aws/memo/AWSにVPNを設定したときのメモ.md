
# AWS VPN設定手順

## 概要

* AWSでVPC(Virtual Private Cloud)を作る
* VPCと社内のVPNルータの接続
* VPNルータはYamaha RTX810

## システム構成

絵を描く

## 設定

### VPCの作成

AWSクラウド上に他とは区切られた (独立した)ネットワークの家を作るイメージ

### サブネットの作成

VPCの中で部屋を区切るイメージ
サブネットごとにAZを分けるのがベター

### ルートテーブルの作成

### セキュリティグループの作成

### Transit Gatewayの作成

### Transit Gateway Attachmentの作成

作成すると↓が自動で作成される
* カスタマーゲートウェイ
* VPN接続

### VPNルータの設定
  * configをVPN接続画面からDL
  * configを編集
  * ルータのconfigをbackup
  * ルータのconfigを更新
    * コマンド投入(BGPを除く)->ルータは通信中になった!->IPSEC IS UP -> ステータスはダウン
    * BGPのコマンド投入->ステータスアップになった!
    * Ping, tracertがタイムアウトする->Transit GatewayにVPCをアタッチ、ルートテーブルにTransit Gatewayを追加

### 導通確認

* EC2インスタンスを作る
  
  ### おまけ。グローバルIPの付与