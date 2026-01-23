# 📅 [TIL] OpenCV 모폴로지 연산 & EasyOCR 텍스트 추출

## 1. 노이즈 제거와 형태 보정 (Morphology)
이미지 처리에서 가장 기초가 되는 **노이즈 제거** 기법입니다. '커널(Kernel)'이라는 작은 필터를 사용해 이미지를 깎거나(침식) 부풀리는(팽창) 원리입니다.

### 핵심 개념 정리

| 연산 | 수식 (Math) | 설명 | 효과 |
| :--- | :--- | :--- | :--- |
| **Opening (열기)** | $$A \circ B = (A \ominus B) \oplus B$$ | **침식($\ominus$)** 후 **팽창($\oplus$)** | 배경의 **자잘한 노이즈(흰 점) 제거**. 좁은 연결 부위를 끊어냄. |
| **Closing (닫기)** | $$A \bullet B = (A \oplus B) \ominus B$$ | **팽창($\oplus$)** 후 **침식($\ominus$)** | 물체 내부의 **작은 구멍(검은 점) 메우기**. 끊어진 부분을 연결함. |

> **💡 쉽게 기억하기:**
> * **Opening:** 뚜껑을 연다 → 겉(배경)을 청소한다.
> * **Closing:** 뚜껑을 닫는다 → 안(내부)을 채운다.

### 🐍 실습 코드 (Python)
배경의 먼지를 없애고(Opening), 도넛 내부의 구멍을 메우는(Closing) 예제입니다.

```python
import cv2
import numpy as np

# 커널 생성 (지우개/붓 역할)
kernel = np.ones((3, 3), np.uint8)

# 1. Opening: 배경 노이즈 제거
opening = cv2.morphologyEx(noisy_image, cv2.MORPH_OPEN, kernel)

# 2. Closing: 내부 구멍 채우기
closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
```

<!-- 
깃허브에 올릴 때, 실행 결과 스크린샷이 있다면 아래 주석을 풀고 이미지 경로를 넣어주세요.
![모폴로지 결과 이미지](./images/morphology_result.png) 
-->

---

## 2. OCR 인식률 높이기 (Preprocessing)
`EasyOCR`이나 `Tesseract` 같은 OCR 도구가 글자를 잘 읽게 하려면 **전처리(Preprocessing)**가 필수입니다. 단순히 흑백으로 바꾸는 것보다 더 나은 기법들을 배웠습니다.

### 🛠️ 핵심 전처리 3단계

1. **Upscaling (확대):**
    * 글자가 너무 작으면 뭉개져 보입니다.
    * `INTER_CUBIC` 보간법을 사용하여 부드럽게 2배 확대합니다.
2. **Grayscale (회색조):**
    * 컬러 정보는 글자 인식에 방해가 될 수 있어 제거합니다.
3. **CLAHE (대비 제한 적응형 히스토그램 평활화):**
    * 일반적인 이진화(`Threshold`)보다 강력합니다.
    * 이미지의 밝기가 불균일할 때, 국소적으로 대비를 높여 글자를 뚜렷하게 만듭니다.

### 🐍 실습 코드 (Advanced Preprocessing)

```python
# 1. 이미지 2배 확대 (Cubic 보간법 사용)
img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# 2. 흑백 변환
gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

# 3. CLAHE 적용 (선명도 개선)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
enhanced_img = clahe.apply(gray)
```

---

## 3. 📂 [Project] 다중 이미지 텍스트 병합기
여러 장의 문서 이미지(`doc1.jpg` ~ `doc5.jpg`)를 읽어 하나의 텍스트 파일(`merged_text.txt`)로 합치는 과제입니다.

### 전체 코드 (Optimized)

```python
import easyocr
import cv2
import numpy as np

# 1. 파일 경로 설정
image_paths = [f'./doc/doc{i}.jpg' for i in range(1, 6)]

# 2. OCR 리더기 생성 (한국어, 영어)
reader = easyocr.Reader(['ko', 'en'])

extracted_texts = []

print("텍스트 추출을 시작합니다...")

for path in image_paths:
    img = cv2.imread(path)
    if img is None: continue
    
    # [핵심] 전처리: 확대 -> 흑백 -> CLAHE
    img_resized = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced_img = clahe.apply(gray)
    
    # [핵심] 텍스트 추출 (전처리된 이미지 사용)
    # contrast_ths: 낮을수록 흐릿한 글자도 인식
    # adjust_contrast: 자동으로 대비를 조절
    texts = reader.readtext(enhanced_img, 
                            detail=0, 
                            paragraph=True,
                            contrast_ths=0.05, 
                            adjust_contrast=0.7)
    
    extracted_texts.append("\n".join(texts))

# 3. 결과 저장 (merge_text.txt)
output_file = 'merge_text.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for i, text in enumerate(extracted_texts, start=1):
        f.write(f"--- Page {i} ---\n")
        f.write(text + "\n\n")

print(f"완료! '{output_file}'에 저장되었습니다.")
```

### 📝 배운 점 & 팁
* **순서:** OCR을 할 때는 **`전처리(확대/보정) → 인식`** 순서가 매우 중요하다. 원본을 바로 넣는 것보다 인식률이 훨씬 좋다.
* **CLAHE:** 단순 `threshold`보다 `CLAHE`가 흐릿한 문서 인식에 훨씬 효과적이다.
