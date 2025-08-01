import telebot
from telebot import types
from config import BOT_TOKEN
from storage.database import get_unsent_news, get_mailings_users, update_sent_news, add_user, update_subscribe_user

# Инициализация бота с токеном
bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def cmd_start(message):
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
    bot.send_message(message.chat.id, WELCOME_MESSAGE, parse_mode="Markdown")
    add_user(message.from_user.id, message.from_user.username)


@bot.message_handler(commands=['subscribe'])
def cmd_subscribe(message):
    update_subscribe_user(message.from_user.id, True)
    bot.send_message(message.chat.id, "🔔 Вы успешно подписались на рассылку новостей!")


@bot.message_handler(commands=['unsubscribe'])
def cmd_unsubscribe(message):
    update_subscribe_user(message.from_user.id, False)
    bot.send_message(message.chat.id, "🔕 Вы успешно отписались от рассылок новостей!")


def check_and_notify():
    unsent_news = get_unsent_news()
    mailings_users = get_mailings_users()

    if not unsent_news or not mailings_users:
        return

    for news_id, title, link, date_published in unsent_news:
        text = f"*📰 {title}*\n📅 {date_published}\n🔗 [Читать новость]({link})"
        
        for user_id, username, mailings in mailings_users:
            try:
                bot.send_message(user_id, text, parse_mode="Markdown")
            except Exception as e:
                print(f"Ошибка при отправке пользователю {user_id}: {e}")

        # После рассылки помечаем новость как отправленную
        update_sent_news(news_id)


