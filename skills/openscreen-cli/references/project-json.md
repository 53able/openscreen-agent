# `.openscreen` への任意の手動ズーム・注釈追加

録画→字幕→自動ズームだけなら、この編集は不要。プロジェクト形式は更新で変わるため、**この例は `version: 2`、`editor.zoomRegions` と `editor.annotationRegions` が配列の場合だけ**使う。録画をCLIの `--project` で作成し、必要なら字幕を生成した後に実施する。既存の編集を上書きせず追記する。

実行前に、プロジェクトが参照するメディアがあることを `info <project> --json` で確認する。下記はスクリプトの構造例。プロジェクトファイルを指定し、タイミング・位置・表示内容を実際の動画に合わせて変更する。2つ目の注釈が不要なら、`annotationRegions.push(...)` を削除する。出力前に動画をプレビューし、対象UIや秘密情報を注釈で覆っていないか確認する。

```bash
node - demo.openscreen <<'JS'
const fs = require('node:fs');
const file = process.argv[2];
const project = JSON.parse(fs.readFileSync(file, 'utf8'));
if (project.version !== 2 ||
    !Array.isArray(project.editor?.zoomRegions) ||
    !Array.isArray(project.editor?.annotationRegions)) {
  throw new Error('想定外のプロジェクト形式。変更せずに現行形式を調べる');
}
const ids = new Set([
  ...project.editor.zoomRegions,
  ...project.editor.annotationRegions,
].map(region => region.id));
if (ids.has('agent-zoom-1') || ids.has('agent-text-1')) {
  throw new Error('同名の編集がある。重複追加せず、既存の領域を確認する');
}
fs.copyFileSync(file, `${file}.bak`, fs.constants.COPYFILE_EXCL);
project.editor.zoomRegions.push({
  id: 'agent-zoom-1', startMs: 2000, endMs: 6000, depth: 3,
  focus: {cx: 0.5, cy: 0.4}, focusMode: 'manual', source: 'manual',
});
project.editor.annotationRegions.push({
  id: 'agent-text-1', startMs: 500, endMs: 4000,
  type: 'text', content: 'One-click setup', textContent: 'One-click setup',
  position: {x: 8, y: 6}, size: {width: 40, height: 12},
  style: {fontSize: 24, color: '#fff'}, zIndex: 1,
});
const tmp = `${file}.${process.pid}.tmp`;
try {
  fs.writeFileSync(tmp, JSON.stringify(project, null, 2));
  fs.renameSync(tmp, file);
} finally {
  if (fs.existsSync(tmp)) fs.unlinkSync(tmp);
}
JS
```

`depth: 3` は1.8倍、`cx` / `cy` はフレーム内の比率。原本の `*.bak` は書き出しの検証が済むまで残す。既存バックアップがある場合は停止して別名を用意する。編集後は `info demo.openscreen --json` でプロジェクトと参照先を確認し、書き出した動画を再生してズームと注釈が意図した箇所にあることを確認する。更新版で未知の構造なら修正せず、現行の仕様に合わせて例を見直す。
