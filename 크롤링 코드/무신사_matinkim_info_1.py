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

driver.execute_script("window.scrollTo(0, 5000);") #matin kim은 size 13000

time.sleep(2)  # 스크롤 후 페이지가 로드될 시간을 줍니다.

css_selector_list = {
    'total_purchase' : '#root > div.sc-18j0po5-0.gpwaIb > div:nth-child(1) > dl:nth-child(2) > dd > span > span',
    '남성' : '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-7.dKfFRD > div > div > div.sc-f7jdv1-7.iTVmMw > p.sc-f7jdv1-8.lfleyW > span',
    '여성' : '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-7.dKfFRD > div > div > div.sc-f7jdv1-7.iTVmMw > p.sc-f7jdv1-8.bsQpbS > span',
    '~18세': '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-6.jAXWNJ > div > div > ul > li:nth-child(1) > span.sc-1cn942r-10.gAaXaK > span',
    '19~23세': '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-6.jAXWNJ > div > div > ul > li:nth-child(2) > span.sc-1cn942r-10.bmsszZ > span',
    '24~28세': '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-6.jAXWNJ > div > div > ul > li:nth-child(3) > span.sc-1cn942r-10.gPjrHj > span',
    '29~33세': '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-6.jAXWNJ > div > div > ul > li:nth-child(4) > span.sc-1cn942r-10.eQvxnq > span',
    '34~39세': '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-6.jAXWNJ > div > div > ul > li:nth-child(5) > span.sc-1cn942r-10.fUALpw > span',
    '40세~' : '#root > div.sc-6b7gvr-0.kVpEUJ > div.sc-8bh7x-0.EVrVI > div.sc-8bh7x-6.jAXWNJ > div > div > ul > li:nth-child(6) > span.sc-1cn942r-10.hqREku > span'
    }

result = {}
                
# 각 요소가 존재하는지 확인 후 텍스트를 가져옵니다.
for key in css_selector_list:
    try:
        category = driver.find_element(By.CSS_SELECTOR, css_selector_list[key])
        result[key] = category.text
                    
    except Exception as e:
        print(f"Error finding {key}: {e}")
        result[key] = None
                
results_list.append(result)

driver.quit()

# 결과를 DataFrame으로 변환하여 CSV 파일로 저장
df = pd.DataFrame(results_list)
df.to_csv('reviews_product_info.csv', index=False)