# 导入必要的库
import re
import uuid
from autogen import UserProxyAgent
from zep_cloud.client import Zep
from zep_cloud import FactRatingExamples, FactRatingInstruction
from llm_config import config_list
from prompt import agent_system_message
from agent import ZepConversableAgent
from util import generate_user_id
import streamlit as st


# 定义全局变量 zep，稍后初始化
zep = None


def initialize_zep_client(api_key):
    """使用提供的 API 密钥初始化 Zep 客户端。"""
    global zep
    try:
        zep = Zep(api_key=api_key)
        return True
    except Exception as e:
        st.error(f"初始化 Zep 客户端失败: {e}")
        return False


def initialize_session(first_name, last_name):
    """初始化会话状态和 Zep 连接。"""
    # 检查是否有有效的 Zep 客户端
    global zep
    if not zep:
        st.error("Zep 客户端未初始化。请输入有效的 API 密钥。")
        return

    if "zep_session_id" not in st.session_state:
        # 生成唯一标识符
        user_id = generate_user_id(first_name, last_name)

        # Streamlit 会话状态
        st.session_state.zep_session_id = str(uuid.uuid4())
        st.session_state.zep_user_id = user_id
        st.session_state.chat_initialized = False
        st.session_state.messages = []  # 存储聊天历史以显示

        try:
            # 定义事实评分指令
            fact_rating_instruction = """Rate facts by relevance and utility. Highly relevant 
            facts directly impact the user's current needs or represent core preferences that 
            affect multiple interactions. Low relevance facts are incidental details that 
            rarely influence future conversations or decisions."""

            fact_rating_examples = FactRatingExamples(
                high="The user is developing a Python application using the Streamlit framework.",
                medium="The user prefers dark mode interfaces when available.",
                low="The user mentioned it was raining yesterday.",
            )

            # 尝试添加用户
            user_exists = False
            try:
                # 尝试获取用户
                zep.user.get(st.session_state.zep_user_id)
                user_exists = True
            except Exception:
                # 用户不存在，创建新用户
                zep.user.add(
                    first_name=first_name,
                    last_name=last_name,
                    user_id=st.session_state.zep_user_id,
                    fact_rating_instruction=FactRatingInstruction(
                        instruction=fact_rating_instruction,
                        examples=fact_rating_examples,
                    ),
                )

            # 为用户添加会话（无论新用户还是现有用户）
            zep.memory.add_session(
                user_id=st.session_state.zep_user_id,
                session_id=st.session_state.zep_session_id,
            )

            # 显示适当消息
            if user_exists:
                st.sidebar.info(f"使用现有用户: {st.session_state.zep_user_id}")
            else:
                st.sidebar.info(f"为新用户 {first_name} {last_name} 创建")

            st.session_state.chat_initialized = True
            st.sidebar.success("Zep 用户/会话初始化成功。")
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "欢迎！😊 今天我能帮您什么忙？",
                }
            )

        # 处理初始化过程中的任何异常
        except Exception as e:
            st.error(f"初始化 Zep 用户/会话失败: {e}")
            st.stop()


def create_agents():
    """创建和配置对话代理。"""
    if st.session_state.chat_initialized:
        # 创建带有 Zep 内存的 autogen 代理
        agent = ZepConversableAgent(
            name="ZEP AGENT",
            system_message=agent_system_message,
            llm_config={"config_list": config_list},
            zep_session_id=st.session_state.zep_session_id,
            zep_client=zep,
            min_fact_rating=0.7,
            function_map=None,
            human_input_mode="NEVER",
        )

        # 创建 UserProxy 代理
        user = UserProxyAgent(
            name="UserProxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False,
            llm_config=False,
        )

        return agent, user
    return None, None


def handle_conversations(agent, user, prompt):
    """处理用户输入并生成助手响应。"""
    # 添加用户消息到显示
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 为后端处理添加 /no_think 标记
    prompt_with_token = f"{prompt} /no_think"

    # 存储用户全名而不是 ID
    user_full_name = f"{st.session_state.get('first_name', '')} {st.session_state.get('last_name', '')}".strip()

    # 如果可用则使用正确名称，否则回退到用户 ID
    display_name = user_full_name if user_full_name else st.session_state.zep_user_id

    # 持久化用户消息并使用事实更新系统消息
    agent._zep_persist_user_message(prompt, user_name=display_name.upper())
    agent._zep_fetch_and_update_system_message()

    # 生成并显示响应
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("思考中...")

        try:
            # 发起单轮聊天
            user.initiate_chat(
                recipient=agent,
                message=prompt_with_token,
                max_turns=1,
                clear_history=False,
            )

            # 从代理中提取响应
            full_response = user.last_message(agent).get("content", "...")

            if not full_response or full_response == "...":
                full_response = "抱歉，我无法生成响应。"

            # 从响应中移除 <think> </think> 标签
            clean_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()

            # 显示响应
            message_placeholder.markdown(clean_response)

            # 将助手响应添加到显示历史
            st.session_state.messages.append(
                {"role": "assistant", "content": clean_response}
            )

        # 处理聊天过程中的任何异常
        except Exception as e:
            error_message = f"聊天过程中出错: {e}"
            raise RuntimeError(error_message) from e


def main():
    """主应用程序入口点。"""
    # 设置页面配置
    st.set_page_config(
        page_title="Zep Memory Agent",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 创建标题和清除按钮的列布局
    col1, col2 = st.columns([5, 1])
    with col1:
        st.title("🧠 Zep Memory Agent")
        powered_by_html = """
    <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
        <span style='font-size: 20px; color: #666;'>Powered by</span>
        <img src="https://files.buildwithfern.com/zep.docs.buildwithfern.com/2025-04-23T01:17:51.789Z/logo/zep-name-logo-pink.svg" width="100"> 
        <span style='font-size: 20px; color: #666;'>and</span>
        <img src="https://docs.ag2.ai/latest/assets/img/logo.svg" width="80">
    </div>
        """
        st.markdown(powered_by_html, unsafe_allow_html=True)

    # 清除聊天历史按钮
    with col2:
        if st.button("Clear ↺"):
            st.session_state.messages = []
            st.rerun()

    # 侧边栏用于 API 密钥、用户信息和控件
    with st.sidebar:
        # API 密钥输入部分
        zep_logo_html = """
        <div style='display: flex; align-items: center; gap: 10px; margin-top: 5px;'>
            <img src="https://files.buildwithfern.com/zep.docs.buildwithfern.com/2025-04-23T01:17:51.789Z/logo/zep-name-logo-pink.svg" width="100"> 
            <span style='font-size: 23px; color: #FFF; line-height: 1; display: flex; align-items: center; margin: 0;'>Configuration 🔑</span>
        </div>
        """
        st.markdown(zep_logo_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("[Get your API key](https://www.getzep.com/)", unsafe_allow_html=True)

        # 使用会话状态持久化 API 密钥
        if "zep_api_key" not in st.session_state:
            st.session_state.zep_api_key = ""

        api_key = st.text_input(
            "Zep API Key",
            type="password",
            value=st.session_state.zep_api_key,
            help="Enter your Zep API key. This is required to use memory features.",
        )

        # 提供 API 密钥时初始化 Zep 客户端
        if api_key:
            # 仅在密钥更改时初始化
            if api_key != st.session_state.zep_api_key or zep is None:
                if initialize_zep_client(api_key):
                    st.session_state.zep_api_key = api_key
                    st.success("✅ Zep 客户端初始化成功")
                else:
                    st.error("❌ 使用提供的密钥初始化 Zep 客户端失败")
        else:
            st.warning("请输入您的 Zep API 密钥以继续！")

        # 仅在 Zep 客户端初始化后显示用户信息部分
        if zep is not None:
            st.divider()
            st.header("👤 User Information")
            first_name = st.text_input("First Name", key="first_name")
            last_name = st.text_input("Last Name", key="last_name")

            if st.button("Initialize Session ✅"):
                if not first_name or not last_name:
                    st.warning("请输入名字和姓氏")
                else:
                    initialize_session(first_name, last_name)

            # 如果已初始化则显示会话信息
            if "zep_session_id" in st.session_state:
                st.divider()
                st.subheader("Session Details 🔽")
                st.info(f"Session ID: {st.session_state.zep_session_id[:8]}...")
                st.info(f"User ID: {st.session_state.zep_user_id}")

    # 主聊天界面
    if st.session_state.get("chat_initialized", False):
        # 创建代理
        agent, user = create_agents()
        if not agent or not user:
            st.error(
                "Failed to create agents. Please check your autogen configuration."
            )
            return

        # 显示聊天历史
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 处理用户输入
        if prompt := st.chat_input("How are you feeling today?"):
            if not st.session_state.chat_initialized:
                st.error("Chat not initialized yet. Try again.")
                return

            handle_conversations(agent, user, prompt)
    else:
        if zep is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            st.info(
                "Please enter your name and initialize a session to begin chatting 💬"
            )


# 运行 Streamlit 应用
if __name__ == "__main__":
    main()
