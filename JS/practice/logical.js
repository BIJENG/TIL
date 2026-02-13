// 논리 연산자: 여러 조건의 조합

let isAdult = true;
let hasTicket = false;

let canPass = isAdult && hasTicket; // 논리 AND
console.log(canPass); // false

canPass = isAdult || hasTicket; // 논리 OR
console.log(canPass); // true

