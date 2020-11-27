# -*- coding: utf-8 -*-
# ドグラ・マグラを形態素解析してみる
# 参考: https://sleepless-se.net/2018/08/28/mecat-wakatigaki/
#

import glob
import os.path
import requests
import zipfile
import re
from janome.tokenizer import Tokenizer
import collections
from typing import Union


def downloadFile(url: str, target_dir='./') -> Union[str, bool]:
    """URL を指定してカレントディレクトリにファイルをダウンロードする
    """
    filename = target_dir + url.split('/')[-1]
    if os.path.exists(filename):
        # 負荷をかけないため
        print(filename, 'is downloaded already.')
        return filename
    r = requests.get(url, stream=True)
    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        print('{} is downloaded.'.format(filename))
        return filename

    # ファイルが開けなかった場合は False を返す
    return False


def unzip(filename: str, target_dir='./') -> list:
    """ファイル名を指定して zip ファイルを展開する
    """
    if not zipfile.is_zipfile(filename):
        print(filename, 'is not zipfile.')
        return -1
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(target_dir)
    zfile.close()

    # 展開したテキストのリストを取得する
    dst_filenames = glob.glob(target_dir + '*.txt')
    print(dst_filenames)
    return dst_filenames


def readSjis(path):
    with open(path, mode="r", encoding='shift_jis') as f:
        text = f.read()
    return text


def preproccessing(text):
    """テキストの前処理をする
    """
    # 作品情報
    lines = text.split('\n')
    title = lines[0].strip()
    author = lines[1].strip()
    print(title, author)

    # ルビ、注釈などの除去
    text = re.split(r'\-{5,}', text)[2]
    text = re.split(r'底本：', text)[0]
    text = re.sub(r'《.+?》', '', text)
    text = re.sub(r'［＃.+?］', '', text)
    # 全角スペース
    text = re.sub(r'\u3000', '', text)
    # 複数の改行
    text = re.sub(r'\n+', '\n', text)
    text = text.strip()
    return text


def wakati(text):
    """テキストを分かち書きにして頻出単語を求める
    """
    t = Tokenizer()
    # 単語頻度
    # c = collections.Counter(t.tokenize(text, wakati=True))

    # 特定の品詞のみ
    c = collections.Counter(token.base_form for token in t.tokenize(text)
                            if token.part_of_speech.startswith('名詞,固有名詞'))

    # 降順で表示
    print(c.most_common()[:30])


def main():
    # ドグラ・マグラ
    URL = 'https://www.aozora.gr.jp/cards/000096/files/2093_ruby_28087.zip'
    # 蟹工船
    # URL = 'https://www.aozora.gr.jp/cards/000156/files/1465_ruby_16804.zip'
    tmp_dir = 'tmp/'

    zip_file = downloadFile(URL, tmp_dir)
    filenames = unzip(zip_file, tmp_dir)
    text = readSjis(filenames[0])
    print(text[:100])

    text = preproccessing(text)
    print(text.split('\n')[:40])
    print(text[:400])

    wakati(text)


if __name__ == "__main__":
    main()
