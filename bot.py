from aiogram import Dispatcher, Bot, executor, types
import json
import pathlib
from rule34 import Rule34Paheal
import requests


TOKEN = json.loads((pathlib.Path(__file__).parent.absolute() / "tokens.json").read_text(encoding="utf-8"))['TELEGRAM_BOT_TOKEN']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def argsparser(message):
	args = {}
	query = []
	for x in message:
		if "=" in x:
			arg = x.split("=")
			args[arg[0]] = arg[1]
		else:
			query.append(x)
	return {
		"query": " ".join(query),
		"args": args
	}

@dp.message_handler(commands=["hentai"])
async def hentai(message: types.Message):
	r34 = Rule34Paheal()
	query = "".join(message.text.split(" ")[1:][0])
	query_args = argsparser(message.text.split(" ")[1:])
	query = query_args['query']
	args = query_args['args']
	sending = False
	if not args:
		args = {
		"pages": "1",
		"per_page": "1"
		}
	k = r34.get_content(query, **args)
	for result in k:
		for x in result:
			sending = True
			try:
				await bot.send_photo(message['chat']['id'], x['url'], x['tags'])
			except:
				...
	await message.reply("OK!" if sending else "Não encontrado!")

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
