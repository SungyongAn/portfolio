# フロントエンド

Vue.js 3 ベースのシングルページアプリケーション

## 技術スタック

- **フレームワーク**: Vue.js 3
- **ビルドツール**: Vite
- **ルーティング**: Vue Router 4
- **UI**: Bootstrap 5, Font Awesome
- **HTTP 通信**: axios
- **WebSocket**: 標準 API

## ディレクトリ構成

```
frontend/
├── src/
│   ├── components/
│   │   ├── common/       # 共通 (LoginForm, UserHeader, MainMenu)
│   │   ├── account/      # アカウント管理
│   │   ├── renrakucho/   # 連絡帳
│   │   ├── chat/         # チャット
│   │   ├── nurse/        # 養護教諭
│   │   └── archive/      # アーカイブ
│   ├── router/           # ルーティング設定
│   ├── App.vue           # ルートコンポーネント
│   └── main.js           # エントリーポイント
└── index.html
```

## 環境構築

### ローカル

```bash
npm install
npm run dev        # 開発サーバー起動
npm run build      # ビルド
```

### Docker

```bash
docker compose up -d
```

### アクセス

- **開発**: http://localhost:5173
- **本番**: http://localhost:80

## 主要コンポーネント

### 共通

- **LoginForm**: ログイン画面（メールアドレス認証）
- **UserHeader**: ユーザー情報表示、戻る・ログアウト
- **MainMenu**: ロール別メインメニュー

### アカウント管理（管理者のみ）

- **AccountManagementMenu**: アカウント管理メニュー
- **AccountForm**: アカウント登録
- **AccountSearch**: アカウント検索
- **AccountUpdateTable**: アカウント更新
- **YearlyProcessingMenu**: 年次処理

### 連絡帳

- **RenrakuchoForm**: 作成・編集
- **RenrakuchoView**: 閲覧
- **PastRenrakuchoSearch**: 過去検索

### チャット

- **ChatRoomList**: ルーム一覧
- **ChatRoom**: リアルタイムチャット（WebSocket）

### その他

- **HealthStatusView**: 健康状態確認（養護教諭）
- **ArchiveManagement**: アーカイブ管理（管理者）

## ルーティング

### 主要ルート

```javascript
"/"; // ログイン
"/main-menu"; // メインメニュー
"/account-management"; // アカウント管理（管理者）
"/renrakucho-form"; // 連絡帳作成
"/chat/:roomId"; // チャットルーム
"/archive-management"; // アーカイブ管理（管理者）
```

### ナビゲーションガード

```javascript
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  // 認証チェック
  if (to.meta.requiresAuth && !token) {
    next({ name: "Login" });
    return;
  }

  // ロールチェック
  if (to.meta.roles) {
    const userRole = localStorage.getItem("role");
    if (!to.meta.roles.includes(userRole)) {
      next({ name: "MainMenu" });
      return;
    }
  }

  next();
});
```

## 状態管理

### localStorage

```javascript
// 保存
localStorage.setItem("token", token);
localStorage.setItem("role", role);
localStorage.setItem("userId", userId);

// 取得
const token = localStorage.getItem("token");

// 削除（ログアウト）
localStorage.clear();
```

## API 通信

### axios 設定

```javascript
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

// トークン自動付与
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// エラーハンドリング
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.clear();
      window.location.href = "/";
    }
    return Promise.reject(error);
  }
);
```

### 使用例

```javascript
// ログイン
await api.post("/api/auth/login", { email, password });

// データ取得
await api.get("/api/accounts/search");

// データ作成
await api.post("/api/renrakucho", data);
```

## WebSocket 通信

### 接続管理

```javascript
export default {
  data() {
    return {
      ws: null,
      messages: [],
    };
  },

  mounted() {
    const token = localStorage.getItem("token");
    const roomId = this.$route.params.roomId;

    this.ws = new WebSocket(
      `ws://localhost:8000/ws/chat/${roomId}?token=${token}`
    );

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.messages.push(data);
    };
  },

  beforeUnmount() {
    if (this.ws) {
      this.ws.close();
    }
  },

  methods: {
    sendMessage(content) {
      this.ws.send(
        JSON.stringify({
          type: "message",
          content: content,
        })
      );
    },
  },
};
```

## 開発ガイド

### 新規コンポーネント追加

1. **コンポーネント作成**

```vue
<template>
  <div>{{ message }}</div>
</template>

<script>
export default {
  name: "ExampleComponent",
  data() {
    return { message: "Hello" };
  },
};
</script>
```

2. **ルート追加**

```javascript
import ExampleComponent from "@/components/ExampleComponent.vue";

routes.push({
  path: "/example",
  component: ExampleComponent,
  meta: { requiresAuth: true },
});
```

### スタイリング

```vue
<!-- Bootstrap -->
<div class="container">
  <button class="btn btn-primary">ボタン</button>
</div>

<!-- Font Awesome -->
<i class="fas fa-user"></i>

<!-- カスタムCSS -->
<style scoped>
.custom {
  color: #333;
}
</style>
```

## 参考資料

- [Vue.js 3](https://v3.ja.vuejs.org/)
- [Vue Router](https://router.vuejs.org/)
- [Vite](https://ja.vitejs.dev/)
- [Bootstrap 5](https://getbootstrap.jp/)
