document.addEventListener('DOMContentLoaded', () => {
    const startGameButton = document.getElementById('startGame');
    const chatContainer = document.getElementById('chatContainer');
    const messagesDiv = document.getElementById('messages');
    const userInput = document.getElementById('userInput');
    const submitChoiceButton = document.getElementById('submitChoice');
    const countdownDiv = document.getElementById('countdown');
    const restartButton = document.getElementById('restart');
    const exitButton = document.getElementById('exit');
    let userHearts = 3;
    let pcHearts = 3;
    let countdownTimer;

    function updateHearts() {
        document.getElementById('userHearts').textContent = '💖'.repeat(userHearts);
        document.getElementById('pcHearts').textContent = '💖'.repeat(pcHearts);
    }

    function resetGame() {
        clearInterval(countdownTimer);
        userHearts = 3;
        pcHearts = 3;
        updateHearts();
        messagesDiv.innerHTML = '';
        countdownDiv.textContent = '';
        startGameButton.style.display = 'block';
        chatContainer.style.display = 'none';
        restartButton.style.display = 'none';
        exitButton.style.display = 'none';
        submitChoiceButton.disabled = false;
    }

    startGameButton.addEventListener('click', () => {
        startGameButton.style.display = 'none';
        chatContainer.style.display = 'block';
        addMessage("게임을 시작하겠습니다.");
        startCountdown();
    });

    submitChoiceButton.addEventListener('click', () => {
        if (validateInput()) {
            processChoice(userInput.value);
        }
    });

    userInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter' && validateInput()) {
            processChoice(userInput.value);
        }
    });

    restartButton.addEventListener('click', resetGame);
    exitButton.addEventListener('click', () => window.location.href = '/');

    function addMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    function startCountdown() {
        let timeLeft = 5;
        countdownDiv.textContent = timeLeft;
        userInput.disabled = false;
        userInput.focus();

        countdownTimer = setInterval(() => {
            timeLeft--;
            countdownDiv.textContent = timeLeft;
            if (timeLeft === 0) {
                clearInterval(countdownTimer);
                countdownDiv.textContent = '땡!';
                userInput.disabled = true;
                processChoice(userInput.value || getRandomChoice());
            }
        }, 1000);
    }

    function getRandomChoice() {
        const choices = ['가위', '바위', '보'];
        return choices[Math.floor(Math.random() * choices.length)];
    }

    function validateInput() {
        if (!['가위', '바위', '보'].includes(userInput.value)) {
            alert('가위, 바위, 보 중 하나를 입력하세요.');
            userInput.value = '';
            return false;
        }
        return true;
    }

    function processChoice(choice) {
        // 선택이 유효하지 않으면 오류 메시지를 표시하고, 함수를 종료합니다.
        if (!['가위', '바위', '보'].includes(choice)) {
            alert('가위, 바위, 보 중 하나를 입력하세요.');
            userInput.value = '';
            userInput.focus(); // 사용자가 다시 입력할 수 있도록 포커스를 줍니다.
            return; // 함수를 여기서 종료합니다. 더 이상의 타이머 로직은 실행되지 않습니다.
        }
        clearInterval(countdownTimer);
        const pcChoice = getRandomChoice();
        const result = determineWinner(choice, pcChoice);
        addMessage(`당신의 선택: ${choice}, PC의 선택: ${pcChoice}, ${result}`);
        if (result === '패배!') userHearts--;
        if (result === '승리!') pcHearts--;
        updateHearts();
        checkGameOver();
        userInput.value = ''; // 입력창 초기화
    }

    function determineWinner(user, pc) {
        if (user === pc) return '무승부';
        if ((user === '가위' && pc === '보') || (user === '바위' && pc === '가위') || (user === '보' && pc === '바위')) return '승리!';
        return '패배!';
    }

    function checkGameOver() {
        if (userHearts === 0 || pcHearts === 0) {
            addMessage(userHearts > pcHearts ? '축하합니다, 승리하셨습니다!' : '아쉽지만, 패배하셨습니다.');
            restartButton.style.display = 'inline';
            exitButton.style.display = 'inline';
            userInput.disabled = true;
            submitChoiceButton.disabled = true;
            clearInterval(countdownTimer); // 게임 오버 시 타이머를 멈춥니다.
        } else {
            userInput.disabled = false; // 사용자 입력을 다시 활성화합니다.
            setTimeout(startCountdown, 1000); // 다음 라운드 준비
        }
    }
    

    updateHearts(); // 초기 하트 상태 업데이트
});
