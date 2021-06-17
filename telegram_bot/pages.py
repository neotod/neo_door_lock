import enum

bot_pages = {} # bots pages wrapper

class Pages(enum.Enum):
    welcome = 0
    login_username = 1
    login_password = 2
    main = 3
    setting = 4
    setting_report = 5
    setting_lock = 6
    report = 7

class Page:
    def __init__(self, id_: Pages, buttons: dict, button_name: str, description: str, prev_page_id):
        self.id_ = id_
        self.buttons = buttons
        self.button_name = button_name
        self.description = description
        self.prev_page_id = prev_page_id


def make_pages():
    welcome_btns = [{'login_username': 'ورود🔑'}]
    text = '''
این بات یه رابط از راه دور بین شما و قفل هوشمند هست.🤖
با این بات میتونید کارای زیر رو انجام بدید:
    <b>*</b> آپشن های مختلف رو فعال یا غیر فعال کنید.
    <b>*</b> از رفت و آمد های اخیر گزارش بگیرید.
    و...

<b>لطفا برای ادامه وارد شوید.</b>👤
    '''
    welcome = Page(Pages.welcome, welcome_btns, None, text, 0)


    login_username_btns = [{'back': 'انصراف↩'}]
    text='''
لطفا نام کاربری خود را وارد کنید
    '''
    login_username = Page(Pages.login_username, login_username_btns, 'login_username', text, Pages.welcome)


    login_password_btns = [{'back': 'انصراف↩'}]
    text='''
لطفا رمز عبور خود را وارد کنید
    '''
    login_password = Page(Pages.login_password, login_password_btns, 'login_username', text, Pages.welcome)


    main_btns = [{'report': 'گزارش📃', 'setting': 'تنظیمات⚙'}, {'logout': 'خروج📛'}]
    text = '''
🎈خوش آمدید
⚠ بهتر است پس از اتمام کار خود با بات، خروج را بزنید تا از اکانت خود خارج شوید.
⚠ در صورتی که از اکانت خود خارج نشوید، بات بصورت خودکار پس از ۵ دقیقه عدم تعامل با بات، از اکانت شما خارج خواهد شد.
    '''
    main = Page(Pages.main, main_btns, None, text, 0) # button name = None, because main page doesn't have any button


    setting_btns = [{'s_report': 'گزارش📜', 's_lock': 'قفل هوشمند🔒'}, {'back': 'بازگشت↩'}]
    text = '''
از این بخش میتونید تنظیمات بخش های مختلف قفل رو تغییر بدید.
    '''
    setting = Page(Pages.setting, setting_btns, 'setting', text, main.id_)


    report_btns = [{'day_report': 'گزارش امروز📗', 'week_report': 'گزارش این هفته📕', 'month_report': 'گزارش این ماه📘'}, {'back': 'بازگشت↩'}]
    text = '''
روی هرکدوم از گزارش هایی که میخواین کلیک کنید و بصورت فایل اکسل خروجی بگیرین.
گزارش خروجی شامل:
<b>تمامی ورودی های موفق و ناموفق، تغییر وضعیت قفل هوشمند، ورود کاربر به بات تلگرام</b<
میباشد.
    '''
    report = Page(Pages.report, report_btns, 'report', text, main.id_)


    setting_report_btns = [{'longtime_report': {'on': 'فعال کردن گزارش بلندمدت✅', 'off': 'غیرفعال کردن گزارش بلندمدت❌'}, 
                            'ontime_report': {'on': 'فعال کردن گزارش لحظه ای✅', 'off': 'غیرفعال کردن گزارش لحظه ای❌'}},
                            {'back': 'بازگشت↩'}]
    text = '''
    '''
    setting_report = Page(Pages.setting_report, setting_report_btns, 's_report', text, setting.id_)


    setting_lock_btns = [{'lock': {'on': 'فعال کردن✅', 'off': 'غیرفعال کردن❌'}}, {'back': 'بازگشت↩'}]
    text = '''
    '''
    setting_lock = Page(Pages.setting_lock, setting_lock_btns, 's_lock', text, setting.id_)


    bot_pages.update({
        welcome.id_: welcome, login_username.id_: login_username, login_password.id_: login_password, main.id_: main, 
        report.id_: report, setting.id_: setting, setting_report.id_: setting_report, setting_lock.id_: setting_lock
    })