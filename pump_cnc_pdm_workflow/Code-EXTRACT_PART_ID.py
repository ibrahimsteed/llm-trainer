import json
import re

def extract_part_id(llm_input) -> dict:
    """
    从上游LLM节点的输出中精确提取备件ID。
    此函数能适应两种输入格式：
    1. 纯文本字符串。
    2. 包含 'llm_output' 键的JSON对象/字典。
    同时，它能处理目标行被反引号(`)包裹的情况。

    :param llm_input: 从上游LLM节点获取的完整输入，可以是字符串或字典。
    :return: 一个包含提取到的备件ID和执行状态的字典。
    """
    llm_output_text = ""
    try:
        # 步骤1: 智能地提取文本内容
        if isinstance(llm_input, dict):
            # 如果输入是字典，尝试获取 'llm_output' 键的值
            llm_output_text = llm_input.get('llm_output', '')
            if not llm_output_text:
                # 兼容Dify标准的 .text 输出
                llm_output_text = llm_input.get('text', '')
        elif isinstance(llm_input, str):
            # 如果输入直接就是字符串
            llm_output_text = llm_input
        else:
            raise TypeError("Input is not a recognized type (dict or str).")
            
        if not llm_output_text:
             return {
                "required_partId": "NO_TEXT_INPUT",
                "extraction_status": "Failed: The input text from the LLM node was empty."
            }

        # 步骤2: 更新正则表达式以适应反引号
        # 模式解释:
        # `?                 - 匹配0个或1个可选的反引号
        # Required Part ID: - 匹配字面文本 (不区分大小写)
        # \s*               - 匹配任意空白
        # ([A-Z0-9\-]+)     - 捕获目标ID
        # `?                 - 匹配0个或1个可选的结尾反引号
        pattern = r"`?Required Part ID:\s*([A-Z0-9\-]+)`?"
        
        # 我们不再限制必须在行首行尾，因为这行本身就足够独特
        match = re.search(pattern, llm_output_text, re.IGNORECASE)

        if match:
            required_part_id = match.group(1)
            return {
                "required_partId": required_part_id,
                "extraction_status": "Success"
            }
        else:
            return {
                "required_partId": "NOT_FOUND",
                "extraction_status": "Failed: No valid Part ID line was found in the text."
            }
            
    except Exception as e:
        return {
            "required_partId": "ERROR",
            "extraction_status": f"An error occurred during extraction: {str(e)}"
        }

def main(llm_data) -> dict:
    """
    Dify工作流的入口函数。
    它接收上游节点的完整输出，并调用处理函数。
    """
    return extract_part_id(llm_data)