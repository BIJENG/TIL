# Llama 추론 프로그램
import json
import redis
from llama_cpp import Llama

# redis = (비유) 엄청 빠른 초소형 데이터베이스 (key:value)
redis_client = redis.from_url("redis://redis:6379", decode_responses=True)

llm = Llama(
    model_path="./models/Llama-3.2-1B-Instruct-Q4_K_M.gguf",
    n_ctx=4096,
    n_threads=2,
    verbose=False,
    chat_format="llama-3",
)

SYSTEM_PROMPT = (
    "You are a helpful assistant. "
    "Always answer in Korean. " # 한국어로 대답하라고 명시
    "Keep it concise."
)

def create_response(question: str):
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        max_tokens=256,
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]

def run():
    while True:
        # [1] Queue에서 job을 deque
        _, job_data = redis_client.brpop("inference_queue")
        job: dict = json.loads(job_data)

        # [2] 추론
        answer = create_response(question=job["question"])

        # [3] 결과를 API 서버로 publish
        channel = f"result:{job['id']}"
        redis_client.publish(channel, answer)
        

# python main.py 로 실행되었을 때만, run()을 호출
if __name__ == "__main__":
    run()