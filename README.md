# 掲示板を作ってみよう！！

## 概要
ubuntuでSQL,pythonを使って掲示板を作成するというもの 
  
## なぜ掲示板を作ったのか
インフラエンジニアの一歩目、研修課題の一環として  
ubuntuを使い、SQLやPythonなどに触れてみるため。
  
## 環境
ubuntu　20.04  

## インストールするもの
  
Apache2  
　$ sudo apt install apache2
    
MySQL  
　$ sudo apt install MySQL
    
Python3  
　$ sudo apt install Python3  
　$ sudo pip3 install mysqlclient  
  
## ー作成手順ー

### 1.userdir モジュールの有効化  
　$ sudo a3enmod userdir  
　$ sudo /init.d/apache2 restart  
  
　userdirモジュールを有効にすることによって  
　各ユーザーのホームディレクトリに  
　Webサイト公開用の仮想ディレクトリを割り当てることができます。  
    
### 2.CGIを有効化  
　/etc/apache2/mods-enabled/userdir.confの  
　OptionsにExecCGIを追加  
  
　~\public_html/.htaccessファイルを作成  
　リポジトリ.htaccessを作成したファイルへ記入  
    
　CGIを有効化することによって特性の拡張子をCGIプログラムとして  
　扱うようにするとともにCGIの実行の許可を与えます。  
    
### 3.MySQLにbbsを作成  
　insert_bbs1.sqlを作成
  
　MySQLで設定したユーザ名でログイン  
  
　insert_bbs1.sqlを読み込む  
　MySQL> source insert_bbs1.sql;  
  
　このコードによってMySQLの中にbbsというデータベースができ、  
　掲示板に書き込んだ内容をDBに保存することができます。  
   
### 4.python3にてBBSを作成  
　bbs.pyを作成  
　コードを書き込むことによってブラウザ上に掲示板を  
　作成することができます。  
    
### 5.ブラウザ上で動作確認  
  
　実際に書き込み、動作するかの確認をします。  
  
### 6.もし、ERRORが起きてしまったら
　ブラウザ上で表示されなかった場合は  

　$ cd /var/log/apache2  
　$ cat error.log  
    
　このコマンドを使ってERRORを確認しに行きましょう。
   
## 以上となります。
  
  
  
  
  
  
