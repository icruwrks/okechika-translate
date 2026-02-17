#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translatedフォルダ内のHTMLファイルからl-page__header-titleを抽出し、
index.htmlのリンクリストを生成するスクリプト
"""

import re
from pathlib import Path
from html.parser import HTMLParser


class TitleExtractor(HTMLParser):
    """HTMLからl-page__header-titleクラスの要素を抽出するパーサー"""
    
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = None
        
    def handle_starttag(self, tag, attrs):
        """開始タグの処理"""
        if tag.lower() in ['h1', 'h2', 'h3', 'div', 'span', 'p']:
            for attr_name, attr_value in attrs:
                if attr_name == 'class' and attr_value and 'l-page__header-title' in attr_value:
                    self.in_title = True
                    break
    
    def handle_endtag(self, tag):
        """終了タグの処理"""
        if self.in_title:
            self.in_title = False
    
    def handle_data(self, data):
        """テキストデータの処理"""
        if self.in_title and not self.title:
            self.title = data.strip()


def extract_title_from_html(html_path):
    """
    HTMLファイルからl-page__header-titleのテキストを抽出
    
    Args:
        html_path: HTMLファイルのパス
        
    Returns:
        str: 抽出されたタイトル、見つからない場合はNone
    """
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        parser = TitleExtractor()
        parser.feed(html_content)
        return parser.title
    except Exception as e:
        print(f"エラー: {html_path.name} の読み込みに失敗: {e}")
        return None


def generate_link_list(translated_dir):
    """
    translatedフォルダ内のHTMLファイルからリンクリストを生成
    
    Args:
        translated_dir: translatedフォルダのパス
        
    Returns:
        list: (ファイル名, タイトル)のタプルのリスト
    """
    html_files = sorted(translated_dir.glob('*.html'))
    
    links = []
    for html_file in html_files:
        title = extract_title_from_html(html_file)
        if not title:
            # タイトルが見つからない場合はファイル名（拡張子なし）を使用
            title = html_file.stem.replace('_translate', '')
        
        links.append((html_file.name, title))
        print(f"[OK] {html_file.name} -> {title}")
    
    return links


def generate_html_list_items(links):
    """
    リンクリストからHTMLのリスト項目を生成
    
    Args:
        links: (ファイル名, タイトル)のタプルのリスト
        
    Returns:
        str: HTMLのリスト項目
    """
    html_items = []
    for filename, title in links:
        html_items.append(
            f'                    <li style="margin-bottom: 10px;">\n'
            f'                        <a href="translated/{filename}">{title}</a>\n'
            f'                    </li>'
        )
    
    return '\n'.join(html_items)


def main():
    """メイン処理"""
    # Windows環境でのUTF-8出力対応
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    
    script_dir = Path(__file__).parent
    translated_dir = script_dir / 'translated'
    
    if not translated_dir.exists():
        print(f"エラー: {translated_dir} が見つかりません")
        return
    
    print("=" * 60)
    print("HTMLタイトル抽出ツール")
    print("=" * 60)
    print(f"対象ディレクトリ: {translated_dir}")
    print("=" * 60)
    print()
    
    # リンクリストを生成
    links = generate_link_list(translated_dir)
    
    print()
    print("=" * 60)
    print(f"合計 {len(links)} 個のファイルを処理しました")
    print("=" * 60)
    print()
    
    # HTMLリスト項目を生成
    html_list = generate_html_list_items(links)
    
    # 結果を出力
    print("以下のHTMLをindex.htmlにコピーしてください:")
    print("-" * 60)
    print(html_list)
    print("-" * 60)
    
    # ファイルにも保存
    output_file = script_dir / 'link_list.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_list)
    
    print()
    print(f"リンクリストを {output_file} に保存しました")


if __name__ == '__main__':
    main()
