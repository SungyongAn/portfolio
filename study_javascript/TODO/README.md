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
    -> CSSのフレームワーク URL参照元：https://getbootstrap.jp/　のCDN経由でインクルードするからリンクを引っ張る
3.[JavaScript]TODOを表示・保存
    ->ブラウザAPIであるdocumentを使用
4.[JavaScript]TODOを削除

・変数
let   ->変数の再代入が可能
const ->定数の宣言 値の再代入不可 
var   ->昔のverで使われていた。ほぼletと同じ扱いで現在は使われていない。

・関数
function 関数名(引数){
    return 戻り値
}

・addEventListener
ブラウザAPIの機能
特定のイベントが起きた時にJavaScriptの処理を追加する

・if構文のルール
その１）条件式を入力しない場合、暗黙的型変換が適用され真偽値(false, true)で判定される。
    falseになる値：false On underfined NaN null 0 ""(空文字)
    trueになる値:上記以外

・ループ処理
その１）forEach()


