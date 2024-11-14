## Load the environment variables

import environ
import os
import json

import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import webbrowser

import streamlit as st
from streamlit_js import st_js, st_js_blocking

env = environ.Env()
environ.Env.read_env("/setup/.env")

from auto_analyze import save_video_to_server, get_text_zh_jp
from generate_report import genrate_report
from drive import upload_video, upload_report
import json
from content_vectorize import prepare_tfidf_embeddings
from simularity_cal import search_similar_articles_tfidf

TEMPFILE_DIR = "/tmp"


def ls_get(k, key=None):
    return st_js_blocking(f"return JSON.parse(localStorage.getItem('{k}'));", key)

def ls_set(k, v, key=None):
    jdata = json.dumps(v, ensure_ascii=False)
    st_js_blocking(f"localStorage.setItem('{k}', JSON.stringify({jdata}));", key)

def init_session():
    user_info = ls_get("user_info")
    credentials = ls_get("credentials")
    if user_info:
        st.session_state["user_info"] = user_info
    if credentials:
        st.session_state["credentials"] = credentials

def auth_flow():
    auth_code = st.query_params.get("code")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json", # replace with you json credentials from your google auth app
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid",
                "https://www.googleapis.com/auth/drive"],
        redirect_uri=env("REDIRECT_URI"),
    )
    if auth_code:
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        st.write("Login Done")
        user_info_service = build(
            serviceName="oauth2",
            version="v2",
            credentials=credentials,
        )
        user_info = user_info_service.userinfo().get().execute()
        assert user_info.get("email"), "Email not found in infos"
        st.session_state["google_auth_code"] = auth_code
        st.session_state["user_info"] = user_info
        st.session_state["credentials"] = credentials
        ls_set("user_info", user_info)
        ls_set("credentials", credentials)
        # TODO fix calling consecutive ls_set is not working 
        # ls_set("google_auth_code", auth_code)
    else:
        authorization_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
        )
        st.link_button("Sign in with Google", authorization_url)

def auth():
    init_session()
    if "user_info" not in st.session_state:
        auth_flow()

    if "user_info" in st.session_state:
        email = st.session_state["user_info"].get("email")
        st.write(f"ログイン完了 {email}")

def main(uploaded_file, movie_title, platform, url, post_date, post_time, uploader, keywords, memo, simular_post):
    ## サーバにファイルを保存
    movie_path, mime_type = save_video_to_server(uploaded_file, TEMPFILE_DIR)
    ## 自動分析
    zh_text, jp_text, error_reason, code = get_text_zh_jp(
                movie_path, 
                TEMPFILE_DIR,
                env("AMIVOICE_ONETIME_TOKEN"), env("DEEPL_API_KEY")
    )
    if error_reason:
        st.error(f"エラーが発生しました：{error_reason} (code: {code})")
        return
    ## 動画を保存
    file = upload_video(st.session_state["credentials"], movie_title, movie_path, mime_type)

    # 記事リストで検索
    st.markdown("## 4. 記事リストの検索結果")
    st.write("しばらくお待ちください...")
    # TF-IDFの埋め込みを保存
    with open('factcheck_articles_with_url_content_C.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
    prepare_tfidf_embeddings(articles)

    # 類似度検索のテスト
    #test_input = "美国制造新冠病毒？"
    #top_articles = search_similar_articles_tfidf(test_input)

    top_articles = search_similar_articles_tfidf(zh_text)
    maxAmount = 4
    for article in top_articles[:maxAmount]:
        simular_post += f"\nタイトル: {article['title']}, URL: {article['url']}, 類似度スコア: {article['similarity_score']:.4f}\n"
    st.markdown(simular_post)
    
    
    if file is None:
        st.write("動画の保存に失敗しました．")
    ## レポートを生成
    report = genrate_report(
        uploaded_file.name,
        movie_title,
        platform,
        url,
        post_date,
        post_time,
        uploader,
        keywords,
        memo,
        zh_text,
        jp_text,
        simular_post,
    )

    st.markdown("## レポート")
    st.markdown(f"```{report}```")
    ## レポートを保存
    file = upload_report(st.session_state["credentials"], movie_title, movie_path, report)
    if file is None:
        st.write("レポートの保存に失敗しました．")
    ## ファイルを削除
    os.remove(movie_path)
        

st.set_page_config(page_title="パンダキャプチャー", page_icon="🐼")
st.title("パンダキャプチャー🐼")

st.markdown("## 1. Google Driveに接続")
auth()

st.markdown("## 2. 動画をアップロード")
uploaded_file = st.file_uploader("動画をアップロードしてください",
                                  type=["mp4", "mov", "avi", "mpeg", "ogv"],
                    )

st.markdown("## 3. 動画情報を入力")
movie_title = st.text_input("動画タイトル")

platform_options = ["抖音（DouYin）", "微博（Weibo）", "西瓜（XiGua）", "小紅書（RED）", "その他"]
platform = st.selectbox("動画のプラットフォーム", platform_options)

if platform == "その他":
    custom_platform = st.text_input("プラットフォーム名を入力してください")
    platform = custom_platform if custom_platform else platform_options[0]

url = st.text_input("動画のURL")
dt_available = st.checkbox("投稿日時不明")
post_date = st.date_input("動画の投稿日", disabled = dt_available)
post_time = st.time_input("動画の投稿時間", disabled = dt_available)

uploader = st.text_input("動画投稿者")
keywords = st.text_input("キーワード")
memo = st.text_area("メモ")
simular_post = ""



btn_disabled = uploaded_file is None or len(movie_title) == 0 or len(platform)==0

if st.button("レポートを生成", disabled=btn_disabled):
    if dt_available:
        post_date = None
        post_time = None
    main(
        uploaded_file,
        movie_title,
        platform,
        url,
        post_date,
        post_time,
        uploader,
        keywords,
        memo,
        simular_post,
    )









