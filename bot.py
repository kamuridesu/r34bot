import json
import os

from aiogram import (
    Dispatcher,
    Bot,
    executor,
    types,
)
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

try:
    from src import Rule34Paheal
    from src import Logger, load
    from src import Luscious
except:
    from .src import Rule34Paheal
    from .src import Logger, load
    from .src import Luscious

logger = Logger("bot.log")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


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
    if query == "":
        return await message.reply("Preciso de ao menos uma tag!")
    args = query_args['args']
    logger.info("Searching for " + query)
    sending = False
    if "per_page" not in args:
        args.update({"per_page": 1})
    if "pages" not in args:
        args.update({"pages": 1})
    args.update({"random": False})
    if args['random'] is not False:
        await message.reply("Ignoring other parameters and sending one random image")
        args['pages'] = 1
        args['per_page'] = 1
        args['random'] = True
    k = r34.get_content(query, **args)
    for result in k:
        print(result)
        for x in result:
            sending = True
            try:
                await bot.send_photo(message['chat']['id'], x['url'], x['tags'])
            except Exception:
                logger.error("Erro ao baixar conteúdo da url " + x['url'])
    await message.reply("OK!" if sending else "Não encontrado!")


@dp.message_handler(commands=['luscious'])
async def luscious(message: types.Message):
    query_args = argsparser(message.text.split(" ")[1:])
    print(query_args)
    chat_id = message['chat']['id']
    query = query_args['query']
    args = query_args['args']
    logger.info("Searching for " + query)
    sending = False
    if "sorting" not in args:
        args.update({"sorting": "date_trending"})
    if "page" not in args:
        args.update({"page": 1})
    if "max_pages" not in args:
        args.update({"max_pages": 1})
    l = Luscious(query, args['sorting'], args['page'], args['max_pages'])
    result = None
    print(args)
    if '--random' in query:
        result = l.get_random()
        await bot.send_message(chat_id, f"Resultados: {result['title']}, Total: {result['total']}")
        for image in result['images']:
            try:
                await bot.send_photo(chat_id, image, result['title'])
                sending = True
            except Exception:
                logger.error("Erro ao baixar conteúdo da url " + image)
        await message.reply("OK!" if sending else "Não encontrado!")
    else:
        msg = await bot.send_message(chat_id, "Aguarde...")
        results = l.get_n_albuns()
        kboard = InlineKeyboardMarkup(resize_keyboard=True)
        [kboard.add(InlineKeyboardButton(x.title,
                                         callback_data="{\"code\":0, \"id\": "
                                         + f"\"{x.id_}\"" + "}"))
         for x in results[1]
        ]
        print(msg)
        # await bot.edit_message_caption(chat_id, results[0], reply_markup=kboard)
        # await bot.edit_message_reply_markup(reply_markup=kboard)
        await bot.send_message(chat_id, results[0], reply_markup=kboard)


async def sendSelected(chat_id, id_):
    l = Luscious()
    album = l.fetch_from_id(id_)
    logger.info("Sending " + album.title)
    for image in album.pictures:
        try:
            await bot.send_photo(chat_id, image, album.title)
        except Exception:
            await bot.send_message(chat_id, "Erro ao enviar imagem!")


@dp.callback_query_handler(lambda call: call)
async def cb(query: types.CallbackQuery):
    data = json.loads(query.data)
    chat_id = query['message']['chat']['id']
    if data['code'] == 0:
        return await sendSelected(chat_id, data['id'])


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
