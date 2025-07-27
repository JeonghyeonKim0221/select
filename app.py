import streamlit as st
import random
import time

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="랜덤 이름 뽑기",
    page_icon="🎉",
    layout="centered"
)

# --- CSS로 디자인 개선 ---
st.markdown("""
<style>
    /* 기본 폰트 및 중앙 정렬 */
    .stApp {
        text-align: center;
    }
    /* 당첨자 이름 스타일 */
    .winner-text {
        font-size: 4.5rem;
        font-weight: 900;
        color: #1a73e8; /* 파란색 계열 */
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }
    /* 남은 사람 태그 스타일 */
    .participant-tag {
        display: inline-block;
        background-color: #f0f2f5;
        color: #333;
        padding: 8px 15px;
        margin: 5px;
        border-radius: 20px;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }
    .participant-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


# --- 세션 상태(Session State) 초기화 ---
# 사용자의 브라우저 세션 동안 데이터를 유지하기 위함
if 'screen' not in st.session_state:
    st.session_state.screen = 'input'
    st.session_state.participants = []
    st.session_state.remaining_participants = []
    st.session_state.winner = None
    st.session_state.name_input_text = "" # 텍스트 입력창 상태 저장

# --- 콜백 함수 (버튼 클릭 시 실행될 로직) ---

def start_picking():
    """입력된 이름들을 처리하고 뽑기 화면으로 전환합니다."""
    names_input = st.session_state.name_input_text
    names = [name.strip() for name in names_input.split('\n') if name.strip()]
    
    if len(names) < 2:
        st.error("최소 2명 이상의 이름을 입력해주세요.", icon="🚨")
    else:
        st.session_state.participants = names
        st.session_state.remaining_participants = names.copy()
        st.session_state.screen = 'picker'

def pick_winner():
    """참여자 중 한 명을 랜덤으로 뽑습니다."""
    if st.session_state.remaining_participants:
        winner = random.choice(st.session_state.remaining_participants)
        st.session_state.winner = winner
        st.session_state.remaining_participants.remove(winner)

def restart_app():
    """모든 상태를 초기화하여 처음 화면으로 돌아갑니다."""
    st.session_state.screen = 'input'
    st.session_state.participants = []
    st.session_state.remaining_participants = []
    st.session_state.winner = None
    st.session_state.name_input_text = ""


# --- 화면 렌더링 로직 ---

# 1. 당첨자가 뽑혔을 경우: 당첨자 화면 표시
if st.session_state.winner:
    st.title("🎉 축하합니다! 🎉")
    st.markdown(f"<p class='winner-text'>{st.session_state.winner}</p>", unsafe_allow_html=True)
    
    # 폭죽 효과
    st.balloons()
    
    # 3초 대기
    time.sleep(3)
    
    # 당첨자 상태 초기화 후 앱 재실행
    st.session_state.winner = None
    st.rerun()

# 2. 이름 입력 화면
elif st.session_state.screen == 'input':
    st.title("🚀 랜덤 이름 뽑기")
    st.markdown("한 줄에 한 명씩 이름을 입력하고<br>'생성하기' 버튼을 눌러주세요.", unsafe_allow_html=True)
    
    st.text_area(
        "참여자 명단",
        placeholder="홍길동\n이순신\n세종대왕\n유관순",
        height=200,
        key="name_input_text",
        label_visibility="collapsed"
    )
    
    st.button("생성하기", on_click=start_picking, type="primary", use_container_width=True)

# 3. 이름 뽑기 화면
elif st.session_state.screen == 'picker':
    st.title("누가 될까요?")
    
    # 아직 뽑을 사람이 남았을 경우
    if st.session_state.remaining_participants:
        st.metric("남은 사람", f"{len(st.session_state.remaining_participants)}명")
        
        # 남은 사람들을 태그 형태로 표시
        st.markdown("---")
        tags_html = "".join([f"<span class='participant-tag'>{name}</span>" for name in st.session_state.remaining_participants])
        st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
        st.markdown("---")

        st.button("💥 뽑기! 💥", on_click=pick_winner, type="primary", use_container_width=True)
    
    # 모든 사람을 다 뽑았을 경우
    else:
        st.success("모든 사람을 뽑았습니다! 🥳")
        st.button("처음으로 돌아가기", on_click=restart_app, use_container_width=True)
