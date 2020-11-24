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

URL = 'https://www.aozora.gr.jp/cards/000096/files/2093_ruby_28087.zip'
tmp_dir = 'tmp/'
OUTPUT_FILE = 'output.txt'

def download_file(url):
    """URL を指定してカレントディレクトリにファイルをダウンロードする
    """
    filename = url.split('/')[-1]
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

def unzip(filename, target_dir):
    """ファイル名を指定して zip ファイルをカレントディレクトリに展開する
    """
    if not zipfile.is_zipfile(filename):
        print(filename, 'is not zipfile.')
        return -1
    zfile = zipfile.ZipFile(filename)
    zfile.extractall(target_dir)
    zfile.close()
    src_filenames = glob.glob(target_dir + '*.txt')
    print(src_filenames)
    return src_filenames

def sjisToUtf8(path):
    with open(path, mode="r", encoding='shift_jis') as f:
        lines = f.readlines()
        print(lines[:10])

def readSjis(path):
    with open(path, mode="r", encoding='shift_jis') as f:
        lines = f.readlines()
    return lines


def convert(text):
    """
    除去
    参考: https://newtechnologylifestyle.net/711-2/
    """
    # ルビ、注釈などの除去
    text  = re.split(r'\-{5,}', text)[2]
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
    text = '\n'.join(text.split('\n')[:400])
    words = {}
    t = Tokenizer()
    # print([ token for token in  t.tokenize(text[:200])])

    c = collections.Counter(t.tokenize(text, wakati=True))
    # for token in t.tokenize(text):
    #     word = token.surface
    #     words[word] = words.get(word, 0) + 1
    # d = [(v, k) for k, v in words.items()]
    # d.sort()
    # d.reverse()

    # 降順で表示
    print(c.most_common()[:30])

def main():
    zip_file = download_file(URL)
    filenames = unzip(zip_file, tmp_dir)
    lines = readSjis(filenames[0])
    print(lines[:10])

    # 作品情報
    title = lines[0].strip()
    author = lines[1].strip()
    print(title, author)
    text = ''.join(lines[2:])
    text = convert(text)
    print(text.split('\n')[:40])
    print(text[:400])

    wakati(text)



if __name__ == "__main__":
    main()


    
