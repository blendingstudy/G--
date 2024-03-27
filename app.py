from flask import  Flask, render_template, request, jsonify
import threading
import time
import configparser
from flask_cors import CORS
from openai.error import OpenAIError, RateLimitError

import openai  # OpenAI 라이브러리 import

app = Flask(__name__)
CORS(app)

# 상황극 시나리오와 주제를 저장할 전역 변수
current_scenario = "시나리오를 기다리고 있습니다..."
scenario_topic = ""

# OpenAI API 키 설정
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['openai']['api_key']

@app.route('/')
def home():
    return render_template('index.html')

def generate_scenario_openai(topic):
    try:
        # 챗 모델을 사용하여 시나리오 생성
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "다음은 주제에 기반한 상황극 시나리오입니다:"},
                {"role": "user", "content": topic}
            ]
        )
        # 여기서 첫 번째 응답 메시지의 내용을 반환합니다.
        return response.choices[0].message['content'].strip()
    except RateLimitError:
        # 정확한 대기 시간을 알 수 없는 경우, 사용자에게 일반적인 안내 메시지를 제공
        return "요청 한도에 도달했습니다. 잠시 후 다시 시도해주세요."
    except OpenAIError as e:
        # 다른 OpenAI 관련 에러 처리
        print(f"OpenAI 에러 발생: {e}")
        return "시나리오 생성 중 오류가 발생했습니다."
    except Exception as e:
        print(f"일반 에러 발생: {e}")
        return "알 수 없는 오류가 발생했습니다."


@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data['topic']
    scenario = generate_scenario_openai(topic)
    return jsonify(scenario=scenario)

if __name__ == "__main__":
    app.run(debug=True)