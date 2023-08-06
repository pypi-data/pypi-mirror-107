#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2021 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

import os

try:
	import ujson as json
except ImportError:
	import json

import time

from tgsdk import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	ReplyKeyboardRemove,
	KeyboardButton,
	ReplyKeyboardMarkup,
	ParseMode,
	PhotoSize,
	MessageEntity,
	Message,
	Chat,
	Bot,
	User
)
from tgsdk.utils.constants import MAX_CAPTION_LENGTH, MAX_MESSAGE_LENGTH
from tgsdk.network.request import Request
from .constants import TestValues


def test__bot__init():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	assert _.token == TestValues.BOT_API_TOKEN
	assert _.base_url == "https://api.telegram.org/bot%s" % TestValues.BOT_API_TOKEN
	assert _.base_file_url == "https://api.telegram.org/file/bot%s" % TestValues.BOT_API_TOKEN

	assert isinstance(_.request, Request)

	assert _._me is None

	assert _.to_dict() == {
		"id": TestValues.BOT_ID,
		"username": TestValues.BOT_USERNAME,
		"first_name": TestValues.BOT_FIRST_NAME
	}
	assert _.me is not None
	assert isinstance(_.me, User)
	assert _.me.id == TestValues.BOT_ID
	assert _.me.username == TestValues.BOT_USERNAME
	assert _.me.first_name == TestValues.BOT_FIRST_NAME

	assert json.loads(_.to_json()) == {
		"id": TestValues.BOT_ID,
		"username": TestValues.BOT_USERNAME,
		"first_name": TestValues.BOT_FIRST_NAME
	}


def test__bot__init__with_urls():
	_ = Bot(
		token=TestValues.BOT_API_TOKEN,
		base_url="https://api.telegram.org/bot",
		base_file_url="https://api.telegram.org/file/bot"
	)

	assert _.token == TestValues.BOT_API_TOKEN
	assert _.base_url == "https://api.telegram.org/bot%s" % TestValues.BOT_API_TOKEN
	assert _.base_file_url == "https://api.telegram.org/file/bot%s" % TestValues.BOT_API_TOKEN
	assert _._me is None

	assert isinstance(_.request, Request)

	assert _._me is None

	assert _.to_dict() == {
		"id": TestValues.BOT_ID,
		"username": TestValues.BOT_USERNAME,
		"first_name": TestValues.BOT_FIRST_NAME
	}
	assert _.me is not None
	assert isinstance(_.me, User)
	assert _.me.id == TestValues.BOT_ID
	assert _.me.username == TestValues.BOT_USERNAME
	assert _.me.first_name == TestValues.BOT_FIRST_NAME

	assert json.loads(_.to_json()) == {
		"id": TestValues.BOT_ID,
		"username": TestValues.BOT_USERNAME,
		"first_name": TestValues.BOT_FIRST_NAME
	}


def test__bot__init__get_me():
	_ = Bot(
		token=TestValues.BOT_API_TOKEN,
		base_url="https://api.telegram.org/bot",
		base_file_url="https://api.telegram.org/file/bot"
	)

	assert _.token == TestValues.BOT_API_TOKEN
	assert _.base_url == "https://api.telegram.org/bot%s" % TestValues.BOT_API_TOKEN
	assert _.base_file_url == "https://api.telegram.org/file/bot%s" % TestValues.BOT_API_TOKEN
	assert _._me is None

	assert isinstance(_.request, Request)

	assert _.me.id == TestValues.BOT_ID
	assert _.me.first_name == TestValues.BOT_FIRST_NAME
	assert _.me.username == TestValues.BOT_USERNAME
	assert isinstance(_._me, User)

	assert _.link == "https://t.me/%s" % TestValues.BOT_USERNAME
	assert _.tg_link == "tg://resolve?domain=%s" % TestValues.BOT_USERNAME

	assert _.to_dict() == {
		"id": TestValues.BOT_ID,
		"username": TestValues.BOT_USERNAME,
		"first_name": TestValues.BOT_FIRST_NAME
	}
	assert json.loads(_.to_json()) == {
		"id": TestValues.BOT_ID,
		"username": TestValues.BOT_USERNAME,
		"first_name": TestValues.BOT_FIRST_NAME
	}

def test__bot__get_me():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	result = _.get_me()

	assert result.is_bot is True
	assert result.id == TestValues.BOT_ID
	assert result.first_name == TestValues.BOT_FIRST_NAME
	assert result.username == TestValues.BOT_USERNAME


def test__bot__build_chat_id__int_above_zero():
	chat_id = Bot.build_chat_id(chat_id=123)

	assert chat_id == -123


def test__bot__build_chat_id__int_below_zero():
	chat_id = Bot.build_chat_id(chat_id=-123)

	assert chat_id == -123


def test__bot__build_chat_id__username_without_at():
	chat_id = Bot.build_chat_id(chat_id="username")

	assert chat_id == "@username"


def test__bot__build_chat_id__username_with_at():
	chat_id = Bot.build_chat_id(chat_id="@username")

	assert chat_id == "@username"


def test__bot__webhook():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	result = _.set_webhook(
		url="https://telegram.org",
		max_connections=100
	)
	assert result is True

	result = _.get_webhook_info()
	assert result.url == "https://telegram.org"
	assert result.max_connections == 100
	assert result.allowed_updates == ["message", "callback_query"]
	assert result.has_custom_certificate is False
	assert result.pending_update_count == 0
	assert result.ip_address is not None
	assert result.ip_address == "149.154.167.99"  # TODO:
	assert result.last_error_date is None
	assert result.last_error_message is None

	result = _.delete_webhook()
	assert result is True

	result = _.get_webhook_info()
	assert result.url == ""
	assert result.max_connections is None
	assert result.allowed_updates == ["message", "callback_query"]
	assert result.has_custom_certificate is False
	assert result.pending_update_count == 0
	assert result.ip_address is None
	assert result.last_error_date is None
	assert result.last_error_message is None

	time.sleep(2)

	result = _.set_webhook(
		url="https://telegram.org",
		allowed_updates=["message"],
		ip_address="149.154.167.99",
		drop_pending_updates=True
	)
	assert result is True

	result = _.get_webhook_info()
	assert result.url == "https://telegram.org"
	assert result.max_connections == 50
	assert result.allowed_updates == ["message"]
	assert result.has_custom_certificate is False
	assert result.pending_update_count == 0
	assert result.ip_address == "149.154.167.99"
	assert result.last_error_date is None
	assert result.last_error_message is None

	result = _.delete_webhook()
	assert result is True


def test__bot__sendMessage():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	result = _.send_message(
		chat_id=TestValues.USER_CHAT_ID,
		text="Test 1",
		disable_web_page_preview=None,
		parse_mode=ParseMode.HTML,
		reply_markup=ReplyKeyboardMarkup(
			keyboard=[
				[
					KeyboardButton(
						text="Button"
					)
				]
			],
			resize_keyboard=True
		)
	)

	assert isinstance(result, Message) is True
	assert result.chat.id == TestValues.USER_CHAT_ID
	assert result.chat.type == Chat.PRIVATE
	assert result.text == "Test 1"
	assert result.from_user.first_name == TestValues.BOT_FIRST_NAME
	assert result.from_user.username == TestValues.BOT_USERNAME
	assert result.from_user.is_bot is True
	assert result.from_user.id == TestValues.BOT_ID
	assert result.date is not None
	assert isinstance(result.date, int) is True
	assert result.message_id is not None
	assert isinstance(result.message_id, int) is True
	assert result.reply_markup is None

	# Long text. More than 4000
	text = "".join((str(i) for i in range(MAX_MESSAGE_LENGTH + 10)))
	result = _.send_message(
		chat_id=TestValues.USER_CHAT_ID,
		text=text,
		disable_web_page_preview=None,
		parse_mode=ParseMode.HTML,
		reply_markup=ReplyKeyboardMarkup(
			keyboard=[
				[
					KeyboardButton(
						text="Button"
					)
				]
			],
			resize_keyboard=True
		)
	)

	assert isinstance(result, Message) is True
	assert result.chat.id == TestValues.USER_CHAT_ID
	assert result.chat.type == Chat.PRIVATE
	assert result.text == text[:4096]
	assert result.from_user.first_name == TestValues.BOT_FIRST_NAME
	assert result.from_user.username == TestValues.BOT_USERNAME
	assert result.from_user.is_bot is True
	assert result.from_user.id == TestValues.BOT_ID
	assert result.date is not None
	assert isinstance(result.date, int) is True
	assert result.message_id is not None
	assert isinstance(result.message_id, int) is True
	assert result.reply_markup is None


	# With inline
	result = _.send_message(
		chat_id=TestValues.USER_CHAT_ID,
		text="Test 2",
		disable_web_page_preview=True,
		reply_markup=InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton(
						text="Button",
						callback_data="callback_data"
					)
				]
			]
		)
	)

	assert isinstance(result, Message) is True
	assert result.chat.id == TestValues.USER_CHAT_ID
	assert result.chat.type == Chat.PRIVATE
	assert result.text == "Test 2"
	assert result.from_user.first_name == TestValues.BOT_FIRST_NAME
	assert result.from_user.username == TestValues.BOT_USERNAME
	assert result.from_user.is_bot is True
	assert result.from_user.id == TestValues.BOT_ID
	assert result.date is not None
	assert isinstance(result.date, int) is True
	assert result.message_id is not None
	assert isinstance(result.message_id, int) is True
	assert result.reply_markup is not None
	assert isinstance(result.reply_markup, InlineKeyboardMarkup) is True
	assert isinstance(result.reply_markup.inline_keyboard[0][0], InlineKeyboardButton) is True
	assert result.reply_markup.inline_keyboard[0][0].text == "Button"
	assert result.reply_markup.inline_keyboard[0][0].callback_data == "callback_data"


def test__bot__sendPhoto():
	_ = Bot(token=TestValues.BOT_API_TOKEN)

	result = _.send_photo(
		chat_id=TestValues.USER_CHAT_ID,
		photo=open("./tests/data/img.jpeg", "rb").read(),
		file_name="img.jpeg",
		caption="<b>caption</b>",
		parse_mode=ParseMode.HTML,
		disable_notification=None
	)

	assert isinstance(result, Message) is True
	assert result.caption == "caption"
	assert result.caption_entities is not None
	assert isinstance(result.caption_entities, list)
	assert isinstance(result.caption_entities[0], MessageEntity)
	assert result.caption_entities[0].type == "bold"
	assert result.caption_entities[0].offset == 0
	assert result.caption_entities[0].length == 7
	assert isinstance(result.photo, list) is True
	assert isinstance(result.photo[0], PhotoSize) is True

	# No caption
	result = _.send_photo(
		chat_id=TestValues.USER_CHAT_ID,
		photo=open("./tests/data/img.jpeg", "rb").read(),
		file_name="img.jpeg"
	)

	assert isinstance(result, Message) is True
	assert result.caption is None
	assert result.caption_entities == []
	assert isinstance(result.photo, list) is True
	assert isinstance(result.photo[0], PhotoSize) is True

	# Caption max length
	caption = "".join(str(i) for i in range(MAX_CAPTION_LENGTH + 10))
	result = _.send_photo(
		chat_id=TestValues.USER_CHAT_ID,
		photo=open("./tests/data/img.jpeg", "rb").read(),
		file_name="img.jpeg",
		caption=caption,
		parse_mode=None,
		disable_notification=None
	)

	assert isinstance(result, Message) is True
	assert result.caption == caption[:MAX_CAPTION_LENGTH]
	assert result.caption_entities == []
	assert isinstance(result.photo, list) is True
	assert isinstance(result.photo[0], PhotoSize) is True
