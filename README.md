# 나만의 RAG 챗봇

Langchain을 활용하여 구축한 RAG(Retrieval-Augmented Generation) 챗봇입니다.

## 🚀 주요 기능

- 📄 PDF 문서 업로드 및 분석
- 💬 문서 기반 질의응답
- 🎨 커스터마이징된 Streamlit UI
- 🌙 다크 모드 지원
- 🗑️ 대화 초기화 기능

## 📋 설치 방법

1. 필요한 라이브러리 설치:
```bash
pip install -r requirements.txt
```

2. OpenAI API 키 설정:
   - Streamlit 앱 실행 후 사이드바에서 API 키 입력
   - 또는 환경변수로 설정: `export OPENAI_API_KEY=your_api_key`

## 🎯 사용 방법

1. 앱 실행:
```bash
streamlit run app.py
```

2. PDF 문서 업로드
3. "문서 분석 시작" 버튼 클릭
4. 채팅창에서 문서에 대해 질문

## 🌐 Streamlit Cloud 배포

1. GitHub에 코드 업로드
2. Streamlit Cloud에서 새 앱 생성
3. GitHub 저장소 연결
4. 메인 파일 경로: `app.py`
5. 환경변수 설정: `OPENAI_API_KEY`

## 📁 프로젝트 구조

```
├── app.py                 # 메인 Streamlit 앱
├── requirements.txt       # 필요한 라이브러리
├── .streamlit/
│   └── config.toml       # Streamlit 설정
└── README.md             # 프로젝트 설명
```

## 🔧 기술 스택

- **Streamlit**: 웹 UI 프레임워크
- **Langchain**: RAG 구현
- **OpenAI**: LLM 및 임베딩
- **FAISS**: 벡터 검색
- **PyPDF2**: PDF 문서 처리
