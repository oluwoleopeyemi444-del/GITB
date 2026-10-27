
import os
import logging
import feedparser

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("BOT_TOKEN")

# Public football news RSS feed
NEWS_FEED = "https://feeds.bbci.co.uk/sport/football/rss.xml"

MAIN_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📰 Latest News", callback_data="news"),
        InlineKeyboardButton("⚽ Scores", callback_data="scores"),
    ],
    [
        InlineKeyboardButton("📅 Fixtures", callback_data="fixtures"),
        InlineKeyboardButton("🏆 Leagues", callback_data="leagues"),
    ],
    [
        InlineKeyboardButton("ℹ️ Help", callback_data="help"),
    ],
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Welcome to Football News Hub!\n\n"
        "Get football headlines, match information, "
        "fixtures and league links.\n\n"
        "Choose an option below:",
        reply_markup=MAIN_MENU,
    )


async def show_news(query):
    feed = feedparser.parse(NEWS_FEED)

    if not feed.entries:
        await query.message.reply_text(
            "Sorry, football news is temporarily unavailable. "
            "Please try again later.",
            reply_markup=MAIN_MENU,
        )
        return

    lines = ["📰 LATEST FOOTBALL NEWS\n"]

    for item in feed.entries[:7]:
        title = item.get("title", "Football update")
        link = item.get("link", "")

        if link.startswith("https://") or link.startswith("http://"):
            lines.append(f"• {title}\n{link}\n")
        else:
            lines.append(f"• {title}\n")

    await query.message.reply_text(
        "\n".join(lines),
        reply_markup=MAIN_MENU,
        disable_web_page_preview=True,
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "news":
        await show_news(query)

    elif query.data == "scores":
        await query.message.reply_text(
            "⚽ Check football scores here:\n"
            "https://www.bbc.com/sport/football/scores-fixtures",
            reply_markup=MAIN_MENU,
        )

    elif query.data == "fixtures":
        await query.message.reply_text(
            "📅 View upcoming football fixtures:\n"
            "https://www.bbc.com/sport/football/scores-fixtures",
            reply_markup=MAIN_MENU,
        )

    elif query.data == "leagues":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "Premier League",
                url="https://www.premierleague.com/"
            )],
            [InlineKeyboardButton(
                "Champions League",
                url="https://www.uefa.com/uefachampionsleague/"
            )],
            [InlineKeyboardButton(
                "La Liga",
                url="https://www.laliga.com/"
            )],
            [InlineKeyboardButton(
                "Serie A",
                url="https://www.legaseriea.it/"
            )],
            [InlineKeyboardButton(
                "Bundesliga",
                url="https://www.bundesliga.com/"
            )],
            [InlineKeyboardButton(
                "⬅️ Main Menu",
                callback_data="home"
            )],
        ])

        await query.message.reply_text(
            "🏆 Choose a football league:",
            reply_markup=keyboard,
        )

    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ HOW TO USE THE BOT\n\n"
            "/start - Open the main menu\n"
            "/news - Get football headlines\n"
            "/help - Show help\n\n"
            "Select a button to explore football updates.",
            reply_markup=MAIN_MENU,
        )

    elif query.data == "home":
        await query.message.reply_text(
            "⚽ Choose an option:",
            reply_markup=MAIN_MENU,
        )


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Reuse the news function without requiring a button click.
    feed = feedparser.parse(NEWS_FEED)

    if not feed.entries:
        await update.message.reply_text(
            "News is temporarily unavailable. Please try again later."
        )
        return

    lines = ["📰 LATEST FOOTBALL NEWS\n"]
    for item in feed.entries[:7]:
        title = item.get("title", "Football update")
        link = item.get("link", "")
        lines.append(f"• {title}\n{link}\n")

    await update.message.reply_text(
        "\n".join(lines),
        disable_web_page_preview=True,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Football News Hub\n\n"
        "/start - Open the menu\n"
        "/news - Latest football headlines\n"
        "/help - Help and commands"
    )


def main():
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is missing. Add it in Railway Variables."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("news", news_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Football News Hub is running.")
    app.run_polling()


if __name__ == "__main__":
    main()
