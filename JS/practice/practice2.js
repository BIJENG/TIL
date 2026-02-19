// 점수 배열을 입력 받아서, 평균을 반환하는 함수

function getAverage(scores) {
    let result = 0;
    for(i = 0; i < scores.length; i++) {
        result = result + scores[i];
    }
    return result / scores.length;
}

console.log(getAverage([80, 90, 75, 83]))