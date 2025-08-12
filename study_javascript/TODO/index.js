// getElementById は index.html の情報を id 情報を元に引っ張ってくる。
// 複数同じ名称の id が存在する場合は一番最初の id が優先される。
const form = document.getElementById("form");
const input = document.getElementById("input");
const ul = document.getElementById("ul");
const reset = document.getElementById("reset");

// 画面を更新した時、local strageにtodosが存在する時に画面上に表示する機能１
// local strageに保存された情報の固定？
const todos = JSON.parse(localStorage.getItem("todos"));

// 画面を更新した時、local strageにtodosが存在する時に画面上に表示する機能２
if(todos) {
    todos.forEach(todo => {
        add(todo);
    })
}

// リセット機能を追加
if(reset) {
    // リセットボタンをクリックした時に確認
    reset.addEventListener("click", function() {
        // 確認メッセージを表示させる
        if(confirm("全てのTODOを削除しますか？")) {
            // localStorage内を全削除
            localStorage.clear();
            // 画面表示されているリストも削除
            ul.innerHTML = "";
        }
    });
}

// addEventListener(type(イベントの種類), listener(null もしくは関数), options or useCapture 詳細はWebへ)
// ここでの submit とは入力欄を選択した後にEnterを押す操作
form.addEventListener("submit", function (event) {
    // 本来発生する機能、動作を発生しないようにする。
    event.preventDefault();
    add();
});

function add(todo) {
    let todoText = input.value;
    // 画面を更新した時、local strageにtodosが存在する時に画面上に表示する機能３
    if (todo) {
        todoText = todo.text;
    }

    // 入力が空の場合は除外する。
    // if (todoText) でも可能 詳細はREADMEへ
    if (todoText.length > 0) {
        const li = document.createElement("li");
        li.innerText = todoText;
        li.classList.add("list-group-item");

        if (todo && todo.completed) {
            li.classList.add("text-decoration-line-through");
        }

        // リストの削除機能
        li.addEventListener("contextmenu", function (event) {
            event.preventDefault();
            // 削除動作
            li.remove();
            saveData();
        });

        li.addEventListener("click", function () {
            li.classList.toggle("text-decoration-line-through");
            saveData();
        });

        ul.appendChild(li);
        // 入力欄を空に戻す
        input.value = "";
        saveData();
    }
}


function saveData() {
    const lists = document.querySelectorAll("li");
    let todos = [];

    // forEachはループ処理
    lists.forEach(list => {
        let todo = {
            text: list.innerText,
            completed: list.classList.contains("text-decoration-line-through")
        };
        // pushはpythonのappendみたいなもの
        todos.push(todo);
    });
    // localStrage に todos を JSON.stringify を使って JSON文字列に変換した上で保存
    localStorage.setItem("todos", JSON.stringify(todos));
}
