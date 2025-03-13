import os
import re
from notion_client import Client
from flask import Flask, request, jsonify, render_template
from notion_client import Client
import re

app = Flask(__name__)

# main処理
# NotionのページURL
url = "https://www.notion.so/111e6142de5980308bb7d8eea15ea7d2?v=111e6142de598063bc48000c50b50df1&pvs=4"

# Notionのページにアクセスするためのクライアントを作成
notion = Client(auth="secret_65R7Ehtpu1XbkVZhKFklHvSdiXdnuFXyekAXtIyreFD")
database_id = "111e6142de5980308bb7d8eea15ea7d2"

#
# 末尾がコロンで終わる行で辞書のkeyを登録
# 次のkeyになる行が来るまで文字列を値に追加
#
import re

def extract_sections_from_text(user_input):
    # セクションタイトルに基づいて分割し、辞書に格納する
    section_dict = {}
    current_section_title = None
    
    # URLパターンの正規表現
    url_pattern = re.compile(r'https?://')

    for line in user_input.strip().split('\n'):
        if ':' in line and not url_pattern.search(line):
            # コロンの後ろの空白をトリムし、セクションタイトルを抽出
            current_section_title = line.split(':')[0]
            section_dict[current_section_title] = ""
        elif current_section_title:
            section_dict[current_section_title] += line + '\n'

    # セクションから不要な改行をトリムする
    trimmed_section_dict = {key: value.strip() for key, value in section_dict.items()}
    return trimmed_section_dict

#
#  NotionAPIに送信するレスポンス作成
#
def add_row_to_notion_database(section_dict):
    response = notion.pages.create(
        **{
            "parent": { "database_id": database_id
            },
            # ページのプロパティを指定する
            "properties": {
                "vocaburaly": {
                    "title": [{
                        "text": {
                            "content": section_dict.get("Phrase", "")
                        }
                    }]
                },
                "Frequency": {
                    "select": {
                        "name": section_dict.get("Frequency of use", "")
                    }
                },
                "Reference": {
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'default',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": section_dict.get("Reference", "")
                        }
                    }],
                },
                "Pronunciation": {
                    "url": section_dict.get("Pronunciation", "")
                }
            },  # end properties
            "children" : [{
                # toc block
                "object": "block",
                "type": "callout",
                "callout": {
                    'color': 'gray_background',
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": section_dict.get("Sentence", "")
                        }
                    }],
                'icon': {'emoji': '🗣', 'type': 'emoji'},
                }
            },{
                # toc block
                "object": "block",
                "type": "toggle",
                "toggle": {
                    'color': 'gray_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'blue',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "意味(English)"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": section_dict.get("Meaning in English", "Meaning in English section not found.")
                                 }
                            }]
                        }
                    }]
                }
            },{
                # toc block
                "object": "block",
                "type": "toggle",
                "toggle": {
                    'color': 'gray_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'blue',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "意味(日本語)"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": section_dict.get("Meaning in Japanese", "Meaning in Japanese section not found.")
                                 }
                            }]
                        }
                    }]
                }
            },{
                # toc block
                "object": "block",
                "type": "callout",
                "callout": {
                    'color': 'yellow_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'default',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "画像"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": "Google Image Search",
                                    "link": {
                                        "url": section_dict.get("Image", "Image section not found.")
                                    }
                                }
                            }]
                        }
                    }],
                'icon': {'emoji': '🖼️', 'type': 'emoji'},
                }
            },{
                # toc block
                "object": "block",
                "type": "callout",
                "callout": {
                    'color': 'purple_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'default',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "語源"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": section_dict.get("Word Origin", "Word Origin section not found.")
                                 }
                            }]
                        }
                    }],
                'icon': {'emoji': '💡', 'type': 'emoji'},
                }
            },{
                # toc block
                "object": "block",
                "type": "callout",
                "callout": {
                    'color': 'purple_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'default',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "コロケーション"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": section_dict.get("Collocation", "Collocation section not found.")
                                 }
                            }]
                        }
                    }],
                'icon': {'emoji': '📢', 'type': 'emoji'},
                }
            },{
                # toc block
                "object": "block",
                "type": "callout",
                "callout": {
                    'color': 'purple_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'default',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "自由記述"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": section_dict.get("Other important points", "Other important points section not found.")
                                 }
                            }]
                        }
                    }],
                'icon': {'emoji': '✏️', 'type': 'emoji'},
                }
            },{
                # toc block
                "object": "block",
                "type": "callout",
                "callout": {
                    'color': 'blue_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'blue',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "例文(English)"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": section_dict.get("Example sentence in English", "Example sentences section not found.")
                                 }
                            }]
                        }
                    }],
                'icon': {'emoji': '📎', 'type': 'emoji'}
                }
            },{
                # toc block
                "object": "block",
                "type": "callout",
                "callout": {
                    'color': 'blue_background',
                    "rich_text": [{
                        'annotations': {'bold': True,
                                            'code': False,
                                            'color': 'blue',
                                            'italic': False,
                                            'strikethrough': False,
                                            'underline': False},
                        "type": "text",
                        "text": {
                            "content": "例文(日本語)"
                        }
                    }],
                    "children":[{
                        "type" : "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": section_dict.get("Example sentence in Japanese", "Example sentences section not found.")
                                 }
                            }]
                        }
                    }],
                'icon': {'emoji': '📎', 'type': 'emoji'}
                }
            },]
        }
    )

    print("notion database create completed")
    print(response) # 追加した内容を表示する


# テキストを処理し、Notionに送信するエンドポイント
@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    user_text = data.get("text")

    print(f"user_text is {user_text}")

    # テキストをセクションに分割
    section_dict = extract_sections_from_text(user_text)

    # Notionに追加
    response = add_row_to_notion_database(section_dict)

    return jsonify({"message": "Data added to Notion", "response": response})

# HTMLフォームのページをレンダリングするエンドポイント
@app.route('/')
def form():
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

# try:
#     while True:
#         # ユーザーにテキストの入力を求める
#         print("Please enter the text (type 'END' on a new line to finish):")
#         user_text = []
#         while True:
#             line = input()
#             if line == "END":
#                 break
#             user_text.append(line)
#         user_text = "\n".join(user_text)

#         print("User input text:")
#         print(user_text)

#         # 入力されたテキストを処理
#         section_dict = extract_sections_from_text(user_text)

#         print("Extracted sections:")
#         print(section_dict)

#         # テキストを新規ページとして追加
#         add_row_to_notion_database(database_id, section_dict)
#         print("辞書登録スクリプト...中止したい場合はCTRL+C\n")
# except KeyboardInterrupt:
#     print("辞書登録スクリプトを終了しました")
