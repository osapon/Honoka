# Honoka for Bootstrap 5

Bootstrap 5 向けの [Honoka](https://github.com/windyakin/Honoka) テーマ実装です。

## 特徴

- Bootstrap 5.3.3 本体をそのまま使用
- 日本語フォント・ウェイト調整を Honoka 流にカスタマイズ
- SCSS の変数上書きのみで構成（Bootstrap 本体を fork しない）

## 使い方

```bash
npm install
npm run build
npm run build:min
```

`dist/css/bootstrap.css` が生成されます。

## 主なカスタマイズ

| 項目 | 値 |
|---|---|
| 日本語フォント | ヒラギノ角ゴ、メイリオを含むスタック |
| `$font-weight-light` | 400 |
| `$font-weight-bold` | 600 |
| `$headings-font-weight` | 600 |
| `$display-font-weight` | 600 |
| `$lead-font-weight` | 400 |
| `$navbar-padding-y` | 1.2rem |
| `$navbar-padding-x` | 1.5rem |
| カラーパレット | Bootstrap 4 互換（#007bff など） |
| 見出しサイズ | RFS 無効（BS4 相当の固定サイズ） |
| リンクの下線 | なし（BS5 既定の underline から変更） |

## 注意点

- **リンクの下線を消している**ため、色のコントラストを十分に確保してください。必要に応じて `$link-decoration` を元に戻すか、ホバー時の装飾を追加してください。
- **ダークモード**は Honoka 本来に存在しないため、`data-bs-theme="dark"` 使用時はテーマカラーの調整が必要になる場合があります。
- ビルド時に表示される `mixed-decls` の Deprecation Warning は Bootstrap 5.3.3 本体由来です。本テーマ側の問題ではありません。

## ライセンス

MIT License. Bootstrap および Honoka と同じライセンスです。
