# WIP

# Pythonで始めるAWS CDK

AWS CDK＋Pythonの記事が少なかったので書いてみた。

## 使ってみた感想

* 土台のところでCloudFormationを使用しているので、CloudFormationの制限事項に引っかからないように注意
* 使い込んでいくと正直、現状では痒いところに手が届かない感が否めない

## はじめに

### AWS CDKってなに？

> AWS クラウド開発キット (AWS CDK) は、使い慣れたプログラミング言語を使用してクラウドアプリケーションリソースをモデル化およびプロビジョニングするためのオープンソースのソフトウェア開発フレームワークです。

[AWS クラウド開発キット](https://aws.amazon.com/jp/cdk/)より

かなり大雑把にまとめると、使い慣れたプログラミング言語でAWSのリソースを定義、作成できるIaC(Infrastructure as Code)ツールですよっと。

### なんでAWS CDKなの？

環境設定をコードで管理したい。けどterraformとかに手を出すほどでもないし、template.ymlは書きたくない…。何よりAWSの公式！

### なんでPythonなの？

(TypeScript分からないから…)
LambdaをPythonで書いていたからその延長線上でPythonでやってみた

## AWS CDKのインストール

* [Getting started with the AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)を参考に進めていく。

### Node.jsのインストール

前提として、Node.jsが必要なのでインストールされていない場合はまずこちらをインストールする
[Node.jsの公式](https://nodejs.org/en/download/)からインストーラをダウンロード。あとはインストーラに従ってポチポチしていけば勝手にインストールしてくれる。

インストールが完了したらバージョンを確認

```sh
$ node -v
v12.18.2
$ npm -v
6.14.5
```

### AWS認証情報の設定

> You must provide your credentials and an AWS Region to use AWS CDK, if you have not already done so.

認証情報とAWSリージョンを提供しなさいよ、っと言われているようです。

AWS CLIをインストールしている人は`aws configure` コマンドを実行すればプロンプトで設定可能ですが、わざわざAWS CLIインストールしたくない場合は手動で設定する。

以下はmac or linuxの設定手順。Windowsの場合は`%USERPROFILE%\.aws\config` と `%USERPROFILE%\.aws\credentials`を作成し、認証情報、リージョンを設定する

```sh
$ mkdir ~/.aws
$ touch ~/.aws/config
$ touch ~/.aws/credentials
```

エディタで`~/.aws/config`を開き、以下の通りリージョンを設定し、保存する

```vi
[default]
region=ap-northeast-1
```

エディタで`~/.aws/credentials`を開き、以下の通り認証情報を設定し、保存する。

```sh
[default]
aws_access_key_id={アクセスキーID}
aws_secret_access_key={シークレットアクセスキー}
```

### AWS CDKのインストール

npmを使用してインストールする

```sh
$ sudo npm install -g aws-cdk
```

バージョンを表示し、インストールされていることを確認。

```sh
$ cdk --version
1.52.0 (build 5263664)
```

## CDK appを作る

* [Your first AWS CDK app](https://docs.aws.amazon.com/cdk/latest/guide/hello_world.html)を参考に進めていく。

プロジェクトディレクトリを作成

```sh
mkdir hello-cdk
cd hello-cdk
```

`cdk init`コマンドを実行

```sh
cdk init app --language python
```

実行が終わったらvirtualenvを起動する
(pip3を使用している場合はpip3に読み替えて実行すること)

```sh
source .env/bin/activate
pip install -r requirements.txt
```

pipenvを使用したい場合は、virtualenvを起動せずに`.env`ディレクトリを削除して代わりにpipenvを起動する

### S3バケットを作成する

```sh
pip install aws-cdk.aws-s3
```

hello_cdk_stack.pyにs3バケットを作成するコードを追加する
(bucket_nameは既存のバケット名と重複するとデプロイ時にエラーになるため、重複しないものへ書き換えること)

```py
from aws_cdk import core
from aws_cdk import aws_s3 as _s3


class HelloCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        bucket = _s3.Bucket(self, "MyFirstBucket", bucket_name="kimi-first-cdk-bucket")
```

デプロイコマンドを実行

```
kimidzuokinoMBP:hello-cdk kimizukasaki$ cdk deploy
hello-cdk: deploying...
hello-cdk: creating CloudFormation changeset...





 ✅  hello-cdk

Stack ARN:
arn:aws:cloudformation:ap-northeast-1:323617333195:stack/hello-cdk/3497b790-ca3f-11ea-9236-0eb7b90bbf8e
```

デプロイ完了後にAWSマネジメントコンソールでS3バケットが作成されていることを確認できた

![](2020-07-20-13-31-33.png)

## サンプルコード



### VPC

### Lambda

https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Function.html

