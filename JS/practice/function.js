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