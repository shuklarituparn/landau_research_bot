import redis
from telegram.ext import ContextTypes
from telegram import Update

"""Я использую redis здесь - в качестве хранилища значений ключей"""
r = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)


def add_data_to_database(update: Update, context=ContextTypes.DEFAULT_TYPE):
    """Добавляем пользовательских данных в базу данных

    Redis поддерживает только хранение значений ключей и использует хэши. В нашем случае у пользователя может
    быть аналогичная задача, например, получение молока, и получение молока (со вкусом шоколада), поэтому, чтобы
    избежать коллизии, я сохраняю каждую задачу с уникальным серийным номером, который генерируется с помощью
    telegram ID и индекса

    """
    print(update.effective_user.first_name)
    user_id = f"user:{update.effective_user.id}"
    index = r.incr(f"{user_id}:Task")
    r.set(f"{user_id}:{index}", update.message.text)


async def show_all_the_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Функция, которая получает все задачи для данного пользователя из базы данных

    :param update: Update от стороны Телеграмма
    :param context: Context (кто отправляет сообшение)
    :return: Ничего  (просто отправлет сообщение включая задачи ползователя)
    """
    user_id = f"user:{update.effective_user.id}"
    index_key = f"{user_id}:Task"
    maximum_index = int(r.get(index_key) or 0)
    task_list = []  # list to store the user tasks
    for i in range(1, maximum_index + 1):
        task = r.get(f"{user_id}:{i}")
        if task:
            task_list.append(task)

    if task_list:
        tasks_text = "\n".join(task_list)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.effective_user.first_name} вот твои задачи:\n{tasks_text}",
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"{update.effective_user.first_name}, у тебя пока не задачи.",
        )


async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция, которая удаляет данная задача для данного пользователя из базы данных"""

    key = int(update.message.text)
    user_id = f"user:{update.effective_user.id}"
    index_key = f"{user_id}:{key}"
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Убираем {r.get(index_key)} из списка"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=f"Поздравляю тебе при заполнении задачи"
    )
    r.delete(index_key)


async def delete_all_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция, которая удаляет все задачи для данного пользователя из базы данных"""
    user_id = f"user:{update.effective_user.id}"
    task_keys = r.keys(f"{user_id}:*")

    if task_keys:
        deleted_count = await r.delete(*task_keys)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Deleted all {deleted_count} tasks."
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="No tasks found to delete."
        )


def close_the_connection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Уходя мы закрываем соединение с базой данных"""
    r.close()
