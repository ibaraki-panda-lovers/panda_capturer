import datetime

def genrate_report(        
        file_name,
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
    ):
    # generate report
    report = f"""
動画タイトル: {movie_title}
ファイル名: {file_name}
プラットフォーム: {platform}
URL: {url}
レポート作成日時: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")}
投稿日時: {post_date} {post_time}
投稿者: {uploader}
キーワード: {keywords}
メモ: {memo}

中国語文字起こし:{zh_text}

日本語翻訳:{jp_text}

関連記事:{simular_post}
"""
    
    return report