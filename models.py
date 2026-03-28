from typing import List, Literal
from pydantic import BaseModel, Field

class DogWalkProfile(BaseModel):
    dog_size: str = Field(description='강아지 크기 [소형견, 중형견, 대형견]')
    weight_kg: float = Field(description='강아지 체중(kg)')
    age_years: int = Field(description='강아지 나이 (살)')
    bcs_score: int = Field(description='강아지 비만도 점수')
    mobility_level: int = Field(description='이동 가능 정도 (0: 정상, 1: 약간 제한, 2: 매우 제한적)')
    joint_issue: int = Field(description='관절 문제 여부 (0: 없음, 1: 있음)')
    mobility_scope: str = Field(description='이동 유형 ("drive" | "walk")')
    preferred_places_types: List[str] = Field(description='선호 장소 유형 (하천, 등산로, 근린공원, 실내 복합물, 주택가 골목)')
    walk_goal: str = Field(description='산책 목표 (예: 배변 위주, 운동 위주, 안전 위주)')

class DogWalkRoute(BaseModel):
    route_name: str = Field(description= "산책 경로의 구체적인 이름")
    place_type: str = Field(description= "장소의 카테고리 (하천, 등산로, 근린공원, 실내 복합물, 주택가 골목, 반려견 놀이터)")
    total_distance_km: float = Field(description= "총 산책 거리 (km)") 
    surface_quality: int = Field(description= "노면 포장 상태 (1~5점, 5: 흙길/우레탄 등 관절에 가장 좋음)")
    slope_level: int = Field(description= "경사도 (1~5점, 1: 평지, 5: 매우 가파름)")
    lighting_level: int = Field(description= "가로등 및 조명 수준 (1~5점, 5: 매우 밝음)")
    crowdedness_level: int = Field(description= "인구 및 자전거 밀집도 (1~5점, 5: 매우 혼잡함)")

    mobility_scope: str = Field(description='이동 유형 ("drive" | "walk")')

    recommendation_reason: str = Field(default="", description= "이 경로를 추천하는 이유")
    estimated_minutes: int = Field(default=0, description='예측 시간 (분)') 
    safety_score: int = Field(default=0, description='경로 안전성 점수')

class CurrentWeatherInfo(BaseModel):
    temperature: float = Field(description= '기온 (섭씨)')
    weather_condition: str = Field(description= '날씨 상태 (영하/쌀쌀함/적당함/더움/폭염)')
    precipitation_prob: float = Field(description= '강수 확률 (%)')
    is_outdoor_recommended : bool = Field(description='야외 산책 권장 여부 (True면 야외, False면 실내 추천)')
    temp_status: str = Field(description= '기온 상태 (영하/쌀쌀함/적당함/더움/폭염)')
    air_quality_value: int = Field(description= "미세먼지 수치")
    air_quality_status: str = Field(description='미세먼지 상태 (좋음/보통/나쁨/매우 나쁨)')
    weather_warning: str = Field(default ="", description= "기온 및 미세먼지에 따른 반려견 건강 주의사항")
    recommendation_msg: str = Field(default="", description= "최종 행동 가이드 메시지")