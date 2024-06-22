import requests
import csv

def get_all_coordinates(api_key, query):
    search_url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    places = []
    page = 1
    is_end = False

    while not is_end:
        params = {"query": query, "page": page}
        response = requests.get(search_url, headers=headers, params=params)
        
        if response.status_code == 200:
            result = response.json()
            for place in result['documents']:
                name = place.get('place_name', '')
                lat = place.get('y', '')
                lng = place.get('x', '')
                address = place.get('address_name', '')
                road_address = place.get('road_address_name', '')
                
                # 좌표로 행정구역 정보 가져오기
                region_1depth_name, region_2depth_name, region_3depth_name = get_administrative_info(api_key, lat, lng)

                places.append((name, lat, lng, address, road_address, region_1depth_name, region_2depth_name, region_3depth_name))
            
            is_end = result['meta']['is_end']
            page += 1
        else:
            print(f"Error {response.status_code}: {response.text}")
            break
    
    return places

def get_administrative_info(api_key, lat, lng):
    coords_url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
    headers = {"Authorization": f"KakaoAK {api_key}"}
    params = {"x": lng, "y": lat}
    response = requests.get(coords_url, headers=headers, params=params)
    
    if response.status_code == 200:
        result = response.json()
        if result['documents']:
            region_1depth_name = result['documents'][0].get('region_1depth_name', '')
            region_2depth_name = result['documents'][0].get('region_2depth_name', '')
            region_3depth_name = result['documents'][0].get('region_3depth_name', '')
            return region_1depth_name, region_2depth_name, region_3depth_name
    
    return '', '', ''

def save_to_csv(data, filename):
    # CSV 파일에 데이터 저장
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["장소 이름", "위도", "경도", "지번 주소", "도로명 주소", "시", "구", "동"])  # 헤더 작성
        writer.writerows(data)  # 데이터 작성

# 사용 예제
api_key = "b27255004a3b168116b4d5cba427620f"  # 여기에 본인의 카카오 API 키를 입력하세요
query = "마뗑킴"
places = get_all_coordinates(api_key, query)

if places:
    save_to_csv(places, 'places.csv')
    print(f"{len(places)}개의 장소가 places.csv 파일에 저장되었습니다.")
else:
    print("검색 결과가 없습니다.")
