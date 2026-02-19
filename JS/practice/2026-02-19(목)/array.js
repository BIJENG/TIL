// 배열
let numbers = [10, 20, 30, 40, 50];

console.log(numbers[0]); // 10
console.log(numbers[1]); // 20
console.log(numbers[2]); // 30
console.log(numbers[3]); // 40
console.log(numbers[4]); // 50


for (let i = 0; i < numbers.length; i++) {
    console.log(numbers[i]);
}

for (const num of numbers) {
    console.log(num);
}

for (const [i, num] of numbers.entries()) {
    console.log(i, num);
}