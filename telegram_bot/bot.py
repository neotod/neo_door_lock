from components import Smart_Lock
from pages import Pages, make_pages, bot_pages

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler
)
from telegram.constants import PARSEMODE_HTML

lock = Smart_Lock()

make_pages()
cur_page_id = Pages.main

TOKEN = "1657461061:AAFLKVgJ3KR1WgRJm6YsLHJ3ts_1n1shWxg"

def start(update, context):
    global cur_page_id
    cur_page_id = Pages.main
    description = bot_pages[cur_page_id].description
    inline_btns = [[]]

    for btn, btn_text in bot_pages[cur_page_id].buttons.items():
        inline_btn = InlineKeyboardButton(btn_text, callback_data=btn)
        inline_btns[0].append(inline_btn)
    
    update.message.reply_html(description, reply_markup=InlineKeyboardMarkup(inline_btns))

def help_(update, context):
    return

def inline_queries(update, context):
    global cur_page_id
    query = update.callback_query
    data = query.data # data is button name

    if 'off' in data or 'on' in data:
        if data == 'lock_off' or data == 'lock_on':
            cur_page_id = Pages.setting_lock
            lock.on = False if 'off' in data else True
                
        elif 'ontime_report' in data or 'longtime_report' in data:
            cur_page_id = Pages.setting_report

            if 'ontime_report' in data:
                lock.oreport_on = False if 'off' in data else True

            elif 'longtime_report' in data:
                lock.lreport_on = False if 'off' in data else True

    elif data == 'back':
        cur_page_id = bot_pages[cur_page_id].prev_page_id
    
    else:
        cur_page_id = Pages.main # just random thing for init
        
        for page in bot_pages.values():
            if page.button_name == data:
                cur_page_id = page.id_
                break
        
    cur_page = bot_pages[cur_page_id]
    description = cur_page.description
    buttons = cur_page.buttons
    inline_btns = [[]]
    for btn in buttons:
        if btn == 'lock' or btn == 'ontime_report' or btn == 'longtime_report':
            option_on = lock.on if btn == 'lock' else (lock.oreport_on if btn == 'ontime_report' else lock.lreport_on) # that's
            another_state = 'off' if option_on else 'on'
            
            inline_btn = InlineKeyboardButton(buttons[btn][another_state], callback_data=f'{btn}_{another_state}')
            # callback_data = lock_on | lock_off | ontime_report_off | ontime_report_on | longtime_report_on | longtime_report_off

        else:
            inline_btn = InlineKeyboardButton(buttons[btn], callback_data=btn)

        if btn == 'back':
            inline_btns.append([])
            inline_btns[1].append(inline_btn)
        else:
            inline_btns[0].append(inline_btn)


    if cur_page_id == Pages.setting_lock:
        description += '\nقلف هوشمند: '
        description += 'فعال✅' if lock.on else 'غیرفعال❌'

    elif cur_page_id == Pages.setting_report:
        description += '\nگزارش لحظه ای: '
        description += 'فعال✅' if lock.oreport_on else 'غیرفعال❌'

        description += '\nگزارش بلند مدت: '
        description += 'فعال✅' if lock.lreport_on else 'غیرفعال❌'


    query.answer()
    query.edit_message_text(description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))


def setting_lock(update, context):
    pass

def report(update, context):
    pass

def back(update, context):
    global cur_page_id
    prev_page_id = bot_pages[cur_page_id].prev_page_id
    cur_page_id = prev_page_id

    description = bot_pages[prev_page_id].description
    buttons = list(bot_pages[prev_page_id].buttons.values())

    update.message.reply_html(description, reply_markup=ReplyKeyboardMarkup.from_column(buttons))

def main():
    updater = Updater(TOKEN, request_kwargs={
        'proxy_url': 'socks5h://127.0.0.1:1080'
    })

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_))

    dispatcher.add_handler(CallbackQueryHandler(inline_queries))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()