from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from storage.database import get_unsent_news, update_subscribe_user, get_mailings_users, update_sent_news, add_user
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    WELCOME_MESSAGE = (
    f"👋 *Привет, {message.from_user.full_name}!* Добро пожаловать в *Новости Лермонтов* 📰\n\n"
    "📌 Здесь ты будешь получать свежие новости и важные события прямо в Telegram.\n\n"
    "⚡ *Как начать?*\n"
    "   ➡️ Чтобы подписаться на рассылку новостей — жми /subscribe\n"
    "   ➡️ Чтобы отписаться — жми /unsubscribe\n\n"
    "💡 Советы:\n"
    "   • Новости приходят *автоматически*, ничего нажимать не нужно.\n"
    "   • Можно подписаться снова в любой момент.\n"
    "   • Если хочешь предложить идею или новый источник — просто напиши в чат.\n\n"
    "🚀 *Подключайся к подписке и будь в курсе событий!*"
)
    await message.answer(WELCOME_MESSAGE, parse_mode="Markdown")
    add_user(message.from_user.id, message.from_user.username)


@dp.message(Command("subscribe"))
async def cmd_subscribe(message: Message):
    update_subscribe_user(message.from_user.id, True)
    await message.answer("🔔 Вы успешно подписались на рассылку новостей!")


@dp.message(Command("unsubscribe"))
async def cmd_unsubscribe(message: Message):
    update_subscribe_user(message.from_user.id, False)
    await message.answer("🔕 Вы успешно отписались от рассылок новостей!")


async def check_and_notify():
    unsent_news = get_unsent_news()
    mailings_users = get_mailings_users()

    if not unsent_news or not mailings_users:
        return

    for news_id, title, link, date_published in unsent_news:
        text = f"*📰 {title}*\n📅 {date_published}\n🔗 [Читать новость]({link})"
        
        for user_id, username, mailings in mailings_users:
            try:
                await bot.send_message(user_id, text, parse_mode="Markdown")
            except Exception as e:
                print(f"Ошибка при отправке пользователю {user_id}: {e}")

        # После рассылки помечаем новость как отправленную
        update_sent_news(news_id)