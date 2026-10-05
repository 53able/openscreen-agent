# OpenScreen CLI agent skill

OpenScreen の CLI をエージェントから利用するための手順と、終了コード・JSON・成果物の検査スクリプトです。録画、ソース一覧、字幕、MP4/GIF 書き出し、プロジェクト梱包を扱います。OpenScreen の公式プロジェクトではありません。

## 対応バージョン

**OpenScreen CLI v1.13.0** を対象とします。macOS にインストールされた v1.13.0 で `help`、合成動画からの `info` / `pack` / MP4 `export --json` とチェッカーを検査しました。`record`、`captions`、GIF、音声後付け、Windows/Linux、および他バージョンは実機での E2E 検査をしていません。したがって、すべての操作が v1.13.0 で動作確認済みという意味ではありません。使う前にインストール版の `help` と[公式 CLI ドキュメント](https://getopenscreen.com/ja/docs/cli/)を確認してください。OpenScreen 自体は別途インストールし、録画にはデスクトップと OS 権限が必要です。

## インストール

[`vercel-labs/skills`](https://github.com/vercel-labs/skills) の CLI に対応した `skills/openscreen-cli/SKILL.md` 配置です。

```bash
npx skills add 53able/openscreen-cli-skill --skill openscreen-cli
```

インストール先やエージェントを選ぶには `npx skills add 53able/openscreen-cli-skill --list` と `npx skills add --help` を参照してください。CLI はスキルを配置するツールであり、OpenScreen アプリ本体はインストールしません。

## 内容

- [`skills/openscreen-cli/SKILL.md`](skills/openscreen-cli/SKILL.md): 分岐付きの実行手順
- [`references/platform-and-protocol.md`](skills/openscreen-cli/references/platform-and-protocol.md): OS 別実行ファイル、オプション、JSON 出力と制限
- [`references/project-json.md`](skills/openscreen-cli/references/project-json.md): バージョン 2 のプロジェクト JSON への編集例（形式の事前検査が必須）
- [`scripts/check-result.py`](skills/openscreen-cli/scripts/check-result.py): CLI 終了コード、JSON イベント、出力の存在を検査

動作上の制限：このチェッカーは動画の画質、音声、個人情報の映り込みを検査しません。録画・字幕・GIFの実機検査も未実施です。無人の Linux 画面録画、GUI 上の編集、汎用動画エンコードは対象外です。

## 開発・検査

```bash
python3 -m unittest discover -s tests -v
npx skills add . --list
```

Python 3.9 以上を使用します。OpenScreen を起動しないチェッカーの単体テストはローカルで実行できます。

## ライセンス

MIT License。詳細は [LICENSE](LICENSE) を参照。OpenScreen 本体と `vercel-labs/skills` のライセンスは、それぞれの公開元を確認してください。
