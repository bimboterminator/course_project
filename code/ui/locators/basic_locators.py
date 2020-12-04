from selenium.webdriver.common.by import By


class LoginPageLocators:
    SIGNBUTTON = (By.XPATH, '//input[contains(@name,"submit") and contains(@value,"Login")]')
    LOGINFIELD = (By.XPATH, '//input[contains(@name,"username")]')
    PASSWDFIELD = (By.XPATH, '//input[contains(@name,"password")]')
    LOGINSHOW = (By.XPATH, '//div[@id="login-name"]/ul/li[1]')
    ERRORMSG = (By.XPATH, '//div[contains(text(),"Invalid username or password")]')
    DENIED = (By.XPATH, '//div[contains(text(),"Ваша учетная запись заблокирована")]')


class MainPageLocators:
    APIHREF = (By.XPATH, '//div[contains(text(), "What is an API")]/parent::div/figure/a')
    FUTUREHREF = (By.XPATH, '//div[contains(text(), "Future of internet")]/parent::div/figure/a')
    SMPTHREF = (By.XPATH, '//div[contains(text(), "Lets talk about SMTP?")]/parent::div/figure/a')
    HOME = (By.XPATH, '//*[contains(text(),"HOME")]')
    FOOTER = (By.XPATH, '//p[contains(text(),"powered by ТЕХНОАТОМ")]/following::p')
    PYTHONHREF = (By.XPATH, '//a[contains(text(), "Python")]')
    HISTORY = (By.XPATH, '//a[contains(text(), "Python history")]')
    FLASK = (By.XPATH, '//a[contains(text(), "About Flask")]')
    NET = (By.XPATH, '//a[contains(text(), "Network")]')
    NEWS = (By.XPATH, '//a[contains(text(), "News")]')
    DWIRE = (By.XPATH, '//a[text()= "Download"]')
    EXMP = (By.XPATH, '//a[text()= "Examples "]')
    LINUX  = (By.XPATH, '//a[text()= "Linux"]')
    DWNLD = (By.XPATH, '//a[text()= "Download Centos7"]')
    LOGOUT = (By.XPATH, '//a[text()= "Logout"]')
    SIGNBUTTON = (By.XPATH, '//input[contains(@name,"submit") and contains(@value,"Login")]')
    VK = (By.XPATH, '//li[contains(text(),"VK ID")]')

class RegPageLocators:
    GOTO = (By.XPATH, '//a[contains(@href,"/reg")]')
    LOGINFIELD = (By.XPATH, '//input[contains(@name,"username")]')
    EMAIL = (By.XPATH, '//input[contains(@name,"email")]')
    PASSWDFIELD = (By.XPATH, '//input[contains(@name,"password")]')
    REPEAT = (By.XPATH, '//input[contains(@placeholder,"Repeat")]')
    TERMS = (By.XPATH, '//input[contains(@type,"checkbox")]')
    REGISTER = (By.XPATH, '//input[contains(@name,"submit") and contains(@value,"Register")]')
    LOGINLENGTH = (By.XPATH, '//div[contains(text(),"Incorrect username length")]')
    WRONGEMAIL = (By.XPATH, '//div[contains(text(),"Invalid email address")]')
    INVEMAIL = (By.XPATH, '//div[contains(text(),"Internal")]')
    USREX = (By.XPATH, '//div[contains(text(),"already")]')
    PASSNOTMATCH = (By.XPATH, '//div[contains(text(),"Passwords must match")]')
