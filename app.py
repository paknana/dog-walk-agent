from agents import get_dog_walk_agent

from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()

model = ChatGroq(
    model= "openai/gpt-oss-20b",
    temperature=0.3
)

walk_agent = get_dog_walk_agent(model)

result = walk_agent.invoke({
    "messages" : [
        {
            'role': 'user',
            'content': '오늘 밖에 비가 엄청 많이 오고 미세먼지도 나쁘다며? 우리 강아지는 2살 웰시코기(중형견) 12kg이고 엄청 건강해서(BCS 5, 관절 문제 없음) 에너지를 쫙 빼줘야 해. 차(drive) 타고 이동할 건데, 이런 날씨에도 안전하게 오랫동안 산책할 수 있는 곳을 이유랑 같이 설명해 줘.' 
        }
    ]
})

print(result['messages'][-1].content)