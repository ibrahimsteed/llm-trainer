# 导入必要的类型和模块
from typing import Union, Dict
from autogen import ConversableAgent, Agent
from zep_cloud.client import Zep
from zep_cloud import Message, Memory


class ZepConversableAgent(ConversableAgent):  # 集成Zep内存的Agent
    """自定义的ConversableAgent，集成了Zep以实现长期记忆功能。"""

    def __init__(
        self,
        name: str,
        system_message: str,
        llm_config: dict,
        function_map: dict,
        human_input_mode: str,
        zep_session_id: str,
        zep_client: Zep,
        min_fact_rating: float,
    ):
        super().__init__(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode=human_input_mode,
            function_map=function_map,
        )
        self.zep_session_id = zep_session_id
        self.zep_client = zep_client
        self.min_fact_rating = min_fact_rating
        # 存储原始系统消息，以便后续从Zep获取相关事实后更新
        self.original_system_message = system_message
        self.register_hook(
            "process_message_before_send", self._zep_persist_assistant_messages
        )
        # 注意：用户消息的持久化需要在Agent处理之前进行，以便获取相关事实。我们将在外部基于Streamlit输入处理此逻辑。

    def _zep_persist_assistant_messages(
        self,
        message: Union[Dict, str],
        sender: Agent,
        recipient: Agent,
        silent: bool,
    ):
        """Agent向用户发送消息时，将消息添加到Zep中。"""
        if sender == self:
            if isinstance(message, dict):
                content = message.get("content", "")
            else:
                content = str(message)

            if content:
                zep_message = Message(
                    role_type="assistant", role=self.name, content=content
                )
                self.zep_client.memory.add(
                    session_id=self.zep_session_id, messages=[zep_message]
                )
        return message

    def _zep_fetch_and_update_system_message(self):
        """获取事实并更新系统消息。"""
        memory: Memory = self.zep_client.memory.get(
            self.zep_session_id, min_rating=self.min_fact_rating
        )
        context = memory.context or "没有回忆起特定的事实。"

        # 更新系统消息以用于下一次推理
        self.update_system_message(
            self.original_system_message
            + f"\n\n关于用户和先前对话的相关事实：\n{context}"
        )

    def _zep_persist_user_message(self, user_content: str, user_name: str = "User"):
        """用户向Agent发送消息时，将消息添加到Zep中。"""
        if user_content:
            zep_message = Message(
                role_type="user",
                role=user_name,
                content=user_content,
            )
            self.zep_client.memory.add(
                session_id=self.zep_session_id, messages=[zep_message]
            )
