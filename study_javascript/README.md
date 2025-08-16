2025/8/9
・JavaScriptの学習を開始

■TODOアプリの作成
・参考動画：https://www.youtube.com/watch?v=E08jeQBa1D0
・Live serverをインストール（ブラウザへファイルの修正した内容を動的に反映させる。）
・TODOディレクトリと配下にindex.htmlを作成

＜操作関連＞
・!を入力後、TABキーを押すと以下の内容が自動で入力される。

________入力される内容________
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    
</body>
</html>
_______ここまで________

charset -- 文字コードの種類を示すための属性や宣言 WebページやCSSファイルなどのテキストデータをコンピュータがどのように解釈するかを定義

・タスクばらし
1.[HTML]TODO入力フォームを作成
2.[Bootstrap]見た目を整える
3.[JavaScript]TODOを表示・保存
4.[JavaScript]TODOを削除
5.[JavaScript]TODOを完了


8/11
・TODOアプリ完成
  =>詳細については中途半端な理解のため、再度動画視聴や自分で調べて細かい説明文をコード内に追加していく予定

8/12
・index.html、index.jsの複数箇所に動作内容の説明文を追加
・TODOにリセットボタンを設置
・Pretter、ESLintをインストール
・ESLintの設定用に.eslintrc.jsを作成。中身は未着手。

8/13
■Vue.jsの学習を開始（書籍を参考）
・Node.jsをインストール
・nvmをインストール
・ltsをインストール
・ToDo_vueディレクトリを作成、配下にindex.htmlを作成してconsole上でのvue.versionの正常表示を確認（16P参照）
・Vue.js devtoolsをGoogle Chromeの機能に追加（「ファイルの URL へのアクセスを許可する」を有効に変更）
・参考書34Pまで学習

8/15
■引き続きVue.jsの学習（参考書35Pより）
・{{message}}のように{{}}でapp.jsから代入？情報を引き出す方法をMustache記法と言う。
・35P-04の<p>{{message}}</P>の利用も可能とあるが、掲載されているapp.jsの内容ではmesssageの該当内容が表示されないため、
  app.jsに以下の宣言を追加することで正常に表示することを確認
  ーーーーー追加内容ーーーーー
  const { createApp } = Vue;
　ーーーーーここまでーーーーー

・参考書とコード内容が変わる理由について確認を行ってみたところVueのバージョン指定が原因と思われることが判明
  ーーーーー書籍記載ーーーーー
  <script src="https://unpkg.com/vue@3.0.0/dist/vue.global.js"></script>
  ーーーーーここまでーーーーー

  ーーーーーバージョン指定を3.0.0から3へ変更ーーーーー
  <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
  ーーーーーここまでーーーーー
  
  以上の変更を行うことでapp.jsに追加した下記内容を削除しても正常にmesssageが表示されることを確認
  ーーーーー以下を改めて削除ーーーー
  const { createApp } = Vue;
　ーーーーーーここまでーーーーーーー

※※※※※※※HTMLで<div>を閉じる？</div>を忘れることが多いため気をつける。※※※※※※※※※

・参考書記載の v-model の装飾子は以下３点
１）.lazy
入力情報の変更を確定してから行う。inputイベントではなく、changeイベントに反応する。

２）.number
入力の値は文字列となるが、こん装飾子を使うと数字として扱われるため、入力した数値に＋１の表示とする場合には１を入力すると２となる。
この装飾子を使わない場合は、１１の表示となる。処理としては parseFloat() でNumber型の値に変更する。

３）.trim
入力した値の両端に空白がある場合、空白を削除する。

・参考書58Pまで学習

8/16
・75Pまで学習
