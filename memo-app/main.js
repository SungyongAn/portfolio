const { app, BrowserWindow, ipcMain, Menu } = require("electron");
const path = require("path");
const fs = require("fs");

let memoWindows = [];
let memoStates = new Map();
let savePath;

function ensureUserDataDir() {
  const dir = app.getPath("userData");
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function saveAllMemos() {
  try {
    const data = memoWindows.map((win) => {
      const bounds = win.getBounds();
      const state = memoStates.get(win) || {};
      return {
        x: bounds.x,
        y: bounds.y,
        width: bounds.width,
        height: bounds.height,
        text: state.text || "",
        bgColor: state.bgColor || "#fff3b0",
        fontColor: state.fontColor || "#000000",
      };
    });

    // 空の配列でも正しいJSONとして保存
    const jsonString = JSON.stringify(data, null, 2);
    console.log("Saving:", jsonString); // デバッグ用
    fs.writeFileSync(savePath, jsonString, "utf-8");
  } catch (e) {
    console.error("saveAllMemos error:", e);
  }
}

function createMemoWindow(state = {}) {
  const win = new BrowserWindow({
    width: state.width || 250,
    height: state.height || 200,
    x: state.x,
    y: state.y,
    frame: false, // frameless
    resizable: true,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
    },
  });

  win.loadFile("memo.html");

  win.webContents.on("did-finish-load", () => {
    win.webContents.send("set-text", state.text || "");
    win.webContents.send("set-colors", {
      bgColor: state.bgColor || "#fff3b0",
      fontColor: state.fontColor || "#000000",
    });
    memoStates.set(win, {
      text: state.text || "",
      bgColor: state.bgColor || "#fff3b0",
      fontColor: state.fontColor || "#000000",
    });
  });

  // 右クリックメニュー
  const contextMenu = Menu.buildFromTemplate([
    {
      label: "背景色変更",
      submenu: [
        {
          label: "🟡 イエロー",
          click: () =>
            win.webContents.send("set-colors", { bgColor: "#fff3b0" }),
        },
        {
          label: "🟢 グリーン",
          click: () =>
            win.webContents.send("set-colors", { bgColor: "#b0f3c8" }),
        },
        {
          label: "🔵 ブルー",
          click: () =>
            win.webContents.send("set-colors", { bgColor: "#b0d4f3" }),
        },
        {
          label: "🟣 ピンク",
          click: () =>
            win.webContents.send("set-colors", { bgColor: "#f3b0e6" }),
        },
        { type: "separator" },
        {
          label: "カスタム...",
          click: () =>
            win.webContents.send("open-color-picker", { type: "bg" }),
        },
      ],
    },
    { type: "separator" },
    {
      label: "文字色変更",
      submenu: [
        {
          label: "⚫ 黒",
          click: () =>
            win.webContents.send("set-colors", { fontColor: "#000000" }),
        },
        {
          label: "⚪ 白",
          click: () =>
            win.webContents.send("set-colors", { fontColor: "#ffffff" }),
        },
        {
          label: "🔴 赤",
          click: () =>
            win.webContents.send("set-colors", { fontColor: "#ff0000" }),
        },
        {
          label: "🔵 青",
          click: () =>
            win.webContents.send("set-colors", { fontColor: "#0000ff" }),
        },
        { type: "separator" },
        {
          label: "カスタム...",
          click: () =>
            win.webContents.send("open-color-picker", { type: "font" }),
        },
      ],
    },
    { type: "separator" },
    { label: "削除", click: () => win.close() },
  ]);

  win.webContents.on("context-menu", () => contextMenu.popup());

  memoWindows.push(win);
  const saveDebounced = debounce(saveAllMemos, 300);
  win.on("move", saveDebounced);
  win.on("resize", saveDebounced);

  win.on("close", () => {
    saveAllMemos();
    memoWindows = memoWindows.filter((w) => w !== win);
    memoStates.delete(win);
  });

  return win;
}

function debounce(fn, delay) {
  let timer;
  return () => {
    clearTimeout(timer);
    timer = setTimeout(fn, delay);
  };
}

// IPC
ipcMain.on("update-color", (e, colors) => {
  const win = BrowserWindow.fromWebContents(e.sender);
  const state = memoStates.get(win) || {};
  memoStates.set(win, { ...state, ...colors });
  saveAllMemos();
});

ipcMain.on("save-text", (e, text) => {
  const win = BrowserWindow.fromWebContents(e.sender);
  const state = memoStates.get(win) || {};
  memoStates.set(win, { ...state, text });
  saveAllMemos();
});

ipcMain.on("delete-memo", (e) => {
  const win = BrowserWindow.fromWebContents(e.sender);
  if (win) win.close();
});

// 起動処理
app.whenReady().then(() => {
  ensureUserDataDir();
  savePath = path.join(app.getPath("userData"), "memos.json");

  // ========== デバッグログ追加 ==========
  console.log("=== デバッグ開始 ===");
  console.log("1. Save path:", savePath);
  console.log("2. File exists:", fs.existsSync(savePath));

  let saved = [];
  try {
    if (fs.existsSync(savePath)) {
      const fileContent = fs.readFileSync(savePath, "utf-8");
      console.log("3. File content:", fileContent);

      // 空ファイルチェック
      if (fileContent.trim() === "") {
        console.log("   -> ファイルが空なので新規作成");
        saved = [];
      } else {
        saved = JSON.parse(fileContent);
        console.log("4. Parsed data:", saved);
        console.log("5. Number of memos:", saved.length);
      }
    } else {
      console.log("3. memos.json が存在しません");
    }
  } catch (e) {
    console.error("保存データ読み込み失敗:", e);
    saved = [];
  }

  console.log("6. Creating windows...");
  // ========== デバッグログ終了 ==========

  if (saved.length === 0) createMemoWindow();
  else saved.forEach((state) => createMemoWindow(state));
});

// app.whenReady().then(() => {
//   ensureUserDataDir();
//   savePath = path.join(app.getPath("userData"), "memos.json");

//   let saved = [];
//   try {
//     if (fs.existsSync(savePath))
//       saved = JSON.parse(fs.readFileSync(savePath, "utf-8"));
//   } catch (e) {
//     console.error("保存データ読み込み失敗:", e);
//     saved = [];
//   }

//   if (saved.length === 0) createMemoWindow();
//   else saved.forEach((state) => createMemoWindow(state));
// });

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
