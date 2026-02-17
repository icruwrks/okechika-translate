# okechika-translate

## 概要

- 桶地下のサイトを翻訳するための個人プロジェクトです
- 解析対象のサイト: https://www.qtes9gu0k.xyz

## 使い方
- taiouhyou.csvを元に、htmlを翻訳します
- 翻訳後は〇〇_translate.htmlになります
- HTMLファイルは`original/`フォルダに配置してください
- 変換後のファイルは`translated/`フォルダに保存されます

## コマンド

### 一括変換（推奨）
`original/`フォルダ内のすべてのHTMLファイルを一括で変換します：
```bash
python translate_html_v3.py
```

### 個別変換
特定のHTMLファイルのみを変換する場合：
```bash
python translate_html_v2.py original\あげぎぺやほせ.html
python translate_html_v2.py 'original\倏俊丣亞乱丌代 _ あげぎぺやほせ.html'
python translate_html_v2.py 'original\什儺伏丂佄代伸 _ あげぎぺやほせ.html'
python translate_html_v2.py 'original\倄乼 _ あげぎぺやほせ.html'
```

## 翻訳の参考リンク

- https://unknownglyphviewer.pages.dev/

