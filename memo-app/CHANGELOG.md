# Changelog

All notable changes to Memo App will be documented in this file.

## [1.0.0] - 2024-12-16

### Added

- 初回リリース
- デスクトップ付箋メモ機能
- フレームレスウィンドウデザイン
- メモのドラッグ移動機能
- ウィンドウのリサイズ機能
- テキストの自動保存
- 背景色のカスタマイズ（プリセット: イエロー、グリーン、ブルー、ピンク）
- 文字色のカスタマイズ（プリセット: 黒、白、赤、青、緑、オレンジ）
- 文字色のカラーピッカー対応
- 右クリックコンテキストメニュー
- メモ削除機能（Delete キー、右クリックメニュー）
- アプリ起動時の状態復元機能
- 複数メモの同時管理
- Windows 版ビルド（.exe ファイル）
- macOS 版ビルド（.app ファイル）

### Technical Details

- Electron v30.5.1 ベース
- データ保存: JSON 形式（memos.json）
- 保存場所:
  - macOS: `~/Library/Application Support/memo-app/memos.json`
  - Windows: `%APPDATA%/memo-app/memos.json`
  - Linux: `~/.config/memo-app/memos.json`

### Fixed

- memos.json が空の場合のエラーハンドリング追加
- JSON パースエラー時の適切なフォールバック処理
- テキストエリア入力中の Delete キー誤動作防止
- 背景色がドラッグエリアにも適用されるように修正

### Build & Distribution

- electron-packager によるパッケージング
- electron-builder による配布用ビルド
- ポータブル版（インストール不要）
- インストーラー版（NSIS）
- 7z 圧縮オプション対応

### Documentation

- README.md 作成
- インストール手順
- 使い方ガイド
- トラブルシューティング

### Known Issues

- Windows SmartScreen 警告表示（コード署名なしのため）
- ファイルサイズが大きい（約 76MB - Electron 本体を含むため）

### Notes

- 本プロジェクトはオープンソースです
- MIT ライセンス
