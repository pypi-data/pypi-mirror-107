import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver = None
_isWire = False

DEFAULT_TIMEOUT = 10
DEFAULT_INTERVAL = 0.4


def init(isWire=False):
    global driver
    if not driver:
        global _isWire
        _isWire = isWire
        if _isWire:
            from seleniumwire import webdriver
            driver = webdriver.Chrome()
        else:
            from selenium import webdriver
            driver = webdriver.Chrome()
        driver.maximize_window()
    else:
        raise Exception("浏览器已经打开，不允许重复调用init")


def kill():
    global driver
    driver.quit()
    driver = None


def getTitle():
    return driver.title


def getUrl():
    return driver.current_url


def open(url):
    driver.get(url)


def anotherPage(timeout=DEFAULT_TIMEOUT):
    if len(driver.window_handles) < 2:
        WebDriverWait(driver, timeout).until(lambda d: len(driver.window_handles) > 1)
    for page in driver.window_handles:
        if page != driver.current_window_handle:
            driver.switch_to.window(page)


def clearAllPages():
    ary = driver.window_handles[:]
    for i in range(1, len(ary)):
        driver.switch_to.window(ary[i])
        driver.close()
    driver.switch_to.window(ary[0])
    driver.get("data:,")


def keepCurrentPage():
    ary = driver.window_handles[:]
    if driver.current_window_handle in ary:
        for page in ary:
            if page != driver.current_window_handle:
                driver.switch_to.window(page)
                driver.close()
    else:
        for i in range(1, len(ary)):
            driver.switch_to.window(ary[i])
    driver.switch_to.window(
        driver.window_handles[0]
    )


def getActionChains():
    return webdriver.ActionChains(driver)


def getRequests(condition=None):
    if not _isWire:
        raise Exception("不支持bs.getRequests操作，init需要指定参数isWire为True")
    if condition:
        ary = list(filter(condition, driver.requests))
    else:
        ary = driver.requests[:]
    return ary


def waitForRequest(url, timeout=None):
    if not _isWire:
        raise Exception("不支持bs.waitRequests操作，init需要指定参数isWire为True")
    driver.wait_for_request(url, timeout)


def setRequestsRule(*ruleList):
    if not _isWire:
        raise Exception("不支持bs.setRequestsRule操作，init需要指定参数isWire为True")
    driver.scopes = ruleList


def clearRequests(rule):
    if not _isWire:
        raise Exception("不支持bs.clearRequests操作，init需要指定参数isWire为True")
    del driver.requests


def _get(find, check, timeout, delay, interval, index):
    endTime = time.time() + timeout
    if delay:
        time.sleep(delay)
    while True:
        ary = find()
        if ary:
            resultAry = None
            if check:
                checkResult = check(ary)
            else:
                checkResult = ary
            if checkResult == True:
                resultAry = ary
            elif checkResult:
                resultAry = checkResult
            if resultAry:
                if index == None:
                    return resultAry
                elif len(resultAry) > index:
                    return [resultAry[index]]
        if time.time() >= endTime:
            return []
        time.sleep(interval)


def getByCss(value, base=None, check=None, timeout=DEFAULT_TIMEOUT, delay=None, interval=DEFAULT_INTERVAL, index=None):
    base = base or driver
    return _get(
        lambda: base.find_elements_by_css_selector(value),
        check,
        timeout,
        delay,
        interval,
        index,
    )


def getByLinkText(value, base=None, check=None, timeout=DEFAULT_TIMEOUT, delay=None, interval=DEFAULT_INTERVAL, index=None, hard=False):
    base = base or driver
    if hard:
        fun = base.find_elements_by_link_text
    else:
        fun = base.find_elements_by_partial_link_text
    return _get(
        lambda: fun(value),
        check,
        timeout,
        delay,
        interval,
        index,
    )


def highlight(*itemList):
    for item in itemList:
        style = "background:#ff66cc; border:2px sold red;"
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", item, style)


def highlightByCss(value, **parDict):
    highlight(
        *getByCss(value, **parDict)
    )


def highlightByLinkText(value, **parDict):
    highlight(
        *getByLinkText(value, **parDict)
    )


def clickByCss(value, index=0, **parDict):
    item = getByCss(value, index=index, **parDict)[0]
    item.click()


def clickByLinkText(value, index=0, **parDict):
    item = getByLinkText(value, index=index, **parDict)[0]
    item.click()


def mouseMoveByCss(value, index=0, **parDict):
    item = getByCss(value, index=index, **parDict)[0]
    getActionChains().move_to_element(item).perform()


def mouseMoveByLinkText(value, index=0, **parDict):
    item = getByLinkText(value, index=index, **parDict)[0]
    getActionChains().move_to_element(item).perform()


def keyboardByCss(value, *keys, index=0, **parDict):
    item = getByCss(value, index=index, **parDict)[0]
    item.send_keys(*keys)


def keyboardByLinkText(value, *keys, index=0, **parDict):
    item = getByLinkText(value, index=index, **parDict)[0]
    item.send_keys(*keys)


def keyboardClearByCss(value, index=0, **parDict):
    item = getByCss(value, index=index, **parDict)[0]
    item.clear()


def keyboardClearByLinkText(value, index=0, **parDict):
    item = getByLinkText(value, index=index, **parDict)[0]
    item.clear()
