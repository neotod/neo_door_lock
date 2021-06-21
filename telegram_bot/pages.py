import enum

bot_pages = {} 
settings_switch_btns = {}
text_handling_pages = [] # pages that need text handling function to work with them

class Pages(enum.Enum):
    welcome = enum.auto()

    login_username = enum.auto()
    login_password = enum.auto()

    main = enum.auto()
    settings = enum.auto()
    report = enum.auto()

    settings_report = enum.auto()
    settings_lock = enum.auto()

class Buttons(enum.IntEnum): # every button except back button in the bot, has a unique id
    back = enum.auto()
    login = enum.auto()
    logout = enum.auto()
    report = enum.auto()
    settings = enum.auto()

    settings_report = enum.auto()
    settings_lock = enum.auto()

    day_report = enum.auto()
    month_report = enum.auto()
    year_report = enum.auto()
    
    settings_lreport_switch = enum.auto()
    settings_lreport_off = enum.auto()
    settings_lreport_on = enum.auto()

    settings_oreport_switch = enum.auto()
    settings_oreport_off = enum.auto()
    settings_oreport_on = enum.auto()

    settings_lock_switch = enum.auto()
    settings_lock_off = enum.auto()
    settings_lock_on = enum.auto()

class Button:
    def __init__(self, id_: Buttons, text: str, next_page_id: int, row_index: int=0):
        self.id_ = id_
        self.text = text
        self.next_page_id = next_page_id
        self.row_index = row_index

class Page:
    def __init__(self, id_: Pages, buttons: dict, description: str):
        self.id_ = id_
        self.buttons = buttons
        self.description = description

def make_pages():
    login_btn  = Button(Buttons.login, 'ورود🔑', Pages.login_username)
    logout_btn = Button(Buttons.logout, 'خروج📛', Pages.welcome, 1)

    report_btn       = Button(Buttons.report, 'گزارش📃', Pages.report)
    day_report_btn   = Button(Buttons.day_report, 'گزارش امروز📗', Pages.main)
    month_report_btn = Button(Buttons.month_report, 'گزارش این ماه📕', Pages.main)
    year_report_btn  = Button(Buttons.year_report, 'گزارش این سال📘', Pages.main)
    
    settings_btn        = Button(Buttons.settings, 'تنظیمات⚙', Pages.settings)
    settings_report_btn = Button(Buttons.settings_report, 'گزارش📜', Pages.settings_report)
    settings_lock_btn   = Button(Buttons.settings_lock, 'قفل هوشمند🔒', Pages.settings_lock)

    settings_lreport_off_btn = Button(Buttons.settings_lreport_off, 'غیرفعال کردن گزارش بلندمدت❌', Pages.settings_report)
    settings_lreport_on_btn  = Button(Buttons.settings_lreport_on, 'فغال کردن گزارش بلندمدت✅', Pages.settings_report)

    settings_oreport_off_btn = Button(Buttons.settings_oreport_off, 'غیرفعال کردن گزارش لحظه ای❌', Pages.settings_report)
    settings_oreport_on_btn  = Button(Buttons.settings_oreport_on, 'فعال کردن گزارش لحظه ای✅', Pages.settings_report)

    settings_lock_off_btn = Button(Buttons.settings_lock_off, 'غیرفعال کردن❌', Pages.settings_lock)
    settings_lock_on_btn  = Button(Buttons.settings_lock_on, 'فعال کردن✅', Pages.settings_lock)
    
    settings_lreport_switch_btn = Button(Buttons.settings_lreport_switch, settings_lreport_on_btn.text, Pages.settings_report)
    settings_oreport_switch_btn = Button(Buttons.settings_oreport_switch, settings_oreport_on_btn.text, Pages.settings_report)

    settings_lock_switch_btn = Button(Buttons.settings_lock_switch, settings_lock_off_btn.text, Pages.settings_lock)
    

    welcome_btns = {
        login_btn.id_: login_btn
    }
    text = '''
این بات یه رابط از راه دور بین شما و قفل هوشمند هست.🤖
با این بات میتونید کارای زیر رو انجام بدید:
    <b>*</b> آپشن های مختلف رو فعال یا غیر فعال کنید.
    <b>*</b> از رفت و آمد های اخیر گزارش بگیرید.
    و...

<b>لطفا برای ادامه وارد شوید.</b>👤
    '''
    welcome_page = Page(Pages.welcome, welcome_btns, text)


    login_username_btns = {
        Buttons.back: Button(Buttons.back, 'انصراف↩', Pages.welcome)
    }
    text='''
لطفا نام کاربری خود را وارد کنید
    '''
    login_username_page = Page(Pages.login_username, login_username_btns, text)

    text='''
لطفا رمز عبور خود را وارد کنید
    '''
    login_password_page = Page(Pages.login_password, login_username_btns, text)

    
    main_btns = {
        report_btn.id_: report_btn, 
        settings_btn.id_: settings_btn,
        logout_btn.id_: logout_btn
    }
    text = '''
🎈خوش آمدید
⚠ بهتر است پس از اتمام کار خود با بات، خروج را بزنید تا از اکانت خود خارج شوید.
⚠ در صورتی که از اکانت خود خارج نشوید، بات بصورت خودکار پس از ۵ دقیقه عدم تعامل با بات، از اکانت شما خارج خواهد شد.
    '''
    main_page = Page(Pages.main, main_btns, text)


    settings_btns = {
        settings_report_btn.id_: settings_report_btn,
        settings_lock_btn.id_: settings_lock_btn,
        Buttons.back: Button(Buttons.back, 'بازگشت↩', Pages.main, 1)
    }
    text = '''
از این بخش میتونید تنظیمات بخش های مختلف قفل رو تغییر بدید.
    '''
    settings_page = Page(Pages.settings, settings_btns, text)


    report_btns = {
        day_report_btn.id_: day_report_btn, 
        month_report_btn.id_: month_report_btn, 
        year_report_btn.id_: year_report_btn, 
        Buttons.back: Button(Buttons.back, 'بازگشت↩', Pages.main, 1)
    }
    text = '''
روی هرکدوم از گزارش هایی که میخواین کلیک کنید و بصورت فایل اکسل خروجی بگیرین.
گزارش خروجی شامل:
<b>تمامی ورودی های موفق و ناموفق، تغییر وضعیت قفل هوشمند، ورود کاربر به بات تلگرام</b> میباشد.
    '''
    report_page = Page(Pages.report, report_btns, text)


    settings_report_btns = {
        Buttons.settings_lreport_switch: settings_lreport_switch_btn, 
        Buttons.settings_oreport_switch: settings_oreport_switch_btn,
        Buttons.back: Button(Buttons.back, 'بازگشت↩', Pages.settings, 1)
    }
    text = '''
<b>گزارش لحظه ای</b>: گزارشی از ورود موفق یا ناموفق که بصورت لحظه ای به شماره تلفن شما ارسال میشود.
<b>گزارش بلندمدت</b>: هر فعالیتی اعم از <b>ورود و خروج ناموفق، تغییر وضعیت قفل و ورود کاربر به بات </b>در سرور ذخیره می شود و هنگام درخواست، گزارش بصورت فایل اکسل خروجی داده میشود.
    '''
    settings_report_page = Page(Pages.settings_report, settings_report_btns, text)


    settings_lock_btns = {
        Buttons.settings_lock_switch: settings_lock_switch_btn,
        Buttons.back: Button(Buttons.back, 'بازگشت↩', Pages.settings, 1)
    }
    text = '''
    '''
    settings_lock_page = Page(Pages.settings_lock, settings_lock_btns, text)


    bot_pages.update({
        welcome_page.id_: welcome_page, 
        login_username_page.id_: login_username_page, 
        login_password_page.id_: login_password_page, 
        
        main_page.id_: main_page, 
        report_page.id_: report_page, 
        settings_page.id_: settings_page, 

        settings_report_page.id_: settings_report_page, 
        settings_lock_page.id_: settings_lock_page,
    })

    settings_switch_btns.update({
        settings_lreport_switch_btn.id_: settings_lreport_switch_btn,
        settings_oreport_switch_btn.id_: settings_oreport_switch_btn,
        settings_lock_switch_btn.id_: settings_lock_switch_btn,

        settings_lreport_off_btn.id_: settings_lreport_off_btn,
        settings_oreport_off_btn.id_: settings_oreport_off_btn,

        settings_lreport_on_btn.id_: settings_lreport_on_btn,
        settings_oreport_on_btn.id_: settings_oreport_on_btn,

        settings_lock_off_btn.id_: settings_lock_off_btn,
        settings_lock_on_btn.id_: settings_lock_on_btn
    })

    text_handling_pages.extend([Pages.login_username, Pages.login_password])