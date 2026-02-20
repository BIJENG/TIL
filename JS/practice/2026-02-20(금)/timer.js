// Timer API = 시간을 다루는 기능

// setTimeout(함수, 시간) : 일정 시간이 지난 후 함수를 실행
// setInterval(함수, 시간) : 일정 시간마다 함수를 반복 실행
// clearTimeout(타이머ID) : setTimeout으로 설정한 타이머를 취소
// clearInterval(타이머ID) : setInterval로 설정한 타이머를 취소




const timerId = setInterval(() => console.log("1초마다 실행"), 1000);
setTimeout(() => clearInterval(timerId), 5000);


