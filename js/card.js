const cardContainer = document.getElementById('card-container'); // 카드들을 담을 컨테이너를 가져옴

// 새로운 카드 요소를 생성하는 함수
function createCard(index) {
    const card = document.createElement('div'); // 새로운 div 요소 생성
    card.classList.add('card'); // 'card' 클래스 추가

    const img = document.createElement('img'); // 새로운 img 요소 생성
    img.src = '../img/main_card.svg'; // 이미지 경로 설정 (실제 이미지 경로로 변경 필요)
    card.appendChild(img); // img 요소를 card 요소에 추가
    
    // 카드를 중앙으로 뒤집는 클릭 이벤트 추가
    card.addEventListener('click', () => flipCard(card));
    
    // 카드를 부채꼴 모양으로 배치하기 위해 각도를 계산
    const angle = (index - 2.5) * 10; // 중앙을 기준으로 각도를 계산 (각도를 10도로 설정)
    const offset = (index - 2) * 40; // 카드를 겹치게 배치하기 위해 X축 오프셋 설정
    card.style.transform = `rotate(${angle}deg) translate(${offset}px, 0)`; // 회전하고 X축으로 이동
    
    return card; // 생성된 카드 요소 반환
}

// 선택된 카드를 중앙으로 뒤집는 함수
function flipCard(selectedCard) {
    const cards = cardContainer.querySelectorAll('.card'); // 모든 카드 요소를 가져옴
    cards.forEach(card => {
        if (card === selectedCard) { // 클릭된 카드인 경우
            card.style.zIndex = 10; // z-index를 높여 가장 위로 보이게 함
            card.style.transform = 'rotate(0deg) translate(-50%, -50%)'; // 중앙으로 이동하고 확대
            card.style.left = '50%'; // 수평 중앙 정렬
            card.style.top = '50%'; // 수직 중앙 정렬
        } else { // 클릭되지 않은 카드인 경우
            card.style.opacity = 0; // 투명하게 만듦
        }
    });
}

// 컨테이너에 5개의 카드를 추가
for (let i = 0; i < 6; i++) {
    const card = createCard(i); // 새로운 카드 생성
    cardContainer.appendChild(card); // 카드 컨테이너에 카드 추가
}
