"""
tools

- 장소 유형(하천, 등산로, 근린공원, 실내 복합물, 주택가 골목, 반려견 놀이터)
- 날씨 (온도, 강수 확률, 미세먼지 수치)
- 안전 및 길 상태 (포장 상태, 밀집도, 가로등, 경사도)
- 초간단 산책 시간 (총 거리, 반려견 동반 여부 (대형/소형견으로 나눔)

"""

from langchain_core.tools import tool
from typing import Union, List, Optional
from models import DogWalkRoute, DogWalkProfile
from mock_db import get_store, get_current_weather

@tool
def save_dog_walk_profile(
    dog_size: str,
    weight_kg: float,
    age_years: int,
    bcs_score: Union[int, str],
    joint_issue: int,
    mobility_scope: str,
    preferred_places_types: List[str],
    walk_goal: str,
) -> str:
    """반려견 산책 추천에 필요한 기본 정보를 저장하는 함수입니다.
    이 함수는 반려견의 기본 상태를 저장하고, 입력값을 바탕으로 mobility_level을 자동 계산합니다.

    mobility_level 기준:
    - 0: 정상적으로 산책 가능
    - 1: 약간 주의가 필요한 상태
    - 2: 이동 부담이 큰 상태
    
    Args:
        dog_size: 강아지 크기 (대형견, 중형견, 소형견)
        weight_kg: 강아지 체중 (kg)
        age_years: 강아지 나이 
        bcs_score: BCS(Body Condition Score, 1~9점)
            - 1~3점: 저체중
              갈비뼈, 요추, 골반뼈가 육안으로 선명하게 보임
            - 4~5점: 적정 체중
              갈비뼈가 만져지고, 위에서 봤을 때 허리가 잘록하며, 배가 아래로 쳐지지 않은 상태
            - 6~9점: 과체중/비만
              갈비뼈가 잘 만져지지 않고, 허리 라인이 없으며 복부 지방이 심한 상태
        joint_issue: 관절 문제 유무 (0: 없음, 1: 있음)
        mobility_scope: 이동 유형 ("drive" | "walk")
        preferred_places_types: 선호 장소 유형 (하천, 등산로, 근린공원, 실내 복합물, 주택가 골목)
        walk_goal: 산책 목표 (예: 짧게/ 운동 위주/ 안전 위주/ 길게)

    Returns:
        str: 저장된 반려견 프로필 정보를 사람이 읽기 쉬운 문자열 형태로 반환합니다.

    Raises:
        ValueError: bcs_score가 1~9 범위를 벗어나는 경우 발생합니다.
    """

    bcs_score = int(bcs_score)
    age_years = int(age_years)
    joint_issue = int(joint_issue)
    weight_kg = float(weight_kg)

    if 4 <= bcs_score <= 5:
        mobility_level = 0
    elif 1 <= bcs_score <= 3 or 6 <= bcs_score <= 7:
        mobility_level = 1
    elif 8 <= bcs_score <= 9:
        mobility_level = 2
    else:
        raise ValueError("bcs_score는 1~9 사이의 정수여야 합니다.")
    
    if joint_issue == 1:
        mobility_level = min(mobility_level + 1, 2)

    profile = DogWalkProfile(
        dog_size=dog_size,
        weight_kg=weight_kg,
        age_years=age_years,
        mobility_level=mobility_level,
        joint_issue=joint_issue,
        mobility_scope=mobility_scope,
        preferred_places_types=preferred_places_types,
        walk_goal=walk_goal,
        bcs_score=bcs_score
    )

    store = get_store()
    store["dog_walk_profiles"].append(profile)

    return f"""반려견 프로필 저장 완료
- 크기: {profile.dog_size}
- 체중: {profile.weight_kg}kg
- 나이: {profile.age_years}살
- BCS 점수: {profile.bcs_score}
- 이동 가능 수준: {profile.mobility_level}
- 관절 문제 여부: {profile.joint_issue}
- 이동 유형: {profile.mobility_scope}
- 선호 장소 유형: {', '.join(profile.preferred_places_types)}
- 산책 목표: {profile.walk_goal}
"""


@tool
def save_walk_route(
    route_name: str,
    place_type: str,
    total_distance_km: float,
    surface_quality: int,
    slope_level: int,
    lighting_level: int,
    crowdedness_level: int,
    mobility_scope: str,
    estimated_minutes: int,
    safety_score: int,
    recommendation_reason: str,
) -> str:
    """추천된 반려견 산책 경로를 저장하는 함수입니다.

    Args:
        route_name: 추천한 산책 경로의 구체적인 이름입니다.
        place_type: 장소 유형 ("하천","근린공원", "실내 복합물", "등산로", "반려견 놀이터")
        total_distance_km: 총 산책 거리 (km)
        surface_quality: 노면 상태 점수(1~5)입니다. 높을수록 산책하기 좋은 노면입니다.
        slope_level: 경사 정도(1~5)입니다. 높을수록 더 가파릅니다.
        lighting_level: 가로등 밝음 수준(1~5)입니다. 높을수록 더 밝습니다.
        crowdedness_level: 혼잡함 수준(1~5)입니다. 높을수록 더 혼잡합니다.)
        mobility_scope: 이동 유형 ("walk"|"drive")
        estimated_minutes: 예상 산책 시간 (분)
        safety_score: 안전 점수 (0~100)
        recommendation_reason: 추천 이유
    
    Returns:
        str: 저장된 산책 경로 정보를 문자열 형태로 변환합니다.
    
    """

    route = DogWalkRoute(
        route_name=route_name,
        place_type=place_type,
        total_distance_km=total_distance_km,
        surface_quality=surface_quality,
        slope_level=slope_level,
        lighting_level=lighting_level,
        crowdedness_level=crowdedness_level,
        mobility_scope=mobility_scope,
        estimated_minutes=estimated_minutes,
        safety_score=safety_score,
        recommendation_reason=recommendation_reason
    )

    store = get_store()
    store["saved_walk_routes"].append(route)

    return f"""추천된 반려견 산책 경로 저장 완료
- 경로 이름: {route.route_name}
- 장소 유형: {route.place_type}
- 총 거리: {route.total_distance_km}km
- 노면 상태: {route.surface_quality}
- 경사도: {route.slope_level}
- 조명 수준: {route.lighting_level}
- 혼잡도: {route.crowdedness_level}
- 이동 유형: {route.mobility_scope}
- 예상 산책 시간: {route.estimated_minutes}분
- 안전 점수: {route.safety_score}
- 추천 이유: {route.recommendation_reason}
"""


@tool 
def calculate_route_safety_score(
    surface_quality: int,
    slope_level: int,
    lighting_level: int,
    crowdedness_level: int,
) -> int:
    """"산책 경로의 노면 및 환경 정보를 바탕으로 안전 점수(0~100점 만점)를 계산하는 함수입니다.

    노면 상태, 경사도, 조명 수준, 혼잡도를 종합하여
    반려견이 비교적 안전하고 쾌적하게 산책할 수 있는지 점수로 환산합니다.

    점수 해석 예시:
    - 80점 이상: 매우 안전
    - 60~79점: 무난함
    - 60점 미만: 주의가 필요함

    Args:
        surface_quality: 포장 상태(1~5, 높을수록 좋음)
        slope_level: 경사도(1~5, 높을수록 가파름)
        lighting_level: 가로등 수준(1~5, 높을수록 밝음)
        crowdedness_level: 밀집도 수준(1~5, 높을수록 혼잡함)

    Returns:
        int: 산책 경로 안전 점수 (0~100)
    """

    surface_score = surface_quality * 25
    slope_score = (6 - slope_level) * 25
    lighting_score = lighting_level * 20
    crowdedness_score = (6 - crowdedness_level) * 15

    raw_score = surface_score + slope_score + lighting_score + crowdedness_score
    safety_score = int(raw_score / 4.25)

    return max(0, min(safety_score, 100))


@tool
def get_walk_context() -> str:
    """저장된 반려견 산책 프로필과 최근 추천 정보를 한 번에 조회하여, 산책 경로를 추천하기 이전에 호출하여 현재 상태를 파악하는 함수입니다.

    Returns:
        str: 반려견 프로필 및 최근 추천 정보를 포함한 문자열
    """

    store = get_store()

    profiles = store.get("dog_walk_profiles", [])
    routes = store.get("saved_walk_routes", [])

    if not profiles:
        return "등록된 반려견 산책 정보가 없습니다. 먼저 프로필을 저장하세요. "
    
    profile = profiles[-1]
    
    result = f"""
    반려견 산책 정보
    - 크기: {profile.dog_size}
    - 체중: {profile.weight_kg}kg
    - 나이: {profile.age_years}세
    - BCS 점수: {profile.bcs_score}
    - 이동 가능 수준: {profile.mobility_level}
    - 관절 문제 여부: {profile.joint_issue}
    - 이동 유형: {profile.mobility_scope}
    - 선호 장소 유형: {', '.join(profile.preferred_places_types)}
    - 산책 목표: {profile.walk_goal}
"""

    if routes:
        route = routes[-1]
        result += f"""
    최근 추천 경로: 
    - 경로 이름: {route.route_name}
    - 장소 유형: {route.place_type}
    - 총 거리: {route.total_distance_km}km
    - 예상 산책 시간: {route.estimated_minutes}분
    - 안전 점수: {route.safety_score}
    - 추천 이유: {route.recommendation_reason}
"""

    return result.strip()


@tool
def search_walk_routes(
    mobility_scope: str,
    preferred_place_types: Optional[List[str]] = None,    
) -> str:
    """저장된 반려견 프로필을 바탕으로 상위 후보 3개를 반환하는 함수입니다. 

    이 함수는 mock DB에 저장된 산책 코스들 중에서
    이동 방식(mobility_scope)과 선호 장소 유형(preferred_place_types)에 맞는 후보를 필터링한 뒤,
    노면 상태, 경사도, 조명 수준, 혼잡도를 바탕으로 내부 점수를 계산하여
    우선순위가 높은 후보 3개를 문자열로 정리해 반환합니다.
    
    Args:
        mobility_scope: 이동 유형 ("walk"|"drive")
        preferred_place_types: 선호 장소 유형 목록

    Returns:
        str: 추천 산책 경로 후보 목록 문자열
    """

    store = get_store()
    routes = store.get("walk_routes", [])

    filtered_routes = []

    for route in routes:
        if route.mobility_scope != mobility_scope:
            continue
        if preferred_place_types and route.place_type not in preferred_place_types:
            continue

        candidate_score = (
            route.surface_quality * 3
            + (6 - route.slope_level) * 4
            + route.lighting_level * 2
            + (6 - route.crowdedness_level) * 2
        )

        filtered_routes.append((route, candidate_score))


    if not filtered_routes:
        return "조건에 맞는 산책 경로 후보가 없습니다."
    
    filtered_routes.sort(key=lambda x: x[1], reverse=True)
    top_routes = filtered_routes[:3]

    result = "추천 산책 경로 후보 목록\n"
    for idx, item in enumerate(top_routes, start=1):
        route_obj = item[0]
        result += (
            f"{idx}. {route_obj.route_name}\n"
            f"   - 장소 유형: {route_obj.place_type}\n"
            f"   - 총 거리: {route_obj.total_distance_km}km\n"
            f"   - 노면 상태: {route_obj.surface_quality}\n"
            f"   - 경사도: {route_obj.slope_level}\n"
            f"   - 조명 수준: {route_obj.lighting_level}\n"
            f"   - 혼잡도: {route_obj.crowdedness_level}\n"
            f"   - 이동 유형: {route_obj.mobility_scope}\n"
        )

    return result.strip()


@tool
def estimate_walk_duration(
    total_distance_km: float,
    dog_size: str,
    age_years: int,
    mobility_level: int,
    joint_issue: int,
) -> int:
    """반려견의 상태와 산책 거리 기준으로 예상 산책 시간을 계산하는 함수입니다.

    강아지의 크기, 나이, 이동 가능 수준, 관절 문제 여부를 반영하여
    기본 이동 속도를 조정한 뒤, 총 산책 거리를 기준으로 예상 소요 시간을 분 단위로 계산합니다.

    기본 속도 기준:
    - 소형견: 3.5 km/h
    - 중형견: 4.0 km/h
    - 대형견: 4.5 km/h

    이동 제한, 관절 문제, 고령 여부가 있으면 속도를 낮춰 계산합니다.

    Args:
        total_distance_km: 총 산책 거리(km)
        dog_size: 강아지 크기 (대형견, 중형견, 소형견)
        age_years: 강아지 나이
        mobility_level: 이동 가능 수준
            - 0: normal
            - 1: slightly_limited
            - 2: limited
        joint_issue: 관절 문제 유무 (0: 없음, 1: 있음)
    
    Returns:
        int: 예상 산책 시간 (분)

    Raises:
        ValueError: total_distance_km가 0 이하인 경우 발생합니다.

    """

    if total_distance_km <= 0:
        raise ValueError("total_distance_km는 0보다 커야 합니다.")
    
    if dog_size == "소형견":
        speed_kmh = 3.5
    elif dog_size == "중형견":
        speed_kmh = 4.0
    elif dog_size == "대형견":
        speed_kmh = 4.5
    else:
        speed_kmh = 4.0

    if mobility_level == 1:
        speed_kmh -= 0.7
    elif mobility_level == 2:
        speed_kmh -= 1.2
    
    if joint_issue == 1:
        speed_kmh -= 0.5

    if age_years >= 10:
        speed_kmh -= 0.5
    
    speed_kmh = max(speed_kmh, 1.5)

    estimate_walk_duration = int((total_distance_km / speed_kmh) * 60)

    return estimate_walk_duration


@tool
def get_realtime_weather() -> str:
    """현재 날씨 데이터를 mock_DB에서 가져옵니다. set_mock_weather()로 설정된 mock 시나리오를 기반으로 동작합니다.

    Returns:
        str: 현재 날씨 정보를 문자열 형태로 반환합니다.
    """

    weather_data = get_current_weather()

    return f"""현재 날씨 정보
            - 기온: {weather_data["temperature"]}도
            - 날씨 상태: {weather_data["weather_condition"]}
            - 강수 확률: {weather_data["precipitation_prob"]}%
            - 미세먼지 수치: {weather_data["air_quality"]}
            """

@tool
def set_mock_weather(weather_scenario: str)-> str:
    """사용자 발화에 맞게 mock 날씨 시나리오를 설정하는 함수입니다.

    지원하는 시나리오:
    - sunny_perfect
    - heavy_rain
    - bad_dust
    - scorching_heat
    - snowing
    - chilly_wind
    - rain_and_bad_dust

    Args:
        weather_scenario: 설정할 mock 날씨 시나리오 이름

    Returns:
        str: 설정 완료 메시지

    Raises:
        ValueError: 지원하지 않는 시나리오 이름이 들어온 경우 발생합니다.
    """

    store=get_store()

    valid_ids = {
        "sunny_perfect",
        "heavy_rain",
        "bad_dust",
        "scorching_heat",
        "snowing",
        "chilly_wind",
        "rain_and_bad_dust"
    }

    if weather_scenario not in valid_ids:
        raise ValueError(f'지원하지 않는 날씨 시나리오입니다: {weather_scenario}')
    
    store['current_weather_id'] = weather_scenario
    return f'현재 날씨가 {weather_scenario}로 설정되었습니다.'


"""
@tool
def check_weather_and_air_quality()-> CurrentWeatherInfo:

    현재 안양시의 실시간 날씨, 기온, 강수 확률, 미세먼지 정보를 조회해서 실외 산책이 가능한지 파악해주는 함수입니다.

    Args:
        temperature: 현재 안양시 기온 (섭씨)
            - 0도 미만: 영하 (산책 시간 단축, 보온 필요)
            - 0도 ~ 10도 미만: 쌀쌀함 (가벼운 외투 필요)
            - 10도 ~ 25도 미만: 적당함 (야외 산책 최적)
            - 25도 ~30도 미만: 더움 (수분 보충 필수)
            - 30도 이상: 폭염 (한낮 야외 산책 위험)
        weather_condition: 실시간 날씨 (비, 맑음, 흐림, 눈)
        precipitation_prob: 강수 확률 (%) (0~100)
        air_quality_value: 미세먼지 수치 (PM10 농도 기준)
            - 0 ~ 30: 좋음
            - 31 ~ 80: 보통
            - 81 ~ 150: 나쁨
            - 150 이상: 매우 나쁨

    Returns:
        CurrentWeatherInfo: 날씨 상태 분석 결과와 실외 산책 적합 여부를 포함한 모델
    

    weather_data = get_current_weather()
    temperature = weather_data["temperature"]
    weather_condition = weather_data["weather_condition"]
    precipitation_prob = weather_data["precipitation_prob"]
    air_quality_value: int = weather_data["air_quality"]

    # 2. 기온 평가
    if temperature < 0: temp_status = "영하"
    elif 0 <= temperature < 10: temp_status = "쌀쌀함"
    elif 10 <= temperature < 25: temp_status = "적당함"
    elif 25 <= temperature < 30: temp_status = "더움"
    else: temp_status = "폭염"

    # 3. 미세먼지 평가
    if air_quality_value <= 30: aq_status = "좋음"
    elif air_quality_value <= 80: aq_status = "보통"
    elif air_quality_value <= 150: aq_status = "나쁨"
    else: aq_status = "매우 나쁨"

    # 4. 야외 산책 가능 여부 판단
    is_outdoor_recommended = True
    if precipitation_prob >= 60 or weather_condition in ["비", "눈"] or air_quality_value > 80 or temperature >= 30 or temperature < -5:
        is_outdoor_recommended = False

    # 5. 최종 모델 객체 생성 후 반환
    weather_info = CurrentWeatherInfo(
        temperature=temperature,
        temp_status=temp_status,
        weather_condition=weather_condition,
        precipitation_prob=precipitation_prob,
        air_quality_value=air_quality_value,
        air_quality_status=aq_status,
        is_outdoor_recommended=is_outdoor_recommended,
        weather_warning=f"{temp_status} / {aq_status}",
        recommendation_msg="야외 산책 가능" if is_outdoor_recommended else "실내 산책 권장"
    )
    
    return weather_info    
"""