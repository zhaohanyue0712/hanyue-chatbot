import streamlit as st
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI
import tempfile
import shutil
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="나만의 RAG 챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv()

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    
    .upload-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
    }
    
    .status-success {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .status-error {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

class RAGChatbot:
    def __init__(self):
        self.vectorstore = None
        self.qa_chain = None
        
    def load_documents(self, uploaded_files):
        """업로드된 문서들을 로드하고 처리"""
        documents = []
        
        for uploaded_file in uploaded_files:
            # 임시 파일로 저장
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # PDF 로더로 문서 로드
                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                documents.extend(docs)
            except Exception as e:
                st.error(f"문서 로드 중 오류 발생: {str(e)}")
            finally:
                # 임시 파일 삭제
                os.unlink(tmp_file_path)
        
        return documents
    
    def create_vectorstore(self, documents):
        """문서들을 벡터스토어로 변환"""
        if not documents:
            return None
            
        # 텍스트 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        # 임베딩 생성
        embeddings = OpenAIEmbeddings()
        
        # FAISS 벡터스토어 생성
        vectorstore = FAISS.from_documents(texts, embeddings)
        
        return vectorstore
    
    def create_qa_chain(self, vectorstore):
        """질의응답 체인 생성"""
        if vectorstore is None:
            return None
            
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        
        return qa_chain
    
    def query(self, question):
        """질문에 대한 답변 생성"""
        if self.qa_chain is None:
            return "먼저 문서를 업로드해주세요."
        
        try:
            response = self.qa_chain.run(question)
            return response
        except Exception as e:
            return f"답변 생성 중 오류가 발생했습니다: {str(e)}"

def main():
    # 메인 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🤖 나만의 RAG 챗봇</h1>
        <p>문서를 업로드하고 AI와 대화해보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 사이드바 설정
    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        
        # API 키 입력
        api_key = st.text_input("OpenAI API 키", type="password", help="OpenAI API 키를 입력하세요")
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        st.markdown("---")
        
        # 다크 모드 토글
        dark_mode = st.checkbox("🌙 다크 모드", value=False)
        
        # 세션 초기화 버튼
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.session_state.vectorstore = None
            st.session_state.qa_chain = None
            st.rerun()
        
        st.markdown("---")
        
        # 앱 정보
        st.markdown("### 📱 앱 정보")
        st.markdown("""
        **버전**: 1.0.0  
        **개발자**: 학생  
        **기술**: Langchain + Streamlit
        """)
    
    # 메인 영역을 두 개의 컬럼으로 분할
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📄 문서 업로드")
        
        # 업로드 섹션
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        
        # 파일 업로드
        uploaded_files = st.file_uploader(
            "PDF 파일을 업로드하세요",
            type=['pdf'],
            accept_multiple_files=True,
            help="분석할 PDF 문서들을 선택하세요"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 문서 처리 버튼
        if st.button("📚 문서 분석 시작", disabled=not uploaded_files, use_container_width=True):
            if not api_key:
                st.markdown('<div class="status-error">OpenAI API 키를 입력해주세요.</div>', unsafe_allow_html=True)
            else:
                with st.spinner("문서를 분석하고 있습니다..."):
                    chatbot = RAGChatbot()
                    
                    # 문서 로드
                    documents = chatbot.load_documents(uploaded_files)
                    
                    if documents:
                        # 벡터스토어 생성
                        vectorstore = chatbot.create_vectorstore(documents)
                        
                        # QA 체인 생성
                        qa_chain = chatbot.create_qa_chain(vectorstore)
                        
                        # 세션 상태에 저장
                        st.session_state.vectorstore = vectorstore
                        st.session_state.qa_chain = qa_chain
                        
                        st.markdown(f'<div class="status-success">✅ {len(documents)}개의 문서가 성공적으로 분석되었습니다!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="status-error">문서를 로드할 수 없습니다.</div>', unsafe_allow_html=True)
        
        # 문서 상태 표시
        if st.session_state.get("qa_chain"):
            st.markdown("### ✅ 문서 상태")
            st.success("문서가 준비되었습니다!")
            st.markdown("이제 질문을 할 수 있습니다.")
    
    with col2:
        st.markdown("### 💬 채팅")
        
        # 채팅 메시지 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # 채팅 히스토리 표시
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>👤 사용자:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><strong>🤖 챗봇:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        
        # 사용자 입력
        if prompt := st.chat_input("문서에 대해 질문해보세요..."):
            # 사용자 메시지 추가
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # 챗봇 응답 생성
            if st.session_state.get("qa_chain"):
                chatbot = RAGChatbot()
                chatbot.qa_chain = st.session_state.qa_chain
                
                with st.spinner("답변을 생성하고 있습니다..."):
                    response = chatbot.query(prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.rerun()
            else:
                st.error("먼저 문서를 업로드하고 분석해주세요.")

if __name__ == "__main__":
    main()