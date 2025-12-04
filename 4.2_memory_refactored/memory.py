import json
import os

def load_memory(file_path):
    """从JSON文件加载对话历史，返回对话历史列表"""
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            history = data.get("history", [])
            print(f"✓ 已加载 {len(history)} 条历史对话")
            return history
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}，将使用新的对话历史")
            return []
    else:
        print("✓ 未找到记忆文件，开始新对话")
        return []

def save_memory(file_path, data):
    """保存对话历史到JSON文件"""
    from datetime import datetime
    
    try:
        # data 应该是一个字典，包含 role_system 和 history
        if isinstance(data, dict):
            save_data = {
                "role_system": data.get("role_system", ""),
                "history": data.get("history", []),
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            # 兼容旧接口：如果传入的是 conversation_history 列表
            save_data = {
                "role_system": "",
                "history": data if isinstance(data, list) else [],
                "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # 确保目录存在（如果文件路径包含目录）
        dir_path = os.path.dirname(file_path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存 {len(save_data['history'])} 条对话到记忆文件")
    except Exception as e:
        print(f"⚠ 保存记忆失败: {e}")