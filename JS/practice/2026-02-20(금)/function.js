// 함수(Function)

function add(num1, num2) {
    return num1 + num2;
}

function wrapper(func) {
    const result = func(1, 2);
    console.log("Wrapper Result: " + result);
}

// 반환(return) = 호출부로 값을 되돌려주는 것

// let result = add(1, 2);
console.log(add); 



const func = add; // 함수도 값이므로 변수에 할당 가능
console.log(func);
console.log(func(1, 2)); // 3

// print라는 새로운 함수 정의
function print(message) {
    console.log(message);
}

const printResult = print("Hello, World!"); // Hello, World!
console.log(printResult); // undefined (print 함수는 반환값이 없으므로 undefined를 반환)