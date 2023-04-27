from app.wkn_config import *
from app.wkn_control import readFile, printDefault, loadScreen, wait_time, writeFile
from app.wkn_proxy import loadProxy, liveProxySocks5, liveProxyHTTP
from webdriver_manager.firefox import GeckoDriverManager
from threading import Thread, active_count
from random import choice, randrange
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import ctypes
import pyfiglet


ctypes.windll.kernel32.SetConsoleTitleW(f"{info_title} - Version {info_version} | Author: {info_author}")

print("*" * os.get_terminal_size().columns)
result = pyfiglet.figlet_format("phucuongds.com", font="Rectangles")
print(result, "_"*32, "support@phucuongds.com\n")
print("*" * os.get_terminal_size().columns)


def runFirefoxDrive(path, value, url):
    global configini_browser_random_time, browser_position, number_success, number_fail

    time_random = randrange(int(configini_browser_random_time[0]), int(configini_browser_random_time[1]))
    proxy = value[0].split(":")

    options = Options()
    options.set_preference('media.autoplay.default', 0)
    options.set_preference("media.volume_scale", "0.0")
    if proxy[2] == 'socks5':
        # socket proxy
        options.set_preference('network.proxy.type', 1)
        options.set_preference('network.proxy.socks', proxy[0])
        options.set_preference('network.proxy.socks_port', int(proxy[1]))
        options.set_preference('network.proxy.socks_remote_dns', False)
    elif proxy[2] == 'http':
        # http proxy
        options.set_preference('network.proxy.type', 1)
        options.set_preference('network.proxy.http', proxy[0])
        options.set_preference('network.proxy.http_port', int(proxy[1]))
        options.set_preference('network.proxy.ssl', proxy[0])
        options.set_preference('network.proxy.ssl_port', int(proxy[1]))
    
    service = Service(executable_path=path, log_path=os.devnull)
    driver = webdriver.Firefox(service=service, options=options)
    driver.set_window_size(value[2], value[3])
    driver.set_window_position(int(value[1]), 0)
    try:
        driver.get(url)
        TIME_TOTAL = time_random
        SCROLL_PAUSE_TIME = TIME_TOTAL // 5
        ADD_TIME = 0
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            ADD_TIME += SCROLL_PAUSE_TIME
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    action = ActionChains(driver)
                    action.move_by_offset(value[1] + (value[2]//2), value[3]//2).click().perform()
                    time.sleep(1)
                    action.move_by_offset(value[1] + (value[2]//2), value[3]//2).click().perform()
                except:
                    pass
                break
            last_height = new_height

        time.sleep(TIME_TOTAL - ADD_TIME)
        number_success = number_success + 1
    except:
        number_fail = number_fail + 1
    driver.quit()
    browser_position.append(value[1])

if __name__ == '__main__':
    try:
        printDefault("1. DOWNLOAD BROWSER DRIVE")
        browser_path = GeckoDriverManager().install()
        printDefault("2. LOAD LINK IN FILE")
        browser_url_list = readFile(file_link)
        number_total = 0
        number_success = 0
        number_fail = 0
        if browser_url_list:
            printDefault("3. LOAD PROFILE IN PATH")
            browser_profile = []
            if configini_browser_profile != '':
                for d in os.listdir(configini_browser_profile):
                    browser_profile.append(os.path.join(configini_browser_profile, d))
            printDefault("4. SET CONFIG WINDOWS")
            if configini_screen == 'manual':
                browser_width, browser_height, browser_position = loadScreen(1, configini_browser_max, configini_hidden)
            else:
                browser_width, browser_height, browser_position = loadScreen(0, configini_browser_max, configini_hidden)
            printDefault("5. STARTING THE PROCESS")
            time_check_license = time.time()
            while True:
                printDefault("5.1 LOAD PROXY")
                if configini_proxy == 'auto':
                    if configini_proxy_protocol == 'all':
                        proxy_list = loadProxy(_protocol=['http', 'socks5'], _timeout=configini_proxy_timeout, _country=configini_proxy_country, _ssl=configini_proxy_ssl, _anonymity=configini_proxy_anonymity)
                    else:
                        proxy_list = loadProxy(_protocol=[configini_proxy_protocol], _timeout=configini_proxy_timeout, _country=configini_proxy_country, _ssl=configini_proxy_ssl, _anonymity=configini_proxy_anonymity)
                else:
                    proxy_list = readFile(file_proxy)
                    if not proxy_list:
                        break
                printDefault("5.2 CHECK PROXY LIVE")
                proxy_live = []
                for p in proxy_list:
                    if p is not None and p != '':
                        x = p.split(":")
                        if x[2] == 'socks5':
                            host = liveProxySocks5(x[0], int(x[1]))
                        else:
                            host = liveProxyHTTP(x[0], int(x[1]))
                        if host is True:
                            proxy_live.append(p)
                writeFile(file_proxy, proxy_live)
                printDefault("5.3 CREATE THREAD BROWSER")
                thread_start = active_count()
                if proxy_live:
                    while len(proxy_live) >= 1:
                        if thread_start < (thread_start + configini_browser_max) and browser_position:
                            bf = ''
                            if browser_profile:
                                bf = browser_profile[0]
                                browser_profile.remove(browser_profile[0])
                            browser_value = [proxy_live[0], browser_position[0], browser_width, browser_height, bf]
                            browser_url = choice(browser_url_list)
                            thread_create = Thread(target=runFirefoxDrive, args=(browser_path, browser_value, browser_url))
                            print(f"- Start {proxy_live[0]}")
                            thread_create.start()
                            proxy_live.remove(proxy_live[0])
                            browser_position.remove(browser_position[0])
                            number_total = number_total + 1
                            time.sleep(1)
                else:
                    printDefault("PROXY NOT FOUND!")
                    wait_time(10)
                printDefault(f"Success: {number_success} - Fail: {number_fail} - Total: {number_total}")
        else:
            printDefault("LINK NOT FOUND!")
    except Exception as e:
        print(e)
    exit = input("PRESS ENTER TO EXIT: ")
