# 💡 [TIL] CSS 심화 & Bootstrap 핵심 정리 (feat. AI 헬스케어)

## 1. Flexbox (1차원 레이아웃)
웹 페이지의 요소들을 **가로(Row) 또는 세로(Column) 한 방향**으로 정렬하고 배치할 때 사용하는 시스템입니다. 복잡한 계산 없이 요소들 사이의 간격과 수직/수평 중앙 정렬을 쉽게 구현할 수 있습니다.

* **헬스케어 적용:** 네비게이션 바 메뉴 정렬, 환자의 바이탈 사인(심박수, 체온 등) 요약 카드들을 일렬로 균일하게 배치할 때 사용합니다.

```css
/* Flexbox 핵심 코드 */
.flex-container {
  display: flex;
  justify-content: space-between; /* 주축(가로) 정렬: 양끝 배치 */
  align-items: center;            /* 교차축(세로) 정렬: 중앙 맞춤 */
}
```

---

## 2. 반응형 디자인 & Media Query
사용자의 기기 화면 크기(PC, 태블릿, 모바일)를 감지하여, 그에 맞는 CSS 스타일을 동적으로 적용하는 기술입니다.

* **헬스케어 적용:** 병동에서 의사가 태블릿으로 EMR을 볼 때, PC용 가로 메뉴를 세로로 변경하여 터치 인터페이스(Hit Area)를 넓게 확보하는 등 오조작을 방지하는 데 필수적입니다.

```css
/* Media Query 핵심 코드 */
@media (max-width: 768px) {
  /* 화면이 768px 이하(모바일/태블릿)일 때 가로 배치를 세로 배치로 변경 */
  .dashboard-menu {
    flex-direction: column; 
  }
}
```

---

## 3. CSS Grid (2차원 레이아웃)
행(Row)과 열(Column)을 **동시에 제어**하여 웹 페이지의 전체 뼈대를 정밀하게 설계하는 레이아웃 시스템입니다. `fr`(Fraction, 비율) 단위를 사용하여 남는 공간을 효율적으로 분배합니다.

* **헬스케어 적용:** 대시보드 설계 시, 왼쪽 200px은 '환자 리스트'로 고정하고, 남은 영역(`1fr`)은 'MRI 사진'과 '차트'가 비율대로 나누어 가지도록 뼈대를 잡습니다.

```css
/* CSS Grid 핵심 코드 */
.grid-container {
  display: grid;
  grid-template-columns: 200px 1fr 2fr; /* 1열 200px 고정, 2열과 3열은 1:2 비율 */
  gap: 15px;                            /* 데이터 가독성을 위한 요소 간 여백 */
}
```

---

## 4. Bootstrap (빠른 UI 구축 프레임워크)
미리 디자인된 CSS 클래스와 컴포넌트(버튼, 모달, 카드 등)를 제공하여 웹 개발 속도를 극대화하는 프레임워크입니다. CSS 파일에 코드를 짤 필요 없이 HTML 태그에 `class` 이름만 부여하면 디자인이 완성됩니다.

* **주의점:** Bootstrap 클래스에만 의존하면 세밀한 디자인 수정이 어렵습니다. 반드시 Flex와 Grid의 원리를 이해한 상태에서 유틸리티 도구로 활용해야 합니다.

**① 12 Grid System (그리드 시스템)**
화면을 가로 12칸으로 나누어 반응형 배치를 돕습니다.
```html
<div class="row">
  <!-- md(데스크톱) 크기 이상에서 12칸 중 4칸(1/3)씩 차지 -->
  <div class="col-md-4">환자 정보</div>
  <div class="col-md-4">처방 내역</div>
  <div class="col-md-4">검사 결과</div>
</div>
```

**② Component: Navbar & Modal (네비게이션 바 & 팝업창)**
자주 쓰이는 UI를 클래스 조합으로 즉시 구현합니다.
```html
<!-- Navbar (네비게이션 바) 뼈대 -->
<nav class="navbar navbar-expand-lg bg-light">
  <a class="navbar-brand" href="#">AI 헬스케어</a>
  <!-- 모바일에서는 햄버거 메뉴로 자동 접힘 -->
</nav>

<!-- Modal (응급 경고/상세 정보 팝업) 뼈대 -->
<button data-bs-toggle="modal" data-bs-target="#alertModal">환자 상세 보기</button>

<div class="modal fade" id="alertModal">
  <div class="modal-dialog">
    <div class="modal-content">혈압: 120/80 mmHg (모달 내용)</div>
  </div>
</div>
```
