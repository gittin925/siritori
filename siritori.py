import streamlit as st

kana = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょぁぃぅぇぉっー"
tyokuonn = "はひふへほかきくけこさしすせそたちつてと"
dakuonn = "ばびぶべぼがぎぐげござじずぜぞだぢづでど"
handakuonn = "ぱぴぷぺぽ"
youonn = "ゃゅょぁぃぅぇぉ","やゆよあいうえお"
tyouonn = "ー"

def check(word):
    return all([(w in kana) for w in word])


def kana_match(end, start):
    if end == start:
        return True

    if end in youonn[0]:
        return youonn[1][youonn[0].index(end)] == start

    if end in tyokuonn: number = tyokuonn.index(end)
    elif end in dakuonn: number = dakuonn.index(end)
    elif end in handakuonn: number = handakuonn.index(end)
    else: return False

    permission = tyokuonn[number]+dakuonn[number] if number>4 else tyokuonn[number]+dakuonn[number]+handakuonn[number]
    return start in permission

def clear_text():
    st.session_state["text"] = ""

st.title("しりとりしとり")

if "word" not in st.session_state:
    st.session_state.word = ""

if "history" not in st.session_state:
    st.session_state.history = []

input_word = st.text_input(f"前の単語：{st.session_state.word if st.session_state.word else "未入力"}",key="text",placeholder="ひらがな入力")

col1, col2, col3 = st.columns([2,1,1])

with col1:
    if st.session_state.history and st.session_state.history[-1][-1]=="ん":
        st.error("終了")
    elif st.button("入力完了"):
        if not input_word:
            st.warning("単語を入力してください")
        #ひらがな以外が含まれていないかを判定
        elif check(input_word):
            if input_word in st.session_state.history:
                st.warning("すでに使われている単語です。")
            elif not st.session_state.word:
                #最初の単語を記録
                st.session_state.word = input_word
                st.session_state.history.append(input_word)
                st.rerun()
            else:
                #つづく単語かを判定
                end = st.session_state.word[-1] if not st.session_state.word.endswith(tyouonn) else st.session_state.word[-2]
                start = input_word[0]
                if kana_match(end,start):
                    st.session_state.word = input_word
                    st.balloons()
                    st.session_state.history.append(input_word)
                    st.rerun()
                    st.write("次の単語を入力")
                else:
                    st.write("つづく単語を入力")
        else:
            st.warning("使用できない文字が含まれています")

with col2:
    if st.button("クリア",on_click=clear_text):
        pass

with col3:
    if st.button("リセット",on_click=clear_text):
        st.session_state.word = ""
        st.session_state.history = []
        st.rerun()

st.text_area("履歴"," - ".join(st.session_state.history),placeholder="しりとりれきが表示される",disabled=True)