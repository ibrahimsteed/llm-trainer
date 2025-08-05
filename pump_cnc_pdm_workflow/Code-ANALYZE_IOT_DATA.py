import json
import re
import ast

def analyze_and_decide(text_content: str) -> dict:

    try:
        if not text_content: raise ValueError("输入的文本内容为空。")
        match = re.search(r"```json\s*([\s\S]*?)\s*```", text_content)
        if not match: raise ValueError("在文本内容中未找到格式为 ```json ... ``` 的数据块。")
        json_like_str = match.group(1).strip()
        cnc_data = ast.literal_eval(json_like_str)
        spindle_load = float(cnc_data.get('spindle_load', 0))
        z_axis_load = float(cnc_data.get('z_axis_load', 0))
        equipment_id = cnc_data.get('equipment_id', 'Unknown')
        timestamp = cnc_data.get('created_at', 'N/A')
        alarm_message = cnc_data.get('alarm_message', '').strip()
        SPINDLE_LOAD_THRESHOLD = 85.0
        Z_AXIS_LOAD_THRESHOLD = 75.0
        decide_flag = 0
        reason = "设备状态正常。"
        if alarm_message and alarm_message != 'nan':
            decide_flag = 1
            reason = f"设备直接告警: {alarm_message}"
        elif spindle_load > SPINDLE_LOAD_THRESHOLD or z_axis_load > Z_AXIS_LOAD_THRESHOLD:
            decide_flag = 1
            reason_parts = []
            if spindle_load > SPINDLE_LOAD_THRESHOLD: reason_parts.append(f"主轴负载高达 {spindle_load}% (阈值: {SPINDLE_LOAD_THRESHOLD}%)")
            if z_axis_load > Z_AXIS_LOAD_THRESHOLD: reason_parts.append(f"Z轴负载高达 {z_axis_load}% (阈值: {Z_AXIS_LOAD_THRESHOLD}%)")
            reason = " | ".join(reason_parts)
        output = {
            "decide_flag": decide_flag,
            "analysis_summary": f"设备ID: {equipment_id} 在 {timestamp} 的状态分析完成。",
            "abnormal_reason": reason,
            "key_metrics": f"主轴负载: {spindle_load}%, Z轴负载: {z_axis_load}%",
            "equipment_id": equipment_id
        }
        return output
    except Exception as e:
        return { "decide_flag": 0, "error": f"解析IoT数据时出错: {str(e)}", "abnormal_reason": "数据处理异常" }


def main(iot_data: str) -> dict:
    """
    Dify工作流会调用此主函数。
    此函数直接返回分析结果字典，其每个键都将成为一个独立的输出变量。
    """
    # 直接返回分析函数的字典结果
    return analyze_and_decide(iot_data)