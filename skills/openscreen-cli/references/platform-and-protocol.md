# 実行ファイル・コマンド・結果の契約

使う前に `help` で実際のインストール版の書式を確認する。下記は当該CLI仕様の操作メモであり、版更新で再確認する。

## 実行ファイル

- macOS: `/Applications/Openscreen.app/Contents/MacOS/Openscreen`。シェルからは例として `OSCLI=/Applications/Openscreen.app/Contents/MacOS/Openscreen; "$OSCLI" help`。
- Windows インストーラー: インストール先の `Openscreen.exe`。現在のユーザー向けなら `%LOCALAPPDATA%\Programs\Openscreen\Openscreen.exe`、全ユーザー向けなら `C:\Program Files\Openscreen\Openscreen.exe`。PowerShellでは `& 'C:\Program Files\Openscreen\Openscreen.exe' help`。
- Linux パッケージ / Nix: `openscreen`。AppImage: ダウンロードした実行ファイルをそのディレクトリから呼ぶ。実ファイル名は版に合わせる。

## 未インストール時の案内

`openscreen` がPATHにないだけなら、上記の実行ファイルをフルパスで呼び出す。実行ファイルも見つからなければ、「OpenScreenの実行ファイルが見つからないため、この環境では録画・書き出しを開始できない」と伝え、[公式インストール手順](https://getopenscreen.com/ja/docs/installation/)と[公式リリース](https://github.com/getopenscreen/openscreen/releases)を案内する。CLIはデスクトップアプリに含まれるため、独立したCLIパッケージの導入コマンドを推測しない。

- 利用環境のOSとCPUアーキテクチャに合う配布物を公式ページで確認して示す。特定のダウンロードURLやパッケージ管理コマンドは、公式情報で確認できたものだけ案内する。
  - macOS: Apple Silicon / Intelに合う `.dmg` を入手し、アプリをApplicationsに配置する。
  - Windows: 公式ガイドのMicrosoft Store、または特定版が必要ならReleasesの `.exe` を案内する。
  - Linux: ディストリビューションに合うパッケージ、またはAppImageを案内する。録画にはデスクトップ環境が必要。
- 導入後は上記のOS別実行ファイルで `help` を実行するよう案内する。エージェントが導入完了を確認できる場合は実行し、成功後に元の依頼へ戻る。
- 本スキルのCLI仕様メモは[v1.13.0](https://github.com/getopenscreen/openscreen/releases/tag/v1.13.0)を対象としている。最新版が同じ仕様とは限らないため、導入した版の `help` と[公式CLIドキュメント](https://getopenscreen.com/ja/docs/cli/)で必要なコマンド・オプションを確認する。必要な機能を確認できなければ処理を止め、対応版が必要なことを説明する。
- インストールの案内だけではダウンロード・インストールを開始しない。利用者が導入作業も依頼している場合は、その範囲で作業する。インストール済みのアプリを無断で置き換えたり、ダウングレードしたりしない。

実行ファイルが存在するのに起動に失敗する場合は、stderrなどを確認して起動エラーとして扱い、再インストールが必要と即断しない。

## 基本コマンド

```bash
openscreen sources --json
openscreen record --window "My App" --duration 20 --project demo.openscreen --json
openscreen captions demo.openscreen --json
openscreen export demo.openscreen -o demo.mp4 --auto-zoom --json
openscreen info demo.openscreen --json
openscreen pack demo.openscreen --out bundle/ --json
```

- `record --display <index>` は `sources` に表示される画面インデックス（既定0）。`--window <title>` はタイトルの部分一致で最初のウィンドウを選び、`--display` より優先。`--mic-device <name>` は名前の部分一致でマイクを選び、`--mic` を含意する。Linuxでは画面共有ポータル側の選択が優先し、`--window` / `--display` はソースを決められない。
- `record --project` は `.openscreen` 拡張子が必要。停止には `--duration`、Ctrl+C、stdinの `stop` / `q` / `quit` を使い、強制終了はしない（stdinを閉じるだけでは停止しない）。WindowsではSIGTERMを使わない。CLI録画にはWebカメラのオプションがない。macOSではクリック取得にアクセシビリティ権限が必要。
- `captions` はプロジェクトの録画音声が必要で、プロジェクトに字幕注釈を書き込む。**動画への焼き込みはexport時**。`--min-words 2 --max-words 7` で一字幕当たりの語数を指定でき、両者の範囲は1〜12。再実行すると先に追加した自動字幕は置換される。初回はモデル取得の通信が発生する。字幕ファイルを書き出すコマンドではない。
- `export --auto-zoom` はOpenScreenのカーソルテレメトリ中のクリックを使う。他の録画アプリのMP4や `--cursor system` 録画では自動ズームは生成できない。`-o out.mp4` と `-o out.gif` から形式を指定する。`--format mp4|gif` は `-o` の拡張子と一致させる。`--quality medium|good|source` はそれぞれ720p/1080p/最小クリップのクロップ後サイズ（アップスケールしない）。CLIのMP4はH.264・60 fps固定でビットレートを調整できない。GIFでは `--gif-fps 15|20|25|30`、`--gif-size medium|large|original` を選べる（GIFに音声はない）。
- MP4のナレーション後付けは `export demo.openscreen -o demo.mp4 --audio voice.m4a --audio-mode replace --audio-offset 0 --json`。`--audio` はmp3/wav/m4a。`mix`（既定）は元音声を40%のゲインで残し、`replace` は元音声を外す。`captions` は録画内の音声しか読めず、書き出し時に後付けしたナレーションから字幕を生成しない。
- 外部MP4用の最小JSONは `{ "version": 2, "media": { "screenVideoPath": "/path/to/clip.mp4" }, "editor": {} }`。動画と同じフォルダーに `.openscreen` として保存する。プロジェクトが参照できるのは録画ディレクトリ内かプロジェクトと同じフォルダーのメディアに限られる。
- `sources -o sources.json` はstdoutのNDJSONと違い、ペイロード本体のみを書き込む。`xvfb-run` のstderr/stdout結合でNDJSONが壊れる場合も使う。シェルで前回のファイルが残っていても、終了コード0を確認してから読む。
- ソースチェックアウトからの起動はアプリとネイティブヘルパーをビルドした後で `npm run cli -- <command> [options]`。Chromiumサンドボックスが起動できない場合の `--no-sandbox` はサブコマンドの**前**に置き、隔離性への影響を理解した環境に限る。通常は付けない。CLIはアプリの単一インスタンスロックを使わないためGUIを開いた状態でも実行できる。

## 終了コードと標準出力の取得例（POSIXシェル）

パイプでCLIの終了コードを失わないよう、一旦別ファイルへ書き込む。出力名は毎回新しくし、失敗時に過去の成果物を誤認しない。

```bash
OSCLI=/Applications/Openscreen.app/Contents/MacOS/Openscreen
"$OSCLI" export demo.openscreen -o demo.mp4 --auto-zoom --json > export.jsonl 2> export.stderr
code=$?
uv run --no-project python skills/openscreen-cli/scripts/check-result.py --command export --exit-code "$code" --input export.jsonl --artifact demo.mp4
```

Linuxでは `OSCLI=openscreen` に変更する。Windows/PowerShellは `$LASTEXITCODE` と `2>` によってCLIの終了コードとstderrを確保する。上の例はこのリポジトリ直下を作業ディレクトリにした場合。スキルをインストールして使う場合は、インストール先のスキルディレクトリにある `scripts/check-result.py` を指定する。

## NDJSON・結果の差分

- `record`、`sources`、`captions`、`export` は成功時に最後の `{"event":"done","success":true,...}` を出す。`record` の `done.projectPath`、`export` の `done.outputPath`、`captions` の `done.projectPath` を使用する。`cursorDataPath` は記載されてもファイルがない場合がある。`warning`や`progress`もあり得る。
- `pack --json` は `started` を送らず成功時に `done` を送る。`done.files` に実際にコピーしたファイルのパスが載る。結果チェッカーには `--artifact <bundle-dir>` を渡し、さらに梱包後のプロジェクトを `info --json` で検査する。`info --json` は `event` のない要約JSONを1つだけ出し、`screenVideoExists` を確認できる。失敗した `pack` または `info` は `done` がなく `error` で終わることがある。
- 終了コード0=成功、1=実行失敗、2=引数誤り。クラッシュ時には `done` がないことがある。必ず終了コードを先に確認する。
- `export` は正常なキャンセル操作を持たない。途中でプロセスを停止した場合、残ったファイルを破棄する。

## 実行境界

Electronはウィンドウを開かなくても画面サーバーを要する。Linux無画面環境で書き出す場合のみ、`xvfb-run` に加えVulkanドライバー（GPUなしならlavapipe等）を用意する。録画にはデスクトップと共有ダイアログへの人の応答が必要。OSアクセス権限を緩めたり、Waylandの`input`グループを無断で追加したりしない（このグループは他のプログラムにもキーボード等の入力を読める権限を与える）。
