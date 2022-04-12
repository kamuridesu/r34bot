from aiogram import Dispatcher, Bot, executor, types
import json
import pathlib
try:
	from src import Rule34Paheal
	from src import Logger, jsonify_quotes, load
except:
	from .src import Rule34Paheal
	from .src import Logger, jsonify_quotes, load
import requests

logger = Logger("bot.log")
TOKEN = load("tokens.json")['TELEGRAM_BOT_TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
r34 = Rule34Paheal()


def argsparser(message):
	args = {}
	query = []
	for x in message:
		if "=" in x:
			arg = x.split("=")
			args[arg[0]] = arg[1]
		elif x not in [" ", ""]:
			query.append(x)
	return {
		"query": " ".join(query),
		"args": args
	}


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	await message.reply("Olá! Use /hentai (tag) [options] para baixar hentai.\nEm tag, utilize tags do rule34.paheal.net, e em options, use per_page= e pages= para definir a quantidade\nEx: /hentai porkyman pages=1 per_page=2\n\nUse /search para pesquisar por alguma tag, como:\n/search porkyman")


@dp.message_handler(commands=["hentai"])
async def hentai(message: types.Message):
	query_args = argsparser(message.text.split(" ")[1:])
	query = query_args['query']
	args = query_args['args']
	logger.info("Searching for " + query)
	sending = False
	if "per_page" not in args:
		args.update({"per_page": 1})
	if "pages" not in args:
		args.update({"pages": 1})
	k = r34.get_content(query, **args)
	for result in k:
		for x in result:
			sending = True
			try:
				await bot.send_photo(message['chat']['id'], x['url'], x['tags'])
			except:
				logger.error("Erro ao baixar conteúdo da url " + x['url'])
	await message.reply("OK!" if sending else "Não encontrado!")


@dp.message_handler(commands=['search'])
async def search(message: types.Message):
	query = "".join(message.text.split(" ")[1:][0])
	if query:
		results = r34.search(query)
		if results:
			response = "\n".join(list(results.keys()))
			return await message.reply(response)
		return await message.reply("Nada encontrado!")



if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
