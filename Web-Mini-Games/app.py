from flask import Flask, render_template, request, jsonify, session
from flask_session import Session  # 세션 확장 기능을 사용하기 위함
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 실제 사용 시 안전한 키로 변경
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    session['user_hearts'] = 3  # 유저 하트 초기화
    session['pc_hearts'] = 3    # PC 하트 초기화
    return render_template('index.html')

@app.route('/Rock_Paper_Scissors')
def game():
    # 게임 페이지를 로드할 때 유저와 PC의 하트 상태를 초기화하지 않습니다.
    return render_template('Rock_Paper_Scissors.html', user_hearts=session.get('user_hearts', 3), pc_hearts=session.get('pc_hearts', 3))

@app.route('/play', methods=['POST'])
def play():
    user_choice = request.json.get('choice', '').lower()
    if not user_choice:
        # 5초 동안 대기한 후 사용자 입력이 없으면 랜덤 선택
        user_choice = random.choice(['가위', '바위', '보'])
    computer_choice = random.choice(['가위', '바위', '보'])
    result, user_wins = determine_winner(user_choice, computer_choice)

    # 하트 감소 로직
    if result == '패배!':
        session['user_hearts'] -= 1
    elif result == '승리!':
        session['pc_hearts'] -= 1

    return jsonify(result=result, user_choice=user_choice, computer_choice=computer_choice, user_hearts=session['user_hearts'], pc_hearts=session['pc_hearts'], user_wins=user_wins)

def determine_winner(user, computer):
    if user == computer:
        return ('무승부', None)
    elif (user == '가위' and computer == '보') or (user == '바위' and computer == '가위') or (user == '보' and computer == '바위'):
        return ('승리!', True)
    else:
        return ('패배!', False)

if __name__ == '__main__':
    app.run(debug=True)