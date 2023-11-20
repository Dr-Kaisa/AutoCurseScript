from selenium import webdriver
import time
from selenium.webdriver.common.by import By


def closeTheAlert(driver):
    driver.find_element(By.CSS_SELECTOR, ".el-scrollbar__view>.topic>.radio>.topic-list>.topic-item svg").click()
    print('点击选项')

    driver.find_element(By.CSS_SELECTOR, "#outContainer>.el-dialog__wrapper>.el-dialog>.el-dialog__footer span").click()
    print('点击关闭')


def ini(driver, account, password, loginAndSelectTime):
    print("正在初始化")
    driver.maximize_window()
    driver.get(
        "https://passport.zhihuishu.com/login?service=https://onlineservice-api.zhihuishu.com/gateway/f/v1/login/gologin")
    time.sleep(1)
    driver.find_element(By.ID, "lUsername").send_keys(account)
    driver.find_element(By.ID, "lPassword").send_keys(password)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "wall-sub-btn").click()
    # 休眠，等待用户通过滑动验证码，并点进课程播放页面
    time.sleep(loginAndSelectTime)

    try:
        driver.find_element(By.CLASS_NAME, "talk-later-btn").click()
    except(Exception):
        pass

    try:

        driver.find_element(By.CSS_SELECTOR, ".el-dialog__header>i").click()
    except(Exception):
        pass
    print("初始化完成")


def unPause(driver):
    video = driver.find_element(By.ID, 'vjs_container_html5_api')
    driver.execute_script("arguments[0].play()", video)


if __name__ == '__main__':
    # 输入账号密码
    account = input("请输入账号\n")
    password = input("请输入密码\n")

    # 实例化浏览器
    driver = webdriver.Edge()
    # 初始化
    ini(driver, account, password, 25)
    # 播放
    print("保存课程列表")
    icofinishlist = driver.find_elements(By.CLASS_NAME, "fl.time_icofinish")  # 存放之前已完成的课程，列表
    Allvideolist = driver.find_elements(By.CLASS_NAME, "clearfix.video")  # 存放全部课程，列表
    Allvideolist[len(icofinishlist)].click()
    sec = 5
    print(fr"保存成功，{sec}秒后进入循环")
    time.sleep(sec)

    print('进入循环')
    while True:

        time.sleep(1)
        try:
            print("正在关闭弹窗")
            closeTheAlert(driver)
        except:
            print("关闭弹窗失败")
        try:
            # 播放视频，防止其他原因暂停播放
            unPause(driver)
        except:
            pass

        time.sleep(0.5)
        # 通存放现在已完成的课程的列表
        Nowicofinish = driver.find_elements(By.CLASS_NAME, "fl.time_icofinish")
        # 当现在已完成比之前已完成多一个，自动播放下一个视频
        if len(Nowicofinish) == len(icofinishlist) + 1:
            icofinishlist = driver.find_elements(By.CLASS_NAME, "fl.time_icofinish")  # 更新已完成的课程，列表
            Allvideolist[len(icofinishlist)].click()
            time.sleep(5)
