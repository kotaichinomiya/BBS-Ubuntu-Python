#!/usr/bin/env python3

import sys

import io

sys.stdout = io.TextIOWrapper( sys.stdout.buffer, encoding = 'utf-8')

#CGIとして実行した際のフォーム情報を取り出すライブラリ
import cgi

form_data=cgi.FieldStorage(keep_blank_values= True )

#MySQLデータベース接続用ライブラリ
import MySQLdb

con=None
cur=None

#設定ファイルを外部設定ファイル（.env）から読み取るライブラリ
#今回はデータベースに接続するための各情報を設定ファイルから読み取るために使用

import os

from pathlib import Path

env_path = Path('.') / '.env'

from dotenv import load_dotenv

load_dotenv( dotenv_path = env_path, verbose = True )


#トップ画面のHTMLを出力する関数
def print_html():
	#html開始
	print('<!DOCTYPE html>')
	print('<html>')
	#head出力
	print('<head>')
	print('<meta charset="UTF-8">')
	print('</head>')
	#body開始
	print( '<body>')
	print( '<p>ひとこと掲示板</p>')
	#書き込みフォームを出
	print('<form action="" method="POST">')
	print( '<input type="hidden" name="method_type" value="tweet">')
	print('<input type="text" name="poster_name" value="" placeholder="なまえ">')
	#罫線の出力
	print( '<br>' )
	print( '<textarea name="body_text" value="" placeholder="本文"></textarea>' )
	print( '<input type="submit" value="投稿">' )
	print( '</form>' )
	print('<hr>')

	#書き込みの一覧を取得するSQL分を作成
	sql="select*from posts"

	#SQLを実行
	cur.execute(sql)

	#取得した書き込みの一覧の全レコードを取り出し
	rows=cur.fetchall()

	#全レコードから1レコードずつ取り出すループ処理
	for row in rows:
		print('<div class="meta">')
		print('<span class="id">'+str(row["id"])+'</span>')
		print('<span class="name">'+str(row["name"])+'</span>')
		print('<span class="date">'+str(row["created_at"])+'</span>')
		print('</div>')
		print('<div class="message"><span>'+str(row['body'])+'</span></div>')
	#body閉じ
	print( '</body>' )
	#html閉じ
	print( '</html>' )

def main():
	#CGIとして実行するためのおまじない
	print( 'content-Type: text/html; charset=utf-8' )
	print('')

	#ここでデータベースに接続しておく
	global con,cur
	try:
		con=MySQLdb.connect(
		host= os.environ.get( 'bbs_db_host' ),
		user= str(os.environ.get( 'bbs_db_user')),
		passwd= str(os.environ.get( 'bbs_db_pass' )),
		db= str(os.environ.get( 'bbs_db_name' )),
		use_unicode = True,
		charset='utf8'
		)

	except MySQLdb.Error as e:
		print('データベース接続に失敗しました。')
		print(e)
		#データベースに接続できなかった場合は、ここで処理を終了
		exit()

	cur=con.cursor(MySQLdb.cursors.DictCursor)

	#フォーム経由のアクセスかを判定
	if('method_type' in form_data):
		#フォーム経由のアクセスである場合は、フォームの種類に従って処理を実行
		proceed_methods()
	else:

		#フォーム経由のアクセスでない場合は、通常のトップ画面を表示
		print_html()
	#一通りの処理が完了したら最後にデータベースを切断しておく
	cur.close()
	con.close()

def proceed_methods():
	method=form_data['method_type'].value

	if(method=='tweet'):
		poster_name=form_data['poster_name'].value
		body_text=form_data['body_text'].value

		sql='insert into posts(name,body) values(%s,%s)'

		cur.execute(sql,(poster_name,body_text))
		con.commit()

		print('<!DOCTYPE html>')
		print('<html>')
		print('<head>')
		print('<meta http-equiv="refresh" content="5; url=./bbs.py">')
		print('</head>')
		print('<body>')
		print('<p>処理が成功しました。5秒後に元のページに戻ります。</p>')
		print('</body>')
		print('</html>')

if __name__ == "__main__":
	main()
