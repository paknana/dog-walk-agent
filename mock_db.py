from models import DogWalkRoute

_weather_scenarios = {
    "sunny_perfect": {
        "temperature": 18.0,
        "weather_condition": "맑음",
        "precipitation_prob": 0.0,
        "air_quality": 25 # 좋음
    },
    "heavy_rain": {
        "temperature": 15.0,
        "weather_condition": "비",
        "precipitation_prob": 90.0,
        "air_quality": 10 # 좋음
    },
    "bad_dust": {
        "temperature": 20.0,
        "weather_condition": "흐림",
        "precipitation_prob": 10.0,
        "air_quality": 160 # 매우 나쁨
    },
    "scorching_heat": {
        "temperature": 33.0,
        "weather_condition": "맑음",
        "precipitation_prob": 0.0,
        "air_quality": 40 # 보통
    },
    "snowing": {
        "temperature": -2.0,
        "weather_condition": "눈",
        "precipitation_prob": 80.0,
        "air_quality": 20 # 좋음
    },
    "chilly_wind": {
        "temperature": 5.0,
        "weather_condition": "흐림",
        "precipitation_prob": 0.0,
        "air_quality": 50 # 보통
    },
    "rain_and_bad_dust": {
    "temperature": 15.0,
    "weather_condition": "비",
    "precipitation_prob": 90.0,
    "air_quality": 160
    },
}

_store= {
    "dog_walk_profiles": [],
    "saved_walk_routes": [],
    "walk_routes": [
        
        DogWalkRoute(
            route_name="평촌 중앙공원 외곽 흙길",
            place_type="근린공원", total_distance_km=1.5,
            slope_level=1, surface_quality=4, lighting_level=5, crowdedness_level=3,
            mobility_scope="walk"
        ),
        DogWalkRoute(
            route_name="학의천 상류 산책로",
            place_type="하천", total_distance_km=2.0,
            slope_level=1, surface_quality=5, lighting_level=3, crowdedness_level=2,
            mobility_scope="walk"
        ),
        DogWalkRoute(
            route_name="자유공원 잔디 광장",
            place_type="근린공원", total_distance_km=1.2,
            slope_level=2, surface_quality=5, lighting_level=4, crowdedness_level=3,
            mobility_scope="walk"
        ),
        DogWalkRoute(
            route_name="안양천 자전거도로 옆 흙길",
            place_type="하천", total_distance_km=3.0,
            slope_level=1, surface_quality=4, lighting_level=4, crowdedness_level=4,
            mobility_scope="walk"
        ),
        DogWalkRoute(
            route_name="범계역 로데오거리 뒷골목",
            place_type="주택가 골목", total_distance_km=1.0,
            slope_level=1, surface_quality=2, lighting_level=5, crowdedness_level=5,
            mobility_scope="walk" # 인파가 많아서 예민한 강아지에겐 비추천
        ),
        DogWalkRoute(
            route_name="모락산 산림욕장 입구",
            place_type="등산로", total_distance_km=1.0,
            slope_level=4, surface_quality=3, lighting_level=2, crowdedness_level=1,
            mobility_scope="walk"
        ),
        DogWalkRoute(
            route_name="하남 스타필드 실내 코스",
            place_type="실내 복합물", total_distance_km=3.0,
            slope_level=1, surface_quality=5, lighting_level=5, crowdedness_level=5,
            mobility_scope="drive"
        ),
        DogWalkRoute(
            route_name="의왕 백운호수 생태탐방로",
            place_type="하천", total_distance_km=2.5,
            slope_level=1, surface_quality=4, lighting_level=4, crowdedness_level=4,
            mobility_scope="drive"
        ),
        DogWalkRoute(
            route_name="안양예술공원 계곡길",
            place_type="등산로", total_distance_km=2.5,
            slope_level=3, surface_quality=3, lighting_level=2, crowdedness_level=4,
            mobility_scope="drive"
        ),
        DogWalkRoute(
            route_name="남양주 아웃도어 펫파크",
            place_type="반려견 놀이터", total_distance_km=1.5,
            slope_level=2, surface_quality=5, lighting_level=3, crowdedness_level=2,
            mobility_scope="drive"
        ),
        DogWalkRoute(
            route_name="광교 호수공원 반려견 놀이터",
            place_type="반려견 놀이터", total_distance_km=2.0,
            slope_level=1, surface_quality=5, lighting_level=5, crowdedness_level=4,
            mobility_scope="drive"
        ),
        DogWalkRoute(
            route_name="과천 서울대공원 반려견 놀이터",
            place_type="반려견 놀이터", total_distance_km=1.0,
            slope_level=1, surface_quality=5, lighting_level=4, crowdedness_level=3,
            mobility_scope="drive"
        )
    ]
}

def get_store():
    return _store

def get_current_weather():
    current_id = _store.get("current_weather_id", "sunny_perfect")
    return _weather_scenarios[current_id]