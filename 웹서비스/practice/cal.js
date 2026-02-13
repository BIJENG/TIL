// 1. 변수를 직접 선언 
let num1 = 10;           
let operator = "/";      // +, -, *, / 중 선택
let num2 = 5;            

let result;

// 2. 연산 처리 로직 
if (operator === "+") {
    result = num1 + num2;
} else if (operator === "-") {
    result = num1 - num2;
} else if (operator === "*") {
    result = num1 * num2;
} else if (operator === "/") {
    if (num2 !== 0) {
        result = num1 / num2;
    } else {
        result = "0으로 나눌 수 없습니다.";
    }
} else {
    result = "잘못된 연산자입니다.";
}

// 3. 결과 출력 (터미널 확인용)
console.log("계산 결과: " + result);