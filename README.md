# OpenScreen CLI をエージェントから使う

画面録画から字幕・書き出しまでを、[OpenScreen の CLI](https://getopenscreen.com/ja/docs/cli/) で進めるためのエージェントスキルです。終了コード、JSON 出力、成果物の存在を検査するスクリプトも同梱しています。OpenScreen の公式プロジェクトではありません。

## インストール

[vercel-labs/skills](https://github.com/vercel-labs/skills) の CLI からインストールできます。

```bash
npx skills add 53able/openscreen-cli-skill --skill openscreen-cli
```

OpenScreen アプリ本体は別途インストールしてください。このコマンドはスキルだけを追加します。インストール対象の確認には `npx skills add 53able/openscreen-cli-skill --list` を使えます。

## できること

- 画面・ウィンドウ・マイクの一覧を確認し、デスクトップで録画する
- 録画音声から字幕を生成し、MP4/GIF に書き出す
- カーソルのクリック情報がある録画に自動ズームを適用する
- `.openscreen` プロジェクトと参照メディアを梱包する
- CLI の終了コード、JSON 出力、生成ファイルを検査する

たとえばエージェントには「OpenScreen でウィンドウを20秒録画して MP4 に書き出し、CLI の結果と動画ファイルの存在を確認して」と依頼できます。録画には実際のデスクトップセッションと OS の許可が必要です。Linux の画面共有ダイアログを無人で操作するスキルではありません。

## 対応する OpenScreen CLI

**対象バージョン：v1.13.0。** macOS 版で `help`、合成動画を使った `info`・`pack`・MP4 `export --json`、同梱チェッカーを検査しました。**実際の画面録画、字幕、GIF、音声後付け、Windows/Linux、および他バージョンは E2E 未検証**です。対象バージョンでも全機能の動作を保証するものではありません。実行前にインストール版の `help` と [公式 CLI ドキュメント](https://getopenscreen.com/ja/docs/cli/)を確認してください。

同梱チェッカーは画質、音声の同期、個人情報の映り込みを判定できません。書き出した動画は別途再生して点検してください。GUI 上の編集や汎用動画エンコードも対象外です。

## ファイルと開発

- [`SKILL.md`](skills/openscreen-cli/SKILL.md)：エージェント向けの実行手順
- [`platform-and-protocol.md`](skills/openscreen-cli/references/platform-and-protocol.md)：OS 別起動方法、オプション、JSON 出力
- [`project-json.md`](skills/openscreen-cli/references/project-json.md)：形式を検査してから行うプロジェクト JSON 編集例
- [`check-result.py`](skills/openscreen-cli/scripts/check-result.py)：CLI 結果の機械的な検査

同梱の Python は `uv` 経由で実行します（Python 3.9 以上）。チェッカーの単体テストは OpenScreen を起動せずに実行できます。

```bash
uv run --no-project python -m unittest discover -s tests -v
```

## ライセンス

[MIT License](LICENSE)。OpenScreen 本体と `vercel-labs/skills` はそれぞれ別のプロジェクトです。
