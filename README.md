Python 基础知识速览（基于 `001.py`、`003.py`、`zhipu.py`）
============================================================

变量与字符串
------------
- 赋值无需显式类型声明（如 `name = "Yanzhen Chen"`），Python 根据右侧值推断类型。
- f-string `print(f"Hello, {name}!")` 可在字符串中直接插入变量。
- 字符串相加默认执行拼接（`"1" + "2"` → `"12"`），若想进行数值计算需调用 `int()` 等转换函数。

输入输出与交互
--------------
- `input("提示语")` 用于读取命令行输入，是实现人机交互的基础。
- `print()` 既能输出变量，也能输出 API 返回的嵌套数据（如 `result['choices'][0]['message']['content']`）。

流程控制
--------
- `while True` 创建无限循环，常配合 `break` 在满足条件时退出（例如检测用户输入或模型回复）。
- `if/else` 用于条件判断，可结合 `in` 进行成员测试（`if user_input in ['再见']:`）。
- 在 `003.py` 中，脚本既根据用户输入决定是否继续，又根据模型的固定回复（如 “好的，我们有缘再见。”）来终止循环，展示了条件嵌套的实践。

函数与模块
----------
- 使用 `import requests`、`import json`、`from requests.utils import stream_decode_response_unicode` 展示了标准库与第三方库的引入。
- 自定义函数 `def call_zhipu_api(messages, model="glm-4-flash"):` 演示了函数定义、默认参数、返回值和异常处理。
- 函数内部通过字典 `headers`、`data` 组织请求参数，并返回解析后的 JSON 数据。

HTTP 请求与数据结构
--------------------
- `requests.post(url, headers=headers, json=data)` 演示了发送 JSON POST 请求的基本写法；`json=` 参数自动序列化字典。
- 通过 `response.status_code` 判断请求是否成功，失败时 `raise Exception(...)` 抛出错误，体现异常处理流程。
- 消息体 `messages` 由列表和字典组合而成，用于封装多轮对话数据：`[{"role": "user", "content": ...}]`。
- `role_system` 字符串与用户输入拼接后传给接口，展示了字符串处理与数据封装的结合场景。

综合示例：对话循环
------------------
- `003.py` 展示了完整的输入 → 拼接系统提示 → 构造 `messages` → 调用 API → 解析回复 → 判断是否结束的一整套流程。
- `zhipu.py` 则给出最简调用示例：一次性构造 `messages`、调用 API 并输出结果，便于理解基础流程。

通过以上脚本可以复习：变量、字符串、输入输出、循环、条件、列表与字典、函数、模块导入、HTTP 请求、异常处理等 Python 基础知识点。实现真实 API 调用的同时，也演示了如何将这些基础语法融会贯通于一个完整的小程序中。
