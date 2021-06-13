import enum

bot_pages = {} # bots pages wrapper

class Pages(enum.Enum):
    main = 0
    setting = 1
    setting_report = 2
    setting_lock = 3
    report = 4

class Page:
    def __init__(self, id_: Pages, buttons: dict, button_name: str, description: str, prev_page_id):
        self.id_ = id_
        self.buttons = buttons
        self.button_name = button_name
        self.description = description
        self.prev_page_id = prev_page_id


def make_pages():
    main_btns = {'report': 'گزارش📃', 'setting': 'تنظیمات⚙'}
    text = '''
    این بات یه رابط از راه دور بین شما و قفل هوشمند هست.🤖
با این بات میتونید کارای زیر رو انجام بدید:
    <b>*</b> آپشن های مختلف رو فعال یا غیر فعال کنید.
    <b>*</b> از رفت و آمد های اخیر گزارش بگیرید.
    و...
    '''
    main = Page(Pages.main, main_btns, None, text, 0) # button name = None, because main page doesn't have any button


    setting_btns = {'s_report': 'گزارش📜', 's_lock': 'قفل هوشمند🔒', 'back': 'بازگشت↩'}
    text = '''
    <b>تنظیمات</b>⚙
از این بخش میتونید تنظیمات بخش های مختلف قفل رو تغییر بدید.
    '''
    setting = Page(Pages.setting, setting_btns, 'setting', text, main.id_)


    report_btns = {'day_report': 'گزارش امروز📗', 'week_report': 'گزارش این هفته📕', 'month_report': 'گزارش این ماه📘', 'back': 'بازگشت↩'}
    text = '''
<b>گزارش📃</b>
    روی هرکدوم از گزارش هایی که میخواین کلیک کنید و بصورت فایل اکسل خروجی بگیرین.
    '''
    report = Page(Pages.report, report_btns, 'report', text, main.id_)


    setting_report_btns = {'longtime_report': {'on': 'فعال کردن گزارش بلندمدت✅', 'off': 'غیرفعال کردن گزارش بلندمدت❌'}, 
                        'ontime_report': {'on': 'فعال کردن گزارش لحظه ای✅', 'off': 'غیرفعال کردن گزارش لحظه ای❌'},
                        'back': 'بازگشت↩'}
    text = '''
<b>تنظیمات > گزارش📜</b>
    '''
    setting_report = Page(Pages.setting_report, setting_report_btns, 's_report', text, setting.id_)


    setting_lock_btns = {'lock': {'on': 'فعال کردن✅', 'off': 'غیرفعال کردن❌'}, 'back': 'بازگشت↩'}
    text = '''
<b> تنظیمات > قفل🔒</b>
    '''
    setting_lock = Page(Pages.setting_lock, setting_lock_btns, 's_lock', text, setting.id_)


    bot_pages.update({main.id_: main, report.id_: report, setting.id_: setting, setting_report.id_: setting_report, setting_lock.id_: setting_lock})