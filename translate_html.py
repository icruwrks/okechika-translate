#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HTMLファイルを対応表CSVに基づいて文字変換するプログラム
"""

import csv
import sys
import os
from pathlib import Path


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


def translate_html_file(input_path, csv_path):
    """
    HTMLファイルを変換して新しいファイルに保存する
    
    Args:
        input_path: 入力HTMLファイルのパス
        csv_path: 変換対応表CSVファイルのパス
    """
    # 変換対応表を読み込む
    translation_table = load_translation_table(csv_path)
    
    # 入力ファイルを読み込む
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"エラー: 入力ファイルが見つかりません: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"エラー: 入力ファイルの読み込みに失敗しました: {e}")
        sys.exit(1)
    
    # テキストを変換
    translated_content = translate_text(html_content, translation_table)
    
    # 出力ファイル名を生成
    input_path_obj = Path(input_path)
    output_filename = f"{input_path_obj.stem}_translate{input_path_obj.suffix}"
    output_path = input_path_obj.parent / output_filename
    
    # 変換後のファイルを保存
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        print(f"変換完了: {output_path}")
        return output_path
    except Exception as e:
        print(f"エラー: 出力ファイルの保存に失敗しました: {e}")
        sys.exit(1)


def main():
    """
    メイン処理
    """
    # コマンドライン引数のチェック
    if len(sys.argv) < 2:
        print("使用方法: python translate_html.py <入力HTMLファイル> [対応表CSVファイル]")
        print("例: python translate_html.py あげぎぺやほせ.html taiouhyou.csv")
        sys.exit(1)
    
    input_html = sys.argv[1]
    
    # CSVファイルのパス（指定がなければデフォルトでtaiouhyou.csv）
    if len(sys.argv) >= 3:
        csv_file = sys.argv[2]
    else:
        # スクリプトと同じディレクトリのtaiouhyou.csvを使用
        script_dir = Path(__file__).parent
        csv_file = script_dir / 'taiouhyou.csv'
    
    print(f"入力ファイル: {input_html}")
    print(f"対応表CSV: {csv_file}")
    print("-" * 50)
    
    # 変換実行
    translate_html_file(input_html, csv_file)


if __name__ == '__main__':
    main()
