from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 웹 드라이버 초기화
driver = webdriver.Chrome()

# 첫 페이지 URL
url = "https://www.musinsa.com/app/goods/3796144"

# 리뷰를 저장할 리스트 초기화
results_list = []

# 페이지 로드
driver.get(url)

# 페이지 스크롤
driver.execute_script("window.scrollTo(0, 5000);") 

time.sleep(2)  # 스크롤 후 페이지가 로드될 시간을 줍니다.

# 각 카테고리의 탭 선택자와 데이터 선택자 정의
categories = {
    '사이즈': {
        'tab': '//*[@id="satisfaction_fragment"]/div[2]/ul/li[2]/button',  # 사이즈 탭의 실제 CSS 선택자로 바꿔주세요
        'big': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(1) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'normal': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(2) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'small': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(3) > div.per',  # 실제 CSS 선택자로 바꿔주세요
    },
    '밝기': {
        'tab': '//*[@id="satisfaction_fragment"]/div[2]/ul/li[3]/button',  # 밝기 탭의 실제 CSS 선택자로 바꿔주세요
        'bright': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(1) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'normal': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(2) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'dark': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(3) > div.per',  # 실제 CSS 선택자로 바꿔주세요
    },
    '색감': {
        'tab': '//*[@id="satisfaction_fragment"]/div[2]/ul/li[4]/button',  # 색감 탭의 실제 CSS 선택자로 바꿔주세요
        'colorful': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(1) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'normal': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(2) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'blurred': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(3) > div.per',  # 실제 CSS 선택자로 바꿔주세요
    },
    '수납공간': {
        'tab': '//*[@id="satisfaction_fragment"]/div[2]/ul/li[5]/button',  # 수납공간 탭의 실제 CSS 선택자로 바꿔주세요
        'spacious': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(1) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'normal': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(2) > div.per',  # 실제 CSS 선택자로 바꿔주세요
        'small': '#satisfaction_mobile_list > div.swiper-slide.swiper-slide-active > ul > li:nth-child(3) > div.per',  # 실제 CSS 선택자로 바꿔주세요
    }
}

# 각 카테고리별 데이터를 크롤링
for category, selectors in categories.items():
    try:
        # 카테고리 탭 클릭
        tab = driver.find_element(By.XPATH, selectors['tab'])
        tab.send_keys(Keys.ENTER)
        time.sleep(2)  # 탭 클릭 후 페이지가 로드될 시간을 줍니다.
        
        # 각 항목의 데이터를 수집
        result = {'category': category}
        for key, selector in selectors.items():
            if key == 'tab':
                continue
            try:
                element = driver.find_element(By.CSS_SELECTOR, selector)
                result[key] = element.text
            except Exception as e:
                print(f"Error finding {category} {key}: {e}")
                result[key] = None
        
        results_list.append(result)
    except Exception as e:
        print(f"Error processing {category}: {e}")

driver.quit()

# 결과를 DataFrame으로 변환하여 CSV 파일로 저장
df = pd.DataFrame(results_list)
df.to_csv('reviews_product_info2.csv', index=False)
