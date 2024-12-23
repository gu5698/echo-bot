from flask import Flask, request, abort, send_file
import os

from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    RichMenuSize,
    RichMenuRequest,
    RichMenuArea,
    RichMenuBounds,
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    MessageAction,
    DatetimePickerAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    ImagemapArea,
    ImagemapBaseSize,
    ImagemapExternalLink,
    ImagemapMessage,
    ImagemapVideo,
    URIImagemapAction,
    MessageImagemapAction,
    FlexMessage,
    FlexBubble,
    FlexImage,
    FlexBox,
    FlexText,
    FlexIcon,
    FlexButton,
    FlexSeparator,
    FlexContainer,
    ConfirmTemplate,
    ButtonsTemplate,
    CarouselTemplate,
    CarouselColumn,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    URIAction,
    Emoji,
    VideoMessage,
    AudioMessage,
    LocationMessage,
    StickerMessage,
    ImageMessage,
    PushMessageRequest,
    BroadcastRequest,
    MulticastRequest,
    TemplateMessage,
)
from linebot.v3.webhooks import (
    MessageEvent,
    FollowEvent,
    PostbackEvent,
    TextMessageContent,
)
import requests
import json

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


def create_rich_menu_1():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        areas = [
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
                action=MessageAction(text="A"),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=834, y=0, width=833, height=843),
                action=MessageAction(text="B"),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1663, y=0, width=834, height=843),
                action=MessageAction(text="C"),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=843, width=833, height=843),
                action=MessageAction(text="D"),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=834, y=843, width=833, height=843),
                action=MessageAction(text="E"),
            ),
            RichMenuArea(
                bounds=RichMenuBounds(x=1662, y=843, width=834, height=843),
                action=MessageAction(text="F"),
            ),
        ]

        rich_menu_to_create = RichMenuRequest(
            size=RichMenuSize(
                width=2500,
                height=1686,
            ),
            selected=True,
            name="圖文選單1",
            chat_bar_text="查看更多資訊",
            areas=areas,
        )

        rich_menu_id = line_bot_api.create_rich_menu(
            rich_menu_request=rich_menu_to_create
        ).rich_menu_id

        with open("./public/richmenu-a.png", "rb") as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={"Content-Type": "image/png"},
            )

        line_bot_api.set_default_rich_menu(rich_menu_id)


def create_rich_menu_2():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        # Create rich menu
        headers = {
            "Authorization": "Bearer " + CHANNEL_ACCESS_TOKEN,
            "Content-Type": "application/json",
        }
        body = {
            "size": {"width": 2500, "height": 1686},
            "selected": True,
            "name": "圖文選單 1",
            "chatBarText": "查看更多資訊",
            "areas": [
                {
                    "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
                    "action": {"type": "message", "text": "A"},
                },
                {
                    "bounds": {"x": 834, "y": 0, "width": 833, "height": 843},
                    "action": {"type": "message", "text": "B"},
                },
                {
                    "bounds": {"x": 1663, "y": 0, "width": 834, "height": 843},
                    "action": {"type": "message", "text": "C"},
                },
                {
                    "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
                    "action": {"type": "message", "text": "D"},
                },
                {
                    "bounds": {"x": 834, "y": 843, "width": 833, "height": 843},
                    "action": {"type": "message", "text": "E"},
                },
                {
                    "bounds": {"x": 1662, "y": 843, "width": 838, "height": 843},
                    "action": {"type": "message", "text": "F"},
                },
            ],
        }

        response = requests.post(
            "https://api.line.me/v2/bot/richmenu",
            headers=headers,
            data=json.dumps(body).encode("utf-8"),
        )
        response = response.json()
        print(response)
        rich_menu_id = response["richMenuId"]

        # Upload rich menu image
        with open("static/richmenu-1.jpg", "rb") as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_id,
                body=bytearray(image.read()),
                _headers={"Content-Type": "image/jpeg"},
            )

        line_bot_api.set_default_rich_menu(rich_menu_id)


create_rich_menu_2()


# 加入好友事件
@line_handler.add(FollowEvent)
def handle_follow(event):
    print(f"Got {event.type} event")


# 訊息事件
@line_handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    text = event.message.text
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if text == "quick_reply":
            postback_icon = request.url_root + "static/postback.png"
            postback_icon = postback_icon.replace("http", "https")
            message_icon = request.url_root + "static/message.png"
            message_icon = message_icon.replace("http", "https")
            datetime_icon = request.url_root + "static/calendar.png"
            datetime_icon = datetime_icon.replace("http", "https")
            date_icon = request.url_root + "static/calendar.png"
            date_icon = date_icon.replace("http", "https")
            time_icon = request.url_root + "static/time.png"
            time_icon = time_icon.replace("http", "https")

            quickReply = QuickReply(
                items=[
                    QuickReplyItem(
                        action=PostbackAction(
                            label="Postback", data="postback", display_text="postback"
                        ),
                        image_url=postback_icon,
                    ),
                    QuickReplyItem(
                        action=MessageAction(
                            label="Message",
                            text="message",
                        ),
                        image_url=message_icon,
                    ),
                    QuickReplyItem(
                        action=DatetimePickerAction(
                            label="Date",
                            data="date",
                            mode="date",
                        ),
                        image_url=date_icon,
                    ),
                    QuickReplyItem(
                        action=DatetimePickerAction(
                            label="Time",
                            data="time",
                            mode="time",
                        ),
                        image_url=time_icon,
                    ),
                    QuickReplyItem(
                        action=DatetimePickerAction(
                            label="Datetime",
                            data="datetime",
                            mode="datetime",
                            initial="2024-01-01T00:00",
                            max="2025-01-01T00:00",
                            min="2023-01-01T00:00",
                        ),
                        image_url=datetime_icon,
                    ),
                    QuickReplyItem(
                        action=CameraAction(
                            label="Camera",
                        ),
                    ),
                    QuickReplyItem(
                        action=CameraRollAction(
                            label="Camera Roll",
                        ),
                    ),
                    QuickReplyItem(
                        action=LocationAction(
                            label="Location",
                        ),
                    ),
                ]
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="請選擇項目", quick_reply=quickReply)],
                )
            )

        if text == "imagemap":
            imagemap_base_url = request.url_root + "static/imagemap"
            imagemap_base_url = imagemap_base_url.replace("http", "https")
            video_url = request.url_root + "static/video.mp4"
            video_url = video_url.replace("http", "https")
            preview_image_url = request.url_root + "static/preview_image.png"
            preview_image_url = preview_image_url.replace("http", "https")

            imagemap_message = ImagemapMessage(
                base_url=imagemap_base_url,
                alt_text="this is an imagemap",
                base_size=ImagemapBaseSize(height=1040, width=1040),
                video=ImagemapVideo(
                    original_content_url=video_url,
                    preview_image_url=preview_image_url,
                    area=ImagemapArea(x=0, y=0, width=1040, height=520),
                    external_link=ImagemapExternalLink(
                        label="點我看更多",
                        link_uri="https://www.youtube.com/@bigdatantue",
                    ),
                ),
                actions=[
                    URIImagemapAction(
                        type="uri",
                        linkUri="https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y=",
                        area=ImagemapArea(x=0, y=520, width=520, height=520),
                    ),
                    MessageImagemapAction(
                        type="message",
                        text="這是FB網頁https://www.facebook.com/NTUEBIGDATAEDU",
                        area=ImagemapArea(x=520, y=520, width=520, height=520),
                    ),
                ],
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[imagemap_message]
                )
            )

        if text == "flex-1":
            url = request.url_root + "static/Logo.jpg"
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            bubble = FlexBubble(
                direction="ltr",
                hero=FlexImage(
                    url=url,
                    size="full",
                    aspectRatio="20:13",
                    aspectMode="cover",
                    action=URIAction(
                        uri="https://www.facebook.com/NTUEBIGDATAEDU", label="label"
                    ),
                ),
                body=FlexBox(
                    layout="vertical",
                    contents=[
                        # title
                        FlexText(text="教育大數據", weight="bold", size="x1"),
                        # review
                        FlexBox(
                            layout="baseline",
                            margin="md",
                            contents=[FlexIcon(size="sm", url="")],
                        ),
                    ],
                ),
            )
        elif text == "flex-2":
            line_flex_json = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "url": "https://picsum.photos/id/237/200/300",
                    "size": "full",
                    "aspectRatio": "4:3",
                    "aspectMode": "cover",
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "國北教大",
                            "weight": "bold",
                            "size": "xl",
                            "contents": [
                                {"type": "span", "text": "國北教大"},
                                {
                                    "type": "span",
                                    "text": "教育大數據微學程",
                                    "size": "md",
                                    "weight": "bold",
                                    "style": "italic",
                                },
                            ],
                        },
                        {
                            "type": "box",
                            "layout": "baseline",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png",
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png",
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png",
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png",
                                },
                                {
                                    "type": "icon",
                                    "size": "sm",
                                    "url": "https://developers-resource.landpress.line.me/fx/img/review_gold_star_28.png",
                                },
                                {
                                    "type": "text",
                                    "text": "5.0",
                                    "size": "sm",
                                    "color": "#999999",
                                    "margin": "md",
                                    "flex": 0,
                                },
                            ],
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "Address",
                                            "color": "#aaaaaa",
                                            "size": "sm",
                                            "flex": 3,
                                        },
                                        {
                                            "type": "text",
                                            "text": "台北市大安區和平東路二段134號",
                                            "wrap": True,
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 7,
                                        },
                                    ],
                                }
                            ],
                        },
                    ],
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Instagram",
                                "uri": "https://instagram.com/ntue.bigdata/",
                            },
                            "style": "primary",
                            "margin": "md",
                        },
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "Youtube",
                                "uri": "https://www.youtube.com/@bigdatantue",
                            },
                            "style": "secondary",
                            "margin": "md",
                        },
                    ],
                },
            }
            line_flex_str = json.dumps(line_flex_json)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        FlexMessage(
                            alt_text="詳細說明",
                            contents=FlexContainer.from_json(line_flex_str),
                        )
                    ],
                )
            )

        # Confirm Template
        if text == "Confirm":
            confirm_template = ConfirmTemplate(
                text="今天學程式了嗎？",
                actions=[
                    MessageAction(label="是", text="是！"),
                    MessageAction(label="否", text="否！"),
                ],
            )
            template_message = TemplateMessage(
                alt_text="Confirm alt text", template=confirm_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[template_message]
                )
            )

        # Buttons Template
        elif text == "Buttons":
            url = request.url_root + "static/Logo.jpg"
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            buttons_template = ButtonsTemplate(
                thumbnail_image_url=url,
                title="示範",
                text="詳細說明",
                actions=[
                    URIAction(
                        label="連結", uri="https://www.facebook.com/NTUEBIGDATAEDU"
                    ),
                    PostbackAction(label="連結", data="ping", displayText="傳了"),
                    MessageAction(label='傳"哈囉"', text="哈囉"),
                    DatetimePickerAction(
                        label="選擇時間", data="時間", mode="datetime"
                    ),
                ],
            )
            template_message = TemplateMessage(
                alt_text="This is a buttons template", template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[template_message]
                )
            )
        # Carousel Template
        elif text == "Carousel":
            url = request.url_root + "static/Logo.jpg"
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            carousel_template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=url,
                        title="第一項",
                        text="這是第一項的描述",
                        actions=[
                            URIAction(
                                label="按我前往 Google", uri="https://www.google.com"
                            )
                        ],
                    ),
                    CarouselColumn(
                        thumbnail_image_url=url,
                        title="第二項",
                        text="這是第二項的描述",
                        actions=[
                            URIAction(
                                label="按我前往 Yahoo", uri="https://www.yahoo.com"
                            )
                        ],
                    ),
                ]
            )
            carousel_message = TemplateMessage(
                alt_text="這是 Carousel Template", template=carousel_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[carousel_message],
                )
            )
        # ImageCarousel Template
        elif text == "ImageCarousel":
            url = request.url_root + "static"
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            image_carousel_template = ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url=url + "/facebook.png",
                        action=URIAction(
                            label="造訪FB",
                            uri="https://www.facebook.com/NTUEBIGDATAEDU",
                        ),
                    ),
                    ImageCarouselColumn(
                        image_url=url + "/instagram.png",
                        action=URIAction(
                            label="造訪IG",
                            uri="https://instagram.com/ntue.bigdata?igshid=YmMyMTA2M2Y=",
                        ),
                    ),
                    ImageCarouselColumn(
                        image_url=url + "/youtube.png",
                        action=URIAction(
                            label="造訪YT",
                            uri="https://www.youtube.com/@bigdatantue",
                        ),
                    ),
                ]
            )
            image_carousel_message = TemplateMessage(
                alt_text="圖片輪播範本", template=image_carousel_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[image_carousel_message],
                )
            )

        if text == "文字":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="這是文字訊息")],
                )
            )
        elif text == "表情符號":
            emojis = [
                Emoji(index=0, productId="5ac1bfd5040ab15980c9b435", emojiId="001"),
                Emoji(index=12, productId="5ac1bfd5040ab15980c9b435", emojiId="002"),
            ]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="$ LINE 表情符號 $", emojis=emojis)],
                )
            )
        elif text == "貼圖":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[StickerMessage(packageId="446", stickerId="1988")],
                )
            )
        elif text == "圖片":
            url = request.url_root + "static/Logo.jpg"
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        ImageMessage(originalContentUrl=url, previewImageUrl=url)
                    ],
                )
            )
        elif text == "影片":
            url = request.url_root + "static/video.mp4"
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        VideoMessage(originalContentUrl=url, previewImageUrl=url)
                    ],
                )
            )
        elif text == "音訊":
            url = request.url_root + "static/music.mp3"
            url = url.replace("http", "https")
            app.logger.info("url=" + url)
            duration = 60000  # in milliseconds
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[AudioMessage(originalContentUrl=url, duration=duration)],
                )
            )
        elif text == "位置":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[
                        LocationMessage(
                            title="Location",
                            address="Taipei",
                            latitude=25.0475,
                            longitude=121.5173,
                        )
                    ],
                )
            )
        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=event.message.text)],
                )
            )

        # Reply message

        # line_bot_api.reply_message(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[
        #             TextMessage(
        #                 text="reply message",
        #             )
        #         ],
        #     )
        # )

        # result = line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text='reply message with http info')]
        #     )
        # )

        # Push Message
        # line_bot_api.push_message_with_http_info(
        #     PushMessageRequest(
        #         to=event.source.user_id,
        #         messages=[TextMessage(text='PUSH!')]
        #     )
        # )

        # Broadcast Message
        # line_bot_api.broadcast_with_http_info(
        #     BroadcastRequest(
        #         messages=[TextMessage(text='BROADCAST!')]
        #     )
        # )

        # Multicast Message
        # line_bot_api.multicast_with_http_info(
        #     MulticastRequest(
        #         to=['U71d6d2d0aeab82f7b35f08a1cc7da929'],
        #         messages=[TextMessage(text='MULTICAST!')],
        #         notificationDisabled=True
        #     )
        # )

        if event.message.text == "postback":
            buttons_template = ButtonsTemplate(
                title="Postback Sample",
                text="Postback Action",
                actions=[
                    PostbackAction(
                        label="Postback Action",
                        text="Postback Action Button Clicked!",
                        data="postback",
                    )
                ],
            )
            template_message = TemplateMessage(
                alt_text="Postback Sample", template=buttons_template
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[template_message]
                )
            )
        # line_bot_api.reply_message_with_http_info(
        #     ReplyMessageRequest(
        #         reply_token=event.reply_token,
        #         messages=[TextMessage(text=event.message.text)]
        #     )
        # )


@line_handler.add(PostbackEvent)
def handle_postback(event):
    # if event.postback.data == "postback":
    #     print("Postback event is triggered")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        postback_data = event.postback.data
        if postback_data == "postback":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="Postback")],
                )
            )
        elif postback_data == "date":
            date = event.postback.params["date"]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text=date)]
                )
            )
        elif postback_data == "time":
            time = event.postback.params["time"]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text=time)]
                )
            )
        elif postback_data == "datetime":
            datetime = event.postback.params["datetime"]
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token, messages=[TextMessage(text=datetime)]
                )
            )


@app.route("/static/imagemap/<size>")
def serve_imagemap(size):
    try:
        # LINE 會請求 1040，我們需要加上 .png
        image_path = os.path.join("static", "imagemap", f"{size}.png")
        if not os.path.exists(image_path):
            abort(404)
        return send_file(image_path, mimetype="image/png")
    except Exception as e:
        print(f"Error serving image: {e}")
        abort(404)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
