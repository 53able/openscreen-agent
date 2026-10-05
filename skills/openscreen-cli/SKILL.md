---
name: openscreen-cli
description: OpenScreenのCLIで画面録画、ソース確認、字幕生成、MP4/GIF書き出し、プロジェクトの梱包を行う。Use when an agent needs a repeatable OpenScreen screen-recording or rendering workflow with machine-readable result checks. Don’t use for GUI editing, unattended Linux recording, or generic video encoding.
---

# OpenScreen CLI 操作

## 手順

1. **実行環境を確定する。** `openscreen help` を実行し、見つからなければ `references/platform-and-protocol.md` のOS別実行ファイルを確認してフルパスで再試行する。実行ファイルも見つからない場合は、同参照の「未インストール時の案内」に従い、OSに合う導入方法と導入後の確認コマンドを利用者に示して録画・書き出しを止める。実行ファイルがあるのに起動できない場合は、未インストールと決めつけず、エラーを確認する。CLIのオプションを表示し、インストール版を記録して自動化では更新を固定する。`record` には実際のデスクトップセッションが必要。録画する画面・音声の範囲と保存先を決め、機密情報を映さない準備をする。OSの録画・入力アクセス権限とLinuxの共有ダイアログは利用者に処理してもらう。起動できなければ止め、CLIを使えたと報告しない。
2. **対象と経路を決める。** 新規録画なら `sources --json` を実行して対象を確認し、Step 3へ。既存 `.openscreen` の書き出しだけなら `info <project> --json` でメディア参照を確認してStep 4へ。他社製動画を使う場合だけ `references/platform-and-protocol.md` の最小プロジェクトを確認する。クリック情報のない動画に自動ズームを期待しない。
3. **録画する。** 人がアクセスを許可したデスクトップで `record --duration <seconds> --project <unique-name>.openscreen --json` を実行する。対象は `--window <title>` / `--display <index>`、音声は `--mic` / `--mic-device <name>` / `--system-audio` から選ぶ。選択の詳細とOS別の停止手段は `references/platform-and-protocol.md` を読む。自動ズーム用のカーソルデータを残すには既定の編集可能カーソルを使い、`--cursor system` を指定しない。正常終了を待ち、強制終了した録画を完成と見なさない。Linuxでは共有対象を人が選択するまで待つ。
4. **必要な処理だけ行う。** 録画内に音声があり字幕が必要なら `captions <project> --json` を実行する。これはプロジェクトに字幕注釈を書き、書き出し時に焼き込む。字幕の語数調整・再実行時の置換は `references/platform-and-protocol.md` を読む。手動ズームやテキスト注釈をJSONで追加する場合に限り `references/project-json.md` を読み、バックアップ・形式検査・`info` による再検証を行う。必要な処理がなければ編集を省く。
5. **書き出す。** MP4は `export <project> -o <unique-output>.mp4 --json` を実行する。クリックテレメトリがある場合だけ `--auto-zoom` を追加する。GIFは `.gif` を指定し、必要なら `--gif-fps` / `--gif-size` を選ぶ。MP4のみナレーションを `--audio` で後付けできる。MP4のCLI書き出しはH.264・60 fps固定。品質・GIF・音声のオプションは `references/platform-and-protocol.md` を読む。外部ナレーションを後付けするだけなら録画側の音声がない場合に `captions` は使えない。
6. **結果を検証する。** 各CLIコマンドの終了コードと `--json` のstdoutを**別々に**記録する。`<skill-dir>` をこの `SKILL.md` のあるディレクトリに置き換え、`uv run --no-project python <skill-dir>/scripts/check-result.py --command <command> --exit-code <code> --input <stdout-file> [--artifact <path>]` を実行する。`record` / `captions` はプロジェクト、`export` は動画を `--artifact` に指定する。検証が失敗したら成果物を採用しない。`info --json` は単一JSON。動画の再生状態、音声と映像のずれ、個人情報や通知の映り込みを別途点検する。動画を再生していなければ画質・音声は未検証と報告する。
7. **移動が必要なら梱包する。** `pack <project> --out <bundle-dir> --json` で参照メディアを含む束を作り、Step 6のチェッカーへ `--artifact <bundle-dir>` を指定する。梱包後のプロジェクトにも `info --json` を実行し、参照動画の存在を確認する。元動画とカーソルデータは削除せず、転送前に共有可否を判断する。不要なら省く。

## エラー処理

- 終了コード1、失敗イベント、`done`欠落、出力欠落は失敗。終了コード2は引数を見直す。`--json` でも引数エラーはstderrに平文で出る。`info` と `pack` は異なる成功時JSON形状を持つので `references/platform-and-protocol.md` を参照する。
- `--auto-zoom` が効かない場合は録画時のカーソルテレメトリとクリックの有無を確認する。後付けMP4からクリック位置は復元できない。
- ディスプレイのないサーバーで `record` を再試行しない。Linuxの無画面書き出しは仮想XとVulkan/ソフトウェアドライバーの構成を要し、録画を無人化するものではない。
- CLIとプロジェクト形式は変化し得る。コマンドが現在の版で不明なら `help` と現行ドキュメントで確認し、未知のフラグを推測しない。
