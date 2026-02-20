// Fetch API = 서버에 HTTP 요청을 보내는 API

fetch("https://jsonplaceholder.typicode.com/posts");
// fetch() 함수는 Promise 객체를 반환한다. 따라서 then() 메서드를 사용하여 응답을 처리할 수 있다.


//GET 요청을 보내고 응답을 처리하는 예시
// fetch("https://jsonplaceholder.typicode.com/posts")
//     .then(response => response.json())
//     .then(data => console.log(data));
//     // 응답이 성공적으로 도착했을 때 실행되는 콜백 함수


// POST 요청을 보내는 예시
fetch("https://jsonplaceholder.typicode.com/posts", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({title: "foo", body: "Body"})
})
    .then(response => response.json())
    .then(data => console.log(data));