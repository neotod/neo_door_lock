from time import sleep
from pandas import read_csv
from hashlib import sha256

import components as compos
from pages import Pages, make_pages, bot_pages

from telegram import (
    Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Message
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler
)
from telegram.constants import PARSEMODE_HTML


TOKEN = "1657461061:AAGK3BxAacBzXAi4Til20h0ax-Y0b1CDEwg"
MAX_SESSION_TIME = 5 * 60 # 5 mins


make_pages()

lock = compos.Smart_Lock()
current_user = None

cur_page_id = Pages.main

login_username_valid = True
login_password_valid = True

login_cur_user_index = 0

inline_query_message = None # the main message which is getting updated constantly
chat_id = 0

def start(update, context):
    global cur_page_id, inline_query_message

    if not current_user:
        cur_page_id = Pages.welcome
    else:
        cur_page_id = Pages.main
        chat_id = update.message.chat.id

    description = bot_pages[cur_page_id].description
    description = get_roadmap_string() + description
    inline_btns = get_page_inline_btns(bot_pages[cur_page_id])

    update.message.reply_html(description, reply_markup=InlineKeyboardMarkup(inline_btns))

def help_(update, context):
    return


def inline_queries(update, context): # main inline queries handler
    global inline_query_message, current_user
    global login_username_valid, login_password_valid


    query = update.callback_query
    inline_query_message = query.message
    data = query.data # data is button name, so it's just usefull for finding the next page's id

    set_next_page(data)

    chat_id = inline_query_message.chat_id
    set_session_removal_task(context, chat_id)

    if 'on' in data or 'off' in data:
        settings_update(data)

    elif data == 'logout':
        current_user = None

    elif data == 'back':
        if cur_page_id == Pages.login_username or cur_page_id == Pages.login_password:
            login_username_valid = True
            login_password_valid = True

    elif data == 'logout':
        remove_task_if_exists(context, chat_id)

    cur_page = bot_pages[cur_page_id]
    inline_btns = get_page_inline_btns(cur_page)
    description = cur_page.description

    if cur_page_id == Pages.setting_lock:
        description += '\nقلف هوشمند: '
        description += 'فعال✅' if lock.on else 'غیرفعال❌'

    elif cur_page_id == Pages.setting_report:
        description += '\nگزارش لحظه ای: '
        description += 'فعال✅' if lock.oreport_on else 'غیرفعال❌'

        description += '\nگزارش بلند مدت: '
        description += 'فعال✅' if lock.lreport_on else 'غیرفعال❌'

    description = f'<b>{get_roadmap_string()}</b>' + description

    query.answer()
    query.edit_message_text(description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))

def text(update, context): # this function handles any other user text input
    global inline_query_message, cur_page_id, current_user
    global login_username_valid, login_password_valid

    if cur_page_id != Pages.login_password and cur_page_id != Pages.login_username:
        update.message.delete()
        return


    cur_page = bot_pages[cur_page_id]
    inline_btns = get_page_inline_btns(cur_page)

    description = cur_page.description
    description += 'لطفا صبر کنید...⏳'
    description = f'<b>{get_roadmap_string()}</b>' + description

    inline_query_message.edit_text(description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))

    message = update.message.text
    chat_id = update.message.chat_id
    update.message.delete()

    if cur_page_id == Pages.login_username or cur_page_id == Pages.login_password:
        if cur_page_id == Pages.login_username:
            login_username_valid = True
            login_password_valid = True
            data = 'username'

        elif cur_page_id == Pages.login_password:
            login_password_valid = True
            data = 'password'

        validate_input({data: message})

        if current_user: # login was successful.
            set_session_removal_task(context, chat_id)
            start(update, context)
            
        else:
            cur_page = bot_pages[cur_page_id]
            inline_btns = get_page_inline_btns(cur_page)
            description = cur_page.description

            if cur_page_id == Pages.login_username and not login_username_valid:
                description += '\n 🛑 نام کاربری وارد شده در سیستم ثبت نشده است.'
                description += '\n دوباره وارد کنید'

            elif cur_page_id == Pages.login_password and not login_password_valid:
                description += '\n 🛑 رمز عبور اشتباه هست.'
                description += '\n دوباره وارد کنید'

            description = f'<b>{get_roadmap_string()}</b>' + description
            inline_query_message.edit_text(description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))


def set_next_page(data):
    global cur_page_id

    if cur_page_id == Pages.report:
        cur_page_id = Pages.main

    elif 'off' in data or 'on' in data:
        if data == 'lock_off' or data == 'lock_on':
            cur_page_id = Pages.setting_lock
                
        elif 'ontime_report' in data or 'longtime_report' in data:
            cur_page_id = Pages.setting_report

    elif 'login' in data:
        cur_page_id = Pages.login_username if 'username' in data else Pages.login_password

    elif not current_user:
        cur_page_id = Pages.welcome

    elif data == 'back':
        cur_page_id = bot_pages[cur_page_id].prev_page_id

    elif data == 'logout':
        cur_page_id = Pages.welcome

    else:
        cur_page_id = Pages.main # just random thing for init
        
        for page in bot_pages.values():
            if page.button_name == data:
                cur_page_id = page.id_
                break

def get_page_inline_btns(page):
    buttons = page.buttons
    inline_btns = []
    for btns_row in buttons:
        inline_btns.append([])

        for btn in btns_row:
            if btn == 'lock' or btn == 'ontime_report' or btn == 'longtime_report':
                option_on = lock.on if btn == 'lock' else (lock.oreport_on if btn == 'ontime_report' else lock.lreport_on) # that's neat!
                another_state = 'off' if option_on else 'on'
                
                inline_btn = InlineKeyboardButton(btns_row[btn][another_state], callback_data=f'{btn}_{another_state}')
                # callback_data = lock_on | lock_off | ontime_report_off | ontime_report_on | longtime_report_on | longtime_report_off

            else:
                inline_btn = InlineKeyboardButton(btns_row[btn], callback_data=btn)
            
            inline_btns[-1].append(inline_btn)


    return inline_btns

def settings_update(data):
    if data == 'lock_off' or data == 'lock_on':
        lock.on = False if 'off' in data else True
                
    elif 'ontime_report' in data or 'longtime_report' in data:
        if 'ontime_report' in data:
            lock.oreport_on = False if 'off' in data else True

        elif 'longtime_report' in data:
            lock.lreport_on = False if 'off' in data else True

def setting_lock(update, context):
    pass

def report(update, context):
    pass

def get_roadmap_string():
    global cur_page_id

    all_pages = []
    cur_page = bot_pages[cur_page_id]
    prev_page_id = cur_page.prev_page_id

    while prev_page_id != 0:
        prev_page = bot_pages[prev_page_id]
        all_pages.append(prev_page.buttons[0][cur_page.button_name])

        cur_page = prev_page
        prev_page_id = cur_page.prev_page_id

    all_pages.append('خانه🏠')

    all_pages.reverse()
    roadmap_string = ' > '.join(all_pages)
    roadmap_string = roadmap_string + '\n'

    return roadmap_string

def validate_input(data: dict):
    global cur_page_id, current_user
    global login_username_valid, login_password_valid, login_cur_user_index

    if 'username' in data:
        username = data['username'].lower()
        users = read_csv('datas/users.csv')
        usernames = dict(users.username)

        if username not in usernames.values():
            login_username_valid = False
        else: # username was valid
            login_cur_user_index = list(usernames.values()).index(username)

    elif 'password' in data:
        password = data['password']
        pass_hash = sha256(password.encode()).hexdigest()
        users = read_csv('datas/users.csv')
        user_pass_hash = users.loc[login_cur_user_index, 'password']

        if pass_hash != user_pass_hash:
            login_password_valid = False
        
    if cur_page_id == Pages.login_username and login_username_valid:
        cur_page_id = Pages.login_password # username was valid go to password page
    elif cur_page_id == Pages.login_password and login_password_valid: # user logged in successfuly, go to main page
        cur_page_id = Pages.main

        current_user = compos.User('neotod', 'soltani', 'neotod')

def remove_task_if_exists(context, task_name):
    jobs = context.job_queue.get_jobs_by_name(task_name)
    if jobs:
        for job in jobs:
            job.schedule_removal()

def set_session_removal_task(context, chat_id: str):
    remove_task_if_exists(context, str(chat_id))

    context.job_queue.run_once(logout, MAX_SESSION_TIME, name=str(chat_id))

def logout(context):
    global current_user, cur_page_id, login_cur_user_index, inline_query_message, chat_id
    
    current_user = None
    cur_page_id = Pages.welcome
    login_cur_user_index = 0

    inline_query_message = None
    chat_id = 0


def main():
    updater = Updater(TOKEN, request_kwargs={
        'proxy_url': 'socks5h://127.0.0.1:1080'
    })

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_))

    dispatcher.add_handler(CallbackQueryHandler(inline_queries))
    dispatcher.add_handler(MessageHandler(Filters.text, text))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()