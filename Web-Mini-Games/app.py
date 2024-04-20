from flask import Flask, render_template, request, jsonify, session
from flask_session import Session  # 세션 확장 기능을 사용하기 위함
import random, time
from random import shuffle


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 실제 사용 시 안전한 키로 변경
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    session['user_hearts'] = 3  # 유저 하트 초기화
    session['pc_hearts'] = 3    # PC 하트 초기화

    return render_template('index.html')


#############  가위바위보 게임  ##############################

@app.route('/Rock_Paper_Scissors')
def game():
    # 게임 페이지를 로드할 때 유저와 PC의 하트 상태를 초기화하지 않습니다.
    return render_template('Games/Rock_Paper_Scissors.html', user_hearts=session.get('user_hearts', 3), pc_hearts=session.get('pc_hearts', 3))

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
    




### 같은 그림의 카드 맞추기 게임 참고사이트(https://codethem.tistory.com/189)
## F5 누르면 게임 실행

# import turtle as t
# import random
# import time

# # 클릭한 이미지 찾기 함수
# def find_card(x,y):
#     min_idx = 0
#     min_dis = 100

#     for i in range(16):
#         distance = turtles[i].distance(x,y)
#         if distance < min_dis:
#             min_dis = distance      # 우리가 클릭한 카드의 위치
#             min_idx = i             # 그 위치를 min_idx 담음
#     return min_idx

# # 정답오답 함수
# def score_update(m):
#     score_pen.clear()       # 클리어 스코프로 기존 값을 지워주고
#     score_pen.write(f"{m}   {score}점/{attempt}번 시도", False, "center", ("", 15))
#     # f스트링을 사용해서 매개 변수로 들어오는 m(메세지) 매개변수를 표시하고, 점수와 시도 횟수 표기

# # 성공인지 실패인지 확인하는 함수
# def result(m):
#     t.goto(0, -60)              # 게임 오버 텍스트를 0,-60위치에 배치
#     t.write(m, False, "center", ("", 30, "bold"))

# def play(x, y):
#     global click_num
#     global first_pick
#     global second_pick
#     global attempt
#     global score

#     if attempt == 12:               # 시도횟수가 12번이면
#         result("Game Over")

#     else:
#         click_num += 1
#         # 클릭한 이미지 찾기
#         card_idx = find_card(x,y)
#         turtles[card_idx].shape(img_list[card_idx])

#         if click_num == 1:
#             first_pick = card_idx
#         elif click_num == 2:
#             second_pick = card_idx
#             click_num = 0
#             attempt += 1

#             if img_list[first_pick]  == img_list[second_pick]:
#                 score += 1
#                 # 정답
#                 score_update("정답")
#                 if score == 8:
#                     result("Success")
#             else:
#                 # 오답
#                 score_update("오답")
#                 # 오답인 경우 이미지가 다시 숨겨지도록 구현
#                 turtles[first_pick].shape(defalut_img)
#                 turtles[second_pick].shape(defalut_img)





# t.bgcolor("pink")
# t.setup(700,700)
# t.up()
# t.ht()
# t.goto(0,280)
# t.write("카드 매칭 게임", False, "center", ("", 30, "bold"))

# # 점수 펜 객체 생성
# score_pen = t.Turtle()  # 터틀객체 생성
# score_pen.up()          # 펜을 들여올려주고
# score_pen.ht()          # 하이드 터틀로 숨김
# score_pen.goto(0, 230)  # 제목보다 조금 아래쪽에 글자를 표시


# # 터틀 객체 생성
# turtles = []
# pos_x = [-210, -70, 70, 210]
# pos_y = [-250, -110, 30, 170]

# for x in range(4):
#     for y in range(4):
#         new_turtle = t.Turtle()
#         new_turtle.up()
#         new_turtle.color("pink")
#         new_turtle.speed(0)
#         new_turtle.goto(pos_x[x], pos_y[y])
#         turtles.append(new_turtle)

# defalut_img = 'Web-Mini-Games\static\images\Flip_the_card\default_img.gif'
# t.addshape(defalut_img)


# # 준비된 이미지를 img를 img_list에 2번씩 삽입
# img_list = []
# for i in range(8):
#     img = f"Web-Mini-Games\static\images\Flip_the_card\img{i}.gif"
#     t.addshape(img)
#     img_list.append(img)
#     img_list.append(img)

# # 준비된 이미지를 img를 랜덤으로 섞음
# random.shuffle(img_list)

# # 준비된 이미지를 화면에 일정히 배치 한 후 
# for i in range(16):
#     turtles[i].shape(img_list[i])

# # 3초간 쉬었다가
# time.sleep(3)

# # 카드 뒷면으로 뒤집음
# for i in range(16):
#     turtles[i].shape(defalut_img)


# click_num = 0           # 클릭 횟수(매 2회 클릭마다 정답 체크)
# score = 0               # 점수 초기값
# attempt = 0             # 시도한 횟수
# first_pick = ""         # 첫 번째 클릭한 이미지
# second_pick = ""       # 두 번째 클릭한 이미지


# t.onscreenclick(play)   # t.onscreenclick(함수) 
# t.done()                # 프로그램 창이 자동으로 닫히지 않게 해줌


### 같은 그림의 카드 맞추기 게임 참고사이트(https://codethem.tistory.com/189)
## 웹으로 변경한 코드

def init_game():
    images = ['img0.png', 'img1.png', 'img2.png', 'img3.png', 'img4.png', 'img5.png', 'img6.png', 'img7.png'] * 2
    random.shuffle(images)
    session['cards'] = images
    session['flipped_indices'] = []
    session['score'] = 0

@app.route('/flip')
def flip_card():
    init_game()  # 게임 초기화
    return render_template('Games/Flip_the_card.html', cards=session['cards'])

@app.route('/flip_card_play', methods=['POST'])
def flip_card_play():
    index = int(request.form['index'])
    if len(session['flipped_indices']) == 2:
        session['flipped_indices'] = []

    if index not in session['flipped_indices']:
        session['flipped_indices'].append(index)

    if len(session['flipped_indices']) == 2:
        idx1, idx2 = session['flipped_indices']
        if session['cards'][idx1] == session['cards'][idx2]:
            session['score'] += 1
            message = "정답!"
            success = True
        else:
            message = "오답!"
            success = False
            session['flipped_indices'] = []  # 불일치 시 카드 인덱스 리셋
        return jsonify(success=success, message=message, cards=session['flipped_indices'])
    return jsonify(success=False, message="카드를 뒤집으세요")

@app.route('/dino')
def dino():
    return render_template('Games/dino-t-rex.html')


if __name__ == '__main__':
    app.run(debug=False)
