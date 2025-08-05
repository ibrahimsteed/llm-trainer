import json

def parse_and_format_rmms_data(input_json_string: str) -> dict:
    """
    解析从RMMS系统获取的、作为字符串的JSON响应，并将其格式化为人类可读的文本。
    此版本直接解析输入的JSON字符串，不再处理任何嵌套结构。

    :param input_json_string: 一个包含API响应的JSON格式字符串。
    :return: 一个包含格式化文本或错误信息的字典。
    """
    try:
        # 步骤1: 直接解析输入的JSON字符串，得到Python字典。
        data = json.loads(input_json_string)

        # 步骤2: 安全地导航到包含备件数据的列表。
        parts_list = data.get('message', {}).get('data', [])

        # 步骤3: 检查备件列表是否为空。
        if not parts_list:
            return {
                "parsed_rmms_info": "备件信息查询成功，但未返回任何具体的备件记录。"
            }

        # 步骤4: 遍历备件列表并格式化每一条记录。
        formatted_parts = []
        for part in parts_list:
            stock_quantity = int(part.get('stock_quantity', 0))
            availability = "有货" if stock_quantity > 0 else "无货，需采购"

            part_info = (
                f"- 备件ID: {part.get('part_id', 'N/A')}\n"
                f"  名称: {part.get('part_name', 'N/A')}\n"
                f"  状态: {availability}\n"
                f"  当前库存: {stock_quantity} 件\n"
                f"  采购提前期: {part.get('lead_time_days', 'N/A')} 天\n"
                f"  适用型号: {part.get('applicable_model', 'N/A')}\n"
                f"  供应商: {part.get('supplier', 'N/A')}\n"
                f"  参考单价: {part.get('unit_price', 'N/A')} 元"
            )
            formatted_parts.append(part_info)
        
        # 步骤5: 将所有格式化后的备件信息合并成一个单一的文本块。
        final_output = "\n\n".join(formatted_parts)
        
        return {"parsed_rmms_info": final_output}

    except json.JSONDecodeError as e:
        return {"parsed_rmms_info": f"错误：输入的RMMS数据不是有效的JSON格式字符串。错误详情: {e}"}
    except Exception as e:
        return {"parsed_rmms_info": f"解析RMMS备件数据时出现未知错误: {str(e)}"}

def main(rmms_input_string: str) -> dict:
    """
    Dify工作流的入口函数。
    它接收一个JSON字符串作为输入，并调用核心处理函数。
    """
    if not rmms_input_string:
        return {
            "parsed_rmms_info": "错误：输入变量为空。"
        }
    return parse_and_format_rmms_data(rmms_input_string)