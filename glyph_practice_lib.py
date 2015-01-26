# -*- coding: utf-8 -*-
"""
create_glyph_practice

搭配教育部某網站可以產生生字練習簿的工具。
輸入：把生字都放在文字檔(text_file)裡
使用：create_glyph_practice text_file
輸出：目前固定為 all.pdf
Dependencies:
 * wkhtmltopdf: 請到 official site 下載最新版來安裝。
 * pdftk: sudo apt-get install pdftk
 * requests: pip install requests --user
在 Ubuntu 12.04 下開發，其他 distro/平台未測試過。

@author: Yan-ren Tsai <elleryq (at) gmail (dot) com>
"""
from __future__ import print_function, unicode_literals
import sys
import os
import codecs
import requests
from itertools import chain
from subprocess import call


# http://sahandsaba.com/thirty-python-language-features-and-tricks-you-may-not-know.html
group_adjacent = lambda a, k: zip(*([iter(a)] * k))

URL = "http://eword.ntpc.edu.tw/export.asp"
chunk_size = 4096
MAX_E_WORD = 30


def get_practice_paper(s, output="practice1.doc"):
    big5_s = s.encode('big5')
    r = requests.post(URL, data={
        'e_word': big5_s,
        'e_file': output
    })
    with open(output, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)


def html2pdf(html):
    pdf = html[:html.rfind('.')] + ".pdf"
    call(["wkhtmltopdf", "-q", "-g", "--zoom", "0.95", "-s", "A4",
          html, pdf])
    return pdf


def pdfjoin(pdfs, output):
    if len(pdfs) > 26:
        print("Not tested!!")

    inputs = []
    cats = []
    for i, pdf in enumerate(pdfs[:26]):
        _id = chr(65 + i)
        inputs.append("{_id}={fn}".format(
            _id=_id,
            fn=pdf
        ))
        cats.append(_id)
    cmd = ["pdftk"]
    cmd.extend(inputs)
    cmd.append('cat')
    cmd.extend(cats)
    cmd.extend(["output", output])
    call(cmd)
    return output


def generate(fn):
    if fn.endswith(".txt"):
        pdf_fn = fn.replace(".txt", ".pdf")
    else:
        pdf_fn = "{0}.pdf".format(fn)
    count = 1
    pdfs = []
    with codecs.open(fn, encoding="utf-8") as f:
        chars = list(chain.from_iterable(
            [line.strip().replace(' ', '') for line in f]))
        reminder = len(chars) % MAX_E_WORD
        if reminder:
            chars.extend(list(' '*(MAX_E_WORD-reminder)))
        grouped_chars = group_adjacent(chars, MAX_E_WORD)
        for g in grouped_chars:
            s = ''.join(g)
            html = "{0}.html".format(count)
            get_practice_paper(s, html)
            pdfs.append(html2pdf(html))
            os.remove(html)
            count = count + 1
    pdf_output = pdfjoin(pdfs, pdf_fn)
    for pdf in pdfs:
        os.remove(pdf)
    return pdf_output


if __name__ == "__main__":
    if len(sys.argv) == 1:
        fn = raw_input('Please input filename:')
        print(fn)
    else:
        fn = sys.argv[1]
    generate(fn)
