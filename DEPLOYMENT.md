# Streamlit Cloud 배포 가이드

## 🚀 배포 단계

### 1. GitHub 저장소 생성
1. GitHub에서 새 저장소 생성
2. 모든 파일을 업로드

### 2. Streamlit Cloud 연결
1. [Streamlit Cloud](https://share.streamlit.io/) 접속
2. "New app" 클릭
3. GitHub 저장소 선택
4. 메인 파일 경로: `app.py`

### 3. 환경변수 설정
Streamlit Cloud 대시보드에서:
- `OPENAI_API_KEY`: OpenAI API 키 입력

### 4. 배포 확인
- 앱이 성공적으로 배포되면 URL 제공
- 브라우저에서 접속하여 테스트

## 📋 배포 체크리스트

- [ ] 모든 파일이 GitHub에 업로드됨
- [ ] requirements.txt 파일 존재
- [ ] .streamlit/config.toml 파일 존재
- [ ] OpenAI API 키 준비됨
- [ ] 로컬에서 테스트 완료

## 🔧 문제 해결

### 일반적인 오류:
1. **모듈 import 오류**: requirements.txt 확인
2. **API 키 오류**: 환경변수 설정 확인
3. **메모리 부족**: 문서 크기 제한

### 지원:
- Streamlit Cloud 문서: https://docs.streamlit.io/streamlit-community-cloud
- GitHub Issues에서 도움 요청
