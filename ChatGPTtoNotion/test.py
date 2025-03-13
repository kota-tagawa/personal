from notion_client import Client
import os

# Notionクライアントの作成
token = os.environ.get("NOTION_TOKEN")
client = Client(auth=token)

# テスト用にページを作成
try:
    response = client.pages.create(
        parent={"database_id": "111e6142de5980308bb7d8eea15ea7d2"},  # ここに自分のデータベースIDを入力
        properties={
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "テストページ"
                        }
                    }
                ]
            }
        }
    )
    print("ページが作成されました:", response)
except Exception as e:
    print("エラー:", e)