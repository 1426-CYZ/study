import streamlit as st
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
# 记忆文件夹路径
MEMORY_FOLDER = "4.2_memory_clonebot"

# 【修改1：更新角色-记忆文件映射】
# 新增“洪梽炫”角色对应的记忆文件
ROLE_MEMORY_MAP = {
   
     "任小妹": "rzm_memory.json", # 新增：对应聊天记录的记忆文件
     "1426": "rzm_memory.json" 
}
    

# ========== 初始记忆系统 ==========

# ========== 主程序 ==========

def get_portrait():
    """返回角色头像的ASCII艺术"""
    return """
00KKKKKKKKKKKKKKKXXXXXXXXXXXXXXXXXXXXXNNNNNNNNNXXKXXNNNNNNNNXkooolodddxdldk0K0OOkkkdlclcc::::;;;;;;;
000KKKKKKKKXXXXXXXXXXXXXXXXXXXXXXNXXNNXXNXNNNNKkx0XNNNXOxkO0OdllllllllllodO0XXNNXOOOxollcccc:::;;;;,
KKKKKKKKKKXXXXXXXXXNNNNNNNNNNNNNNNNNNNXXXXNNNXkodKNNNXkllllllcccccccclllodxk0NWWNKOkdlllllcc:::;;;;;
XXKKXXXXXXXXXXXXXXXNNNNNNNNNNNNNNNNNNKOkkkO00kxook00kdollllcc::c::cccclloxO0KNX0OOxdollllcccc:::::::
XXXXXXXXXXXXXXNNXXXNNNNNNXNNNNNNNNNNNXXXK0OOOxdddollllcccccccccccccccclloxxxk0XKkdoollcccccc:::::;;;
NNNXXXNNNNNNNNNNNNNNNNNNNNXXXXXXXNNNXNNNNNNNNXKK0kxdlcccccccccccccc:cccclcclldO0xooolcc::::::::::;;;
KXXOxk0KKXNNNXXK00KXXXKKXXXKKK0OOO0OOkkkkO0KNNNXKK0Odlcc:::cccccccc::::ccccclodollllccc::::::::;;;;,
kO0OxxxxOKXXXKK0000KK0OkkO0K00KK0kxxdoodddxOKNWNX00kollcccc::ccccccc::::cccccccccccc:::::::::::::::c
ddxkkkxxkO00000KX0kxkO00OkOOOkkOOOkkOOkkO0KKXNNNNNN0dlcccccc::ccccc::::::::::ccc::c:::::::::::::::cc
dddxxxxxxxxxxxkk0K0kxdxxxkkkOkxddxxxkkO0000OkkkOKXX0kollccc::::::::::::::::::::c::::::ccccccccccccll
xxxdxxxdddxxxkkkOOOOOkxxxxxxxxxdooddddddxxxxdxxO00OOOxdoolllcccccccccccccccclllccccccccllllodxxOOkkk
O0OO00OOOOOOO000000000000000000000OOOkkkkOO00OOOkkkkkOkxxddddoooooodddddddddxxkkkxdddddxxxk0XXKXXK0O
doodoxOOxxO00000000OkollldkO00000KKKKKK0KKKKKKKKKKKKK00OOOOO00O0000KKKKKKKKKXXXXK0OOOOOkkkkOK00000OO
';:;,,;,,,cooloxxkkxc,''',:cllllloxkkkOOOOOOO0OOOOOOOOOkOOOOOOO0000000000000000OkOOOOOOkkkkO00OO0OOO
...','.....'..'',;cc;'',,,,,,;;:;,;cllloddxkxxxxxddddoooolllllllllllllllllccc::;;;;,,,,,,,,''''
............''''',::;,,;;;;,,,,,,';clllccldxkkkkkkkxxxddddooooooooooddddddoolc::;;;,,,,,,,,,,''
,,,;;;;;;;:cllodddl:,,,,,,'''',,';::cc,';:clccdkkkkkkkkkxxxddddoooooooddddxxxddolcc::;;;,,,,,,,,,,''
odddddxxkkOOO000Oo;,,,'''......''';::;..''';,..okOOkkkkkkxxxddddoooooooodddxxxdoolcc:::;;;,,,,,,,,,,
xxkkkOOO00000Odol:,''............',;;;.. ...',.,xOOOkkkkkxxxddddoooooooodddxxxdoolcc:::;;;,,,,,,,,,,
kkOOOO00000Oxl:,;c:;;;;;,,'........',;;,'.....;;cxOOkkOkkkxxxxddddoddoooodddddddolcc::;;;;;,,,,,,,,,
kkkOOO00Oxc,'',:c::;;,,;;;,........',,,,,,,;:c;oOOOOOOkkkkxxxxddodddddddddxxxxddolcc::;;;;;,,,,,,,,,,
xxxxkkOko;',;::;,,,,,,,,,,,,'.......',,,;;:::;;d00OO0OOOkkkxxxdddddddddddddddddoolc:::;;;,,,,,,,,,,,
kkkkkko:',:;'.........................'''',,,;lxkkkkkkkkxxxxdddddddddddxxxxxxxdollc:::;;;,,,,,,,,,,,
OOOOOo,';:;''....... ...    .'............',,cxOOkkkkkxxddddddoooooooddddxxkkkxdolllc::;;;;;;;;;,,,,
kkxxo,':;''''''.............'...........''';oOKK0OOOOOkkkkxxxddoooooollccclllllllcccc::;;;;;;;;;;;,,
xxxo,,:;,,,,,'''''.....................',;lk0KKKK00OOkkkkxxxxddddoodddddxxxxxddooodolccc:;;;;;;;,,,,
OOd,':;'',,,,,,,,''''..................',:dO000000OOOkkkkkxxxxdddddddddddddxxdoll::;;::;;;;;;;,,,,,,
OOc.;;,,,,,,;;,,,'''......       .....'';:ldOOO00OOOOkxxkxxxddddddddddddddddolclllc::::;;;;;;;,,,,,,
ko,';,,,,;;,;,,'''..';l:.        ......';:ldkOOOOOOkkkxxxxxddddoodddddxxxxxddooodolccc:;;;;;;;,,,,,,
o:.,;,,,,;,,;,.',;codkd,...............'',:oxxxxxxxxxxxxdddddddooooooodddddddooolcccllc::;;;;;;;,,,,
,..,,',,,',clllodxkOkd;''..............',,;:lddddxxxxxxddddddddoooddooooolooooolc:ccccc:;;;;;;;;,,,,
'...'''''':ooolclooxxc................'''',;:oxxxxxxdddddddoooooodddddddooodoolllcc::ccc:;;:;;;;,,,,
''..''....''''.'',;c:'. ........... ...'''',,;clddddddddoc;;:llllllloodddddddddolcllcccc:::;;;;,,,,,,
'''.....'''''.....,:;...................',,',;;;cdxxkkkkxoccooooolclclllllcloddoolccllc::::;;;;;;,,''
c:;;,,''''.'''''',;;,.'''..'''''....'.......',,,;ldxkxxkxxkxxxddddddooooolccccloodolllcccc:;;;;;;,,,,
llccccc::;;,,'''';:,','..''..'''''.';;,.....'''',:cllcoolldxkxxxdoodxxddxxdoc;;:cllllooodxxocc::;;;;
lcc::cccccccc::;;c:'....'''...'''''';::;'....'',';:;.....';:coddccoddoooodxdollolcccll:;:loxxxxddool
lllccccccccccccccc,....''...''''''',;:cc:,'....'',;'.       ..,,''';;,;cllddxddddollooccccloc:cloddd
ooolllccllcccccclc,....''.'''''''',,;;cccc:;'......';::;;'.... ...  ...'cooodollloddolllllollcclllll
lllllllcclcccllloc,',,,,''''''''..',;;:ccccc:,.'..,;:;,;:c;...........  .,:c:....,;cloooolllollllllo
lllllllllllllllllc;,,'''.....'''''',;;;:ccllc,,,'',,'.''',::,.''.''....... ..      .,clcll::clccllll
ooooooollllcccc:;;;,''..........''..,;;;::::,',,'...'.....';,.';;,'',,'..............,,',:..,c:,,,,,
lllllcccccccc::;;;;'..........'''....',,,,;;,,'.'...'.....',;'';;;,,;;,'.''''...'''''.'......'...   
c::ccccccccc:;;;::,............''',''..''''','..,'.........,;::;;'.... ...  ...'cooodollloddolllllol
"""

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
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
     # 【修改2：新增“洪梽炫”的人格设定】
         
        "任小妹": """
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
        """     
            
            }
    
    personality = role_personality.get(role_name, "你是我的闺蜜。")
    
    # ========== 第三步：整合记忆和人格 ==========
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
# 【修改3：选择“洪梽炫”角色】
role_system = roles("任小妹")

# 【结束对话规则】
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

# ========== Streamlit Web 界面 ==========
st.set_page_config(
    page_title="AI角色扮演聊天",
    page_icon="🎭",
    layout="wide"
)

# 初始化 session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "任小妹"
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# 页面标题
st.title("🎭 AI角色扮演聊天")
st.markdown("---")

# 侧边栏：角色选择和设置
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 角色选择
    selected_role = st.selectbox(
        "选择角色",
        ["任小妹", "1426"],
        index=0 if st.session_state.selected_role == "1426" else 1
    )
    
    # 如果角色改变，重新初始化对话
    if selected_role != st.session_state.selected_role:
        st.session_state.selected_role = selected_role
        st.session_state.initialized = False
        st.session_state.conversation_history = []
        st.rerun()
    
    # 清空对话按钮
    if st.button("🔄 清空对话"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 说明")
    st.info(
        "- 选择角色后开始对话\n"
        "- 对话记录不会保存\n"
        "- AI的记忆基于初始记忆文件"
    )

# 初始化对话历史（首次加载或角色切换时）
if not st.session_state.initialized:
    role_system = roles(st.session_state.selected_role)
    system_message = role_system + "\n\n" + break_message
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]
    st.session_state.initialized = True

# 显示对话历史
st.subheader(f"💬 与 {st.session_state.selected_role} 的对话")

# 显示角色头像（在聊天窗口上方）
st.code(get_portrait(), language=None)
st.markdown("---")  # 分隔线

# 显示历史消息（跳过 system 消息）
for msg in st.session_state.conversation_history[1:]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

# 用户输入
user_input = st.chat_input("输入你的消息...")

if user_input:
    # 检查是否结束对话
    if user_input.strip() == "再见":
        st.info("对话已结束")
        st.stop()
    
    # 添加用户消息到历史
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_input)

# 【系统消息】
system_message = role_system + "\n\n" + break_message

# ========== 对话循环 ==========
try:
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        if user_input in ['再见']:
            print("对话结束")
            break
        
        conversation_history.append({"role": "user", "content": user_input})
        
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        portrait = """
00KKKKKKKKKKKKKKKXXXXXXXXXXXXXXXXXXXXXNNNNNNNNNXXKXXNNNNNNNNXkooolodddxdldk0K0OOkkkdlclcc::::;;;;;;;
000KKKKKKKKXXXXXXXXXXXXXXXXXXXXXXNXXNNXXNXNNNNKkx0XNNNXOxkO0OdllllllllllodO0XXNNXOOOxollcccc:::;;;;,
KKKKKKKKKKXXXXXXXXXNNNNNNNNNNNNNNNNNNNXXXXNNNXkodKNNNXkllllllcccccccclllodxk0NWWNKOkdlllllcc:::;;;;;
XXKKXXXXXXXXXXXXXXXNNNNNNNNNNNNNNNNNNKOkkkO00kxook00kdollllcc::c::cccclloxO0KNX0OOxdollllcccc:::::::
XXXXXXXXXXXXXXNNXXXNNNNNNXNNNNNNNNNNNXXXK0OOOxdddollllcccccccccccccccclloxxxk0XKkdoollcccccc:::::;;;
NNNXXXNNNNNNNNNNNNNNNNNNNNXXXXXXXNNNXNNNNNNNNXKK0kxdlcccccccccccccc:cccclcclldO0xooolcc::::::::::;;;
KXXOxk0KKXNNNXXK00KXXXKKXXXKKK0OOO0OOkkkkO0KNNNXKK0Odlcc:::cccccccc::::ccccclodollllccc::::::::;;;;,
kO0OxxxxOKXXXKK0000KK0OkkO0K00KK0kxxdoodddxOKNWNX00kollcccc::ccccccc::::cccccccccccc:::::::::::::::c
ddxkkkxxkO00000KX0kxkO00OkOOOkkOOOkkOOkkO0KKXNNNNNN0dlcccccc::ccccc::::::::::ccc::c:::::::::::::::cc
dddxxxxxxxxxxxkk0K0kxdxxxkkkOkxddxxxkkO0000OkkkOKXX0kollccc::::::::::::::::::::c::::::ccccccccccccll
xxxdxxxdddxxxkkkOOOOOkxxxxxxxxxdooddddddxxxxdxxO00OOOxdoolllcccccccccccccccclllccccccccllllodxxOOkkk
O0OO00OOOOOOO000000000000000000000OOOkkkkOO00OOOkkkkkOkxxddddoooooodddddddddxxkkkxdddddxxxk0XXKXXK0O
doodoxOOxxO00000000OkollldkO00000KKKKKK0KKKKKKKKKKKKK00OOOOO00O0000KKKKKKKKKXXXXK0OOOOOkkkkOK00000OO
';:;,,;,,,cooloxxkkxc,''',:cllllloxkkkOOOOOOO0OOOOOOOOOkOOOOOOO0000000000000000OkOOOOOOkkkkO00OO0OOO
...','.....'..'',;cc;'',,,,,,;;:;,;cllloddxkxxxxxddddoooolllllllllllllllllccc::;;;;,,,,,,,,''''
............''''',::;,,;;;;,,,,,,';clllccldxkkkkkkkxxxddddooooooooooddddddoolc::;;;,,,,,,,,,,''
,,,;;;;;;;:cllodddl:,,,,,,'''',,';::cc,';:clccdkkkkkkkkkxxxddddoooooooddddxxxddolcc::;;;,,,,,,,,,,''
odddddxxkkOOO000Oo;,,,'''......''';::;..''';,..okOOkkkkkkxxxddddoooooooodddxxxdoolcc:::;;;,,,,,,,,,,
xxkkkOOO00000Odol:,''............',;;;.. ...',.,xOOOkkkkkxxxddddoooooooodddxxxdoolcc:::;;;,,,,,,,,,,
kkOOOO00000Oxl:,;c:;;;;;,,'........',;;,'.....;;cxOOkkOkkkxxxxddddoddoooodddddddolcc::;;;;;,,,,,,,,,
kkkOOO00Oxc,'',:c::;;,,;;;,........',,,,,,,;:c;oOOOOOOkkkkxxxxddodddddddddxxxxddolcc::;;;;;,,,,,,,,,
xxxxkkOko;',;::;,,,,,,,,,,,,'.......',,,;;:::;;d00OO0OOOkkkxxxdddddddddddddddddoolc:::;;;,,,,,,,,,,,
kkkkkko:',:;'.........................'''',,,;lxkkkkkkkkxxxxdddddddddddxxxxxxxdollc:::;;;,,,,,,,,,,,
OOOOOo,';:;''....... ...    .'............',,cxOOkkkkkxxddddddoooooooddddxxkkkxdolllc::;;;;;;;;;,,,,
kkxxo,':;''''''.............'...........''';oOKK0OOOOOkkkkxxxddoooooollccclllllllcccc::;;;;;;;;;;;,,
xxxo,,:;,,,,,'''''.....................',;lk0KKKK00OOkkkkxxxxddddoodddddxxxxxddooodolccc:;;;;;;;,,,,
OOd,':;'',,,,,,,,''''..................',:dO000000OOOkkkkkxxxxdddddddddddddxxdoll::;;::;;;;;;;,,,,,,
OOc.;;,,,,,,;;,,,'''......       .....'';:ldOOO00OOOOkxxkxxxddddddddddddddddolclllc::::;;;;;;;,,,,,,
ko,';,,,,;;,;,,'''..';l:.        ......';:ldkOOOOOOkkkxxxxxddddoodddddxxxxxddooodolccc:;;;;;;;,,,,,,
o:.,;,,,,;,,;,.',;codkd,...............'',:oxxxxxxxxxxxxdddddddooooooodddddddooolcccllc::;;;;;;;,,,,
,..,,',,,',clllodxkOkd;''..............',,;:lddddxxxxxxddddddddoooddooooolooooolc:ccccc:;;;;;;;;,,,,
'...'''''':ooolclooxxc................'''',;:oxxxxxxdddddddoooooodddddddooodoolllcc::ccc:;;:;;;;,,,,
''..''....''''.'',;c:'. ........... ...'''',,;clddddddddoc;;:llllllloodddddddddolcllcccc:::;;;;,,,,,
'''.....'''''.....,:;...................',,',;;;cdxxkkkkxoccooooolclclllllcloddoolccllc::::;;;;;;,,'
c:;;,,''''.'''''',;;,.'''..'''''....'.......',,,;ldxkxxkxxkxxxddddddooooolccccloodolllcccc:;;;;;;,,,
llccccc::;;,,'''';:,','..''..'''''.';;,.....'''',:cllcoolldxkxxxdoodxxddxxdoc;;:cllllooodxxocc::;;;;
lcc::cccccccc::;;c:'....'''...'''''';::;'....'',';:;.....';:coddccoddoooodxdollolcccll:;:loxxxxddool
lllccccccccccccccc,....''...''''''',;:cc:,'....'',;'.       ..,,''';;,;cllddxddddollooccccloc:cloddd
ooolllccllcccccclc,....''.'''''''',,;;cccc:;'......';::;;'.... ...  ...'cooodollloddolllllollcclllll
lllllllcclcccllloc,',,,,''''''''..',;;:ccccc:,.'..,;:;,;:c;...........  .,:c:....,;cloooolllollllllo
lllllllllllllllllc;,,'''.....'''''',;;;:ccllc,,,'',,'.''',::,.''.''....... ..      .,clcll::clccllll
ooooooollllcccc:;;;,''..........''..,;;;::::,',,'...'.....';,.';;,'',,'..............,,',:..,c:,,,,,
lllllcccccccc::;;;;'..........'''....',,,,;;,,'.'...'.....',;'';;;,,;;,'.''''...'''''.'......'...   
c::ccccccccc:;;;::,............''',''..''''','..,'.........,;::;;'.... ...  ...'cooodollloddolllllol
lllllllllllllllllc;,,'''.....'''''',;;;:ccllc,,,'',,'.''',::,.''.''....... ..      .,clcll::clccllll
ooooooollllcccc:;;;,''..........''..,;;;::::,',,'...'.....';,.';;,'',,'..............,,',:..,c:,,,,,
lllllcccccccc::;;;;'..........'''....',,,,;;,,'.'...'.....',;'';;;,,;;,'.''''...'''''.'......'...   
c::ccccccccc:;;;::,............''',''..''''','..,'.........,;::;;'.... ...  ...'cooodollloddolllllol
lllllllllllllllllc;,,'''.....'''''',;;;:ccllc,,,'',,'.''',::,.''.''....... ..      .,clcll::clccllll
ooooooollllcccc:;;;,''..........''..,;;;::::,',,'...'.....';,.';;,'',,'..............,,',:..,c:,,,,,
lllllcccccccc::;;;;'..........'''....',,,,;;,,'.'...'.....',;'';;;,,;;,'.''''...'''''.'......'...   
c::ccccccccc:;;;::,............''',''..''''','..,'.........,;::;;'.... ...  ...'cooodollloddolllllol
"""
        print(portrait + "\n" + assistant_reply)
        
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    print("\n\n程序被用户中断")
except Exception as e:
    print(f"\n\n发生错误: {e}")
