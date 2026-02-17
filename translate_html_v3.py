#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTMLファイルを対応表CSVに基づいて文字変換するプログラム（一括変換版）
original/フォルダ内のすべてのHTMLファイルを一括で変換します
HTMLの構造、CSS、JavaScript、属性値は保護し、テキストコンテンツのみを変換します
"""

import csv
import sys
import re
from pathlib import Path
from html.parser import HTMLParser


def load_translation_table(csv_path):
    """
    CSVファイルから変換対応表を読み込む
    
    Args:
        csv_path: CSVファイルのパス
        
    Returns:
        dict: 変換元文字をキー、変換先文字を値とする辞書
    """
    translation_table = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                source = row.get('変換元', '').strip()
                target = row.get('変換先', '').strip()
                if source and target:
                    translation_table[source] = target
        
        print(f"変換対応表を読み込みました: {len(translation_table)}件")
        return translation_table
        
    except FileNotFoundError:
        print(f"エラー: CSVファイルが見つかりません: {csv_path}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: CSVファイルの読み込みに失敗しました: {e}")
        sys.exit(1)


def translate_text(text, translation_table):
    """
    テキストを対応表に基づいて変換する
    
    Args:
        text: 変換対象のテキスト
        translation_table: 変換対応表の辞書
        
    Returns:
        str: 変換後のテキスト
    """
    result = []
    for char in text:
        # 対応表に存在する文字は変換、存在しない文字はそのまま
        result.append(translation_table.get(char, char))
    return ''.join(result)


class HTMLTranslator(HTMLParser):
    """
    HTMLを解析して、テキストコンテンツのみを変換するパーサー
    """
    
    def __init__(self, translation_table):
        super().__init__()
        self.translation_table = translation_table
        self.output = []
        self.in_script = False
        self.in_style = False
        
    def handle_starttag(self, tag, attrs):
        """開始タグの処理"""
        # scriptとstyleタグの開始を記録
        if tag.lower() == 'script':
            self.in_script = True
        elif tag.lower() == 'style':
            self.in_style = True
        
        # タグをそのまま出力
        attrs_str = ''
        if attrs:
            attrs_list = []
            for attr_name, attr_value in attrs:
                if attr_value is None:
                    attrs_list.append(attr_name)
                else:
                    # 属性値は変換しない（クラス名、ID、URLなどを保護）
                    attrs_list.append(f'{attr_name}="{attr_value}"')
            attrs_str = ' ' + ' '.join(attrs_list)
        
        self.output.append(f'<{tag}{attrs_str}>')
    
    def handle_endtag(self, tag):
        """終了タグの処理"""
        # scriptとstyleタグの終了を記録
        if tag.lower() == 'script':
            self.in_script = False
        elif tag.lower() == 'style':
            self.in_style = False
        
        self.output.append(f'</{tag}>')
    
    def handle_data(self, data):
        """テキストデータの処理"""
        # scriptとstyleタグ内のテキストは変換しない
        if self.in_script or self.in_style:
            self.output.append(data)
        else:
            # テキストコンテンツのみを変換
            translated = translate_text(data, self.translation_table)
            self.output.append(translated)
    
    def handle_comment(self, data):
        """コメントの処理"""
        # コメントはそのまま出力
        self.output.append(f'<!--{data}-->')
    
    def handle_decl(self, decl):
        """DOCTYPE宣言の処理"""
        self.output.append(f'<!{decl}>')
    
    def handle_pi(self, data):
        """処理命令の処理"""
        self.output.append(f'<?{data}>')
    
    def get_output(self):
        """変換結果を取得"""
        return ''.join(self.output)


def translate_html_file(input_path, translation_table, output_dir):
    """
    HTMLファイルを変換して新しいファイルに保存する
    
    Args:
        input_path: 入力HTMLファイルのパス
        translation_table: 変換対応表の辞書
        output_dir: 出力先ディレクトリ
        
    Returns:
        Path: 出力ファイルのパス、失敗時はNone
    """
    # 入力ファイルを読み込む
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"  ⚠ エラー: 入力ファイルが見つかりません: {input_path}")
        return None
    except Exception as e:
        print(f"  ⚠ エラー: 入力ファイルの読み込みに失敗しました: {e}")
        return None
    
    # HTMLを解析して変換
    parser = HTMLTranslator(translation_table)
    parser.feed(html_content)
    translated_content = parser.get_output()
    
    # 出力ファイル名を生成
    input_path_obj = Path(input_path)
    output_filename = f"{input_path_obj.stem}_translate{input_path_obj.suffix}"
    output_path = output_dir / output_filename
    
    # _filesフォルダへの参照を更新 (xxx_files/ -> ../files/xxx_files/)
    basename = input_path_obj.stem
    files_folder_old = f"{basename}_files/"
    files_folder_new = f"../files/{basename}_files/"
    translated_content = translated_content.replace(files_folder_old, files_folder_new)
    
    # 変換後のファイルを保存
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        print(f"  ✓ 変換完了: {output_path.name}")
        return output_path
    except Exception as e:
        print(f"  ⚠ エラー: 出力ファイルの保存に失敗しました: {e}")
        return None


def translate_all_html_files(input_dir, csv_path, output_dir):
    """
    指定ディレクトリ内のすべてのHTMLファイルを変換する
    
    Args:
        input_dir: 入力ディレクトリ（original/）
        csv_path: 変換対応表CSVファイルのパス
        output_dir: 出力ディレクトリ（translated/）
    """
    # 変換対応表を読み込む
    translation_table = load_translation_table(csv_path)
    
    # 出力ディレクトリを作成
    output_dir.mkdir(exist_ok=True)
    
    # HTMLファイルを検索
    html_files = list(input_dir.glob('*.html'))
    
    if not html_files:
        print(f"\nエラー: {input_dir} にHTMLファイルが見つかりません")
        return
    
    print(f"\n{len(html_files)}個のHTMLファイルを変換します...")
    print("-" * 60)
    
    # 各HTMLファイルを変換
    success_count = 0
    fail_count = 0
    
    for html_file in html_files:
        print(f"\n変換中: {html_file.name}")
        result = translate_html_file(html_file, translation_table, output_dir)
        if result:
            success_count += 1
        else:
            fail_count += 1
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print(f"変換完了: {success_count}個成功, {fail_count}個失敗")
    print("=" * 60)


def main():
    """
    メイン処理
    """
    # Windows環境でのUTF-8出力対応
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    # スクリプトのディレクトリを取得
    script_dir = Path(__file__).parent
    
    # デフォルトのパス設定
    input_dir = script_dir / 'original'
    output_dir = script_dir / 'translated'
    csv_file = script_dir / 'taiouhyou.csv'
    
    # コマンドライン引数で上書き可能
    if len(sys.argv) >= 2:
        input_dir = Path(sys.argv[1])
    if len(sys.argv) >= 3:
        output_dir = Path(sys.argv[2])
    if len(sys.argv) >= 4:
        csv_file = Path(sys.argv[3])
    
    # 入力ディレクトリの存在確認
    if not input_dir.exists():
        print(f"エラー: 入力ディレクトリが見つかりません: {input_dir}")
        print("\n使用方法: python translate_html_v3.py [入力ディレクトリ] [出力ディレクトリ] [対応表CSVファイル]")
        print(f"デフォルト: python translate_html_v3.py original translated taiouhyou.csv")
        sys.exit(1)
    
    print("=" * 60)
    print("HTML一括変換ツール v3")
    print("=" * 60)
    print(f"入力ディレクトリ: {input_dir}")
    print(f"出力ディレクトリ: {output_dir}")
    print(f"対応表CSV: {csv_file}")
    print("=" * 60)
    
    # 一括変換実行
    translate_all_html_files(input_dir, csv_file, output_dir)



if __name__ == '__main__':
    main()
