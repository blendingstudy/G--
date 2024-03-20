from flask import Flask, request, jsonify, render_template
import configparser
import openai

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['openai']['api_key']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['content']  # JSON 데이터로부터 사용자 입력을 받음
    response = generate_response(user_input)
    return jsonify({"answer": response})

def generate_response(user_input):
    try:
        # 챗 모델을 사용하여 API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I couldn't process your request."

if __name__ == '__main__':
    app.run(debug=True)
