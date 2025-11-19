Python基础知识总结
==================

本文档总结了 `001.py`、`003.py`、`zhipu.py` 三个文件中涵盖的Python基础知识。

## 1. 变量与赋值（`001.py`、`003.py`、`zhipu.py`）

- **变量定义**：Python使用 `=` 进行变量赋值，无需声明类型
  ```python
  name = "Yanzhen Chen"
  x = "1"
  y = "2"
  user_input = input("请输入你要说的话：")
  ```

- **变量命名**：遵循标识符命名规则，区分大小写

## 2. 字符串操作（`001.py`、`003.py`、`zhipu.py`）

- **f-string格式化**：使用 `f"..."` 在字符串中嵌入变量
  ```python
  print(f"Hello, {name}!")
  ```

- **字符串拼接**：使用 `+` 运算符连接字符串
  ```python
  print(x + y)  # 输出 "12"（字符串拼接，非数值相加）
  content = role_system + user_input
  ```

- **字符串字面量**：使用单引号或双引号定义字符串

## 3. 输入输出（`001.py`、`003.py`、`zhipu.py`）

- **print()函数**：输出内容到控制台
  ```python
  print("Hello, World!")
  print(reply)
  ```

- **input()函数**：从用户获取输入，返回字符串类型
  ```python
  user_input = input("请输入你要说的话：")
  ```

## 4. 模块导入（`003.py`、`zhipu.py`）

- **import语句**：导入标准库或第三方模块
  ```python
  import requests
  import json
  ```

- **from...import语句**：从模块中导入特定内容
  ```python
  from requests.utils import stream_decode_response_unicode
  ```

## 5. 函数定义与调用（`003.py`、`zhipu.py`）

- **函数定义**：使用 `def` 关键字定义函数
  ```python
  def call_zhipu_api(messages, model="glm-4-flash"):
      # 函数体
  ```

- **函数参数**：
  - 位置参数：`messages`
  - 默认参数：`model="glm-4-flash"`（调用时可省略）

- **函数返回值**：使用 `return` 返回结果
  ```python
  return response.json()
  ```

- **函数调用**：通过函数名和参数调用
  ```python
  result = call_zhipu_api(messages)
  ```

## 6. 数据结构

### 6.1 字典（Dictionary）（`003.py`、`zhipu.py`）

- **字典创建**：使用花括号 `{}` 定义键值对
  ```python
  headers = {
      "Authorization": "...",
      "Content-Type": "application/json"
  }
  data = {
      "model": model,
      "messages": messages,
      "temperature": 0.5
  }
  ```

- **字典访问**：通过键访问值
  ```python
  result['choices'][0]['message']['content']
  ```

### 6.2 列表（List）（`003.py`、`zhipu.py`）

- **列表创建**：使用方括号 `[]` 定义
  ```python
  messages = [
      {"role": "user", "content": role_system + user_input}
  ]
  ```

- **列表索引**：使用索引访问元素（从0开始）
  ```python
  result['choices'][0]  # 访问列表第一个元素
  ```

- **嵌套结构**：列表和字典可以嵌套使用
  ```python
  result['choices'][0]['message']['content']  # 字典->列表->字典->键
  ```

## 7. 控制流

### 7.1 条件判断（`003.py`、`zhipu.py`）

- **if语句**：根据条件执行代码
  ```python
  if response.status_code == 200:
      return response.json()
  else:
      raise Exception(...)
  ```

- **比较运算符**：`==`（等于）、`!=`（不等于）等
  ```python
  if reply == "好的，我们有缘再见。":
      print("对话结束。")
  ```

### 7.2 循环（`003.py`）

- **while循环**：当条件为真时重复执行
  ```python
  while True:  # 无限循环
      # 循环体
      if 条件:
          break  # 退出循环
  ```

- **break语句**：跳出循环
  ```python
  if user_input in ['再见']:
      break
  ```

## 8. 异常处理（`003.py`、`zhipu.py`）

- **raise语句**：主动抛出异常
  ```python
  raise Exception(f"API调用失败: {response.status_code}, {response.text}")
  ```

- **异常信息**：使用f-string格式化异常消息

## 9. HTTP请求（`003.py`、`zhipu.py`）

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

## 10. 代码注释（`003.py`）

- **单行注释**：使用 `#` 开头
  ```python
  # 多轮对话循环，直到用户输入 '再见' 结束
  ```

- **行内注释**：在代码行末尾添加说明
  ```python
  while True:  # 表示"当条件为真时一直循环"
  ```

## 11. 代码组织

- **代码顺序**：从上到下顺序执行
- **作用域**：函数内部定义的变量在函数外部不可访问
- **代码复用**：通过函数封装重复逻辑

## 12. 集合与去重（`004.2.py`）

- **集合创建**：`guessed_roles = set()` 用于记录已经识破的角色，集合天然去重。
- **集合操作**：`guessed_roles.add(current_role)`、`if role in guessed_roles:`、`len(guessed_roles)`。
- **差集逻辑**：配合 `ROLE_SEQUENCE` 使用集合判断还有多少角色未被猜中。

## 13. 字典推导式与映射（`004.2.py`）

- **字典推导式**：`role_histories = {role: build_conversation(role) for role in ROLE_SEQUENCE}` 一次性为每个角色建立独立的对话历史。
- **多层映射**：通过 `ROLE_PROMPTS`、`ROLE_EXAMPLES`、`ROLE_ACTION_TAILS` 维护不同的设定、示例和动作描述。

## 14. 正则表达式与字符串处理（`004.2.py`）

- **导入模块**：`import re`
- **正则替换**：`re.sub(r"\s+", "", user_text)` 去除空白后匹配 “你是 + 关键字” 的句式。
- **字符串方法**：`strip()`、`rstrip()` 清理输入；`f"{assistant_reply.rstrip()} {action_tail}"` 追加动作括号。
- **任意判断**：`any(keyword in cleaned_input for keyword in keywords)` 与 `contains_role_guess()` 搭配使用。

## 15. 控制流程扩展（`004.2.py`）

- **for 循环配合 break**：在 `advance_role()` 中循环查找下一个尚未识破的角色并在满足条件后 `return`。
- **continue 的运用**：在多处判断（如识破角色、切换角色）后继续下一轮循环，保证游戏流程顺畅。
- **全局变量**：在函数内使用 `global current_role_index` 等声明以修改外部状态。

## 总结

这些文件涵盖了Python编程的核心基础知识：
- ✅ 变量、数据类型（字符串、字典、列表）
- ✅ 输入输出（print、input）
- ✅ 模块导入（import、from...import）
- ✅ 函数定义与调用
- ✅ 控制流（if/else、while、break）
- ✅ 异常处理（raise）
- ✅ HTTP网络请求（requests库）
- ✅ 嵌套数据结构访问
- ✅ 代码注释
