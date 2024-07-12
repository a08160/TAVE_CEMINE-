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

# 페이지 번호
j = 3

# 페이지 이동 플래그
has_next_page = True

while has_next_page:
    try:
        # 스크롤 해줘야 다음 페이지로 넘어가짐
        driver.execute_script("window.scrollTo(0, 12000);")  # matin kim은 size 13000
        time.sleep(2)  # 스크롤 후 페이지가 로드될 시간을 줍니다.

        # 현재 페이지의 모든 리뷰 요소를 가져옵니다.
        for i in range(3, 13):
            css_selector_list = {
                'user_id': f'#style_estimate_list > div > div:nth-child({i}) > div.review-profile > div > div.review-profile__text > p.review-profile__name',
                'product_name': f'#style_estimate_list > div > div:nth-child({i}) > div.review-goods-information.logInformationClick > div.review-goods-information__item > a',
                'size': f'#style_estimate_list > div > div:nth-child({i}) > div.review-goods-information.logInformationClick > div.review-goods-information__item > p > span',
                'review_text': f'#style_estimate_list > div > div:nth-child({i}) > div.review-contents.gtm-catch-click.logExpandClick > div.review-contents__text',
                'review_date': f'#style_estimate_list > div > div:nth-child({i}) > div.review-profile > div > div.review-profile__text > p.review-profile__date',
                'size_tag': f'#style_estimate_list > div > div:nth-child({i}) > div.review-contents.gtm-catch-click.logExpandClick > div.review-evaluation--type2 > ul > li:nth-child(1) > span',
                'brightness_tag': f'#style_estimate_list > div > div:nth-child({i}) > div.review-contents.gtm-catch-click.logExpandClick > div.review-evaluation--type2 > ul > li:nth-child(2) > span',
                'color_tag': f'#style_estimate_list > div > div:nth-child({i}) > div.review-contents.gtm-catch-click.logExpandClick > div.review-evaluation--type2 > ul > li:nth-child(3) > span',
                'storage_tag': f'#style_estimate_list > div > div:nth-child({i}) > div.review-contents.gtm-catch-click.logExpandClick > div.review-evaluation--type2 > ul > li:nth-child(4) > span'
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

        # 다음 페이지로 이동 (필요한 경우)
        try:
            next_page_button = driver.find_element(By.XPATH, f'//*[@id="style_estimate_list"]/div/div[13]/div/button[{j}]')
            next_page_button.send_keys(Keys.ENTER)
            j += 1
            time.sleep(2)  # 페이지 이동 후 로딩 시간을 줍니다.
        except Exception as e:
            print(f"Reached the last page or error navigating to page {j}. Stopping pagination.")
            has_next_page = False

    except Exception as e:
        print(e)
        has_next_page = False

# 웹 드라이버 종료
driver.quit()

# 결과를 DataFrame으로 변환하여 CSV 파일로 저장
df = pd.DataFrame(results_list)
df.to_csv('reviews_matin_kim_2.csv', index=False)
