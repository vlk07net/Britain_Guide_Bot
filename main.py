import logging
import os

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


# ============================================
# SETTINGS
# ============================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

# External news source (not owned by this bot) — plain link, hardcoded.
SITE_URL = "https://www.telegraph.co.uk/"
SITE_NAME = "The Telegraph"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip()
BRAND = "Britain Guide"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# ============================================
# HELPERS
# ============================================
def btn(text, data):
    return types.InlineKeyboardButton(text=text, callback_data=data)


def site_btn():
    # Plain external link to a third-party news site (opens in Telegram's browser).
    return types.InlineKeyboardButton(
        text=f"📰 Read the news on {SITE_NAME}",
        url=SITE_URL,
    )


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [button for button in row if button is not None]
        if row:
            markup.row(*row)
    return markup


BTN_HEADLINES = ("📋 Today's reads", "headlines")
BTN_MENU = ("🗂 Contents", "menu")


def article_rows():
    return [
        [site_btn()],
        [btn(*BTN_HEADLINES), btn(*BTN_MENU)],
    ]


# ============================================
# SCREEN TEXTS
# ============================================
TEXT_START = (
    f"🇬🇧 <b>Welcome to {BRAND}!</b>\n\n"
    "<i>A small seasonal guide to culture, food and travel in Britain.</i>\n\n"
    "Each season, a short selection of reads to enjoy right here in the chat.\n\n"
    "To begin, tap <b>Today's reads</b>."
)

TEXT_HEADLINES = (
    "📋 <b>Today's reads</b>\n\n"
    "Three reads picked for today, each available in full in the chat.\n\n"
    "<b>Culture</b> — five museums to see this autumn.\n\n"
    "<b>Food</b> — five classic British dishes.\n\n"
    "<b>Travel</b> — five places for a weekend away.\n\n"
    "Tap a title to open the article."
)

TEXT_CULTURE = (
    "🎨 <b>Five museums to see this autumn</b>\n\n"
    "<b>London — The British Museum</b>\n"
    "Two million years of history, from the Rosetta Stone to the "
    "Parthenon sculptures. Free to enter.\n\n"
    "<b>London — The National Gallery</b>\n"
    "Western European painting from the 13th to the 19th century, on "
    "Trafalgar Square. Van Gogh, Turner and Van Eyck.\n\n"
    "<b>London — Tate Modern</b>\n"
    "Modern and contemporary art in a former power station on the "
    "Thames. The Turbine Hall alone is worth the trip.\n\n"
    "<b>London — Victoria and Albert Museum</b>\n"
    "The world's leading museum of art, design and performance — "
    "fashion, ceramics and much more.\n\n"
    "<b>Edinburgh — National Museum of Scotland</b>\n"
    "From Scottish history to science and world cultures, under one "
    "grand roof.\n\n"
    "<i>Dates and opening hours: please check the museums' official sites.</i>"
)

TEXT_CUISINE = (
    "🍽 <b>Five classic British dishes</b>\n\n"
    "<b>Fish and chips</b>\n"
    "Battered fish with thick-cut chips, best from the seaside. Salt, "
    "vinegar and mushy peas on the side.\n\n"
    "<b>Sunday roast</b>\n"
    "Roast meat, potatoes, vegetables, Yorkshire pudding and gravy — "
    "the great weekend ritual.\n\n"
    "<b>Full English breakfast</b>\n"
    "Eggs, bacon, sausage, beans, tomato, mushrooms and toast. A meal "
    "that sets you up for the day.\n\n"
    "<b>Shepherd's pie</b>\n"
    "Minced lamb under a golden mash crust — proper comfort food for "
    "autumn.\n\n"
    "<b>Afternoon tea</b>\n"
    "Scones with clotted cream and jam, finger sandwiches and cakes, "
    "with a pot of tea.\n\n"
    "<i>Amounts and cooking times can be adjusted to taste.</i>"
)

TEXT_TRAVEL = (
    "🏡 <b>Five places for a weekend away</b>\n\n"
    "<b>The Cotswolds</b>\n"
    "Honey-coloured stone villages, rolling hills and country pubs. "
    "The picture-book English countryside.\n\n"
    "<b>Bath</b>\n"
    "Roman baths, Georgian crescents and honey-toned architecture. A "
    "UNESCO World Heritage city.\n\n"
    "<b>Edinburgh</b>\n"
    "A castle on a crag, the Royal Mile and the New Town. Dramatic in "
    "any season, magic in autumn.\n\n"
    "<b>The Lake District</b>\n"
    "Mountains, lakes and the landscapes that inspired Wordsworth. "
    "Walking country at its finest.\n\n"
    "<b>St Ives (Cornwall)</b>\n"
    "A harbour town of light and art, with the Tate St Ives and some "
    "of the country's best beaches.\n\n"
    "<i>For lodging, midweek booking is recommended.</i>"
)

TEXT_MENU = (
    "🗂 <b>Contents</b>\n\n"
    "From this menu you can:\n\n"
    "• Read <b>today's reads</b> and the articles, right here.\n"
    "• Browse the sections: Culture, Food, Travel.\n"
    "• Check the glossary and frequently asked questions.\n"
    "• Learn more about the project and get in touch."
)

TEXT_GLOSSARY = (
    "📖 <b>Little glossary</b>\n\n"
    "<b>High street</b> — the main shopping street of a town.\n\n"
    "<b>Pub</b> — the public house; the heart of British social life.\n\n"
    "<b>Bank holiday</b> — a public holiday, often a long weekend.\n\n"
    "<b>The Tube</b> — the London Underground.\n\n"
    "<b>Cream tea</b> — scones with clotted cream and jam, plus tea.\n\n"
    "<b>Listed building</b> — a building protected for its historic or "
    "architectural interest."
)

TEXT_FAQ = (
    "❓ <b>Frequently asked questions</b>\n\n"
    "<b>Is this bot official?</b>\n"
    f"No. It's an independent guide, not affiliated with {SITE_NAME} or "
    "any publication. The news button simply links to their public site. "
    "It never asks for passwords, codes or card details.\n\n"
    "<b>How often is it updated?</b>\n"
    "The selection of reads is refreshed each season.\n\n"
    "<b>How do I mute notifications?</b>\n"
    "From the Telegram chat settings you can mute or disable "
    "notifications.\n\n"
    "<b>Can I share an article?</b>\n"
    "Yes. Use Telegram's forward function."
)

TEXT_ABOUT = (
    f"ℹ️ <b>About {BRAND}</b>\n\n"
    f"{BRAND} gathers, each season, a few reads about Britain: "
    "museums, traditional food and beautiful places to visit.\n\n"
    "The idea is simple: short, pleasant texts to read right in "
    "Telegram, without ads and without rushing.\n\n"
    f"For the latest news, the button links to {SITE_NAME} "
    "(telegraph.co.uk), an independent news site."
)


def contact_text():
    email_line = (
        f"• E-mail: {CONTACT_EMAIL}\n\n"
        if CONTACT_EMAIL
        else "• A contact address will be added soon.\n\n"
    )
    return (
        "✏️ <b>Contact</b>\n\n"
        "For suggestions, corrections or article ideas:\n"
        + email_line
        + "Thank you for every message!"
    )


# ============================================
# SCREENS: callback_data -> (text, buttons)
# ============================================
SCREENS = {
    "headlines": (
        TEXT_HEADLINES,
        [
            [btn("🎨 Culture — autumn museums", "culture")],
            [btn("🍽 Food — classic dishes", "cuisine")],
            [btn("🏡 Travel — five places", "travel")],
            [btn(*BTN_MENU)],
        ],
    ),
    "culture": (TEXT_CULTURE, article_rows()),
    "cuisine": (TEXT_CUISINE, article_rows()),
    "travel": (TEXT_TRAVEL, article_rows()),
    "menu": (
        TEXT_MENU,
        [
            [site_btn()],
            [btn(*BTN_HEADLINES)],
            [btn("📖 Glossary", "glossary"), btn("❓ FAQ", "faq")],
            [btn("✏️ Contact", "contact"), btn("ℹ️ About", "about")],
        ],
    ),
    "glossary": (TEXT_GLOSSARY, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "faq": (TEXT_FAQ, [[btn(*BTN_HEADLINES)], [btn(*BTN_MENU)]]),
    "contact": (
        contact_text(),
        [[btn(*BTN_MENU), btn("ℹ️ About", "about")]],
    ),
    "about": (
        TEXT_ABOUT,
        [[site_btn()], [btn(*BTN_MENU), btn("✏️ Contact", "contact")]],
    ),
}


# ============================================
# HANDLERS
# ============================================
@bot.message_handler(commands=["start"])
def start(message):
    markup = make_markup([[site_btn()], [btn(*BTN_HEADLINES), btn(*BTN_MENU)]])
    bot.send_message(message.chat.id, TEXT_START, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data in SCREENS)
def show_screen(call):
    bot.answer_callback_query(call.id)
    text, rows = SCREENS[call.data]
    markup = make_markup(rows)
    try:
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
    except ApiTelegramException:
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    bot.set_chat_menu_button(menu_button=types.MenuButtonDefault(type="default"))

    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
