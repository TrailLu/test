from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式，不弹出界面
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')  # 可选，防止部分网站检测窗口大小

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.bilibili.com/")

# 等待页面加载和搜索框出现
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "nav-search-input"))
)

# 输入关键词
search_box = driver.find_element(By.CLASS_NAME, "nav-search-input")
search_box.send_keys("良子")

# 点击搜索按钮
search_button = driver.find_element(By.CLASS_NAME, "nav-search-btn")
search_button.click()

# 切换到新标签页（B站搜索会新开标签页）
WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
driver.switch_to.window(driver.window_handles[1])

# 等待搜索结果加载
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".bili-video-card__info--tit"))
)

# 循环抓取前10页视频标题

# 不限页数，直到没有“下一页”为止
page = 0
while True:
    # 等待当前页视频标题加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".bili-video-card__info--tit"))
    )
    videos = driver.find_elements(By.CSS_SELECTOR, ".bili-video-card__info--tit")
    # 检测当前真实页码
    try:
        current_page_elem = driver.find_element(By.CSS_SELECTOR, '.vui_pagenation--btn.vui_pagenation--btn-active')
        current_page = current_page_elem.text.strip()
        print(f"当前真实页码：{current_page}")
    except Exception as e:
        print("未能检测到当前页码", e)
    print(f"第{page+1}页：")
    for video in videos:
        print(video.text)
    # 尝试点击“下一页”按钮（更稳健的方式）
    try:
        next_btns = driver.find_elements(By.CSS_SELECTOR, '.vui_pagenation--btn-side')
        print("分页按钮文本：", [btn.text for btn in next_btns])
        next_btn = None
        for btn in next_btns:
            if "下一" in btn.text and btn.is_enabled():
                next_btn = btn
                break
        if not next_btn or not next_btn.is_enabled():
            print("已到最后一页，没有更多页面。")
            break
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(1)
        page += 1
    except Exception as e:
        print("没有更多页面或下一页按钮未找到。", e)
        break
    try:
        # 打印分页区HTML，辅助调试
        pagination = driver.find_element(By.CSS_SELECTOR, '.vui_pagenation')
        print('分页区HTML：', pagination.get_attribute('outerHTML'))
    except Exception as e:
        print('未能找到分页区', e)

driver.quit()