from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

def getAccount():
    file = open("account.txt")
    account = file.readline()
    password = file.readline()
    file.close()
    return account, password

# 初始化浏览器
def ini():


    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get(
        "https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin")
    return driver

# 登录
def login(driver, args):
    driver.find_element(By.ID, "lUsername").send_keys(args[0])
    driver.find_element(By.ID, "lPassword").send_keys(args[1])
    try:
        driver.find_element(By.CLASS_NAME, "wall-sub-btn").click()
    except:
        pass


def closeGarbageMessage():
    try:
        driver.find_element(By.CLASS_NAME, "talk-later-btn").click()
    except(Exception):
        pass

    try:

        driver.find_element(By.CSS_SELECTOR, ".el-dialog__header>i").click()
    except(Exception):
        pass


# 返回全部课程列表
def getAllTheCurseLIst():
    return driver.find_elements(By.CLASS_NAME, "clearfix.video")


# 返回之前已完成的课程
def getTheFinishedCurse():
    return driver.find_elements(By.CLASS_NAME, "fl.time_icofinish")


def unPause(driver):
    video = driver.find_element(By.ID, 'vjs_container_html5_api')
    driver.execute_script("arguments[0].play()", video)


def closeTheAlert(driver):
    driver.find_element(By.CSS_SELECTOR, ".el-scrollbar__view>.topic>.radio>.topic-list>.topic-item svg").click()
    print('点击选项')
    sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, "#outContainer>.el-dialog__wrapper>.el-dialog>.el-dialog__footer span").click()
    print('点击关闭')



if __name__ == '__main__':

    # 初始化浏览器
    print("正在初始化浏览器")
    driver = ini()

    # 获取账号密码并登录
    while True:
        if driver.find_element(By.ID, "lPassword"):
            print("登录中...")
            login(driver, getAccount())
            break

    # 等待用户通过滑动验证码，并进入播放页面
    while True:
        print("等待进入播放页面")
        if driver.find_elements(By.CLASS_NAME, "clearfix.video"):
            print("已进入播放页面")
            sleep(2)
            closeGarbageMessage()
            print("关闭垃圾弹窗，即将开始播放\n")

            sleep(3)
            try:
                closeTheAlert(driver)
            except:
                pass

            Allvideolist = getAllTheCurseLIst()
            print(f'全部课程数：     {len(Allvideolist)}')
            lastFinishedCurse = getTheFinishedCurse()
            print(f'之前已完成课程数：{len(lastFinishedCurse)}')

            # 进入未完成课程页面
            Allvideolist[len(lastFinishedCurse)].click()
            sleep(0.5)
            Allvideolist[len(lastFinishedCurse)].click()
            sleep(0.5)
            Allvideolist[len(lastFinishedCurse)].click()
            # 开始播放
            while True:
                sleep(1)
                try:
                    print("正在关闭弹窗")
                    closeTheAlert(driver)
                except:
                    print("关闭弹窗失败")
                # 播放视频，防止其他原因暂停播放
                try:

                    unPause(driver)
                except:
                    pass

                sleep(1)
                # 存放现在已完成的课程的列表
                try:
                    nowFinishedCurse = getTheFinishedCurse()
                except:
                    nowFinishedCurse = getTheFinishedCurse()

                # 输出播放信息
                print("-------------------------------------------------------")
                print(f'全部课程数：     {len(Allvideolist)}')
                print(f'之前已完成课程数：{len(lastFinishedCurse)}')
                print(f'现在已完成课程数：{len(nowFinishedCurse)}')
                try:
                    tt = driver.find_element(By.CSS_SELECTOR, ".current_play>.cataloguediv-c>div>div span").text
                    print(f"当前视频进度：    {tt}")
                except:
                    pass
                # 当现在已完成比之前已完成多一个，自动播放下一个视频
                if len(nowFinishedCurse) == len(lastFinishedCurse) + 1:
                    sleep(10)
                    Allvideolist[len(nowFinishedCurse)].click()
                    sleep(2)
                    print(f"正在播放：{driver.find_element(By.CLASS_NAME, "current_play")}")
                    print(f"要播放的：{Allvideolist[len(nowFinishedCurse)]}")
                    # 检测视频是否切换成功
                    if driver.find_element(By.CLASS_NAME, "current_play")==Allvideolist[len(nowFinishedCurse)]:
                        lastFinishedCurse = nowFinishedCurse


        sleep(2)
