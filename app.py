import streamlit as st
import random
import time

# --------------------------------------------------------------------------
# 페이지 렌더링 함수
# --------------------------------------------------------------------------

def render_input_page():
    """첫 번째 화면: 사용자로부터 이름 목록을 입력받는 페이지입니다."""
    st.title("랜덤 선정 프로그램 🎯")
    st.header("1. 이름 입력")
    st.write("선정할 사람들의 이름을 한 줄에 한 명씩 입력해주세요.")

    # 사용자가 이름을 입력할 텍스트 영역
    names_input = st.text_area(
        "이름 목록:", 
        height=200, 
        placeholder="예시)\n홍길동\n이순신\n세종대왕",
        key="names_input_area" # 명시적인 key 추가
    )

    # '생성하기' 버튼을 누르면 입력된 이름을 처리
    if st.button("생성하기", key="generate_button", type="primary"):
        if names_input:
            # 입력된 텍스트를 줄바꿈 기준으로 나누고, 빈 줄은 제거
            names = [name.strip() for name in names_input.split('\n') if name.strip()]
            if names:
                # 세션 상태에 이름 목록 저장 및 페이지 전환
                st.session_state.names_list = names
                st.session_state.remaining_names = names.copy()
                st.session_state.page = "selection"
                st.rerun()
            else:
                st.warning("유효한 이름을 입력해주세요.")
        else:
            st.warning("이름을 입력해주세요.")

def render_selection_page():
    """두 번째 화면: 남은 사람들 중에서 한 명을 선정하는 페이지입니다."""
    st.title("랜덤 선정 프로그램 🎯")
    st.header("2. 선정하기")
    
    # 남은 사람이 없으면 종료 페이지로 이동
    if not st.session_state.remaining_names:
        st.session_state.page = "end"
        st.rerun()

    # 남은 사람 목록 표시
    st.write(f"**남은 사람 ({len(st.session_state.remaining_names)}명):**")
    st.info(", ".join(st.session_state.remaining_names))
    st.write("") # 여백

    # '한 명 선정하기' 버튼을 누르면 랜덤으로 한 명 선택
    if st.button("🎉 한 명 선정하기! 🎉", key="pick_one_button", type="primary"):
        selected_name = random.choice(st.session_state.remaining_names)
        st.session_state.selected_name = selected_name
        
        # 선택된 사람은 남은 목록에서 제거
        st.session_state.remaining_names.remove(selected_name)
        st.session_state.page = "result"
        st.rerun()

def render_result_page():
    """선정된 사람의 이름을 폭죽 효과와 함께 3초간 보여주는 페이지입니다."""
    
    # 폭죽 효과
    st.balloons()
    
    st.title("🎉 당첨! 🎉")
    
    selected_name = st.session_state.get("selected_name", "오류 발생")
    
    # HTML과 CSS를 사용하여 선택된 이름을 더 크게 표시 (font-size: 6.5rem)
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 300px; background-color: #f0f2f6; border-radius: 10px; padding: 20px;">
        <h1 style='text-align: center; font-size: 6.5rem; font-weight: bold; color: #FF4B4B; text-shadow: 2px 2px 4px #cccccc;'>
            {selected_name}
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # 3초 카운트다운 진행률 표시줄
    progress_bar = st.progress(0, text="남은 시간: 3.0초")
    
    for i in range(30):
        time.sleep(0.1)
        progress_value = (i + 1) / 30
        remaining_time = 3.0 - (i + 1) * 0.1
        # remaining_time이 음수가 되지 않도록 처리
        if remaining_time < 0:
            remaining_time = 0
        progress_bar.progress(progress_value, text=f"남은 시간: {remaining_time:.1f}초")

    progress_bar.empty()

    # '계속하기' 버튼을 눌러 다음 단계로 진행
    if st.button("계속하기", key="continue_button"):
        if not st.session_state.remaining_names:
            st.session_state.page = "end"
        else:
            st.session_state.page = "selection"
        st.rerun()

def render_end_page():
    """모든 사람을 선정한 후, 다시 시작할 수 있는 페이지입니다."""
    st.title("✅ 선정 완료 ✅")
    st.header("모든 사람을 성공적으로 선정했습니다!")
    st.balloons()
    
    if "names_list" in st.session_state:
        st.write("**전체 참여자 목록:**")
        st.success(", ".join(st.session_state.names_list))

    # '처음으로 돌아가기' 버튼을 누르면 모든 상태를 초기화하고 첫 페이지로 이동
    if st.button("처음으로 돌아가기", key="restart_button"):
        # 세션 상태의 모든 키를 삭제하여 초기화
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# --------------------------------------------------------------------------
# 메인 애플리케이션 로직
# --------------------------------------------------------------------------

def main():
    """메인 함수: 앱의 전체적인 흐름을 제어합니다."""
    
    # Streamlit의 세션 상태(session_state)를 사용하여 페이지 상태와 데이터를 관리합니다.
    # 이렇게 하면 사용자가 버튼을 누를 때마다 정보가 초기화되는 것을 방지할 수 있습니다.
    
    # 앱이 처음 실행될 때 'page' 상태를 'input'으로 초기화
    if "page" not in st.session_state:
        st.session_state.page = "input"

    # 현재 페이지 상태에 따라 적절한 함수를 호출하여 페이지를 렌더링
    if st.session_state.page == "input":
        render_input_page()
    elif st.session_state.page == "selection":
        render_selection_page()
    elif st.session_state.page == "result":
        render_result_page()
    elif st.session_state.page == "end":
        render_end_page()

if __name__ == "__main__":
    main()
