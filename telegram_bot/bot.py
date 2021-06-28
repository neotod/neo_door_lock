import os
import sys
import re
import pandas
import logging
import hashlib
import argparse
import jdatetime

from parts import *

from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
)
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler
)
from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN


MAX_SESSION_TIME = 5 * 60 # 5 mins
DOCUMENT_DESTRUCTION_TIME = 30
LOGS_DIR = os.path.join('datas', 'log.log')


pages.make_pages()

smart_lock = classes.Smart_Lock()
current_user = None

cur_page_id = ids.Pages.welcome

login_username_valid = True
login_password_valid = True

login_cur_user_index = 0

inline_query_message = None # the main message which is getting updated constantly
chat_id = 0 # current chat (user with bot) id

whereami = ['خانه🏠']

# logging.basicConfig(filename=LOGS_DIR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    global cur_page_id, inline_query_message, whereami, chat_id

    if not current_user:
        cur_page_id = ids.Pages.welcome

    else:
        user_obj = update.effective_user
        if user_obj.username != current_user.telegram_obj.username: # only one user can use the bot at the same time
            update.message.reply_text(text='⚠کاربر دیگری در حال استفاده از بات است، لطفا حداکثر پس از ۵ دقیقه دیگر مراجعه کنید.')
            return

        else:
            cur_page_id = ids.Pages.main
            chat_id = update.message.chat.id
            inline_query_message.delete()
            inline_query_message = None
            
    whereami = ['خانه🏠']
    whereami_string = '<b>' + ' > '.join(whereami) + '</b>\n'
    description = pages.bot_pages[cur_page_id].description
    description = whereami_string + description
    inline_btns = get_page_inline_btns(pages.bot_pages[cur_page_id])

    if update.message:
        inline_query_message = update.message.reply_html(description, reply_markup=InlineKeyboardMarkup(inline_btns))
    else:
        query = update.callback_query
        chat_id = query.message.chat_id
        inline_query_message = query.bot.send_message(chat_id, description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))
        query.answer()

    user = update.effective_user
    logger.info(f'New user starts the bot, user info: \t\nfname: {user.first_name}\t\nlname: {user.last_name}\t\nusername: {user.username}\n')

def help_(update, context):
    return


def inline_queries(update, context):
    '''main inline queries handler'''

    global inline_query_message, current_user, cur_page_id, smart_lock, whereami
    global login_username_valid, login_password_valid

    query = update.callback_query

    if not inline_query_message:
        inline_query_message = query.message

    if query.message != inline_query_message:
        query.answer(text='⚠لطفا با آخرین پیام از طرف بات، با بات کار کنید!', show_alert=True)
        return

    button_id = int(query.data) # data is id of the button that was clicked by user
    inline_query_message = query.message
    
    if current_user:
        user_obj = update.effective_user
        if user_obj.username != current_user.telegram_obj.username: # only one user can use the bot at the same time
            query.answer()
            query.edit_message_text(text='⚠کاربر دیگری در حال استفاده از بات است، لطفا حداکثر پس از ۵ دقیقه دیگر مراجعه کنید.')
            return
    else:
        if button_id != ids.Buttons.login and cur_page_id != ids.Pages.login_username and cur_page_id != ids.Pages.login_password:
            start(update, context)
            return
        elif (button_id != ids.Buttons.login and button_id != ids.Buttons.back) and (cur_page_id == ids.Pages.welcome or cur_page_id == ids.Pages.login_username or cur_page_id == ids.Pages.login_password):
            query.answer(text='⚠لطفا اول لاگین کنید!', show_alert=True)
            return

    chat_id = inline_query_message.chat_id
    set_session_removal_task(context, chat_id) # everytime user interacts with the bot, session removal task will get removed


    if button_id == ids.Buttons.logout or (button_id == ids.Buttons.back and (cur_page_id == ids.Pages.login_username or cur_page_id == ids.Pages.login_password)):
        logout(context)
    
    elif button_id == ids.Buttons.day_report or button_id == ids.Buttons.month_report or button_id == ids.Buttons.year_report:
        file_made = output_report(update, context, button_id)

        if file_made:
            remove_task_if_exists(context, 'temp_file_remove')

            task = lambda _: os.remove('datas/temp.csv')
            context.job_queue.run_once(task, 5, name='temp_file_remove')

        if whereami[-1] == 'گزارش📃':
            whereami.pop()

    elif (cur_page_id == ids.Pages.settings_lock or cur_page_id == ids.Pages.settings_report) and button_id in pages.settings_switch_btns:
        settings_update(button_id)

    elif button_id == ids.Buttons.back:
        whereami.pop(-1)
        
    else:
        button_text = pages.bot_pages[cur_page_id].buttons[button_id].text
        whereami.append(button_text)

    next_page_id = set_next_page(button_id)
    cur_page_id = next_page_id

    next_page = pages.bot_pages[next_page_id]
    inline_btns = get_page_inline_btns(next_page)
    description = next_page.description

    description = settings_description_update(description)
    
    whereami_string = '<b>' + ' > '.join(whereami) + '</b>\n'
    description = whereami_string + description

    query.answer()
    query.edit_message_text(description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))

def text(update, context):
    '''main text input handler'''

    global inline_query_message, cur_page_id, current_user, whereami
    global login_username_valid, login_password_valid

    if cur_page_id not in pages.text_handling_pages:
        update.message.delete()
        return


    cur_page = pages.bot_pages[cur_page_id]
    inline_btns = get_page_inline_btns(cur_page)

    if cur_page_id == ids.Pages.login_username or cur_page_id == ids.Pages.login_password: # login part
        description = cur_page.description
        description += 'لطفا صبر کنید...⏳'
        whereami_string = '<b>' + ' > '.join(whereami) + '</b>\n'
        description = whereami_string + description

        inline_query_message.edit_text(description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))

        message = update.message.text
        chat_id = update.message.chat_id
        update.message.delete()

        if cur_page_id == ids.Pages.login_username:
            login_username_valid = True
            login_password_valid = False
            data = 'username'

        elif cur_page_id == ids.Pages.login_password:
            login_password_valid = True
            data = 'password'

        validate_input({data: message})

        if login_username_valid and login_password_valid: # login was successful.
            cur_page_id = ids.Pages.main
            user_obj = update.effective_user
            current_user = classes.User(user_obj, 'neotod', 'soltani', 'neotod')

            if smart_lock.lreport_on:
                event = classes.Event(classes.Events.user_login, 'ورود کاربر به تلگرام')
                event_info = f'username: {current_user.username}'
                report(event, event_info)

            logger.info(f'SUCCESSFUL LOGIN \n TELEGRAM => F: {user_obj.first_name}, L: {user_obj.last_name}, U: {user_obj.username} \n BOT => username: {current_user.username}\n')
            
            set_session_removal_task(context, chat_id)
            start(update, context)
            
        else:
            if cur_page_id == ids.Pages.login_username and login_username_valid:
                cur_page_id = ids.Pages.login_password # username was valid go to password page
                login_password_valid = True

            cur_page = pages.bot_pages[cur_page_id]
            inline_btns = get_page_inline_btns(cur_page)
            description = cur_page.description

            if cur_page_id == ids.Pages.login_username and not login_username_valid:
                description += '\n 🛑 نام کاربری وارد شده در سیستم ثبت نشده است.'
                description += '\n دوباره وارد کنید'

            elif cur_page_id == ids.Pages.login_password and not login_password_valid:
                description += '\n 🛑 رمز عبور اشتباه هست.'
                description += '\n دوباره وارد کنید'

            whereami_string = '<b>' + ' > '.join(whereami) + '</b>\n'
            description = whereami_string + description
            inline_query_message.edit_text(description, parse_mode=PARSEMODE_HTML, reply_markup=InlineKeyboardMarkup(inline_btns))

def get_page_inline_btns(page):
    global smart_lock

    inline_btns = []
    for btn_id, btn in page.buttons.items():
        
        inline_btn = InlineKeyboardButton(btn.text, callback_data=int(btn.id_))
        try:
            inline_btns[btn.row_index].append(inline_btn)
        except IndexError:
            inline_btns.append([])
            inline_btns[btn.row_index].append(inline_btn)

    return inline_btns

def set_next_page(button_id):
    global cur_page_id

    next_page_id = cur_page_id

    try:
        next_page_id = pages.bot_pages[cur_page_id].buttons[button_id].next_page_id
    except KeyError as e: # user is interacting with bot thorugh another message (old message maybe)
        print('key error ', e)

    return next_page_id

def settings_update(button_id):
    global smart_lock, cur_page_id

    if button_id == ids.Buttons.settings_lock_switch:
        smart_lock.on = False if smart_lock.on else True # switch the state
        next_btn = pages.settings_switch_btns[ids.Buttons.settings_lock_off] if smart_lock.on else pages.settings_switch_btns[ids.Buttons.settings_lock_on]

        if smart_lock.lreport_on:
            event = classes.Event(classes.Events.lock_state_change, 'تغییر وضعیت قفل')
            event_info = 'current_state: '
            event_info += 'on' if smart_lock.on else 'off'
            report(event, event_info)
                
    elif button_id == ids.Buttons.settings_lreport_switch:
        smart_lock.lreport_on = False if smart_lock.lreport_on else True # switch the state
        next_btn = pages.settings_switch_btns[ids.Buttons.settings_lreport_off] if smart_lock.lreport_on else pages.settings_switch_btns[ids.Buttons.settings_lreport_on]

    elif button_id == ids.Buttons.settings_oreport_switch:
        smart_lock.oreport_on = False if smart_lock.oreport_on else True # switch the state
        next_btn = pages.settings_switch_btns[ids.Buttons.settings_oreport_off] if smart_lock.oreport_on else pages.settings_switch_btns[ids.Buttons.settings_oreport_on]

    pages.bot_pages[cur_page_id].buttons[button_id].text = next_btn.text

def settings_description_update(description):
    if cur_page_id == ids.Pages.settings_lock:
        description += '\n<b>قلف هوشمند: </b>'
        description += 'فعال✅' if smart_lock.on else 'غیرفعال❌'

    elif cur_page_id == ids.Pages.settings_report:
        description += '\n<b>گزارش لحظه ای: </b>'
        description += 'فعال✅' if smart_lock.oreport_on else 'غیرفعال❌'

        description += '\n<b>گزارش بلند مدت: </b>'
        description += 'فعال✅' if smart_lock.lreport_on else 'غیرفعال❌'

    return description

def output_report(update, context, button_id: ids.Buttons):
    '''report_interval = day | week | month'''

    global inline_query_message

    df = pandas.read_csv('datas/report.csv')
    records_dates = list(df['تاریخ'])
    cur_date = jdatetime.datetime.now()

    query = update.callback_query
    chat_id = query.message.chat_id

    same_date_indexes = []
    for i in range(len(records_dates)):
        year, month, day = [int(part) for part in records_dates[i].split('-')]

        is_same_date = False
        if year == cur_date.year:
            if button_id == ids.Buttons.year_report:
                is_same_date = True
            else:
                if month == cur_date.month:
                    if button_id == ids.Buttons.month_report:
                        is_same_date = True
                    else:
                        if day == cur_date.day:
                            if button_id == ids.Buttons.day_report:
                                is_same_date = True

        if is_same_date:
            same_date_indexes.append(i)

    if same_date_indexes:
        records = [list(df.loc[i]) for i in same_date_indexes]

        new_df = pandas.DataFrame([list(df.columns)])
        for record in records:
            new_df = new_df.append([list(record)])

        new_df.to_csv('datas/temp.csv', sep='\t', encoding='utf-16', index=False, header=False)

        with open('datas/temp.csv', 'rb') as f:

            file_name = f'report_{str(cur_date)[:-7]}.csv'.replace(':', '_').replace(' ', '_')

            if button_id == ids.Buttons.year_report:
                file_name = f'year_{file_name}'
            elif button_id == ids.Buttons.month_report:
                file_name = f'month_{file_name}'
            elif button_id == ids.Buttons.day_report:
                file_name = f'day_{file_name}'

            message = query.bot.send_document(chat_id, f, filename=file_name, caption='🛑 این فایل پس از سی ثانیه بصورت خودکار پاک خواهد شد.')
            set_message_removal_task(context, message, DOCUMENT_DESTRUCTION_TIME)
        
        return True
    
    else:
        message = query.bot.send_message(chat_id, text='در این مدت زمان گزارشی ثبت نشده است.')
        set_message_removal_task(context, message, DOCUMENT_DESTRUCTION_TIME)
        return False

def report(event: classes.Event, more_info: str):
    event_text = event.name # event names: تغییر وضعیت قفل | ورود کاربر به تلگرام | ورود

    now_date = str(jdatetime.datetime.now().date())
    now_time = str(jdatetime.datetime.now().time())[:-7]
    df = pandas.DataFrame([[now_date, now_time, event_text, more_info]])
    df.to_csv('datas/report.csv', mode='a', encoding='utf-8-sig', header=False, index=False)

def validate_input(data: dict):
    global cur_page_id, current_user
    global login_username_valid, login_password_valid, login_cur_user_index

    if 'username' in data:
        username = data['username'].lower()
        users = pandas.read_csv('datas/users.csv')
        usernames = dict(users.username)

        if username not in usernames.values():
            login_username_valid = False
        else: # username was valid
            login_cur_user_index = list(usernames.values()).index(username)

    elif 'password' in data:
        password = data['password']
        pass_hash = hashlib.sha256(password.encode()).hexdigest()
        users = pandas.read_csv('datas/users.csv')
        user_pass_hash = users.loc[login_cur_user_index, 'password']

        if pass_hash != user_pass_hash:
            login_password_valid = False

def remove_task_if_exists(context, task_name):
    jobs = context.job_queue.get_jobs_by_name(task_name)
    if jobs:
        for job in jobs:
            job.schedule_removal()

def set_session_removal_task(context, chat_id: str):
    remove_task_if_exists(context, str(chat_id))
    
    context.job_queue.run_once(lambda _:logout(context), MAX_SESSION_TIME, name=str(chat_id))

def message_remove(message):
    try: # maybe user itself deleted that message
        message.delete()
    except:
        pass

def set_message_removal_task(context, message, time):
    remove_task_if_exists(context, str(message.message_id))

    context.job_queue.run_once(lambda _:message_remove(message), time, name=str(message.message_id))

def logout(context):
    '''cleanup function'''

    global current_user, cur_page_id, inline_query_message, chat_id, whereami
    global login_username_valid, login_password_valid, login_cur_user_index

    login_username_valid = login_password_valid = True
    
    current_user = None
    login_cur_user_index = 0

    inline_query_message = None

    remove_task_if_exists(context, chat_id)
    chat_id = 0

    whereami = ['خانه🏠']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('token', help='telegram bot api token')
    args = parser.parse_args()
    
    token = args.token

    updater = Updater(token, request_kwargs={
        'proxy_url': 'socks5h://127.0.0.1:1081' # this ip:port of my outline client
    })

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_))

    dispatcher.add_handler(CallbackQueryHandler(inline_queries))
    dispatcher.add_handler(MessageHandler(Filters.text, text))


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    try:
        main()
    except:
        logger.exception('An exception occured.')