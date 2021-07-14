import re

def del2():
    r = open('ys19_new.csv', mode='rt', encoding='utf-8')
    text = r.read()
    print(text)

    text = re.sub('(<([^>]+)>)', '', text)
    print(text)

    nospace = re.sub('&nbsp;', '', text)
    print(nospace)

    f = open('ys19_noTag2.csv', mode='wt', encoding='utf-8')
    f.write(nospace)
    f.close()


def del1():
    r = open('ScrapData/ys_press_20.csv', mode='rt', encoding='utf-8')
    text = r.read()
    # print(r.read())

    # test = '<div class=""hwp_editor_board_content"" id=""hwpEditorBoardContent"" data-jsonlen=""16294"" data-hjsonver=""1.0""><!--[data-hwpjson]{""documentPr"": {</div> hello my name is juntae <div class=""hwp_editor_board_content"" id=""hwpEditorBoardContent"" data-jsonlen=""16294"" data-hjsonver=""1.0""><!--[data-hwpjson]{""documentPr"": {</div> hello my name is juntae'

    p = re.compile(r'<div class=""hwp_editor_board_content"".*?</div>', re.DOTALL)
    # m = p.match(test)
    # print(m)

    text = p.sub("", text)
    print(text)
    print("done")

    f = open('new.csv', mode='wt', encoding='utf-8')
    f.write(text)
    f.close()


del2()