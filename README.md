Python基础知识总结
==================

本文档总结了项目中所有Python文件（`001.py`、`003.py`、`004.0.py`、`004.1.py`、`004.2.py`、`005.0.py`）涵盖的Python基础知识。

## 1. 变量与赋值

### 1.1 变量定义（`001.py`、`003.py`、`004.0.py`等）

- **变量赋值**：Python使用 `=` 进行变量赋值，无需声明类型
  ```python
  name = "Yanzhen Chen"
  x = "1"
  y = "2"
  user_input = input("请输入你要说的话：")
  ```

- **变量命名**：遵循标识符命名规则，区分大小写
- **动态类型**：Python是动态类型语言，变量类型由赋值决定

### 1.2 全局变量（`004.2.py`）

- **global关键字**：在函数内修改全局变量需要使用 `global` 声明
  ```python
  def advance_role():
      global current_role_index, current_role, conversation_history
      current_role_index = (current_role_index + 1) % len(ROLE_SEQUENCE)
  ```

## 2. 字符串操作

### 2.1 字符串创建（`001.py`）

- **字符串字面量**：使用单引号或双引号定义字符串
  ```python
  name = "Yanzhen Chen"
  x = "1"
  ```

### 2.2 字符串拼接（`001.py`、`003.py`）

- **+ 运算符**：连接字符串
  ```python
  print(x + y)  # 输出 "12"（字符串拼接，非数值相加）
  content = role_system + user_input
  ```

### 2.3 f-string格式化（`001.py`、`003.py`、`004.1.py`、`004.2.py`）

- **f-string**：使用 `f"..."` 在字符串中嵌入变量
  ```python
  print(f"Hello, {name}!")
  print(f"你识破了{matched_role}！当前进度：{len(guessed_roles)}/{len(ROLE_SEQUENCE)}。")
  ```

### 2.4 字符串方法（`004.1.py`、`004.2.py`）

- **strip()**：去除字符串首尾空白字符
  ```python
  cleaned_input = user_input.strip()
  stripped_input = user_input.strip()
  ```

- **rstrip()**：去除字符串右侧空白字符
  ```python
  assistant_reply = f"{assistant_reply.rstrip()} {action_tail}"
  ```

- **in 操作符**：检查子字符串是否在字符串中
  ```python
  if "恭喜你" in reply or "猜对了" in reply:
  if "恭喜，回答正确" in assistant_reply:
  ```

## 3. 输入输出

### 3.1 print()函数（`001.py`、`003.py`、`004.0.py`等）

- **输出内容**：输出内容到控制台
  ```python
  print("Hello, World!")
  print(reply)
  print("=" * 50)  # 重复字符串50次
  ```

### 3.2 input()函数（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **获取用户输入**：从用户获取输入，返回字符串类型
  ```python
  user_input = input("请输入你要说的话：")
  user_input = input("请提问：")
  ```

## 4. 模块导入

### 4.1 import语句（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **导入标准库或第三方模块**
  ```python
  import requests
  import json
  import random
  import re
  ```

### 4.2 from...import语句（`003.py`、`004.1.py`、`004.2.py`）

- **从模块中导入特定内容**
  ```python
  from requests.utils import stream_decode_response_unicode
  from xunfei_tts import text_to_speech
  ```

## 5. 数据结构

### 5.1 列表（List）

#### 列表创建（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **使用方括号 `[]` 定义**
  ```python
  messages = [
      {"role": "user", "content": role_system + user_input}
  ]
  ROLE_NAMES = list(ROLE_PROMPTS.keys())  # 将字典的键转换为列表
  ROLE_SEQUENCE = list(ROLE_PROMPTS.keys())
  ```

#### 列表索引（`003.py`、`004.0.py`等）

- **使用索引访问元素（从0开始）**
  ```python
  result['choices'][0]  # 访问列表第一个元素
  current_role = ROLE_SEQUENCE[current_role_index]
  ```

#### 列表推导式（`004.1.py`）

- **简洁创建列表**
  ```python
  other_roles = [role for role in ROLE_NAMES if role != current_role]
  ```

### 5.2 字典（Dictionary）

#### 字典创建（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **使用花括号 `{}` 定义键值对**
  ```python
  headers = {
      "Authorization": "...",
      "Content-Type": "application/json"
  }
  
  ROLE_PROMPTS = {
      "盲眼诗人": "你是一个盲眼的吟游诗人...",
      "跟踪诗人的狂热暗恋者": "你是一个暗中跟踪诗人的狂热暗恋者..."
  }
  ```

#### 字典访问（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **通过键访问值**
  ```python
  result['choices'][0]['message']['content']
  role_system[current_role]["system_prompt"]
  ROLE_ACTION_TAILS.get(current_role, "")  # 使用get()方法，提供默认值
  ```

#### 嵌套字典（`004.0.py`）

- **字典中可以嵌套字典**
  ```python
  role_system = {
      "诗人": {
          "keywords": ["诗歌", "诗句", "诗词"],
          "system_prompt": "你是一个看不见的诗人..."
      },
      "跟踪诗人的人": {
          "keywords": ["跟踪", "监视", "观察"],
          "system_prompt": "你是一个暗中跟踪诗人的..."
      }
  }
  ```

#### 字典推导式（`004.2.py`）

- **简洁创建字典**
  ```python
  role_histories = {role: build_conversation(role) for role in ROLE_SEQUENCE}
  ```

### 5.3 集合（Set）（`004.2.py`）

- **集合创建**：使用 `set()` 创建空集合，集合天然去重
  ```python
  guessed_roles = set()
  ```

- **集合操作**：
  ```python
  guessed_roles.add(current_role)  # 添加元素
  if role in guessed_roles:  # 检查元素是否存在
  len(guessed_roles)  # 获取集合长度
  ```

### 5.4 嵌套结构（`003.py`、`004.0.py`、`004.2.py`）

- **列表和字典可以嵌套使用**
  ```python
  result['choices'][0]['message']['content']  # 字典->列表->字典->键
  ROLE_EXAMPLES = {
      "盲眼诗人": [
          {"role": "user", "content": "你现在身在何处？"},
          {"role": "assistant", "content": "雨丝落在铁门上..."}
      ]
  }
  ```

## 6. 函数定义与调用

### 6.1 函数定义（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **使用 `def` 关键字定义函数**
  ```python
  def call_zhipu_api(messages, model="glm-4-flash"):
      # 函数体
      return response.json()
  ```

### 6.2 函数参数

- **位置参数**：`messages`
- **默认参数**：`model="glm-4-flash"`（调用时可省略）
- **类型提示**（`004.2.py`）：
  ```python
  def build_role_anchor(role_name: str) -> str:
      return f"你必须扮演{role_name}..."
  ```

### 6.3 函数返回值

- **使用 `return` 返回结果**
  ```python
  return response.json()
  return history
  ```

### 6.4 函数调用

- **通过函数名和参数调用**
  ```python
  result = call_zhipu_api(messages)
  conversation_history = build_conversation(role_name)
  text_to_speech(assistant_reply)
  ```

## 7. 控制流

### 7.1 条件判断

#### if语句（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **根据条件执行代码**
  ```python
  if response.status_code == 200:
      return response.json()
  else:
      raise Exception(...)
  ```

#### 比较运算符

- **`==`（等于）、`!=`（不等于）、`in`（成员运算符）**
  ```python
  if reply == "好的，我们有缘再见。":
  if "恭喜你" in reply or "猜对了" in reply:
  if role != current_role or role in guessed_roles:
  ```

#### 逻辑运算符

- **`and`、`or`、`not`**
  ```python
  if role != current_role or role in guessed_roles:
  if "恭喜你" in reply or "猜对了" in reply:
  ```

### 7.2 循环

#### while循环（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **当条件为真时重复执行**
  ```python
  while True:  # 无限循环
      user_input = input("请提问：")
      if 条件:
          break  # 退出循环
  ```

#### for循环（`004.1.py`、`004.2.py`）

- **遍历序列（列表、字典等）**
  ```python
  for role, keywords in ROLE_KEYWORDS.items():  # 遍历字典
      if contains_role_guess(cleaned_input, keywords):
          matched_role = role
          break
  
  for _ in range(len(ROLE_SEQUENCE)):  # 使用range()生成数字序列
      current_role_index = (current_role_index + 1) % len(ROLE_SEQUENCE)
  ```

#### break语句（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

- **跳出循环**
  ```python
  if reply == "好的，我们有缘再见。":
      print("对话结束。")
      break
  ```

#### continue语句（`004.1.py`、`004.2.py`）

- **跳过当前循环，继续下一轮**
  ```python
  if cleaned_input == "下一个角色":
      advance_role()
      continue  # 跳过后续代码，继续下一轮循环
  ```

#### return语句（`004.2.py`）

- **在函数中提前返回，也可用于退出循环逻辑**
  ```python
  def advance_role():
      if len(guessed_roles) == len(ROLE_SEQUENCE):
          return  # 提前返回
      for _ in range(len(ROLE_SEQUENCE)):
          if candidate not in guessed_roles:
              current_role = candidate
              return  # 找到后立即返回
  ```

## 8. 随机数模块（`004.0.py`、`004.1.py`、`004.2.py`）

### 8.1 random模块

- **导入模块**：`import random`
- **random.choice()**：从序列中随机选择一个元素
  ```python
  current_role = random.choice(list(role_system.keys()))
  current_role = random.choice(ROLE_NAMES)
  ```

- **random.randrange()**：生成指定范围内的随机整数
  ```python
  current_role_index = random.randrange(len(ROLE_SEQUENCE))
  ```

## 9. 正则表达式（`004.2.py`）

### 9.1 re模块

- **导入模块**：`import re`
- **re.sub()**：正则替换
  ```python
  normalized = re.sub(r"\s+", "", user_text)  # 去除所有空白字符
  ```

- **正则表达式模式**：
  - `r"\s+"`：匹配一个或多个空白字符
  - 使用原始字符串（r"..."）避免转义问题

## 10. 异常处理（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

### 10.1 raise语句

- **主动抛出异常**
  ```python
  raise Exception(f"API调用失败: {response.status_code}, {response.text}")
  ```

- **异常信息**：使用f-string格式化异常消息

## 11. HTTP请求（`003.py`、`004.0.py`、`004.1.py`、`004.2.py`）

### 11.1 requests库

- **POST请求**：使用 `requests.post()` 发送HTTP POST请求
  ```python
  response = requests.post(url, headers=headers, json=data)
  ```

- **请求参数**：
  - `url`：请求地址
  - `headers`：请求头（字典格式）
  - `json`：JSON格式的请求体（自动序列化）

- **响应处理**：
  - `response.status_code`：HTTP状态码
  - `response.json()`：解析JSON响应为Python字典
  - `response.text`：获取响应文本

## 12. 代码注释

### 12.1 单行注释（`003.py`、`004.0.py`等）

- **使用 `#` 开头**
  ```python
  # 多轮对话循环，直到用户输入 '再见' 结束
  # 游戏设置
  ```

### 12.2 行内注释

- **在代码行末尾添加说明**
  ```python
  while True:  # 表示"当条件为真时一直循环"
  ```

### 12.3 注释掉的代码

- **使用 `#` 注释掉暂时不用的代码**
  ```python
  #while True:  # 表示"当条件为真时一直循环"
  # role_system = ["你是一个看不见的诗人..."]
  ```

## 13. 代码组织

### 13.1 代码执行顺序

- **从上到下顺序执行**

### 13.2 作用域

- **函数内部定义的变量在函数外部不可访问**
- **使用 `global` 关键字在函数内修改全局变量**

### 13.3 代码复用

- **通过函数封装重复逻辑**
- **使用字典、列表等数据结构组织相关数据**

### 13.4 模块化设计（`004.1.py`、`004.2.py`）

- **将功能拆分为多个函数**
  ```python
  def build_game_system(role_name: str) -> str:
      # 构建游戏系统提示词
  
  def build_conversation_history(role_name: str):
      # 构建对话历史
  
  def print_intro():
      # 打印游戏介绍
  ```

## 14. 字符串格式化与拼接技巧

### 14.1 多行字符串（`004.1.py`、`004.2.py`）

- **使用三引号定义多行字符串**
  ```python
  return f"""你正在玩"谁是卧底"游戏。你的身份是：{role_name}

游戏规则：
1. 用户会通过提问来猜测你的身份
2. 你可以通过暗示、描述、举例等方式来回答
...
"""
  ```

### 14.2 字符串重复（`004.1.py`、`004.2.py`）

- **使用 `*` 运算符重复字符串**
  ```python
  print("=" * 50)  # 输出50个等号
  ```

## 15. 高级特性

### 15.1 列表/字典方法

- **list()**：将其他序列转换为列表
  ```python
  ROLE_NAMES = list(ROLE_PROMPTS.keys())
  ```

- **dict.get()**：安全获取字典值，提供默认值
  ```python
  action_tail = ROLE_ACTION_TAILS.get(current_role, "")
  ```

### 15.2 模运算（`004.2.py`）

- **使用 `%` 进行模运算，实现循环索引**
  ```python
  current_role_index = (current_role_index + 1) % len(ROLE_SEQUENCE)
  ```

### 15.3 条件表达式与逻辑判断

- **使用 `or` 提供默认值**
  ```python
  if not other_roles:
      print("目前只有这一个角色，无法切换。")
  ```

## 16. 类与面向对象（`xunfei_tts.py`）

- **class 定义类**：使用 `class 类名(object):` 定义一个类，并在 `__init__` 中初始化属性  
  ```python
  class Ws_Param(object):
      def __init__(self, APPID, APIKey, APISecret, Text):
          self.APPID = APPID
          self.APIKey = APIKey
          self.APISecret = APISecret
          self.Text = Text
  ```

- **实例属性**：通过 `self.xxx` 访问和保存每个实例自己的数据  

## 17. typing 类型提示与泛型容器（`memory-decoupling/*.py`）

- **基础类型提示**：使用 `变量名: 类型` 来标注函数参数和返回值  
  ```python
  from typing import List, Dict, Any

  def call_zhipu_api(messages: List[Dict[str, Any]], model: str = "glm-4-flash") -> Dict[str, Any]:
      ...
  ```

- **容器类型**：`List[Dict[str, Any]]` 表示“由字典组成的列表”，`Dict[str, Any]` 表示“键为字符串、值为任意类型的字典”。  

## 18. 包与相对导入（`memory-decoupling/*.py`）

- **包结构**：通过目录+模块划分功能，例如 `memory-decoupling/api.py`、`memory-decoupling/chat.py` 等  

- **相对导入（同一包内）**：使用 `from .模块 import 名称` 导入同一包中的其他模块  
  ```python
  from .api import call_zhipu_api
  from .memory import load_memory, save_memory
  ```

## 19. 文件与路径操作进阶（`memory_101.0.py`、`xunfei_tts.py`、`memory-decoupling/memory.py`）

- **os.path.join 与 exists**：跨平台拼接路径、判断文件是否存在  
  ```python
  import os

  if os.path.exists(memory_path):
      with open(memory_path, 'r', encoding='utf-8') as f:
          data = json.load(f)
  ```

- **创建目录与删除文件**：`os.makedirs()` 创建目录，`os.remove()` 删除文件（在 TTS 模块中用于生成和清理音频文件）。  

## 20. WebSocket、多线程与回调函数（`xunfei_tts.py`）

- **回调函数**：将函数名作为参数传入，在特定事件发生时由库自动调用，例如 `on_message`、`on_error`、`on_close`、`on_open`。  

- **WebSocket 客户端**：使用第三方库 `websocket.WebSocketApp` 建立长连接，并在回调中处理数据：  
  ```python
  ws = websocket.WebSocketApp(wsUrl,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
  ws.on_open = lambda ws: on_open(ws, wsParam)
  ```

- **线程 `_thread`**：通过 `thread.start_new_thread(func, args)` 在后台启动新的线程执行任务，不阻塞主线程。  

## 21. 第三方 GUI / Web 框架（`6.2_memory_clonebot_streamlit.py`）

- **Streamlit 基本用法**：用于快速搭建 Web 界面  
  ```python
  import streamlit as st

  st.set_page_config(page_title="Talk is cheap Vibe me a future", page_icon="🗨", layout="wide")
  st.title("Talk is cheap 🗨 Vibe me a future")
  user_input = st.chat_input("输入你的消息...")
  ```

- **会话状态 `st.session_state`**：用于在多次请求之间保存对话历史、当前选中角色等状态。  

- **上下文组件**：`with st.sidebar:` 定义侧边栏区域，`with st.chat_message("user"):` 定义对话气泡区域。  

## 22. 模块化分层与解耦设计（`memory_101.0.py`、`memory_101.1.py`、`memory-decoupling/*.py`）

- **按职责拆分模块**：  
  - `api` 只负责调用大模型接口  
  - `memory` 只负责读写记忆文件  
  - `roles` 只负责角色设定和规则文案  
  - `logic` 只负责结束对话等业务判断  
  - `chat` 只负责“一轮对话”的封装  
  - `main` 只负责主循环和异常处理  

- **好处**：每个模块更专一、易于测试和复用，也方便你单独替换某一层实现。  

## 总结

这些文件涵盖了Python编程的核心基础知识：

### 基础语法
- ✅ 变量、数据类型（字符串、字典、列表、集合）
- ✅ 输入输出（print、input）
- ✅ 模块导入（import、from...import）
- ✅ 代码注释

### 数据结构
- ✅ 列表（创建、索引、推导式）
- ✅ 字典（创建、访问、嵌套、推导式）
- ✅ 集合（创建、操作）
- ✅ 嵌套数据结构

### 函数与控制流
- ✅ 函数定义与调用
- ✅ 函数参数（位置参数、默认参数、类型提示）
- ✅ 控制流（if/else、while、for、break、continue、return）
- ✅ 全局变量（global关键字）

### 高级特性
- ✅ 列表推导式、字典推导式
- ✅ 字符串方法（strip、rstrip、in操作符）
- ✅ 正则表达式（re模块）
- ✅ 随机数（random模块）
- ✅ 异常处理（raise）
- ✅ HTTP网络请求（requests库）
- ✅ 模块化设计

这些知识点为Python编程打下了坚实基础，可以在此基础上学习更高级的特性（如类、装饰器、生成器等）。
