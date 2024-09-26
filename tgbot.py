from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import re as re
import sqlalchemy as db

data = {"10" : "Привет пользователь!)"}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Привет)){update.effective_user.first_name}. \nКоманды:\n /get - получить сообщение по коду\n /add - добавить сообщение\n /getf - просмотр фио преподавателей')

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = re.findall(r'\".*?\"', update.message.text)
    if len(raw) != 1:
        await update.message.reply_text("Капец капец")
        return
    code = raw[0].replace('""', "")
    await update.message.reply_text(data[code])

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = re.findall(r'\".*?\"', update.message.text)
    if len(raw) != 2:
        await update.message.reply_text("Капец капец")
        return
    code = re.findall(r'\".*?\"', update.message.text)[0].replace('""', "")
    message = re.findall(r'\".*?\"', update.message.text)[1].replace('""', "")
    data[code] = message
    await update.message.reply_text("Ура ура")

async def get_fio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    raw = update.message.text.split(" ")
    if len(raw) != 2 :
        await update.message.reply_text("Проблема((")
        return
    id = int(raw[1])
    engine = db.create_engine("mysql+pymysql://root@127.0.0.1/gg?charset=utf8mb4")
    conn = engine.connect()
    query = db.text(f"SELECT * FROM hh WHERE id = {id}")
    MuSQL = conn.execute(query).fetchall()
    await update.message.reply_text(str(MuSQL[0][0])+"\n" + str(MuSQL[0][1]))

app = ApplicationBuilder().token("7517972982:AAF4PuaF2fCoC2klstFV0rSuYvmRZJ6ku4U").build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("get",get))
app.add_handler(CommandHandler("add",add))
app.add_handler(CommandHandler("getf",get_fio))


app.run_polling()