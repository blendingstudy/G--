function flipCard(index) {
    fetch('/Flip_the_card_play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `index=${index}`
    }).then(response => response.json())
      .then(data => {
        console.log(data);  // 데이터 구조 확인
        if (data.success) {
            alert(data.message);  // 여기서 undefined가 나오는지 확인
            if (data.cards) {
                data.cards.forEach(idx => {
                    document.getElementsByClassName('card')[idx].classList.add('flipped');
                });
            }
            if (data.time) {
                alert(`게임 성공! 걸린 시간: ${data.time}초`);
            }
        } else {
            if (data.index1 !== undefined) {
                setTimeout(() => {
                    const cards = document.getElementsByClassName('card');
                    cards[data.index1].classList.remove('flipped');
                    cards[data.index2].classList.remove('flipped');
                }, 1000);
            }
            alert(data.message);  // 이 경고에서도 undefined가 나온다면 data.message가 문제
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}
