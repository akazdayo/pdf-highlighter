# from spire.pdf.common import TextFindParameter
import pymupdf
import gemini


def mark_word(page, text):
    """Underline each word that contains 'text'."""
    found = 0
    wlist = page.get_text("words", delimiters=None)  # make the word list
    for w in wlist:  # scan through all words on page
        if text in w[4]:  # w[4] is the word's string
            found += 1  # count
            r = pymupdf.Rect(w[:4])  # make rect from word bbox
            page.add_underline_annot(r)  # underline
    return found


doc = pymupdf.open("quantum.pdf")

result = gemini.get_pdf_text("quantum.pdf")
texts = []
for text in result["texts"]:
    texts.append(text["text"])

for text in texts:
    # 矩形領域内で指定のテキストの出現箇所を検索する
    found = mark_word(doc[25], text)

doc.save("marked-" + doc.name)
