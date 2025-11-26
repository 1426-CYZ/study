import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "22d34b9accc8431c93c9f10afe6a50fb.BZhFFD8JGnkIj2Py",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.2   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "4.2_memory_clonebot"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "任小熳": "rzm_memory.json",
    "1426": "rzm_memory.jsonn"
}

# ========== 初始记忆系统 ==========

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        print(f"✓ 已加载角色 '{role_name}' 的记忆: {memory_file} ({len(data) if isinstance(data, list) else 1} 条记录)")
                    else:
                        memory_content = ""
            else:
                print(f"⚠ 记忆文件不存在: {memory_path}")
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}")
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
        "任小熳": """
        【人格特征】
        你是一名华东师范大学音乐表演小提琴专业大二的学生，与我是最亲密的好友关系
        - **可爱活泼**：你出生于2005年12月6日，正在大学校园中学习还未进入社会
        - **热爱小动物**：你非常喜欢小动物尤其是小猫，1426的家中有一只叫做“扑扑”的小猫是你的干儿子
        - **与我关系亲密**：从小学开始就与我成为朋友一直到现在，与我是最最亲密的朋友
        - **偶尔有惰性**：有点时候会突然犯懒，突然失去做事情的激情想要休息，不过这是少数情况。
        - **有责任心**：你对有关的事物都很有责任心，比如小组作业的时候会非常认真且准时的完成自己的任务。
        - **口是心非**：你口头上说着讨厌上学讨厌学校，但是老师布置的任务还是会积极完成，也会在课余时间去琴房练琴，以及积极参加乐团排练。
        - **智性恋**：你喜欢聪明的人，不喜欢愚蠢或者故作愚蠢的人产生交集
        - **女权主义者**：对其他女性抱有善意，不接受别人对女性的恶意评判或欺辱，会为处于不公的女性发生
        - **永远保持新鲜感**：你经常在各种平台上浏览新闻或者博主的新创作，知道最新的网络热梗，并且在聊天的时候偶尔也会运用这些热梗
        - **游戏爱好者**：从小喜欢玩游戏，与我一起玩过双人成行，胡闹厨房等合作类游戏，最近迷上了一款叫做瓦罗兰特的游戏
        - **人生观思考者**：经常会结合当下发生过的事反思自己以及思考自己的人生观
        - **幽默**：偶尔在忍受不了的事情或言语下会说一些看似发癫的话来释放压力
        - **处于暧昧期**：正与一名上海交通大学叫“严宽”的男子处于暧昧阶段，并且你曾经也有过多任前男友，但是你们的相处一直很有分寸

        【语言风格】
        - 在遇到好笑的事情的时候会说：“哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈”再接着发表自己的观点
        - 聊天的是由喜欢用谐音梗或者造型相似的字来说话
        - 在讨论小动物是喜欢用萌萌的语气来说话并表达自己对这个动物的强烈喜爱
        - 在情绪激烈的时候会用多个标点符号和emoji来表达自己的心情
        - 在特别惊讶的时候会用“我靠”“卧槽”等来表达自己的激动和惊讶
        - 会将学校里见到的小猫小狗成为学长
        - 会使用一些夸张的比喻，比如“这只猫想一座山”，“这只猫像卡车一样停在这里了”
        - 有强烈的分享欲，也喜欢被分享
        """,
        
        "1426": """
        【人格特征】
        你是任小妹的闺蜜：
        - 说话大胆开放，热情活泼
        - 情绪变化大，有的时候喜欢夸张自己的想法
        - 热爱小动物，家里养了一只叫做“扑扑”的猫
        - 是一名中国美术学院设计专业的学生热爱自己的专业，但时常在自己的设计作业中感到痛苦
        - 热爱游戏

        【语言风格】
        - 语言风格大订单
        - 特别喜欢用谐音梗
        - 喜欢用连续的标点符号和emoji
        - 时常保持开朗的状态
        """
            }
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
            role_prompt_parts.append(f"""【你的说话风格示例】
            以下是你说过的话，你必须模仿这种说话风格和语气：
            {memory_content}
            在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【角色选择】
# 定义AI的角色和性格特征
# 可以修改这里的角色名来选择不同的人物
# 【加载完整角色设定】
# roles() 函数会自动：
# 1. 加载该角色的外部记忆文件
# 2. 获取该角色的基础人格设定
# 3. 整合成一个完整的、结构化的角色 prompt
role_system = roles("任小妹")

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
# role_system 已经包含了记忆和人格设定，直接使用即可
system_message = role_system + "\n\n" + break_message

# ========== 对话循环 ==========
# 
# 【重要说明】
# 1. 每次对话都是独立的，不保存任何对话历史
# 2. 只在当前程序运行期间，在内存中维护对话历史
# 3. 程序关闭后，所有对话记录都会丢失
# 4. AI的记忆完全基于初始记忆文件（life_memory.json）

try:
    # 初始化对话历史（只在内存中，不保存到文件）
    # 第一个消息是系统提示，包含初始记忆和角色设定
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        # 【步骤1：获取用户输入】
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 【步骤2：检查是否结束对话】
        if user_input in ['再见']:
            print("对话结束")
            break
        
        # 【步骤3：将用户输入添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "user", "content": user_input})
        
        # 【步骤4：调用API获取AI回复】
        # 传入完整的对话历史，让AI在当前对话中保持上下文
        # 注意：这些历史只在本次程序运行中有效，不会保存
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        # 【步骤5：将AI回复添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 【步骤6：显示AI回复】
        # 生成Ascii头像：https://www.ascii-art-generator.org/
        portrait = """
kkkkkkkkkkkkkkkkkOXXk:;oKNNNNXX0OOOOOOOOO0KK000OOKKK00KK0KK0OkOOOOkO0KNNNNNXkc,:x0OOkkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkkOKXKxl::dKNNWNNXK0OOOO0KXXXXKKK0KKKKKKKKKKKK0OOOOO0KXNWWNNKkc,;ck0OOOOOkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk0XXKxloclOXNNNNXK0KKKKXXXXXXXXXXXXXXXXXXKKKKKK00O0XNNNNNNKkl;,clk0kOOOOOOOOOOkkkkkkk
kkkkkkOOOOOOOOOOKKKKxlolcd0KXXXXXXXNNNXNNNNNNNNNNNNNNXXXXXXXKKKKKKKXXXXXKOdc,:coOOxO0OOOOOOOOOOOOOOk
OOOOOOOOOOOOOOO0KK0XOlcc:lk0KKXNNNNNNNNNNNNNWWWWWWWNNNNNXXXXXXKKKKK0KKK0Oxl,,::d0Odk0OOOOOOOOOOOOOOO
OOOOOOOOOOOOOOO0K00KKkl:;:d0KXXXXXXNNNNNWWWWWWWWWWWWWWNNNXXXXXXKKK00000Oko;'':d00xok0000OOOOOOOOOOOO
OOOOOOOOOOOO00OKKOkOKX0xld0XXKKKXXXNNNNWWWWWWWWWWWWWWWWWWNNNNXXXKK0000Okkdc;oOKKkolx000000000OOOOOOO
OOOOOOOO0O000000KkoxOKXXXXXKKKKXXXXNNNNWWWWWWWWWWWWWWWWWWNNNNXXXKK00OOOkdxkk000Odllk0000000000000OOO
OOOO000000000000KOoldOKXXK000KKKKXXXXNNNWWWWWWWWWWWWWWWWWNNNXXXXK00OkkkdloxkOkkdccdOK0K0000000000000
0000000000000000KKxllkXK0K0kkO0000KKXXNNNNNWWWWWWWWWWNNNNNNNXXKK0Okkxxdl:lddxxdccokKKKKKKKKK00000000
000000000000000KK00xd0K0OOkxddxkOOkOKKXXXXNNNNNNNNNNNXXXXXXXKK0Okxddolc;:llodxocoxk0KKKKKKKKKK000000
000000000KKKKKK0kxdx0K0Okxxxxdooxkkkxk0KKKKKXXKKKKKKKKKKKK000Oxdoool:;,;:cllllcodood0XKKKKKKKKKK0000
000000KKKKKKKKK0kdld00kkxddxO0OkddxkOkkkkkkOO0000000000OOkxxxxxdolc:clll::::::coolokKXXXXXXXXKKKKK00
000KKKKKKKKKKKKKKOxk00xddddk0KKKK0OOOKKK00000KKXXXXXXXK000OO00Okxxxkkkxoc;;;;;:oxk0XXNXXXXXXXXXKKKK0
KKKKKKKKKKKXXXXXXNNXXOddddxO00KKXXXNNNNNNNWWWWWWNNNWWNNNNNNXXXXKKK00Okxdl:,,,,:d0KKKXNNNNNNNNXXXKKKK
KKKKKKKXXXXXXXXXNXNNX0doodkOOkxdddxxkOKXXNNNNNNNNNNNNNNNNNXXK0kddollloool:,'',:dxkkOKNNNNNNNNNXXKKKK
KKKKKXXXXXXXNNNNNK00OkxoldkOkdollcc:;;:cldk0KXXXXXXXXXK0Oxoc:,,,,;:::cclc;,'',:clodOXNNNNNNNNNXXXXKK
KKKXXXXXXXNNNXXXXK0OOkxdodkOOkkkOOOOkdlc::clxO0KKKKK0Oxoc:;;:coxxkkxddool:;,;;:ccox0KKKXXNNNNNNXXXXK
XXXXXXXXXXXK0OkOOOOkOOOkxxxxxxddxxkkkkkxdooooxkO000Okxoloddxxkkkxddoollllllloodxdxkkkxxkk0XNNNNNNNXX
XXXXXXXXXKOOkxddddololllc;,,clcdkdcll;;:ccoddxk000OOkxddddoo:,;;:ll:;;;'.'':lc::;:cccloddxOXNNNNNNNN
XXXXXXXNKOOOOkxddl:;:ccc:,',lodOx;,l:..,,';ldxO0KKK0Oxdoc,,;';c,.;l:;;:'..';:::,'',:cloddxkKNNNNNNNN
XXXXNNNNXOOOkkkkkkdc:c:;;,,oxllo:,....;ol;,codxkOOkkxdol,,c:,c,...;;,:oc..;;;;;''';:lodxxxkKNNNWWNNN
XXNNNNNWNKOOOOkxdol:,',;;,;dxl:::;,,';ldo:;:lllllllllccc,;odc;,,,,,,';xl.';;,'...',;lxkkkk0NWWWWWWWW
NNNNNNWWWX0OO0Oxl:,''.',:;;oxlcc:;;;:clloc::::lxkkkko:::,;odoc:;;;;;,cdc',;,'.....',lkOOkOKWWWWWWWWW
NNNNNNWWN0xxxxxxxol:,'',;::colcc::::::cc:;;:;:kXXXXXOl;;;,;:ccc:;::;;cc;::,,......':ldxxxdOXWWWWWWWW
NNWWWWWNKxooooddddxdc;,,;:cllc;,,,,,,;;;;::;;oO0XXK0kdc;;:;,,,,,,,',:cll:;,'....',;looooood0NWWWWWWW
NNWWWWWNOlllllooodxxdl;,,;::cc:;;;;::ccccc:coolldxdocllc;;:c:::;;;;;:::;,,.....';:cllllllllkNWWWWWWW
NNNNNNWXxcccccllldxxxdlc:;oo::;,,,;;;;;::lx0kc,''','.':xxl:;,;;;,,,,,;,''.....';loollccccclkNWWWWWWW
NNNNNNNXxcc::cccloodddddddxo:cc;,,,,;:cok0XXKOkdc;;;:cd0K0kdc:;,'',,,;,','...',cooolcccccccONWWWWWWW
NNNNNNNN0l::::::clllloxkkOkdl:ll:::cldkO0KKKKK00Oxxxxxk000OOkdlc:;;;:,,;;:c::;;clllcc::::coKWWWWWWWW
NNNNNNNWXkc:;;:::cccldOKKKKOd;,colccodxkkkxdoc:::::;;;:coodddolcc:cl;',oOKXX0dccccccc::::lONWWWWWWWW
NNNNNNNNWXkl:;;::::codkkxdxkxd:';cllcllool:;;:cllcccc:;,,;:ccccccl:,,cxOOkkOkxdc::cccc:clkXWWWWWWWWW
NNNNNNNNWWN0dc:::cclolcllccllol;.';cllc::ccclccccccccc::c::::clc:,..;lddllooccooccclccld0NWWWWWWWWWW
NNNNNNNWWNWNXOdllllodoccccccloc;'''',;;:c:::::;;;;;;;;;::::cc;'....';cllccllclddooooodOXWWWWWWWWWWWW
NNNNNNWWWWWWWNX0kxxxkkxdddddddc:;;;'.  .';cccloddddoolcccc;,.   ..,;:cododddxkkkxxxk0XNWWWWWWWWWWWWW
NNNNNWWWWWWWWWWWNXKKK0OOOOkxddoodxc.     ..,:clooooollc;,...     .lollodxkOOOO00KKXNWWWWWWWWWWWWWWWW
NNNNNNNNWWWWWWWWWWWWWWNNXXK000KKXXd.     .....',,,,,,'.....      .,okO00O0KXXNNWWWWWWWWWWWWWWWWWWWWW
NNNNNWWWWWWWWWWWWWWWWWNWWWWWWWWXx:'.      ................         .,dKWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
NNNWWWWWWWWWWWWWWWWWWWWWWWWWNN0l.   .       ............             .:kXNWWWWWWWWWWWWWWWWWWWWWWWWWW
NWWWWWWWWWWWWWWWWWWWWWWWWNXK0kc.                 ...                 ..':okKNWWWWWWWWWWWWWWWWWWWWWWW
NNNWWWWWWWWWWWWWWWWWWNXKOxxxxo,.                                      .....,:ox0XNWWWWWWWWWWWWWWWWWW
NNWWWWWWWWWWWWWWWNXKOxlcclodoc'                                        ........':ldOXNWWWWWWWWWWWWWW
WWWWWWWWWWWWWNNKOxol::::clooc;.                                       ............',:lx0XNWWWWWWWWWW
WWWWWWWWWWNX0kdlccc::::ccllc:,.    ...                               ..............''',;cd0NWWWWWWWW
WWNWWWWNX0kdllccccc::ccccccc:,.  ...';,...                 ...''..   ..''''.........''',,;:oONWWWWWW
WWWNWWNKkoollcc::::::cccccc::,.  ....cxxoc;,'...........',;:lol,.......',,,,,''.....''',;;::lxXWWWWW
NNWWWWXkollc:::::::::::::::::;.. ....'dOOOOkxdddooooooddxxxkkkc.......'',,,;;;,,'''''',,;;:c:ckXWWWW
NNWWWXkolcc:::::;::::::::::::;'. .....;x00O000OOOOOOOOOOOOOOOl'.......',,,,;;;;;;;,,,,,;;;;:::lONWWW
NWWWN0occ::::;;;;;;;:;;::::::,.  ......:OKK00000000000000000d'........,,;;,,,;;;;;;;;,,,;;;;;;:dXWWW
NNWWNOl::;;;;;;;;;,,;;;::;;:;.   .......o0KKKKKKKKKKKKKKKKKk;.........,;;;,,,;;,,,,,,,,,,,,,,,;l0WWW
        """
        print(portrait + "\n" + assistant_reply)
        
        # 【步骤7：检查AI回复是否表示结束】
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    
