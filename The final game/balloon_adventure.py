# 课程作业：高空氦气球大冒险
# 开发适配：大二Python基础（Tkinter+matplotlib）
# 运行前需安装：pip install matplotlib

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

# ===================== 全局变量初始化 =====================
root = tk.Tk()
root.title("高空氦气球大冒险 - 脑洞版")
root.geometry("900x800")  # 主窗口大小，注意是英文x
root.configure(bg="#F5F5DC")  # 浅米色背景

# 1. 参数变量初始化
# 环境参数
weather_var = tk.StringVar(value="晴天（☀️ 适合拍照）")
location_var = tk.StringVar(value="平原（🌾 软着陆）")
height_var = tk.StringVar(value="低空（3000m 新手）")

# 设备参数
balloon_size_var = tk.StringVar(value="中型气球（🎈🎈 堪比汽车）")
helium_var = tk.StringVar(value="普通氦气（3罐）")
balloon_material_var = tk.StringVar(value="抗压尼龙（✅ 耐造）")

# 人体参数
weight_var = tk.StringVar(value="60kg（中 标准）")
equipment_var = tk.StringVar(value="带降落伞（🪂 保命）")

# 脑洞buff
buff_var = tk.StringVar(value="无")

# 2. AI台词模板（覆盖不同难度场景）
ai_lines = {
    "🔬 物理学家": {
        "short_3": "浮力刚好托住你，平稳落地！",
        "long_3": "60kg体重+中型气球的浮力约1500N，抵消重力后剩余浮力小，低空环境下能平稳落地，无安全风险。",
        "short_6": "浮力够托住你，但大风会让你乱晃！",
        "long_6": "60kg体重+巨型气球的浮力约3000N，能抵消重力，但高空风速大，你会像风筝一样横向飘，没法稳定悬浮。",
        "short_9": "浮力过剩，宠物能帮你稳重心！",
        "long_9": "60kg体重+巨型气球的浮力约3000N，宠物同行增加5kg负重，能小幅降低上升速度，但高空仍需注意防风。",
        "chat": {
            "浮力怎么算？": "重力=体重×9.8，浮力=气球体积×空气密度×9.8，巨型气球体积约300m³，浮力≈3000N！",
            "大风影响有多大？": "高空风速超10m/s，会让你每秒横向飘10米，根本控制不了方向～",
            "不同体重影响？": "40kg体重浮力过剩更明显，80kg需要巨型气球才能抵消重力！"
        }
    },
    "🤪 吐槽博主": {
        "short_3": "平平无奇，流量一般！",
        "long_3": "家人们！中型气球+低空跳伞，画面太普通，直播最多500播放，建议加宠物或卡通气球！",
        "short_6": "带自拍杆直播必火！",
        "long_6": "家人们！高空大风+宠物脸气球，这流量密码拿捏了！建议标题写‘挑战最晃跳伞，全程尖叫版’，弹幕绝对爆炸！",
        "short_9": "宠物+巨型气球，流量破万！",
        "long_9": "巨型卡通气球+带狗跳伞，这画面谁不爱？标题写‘带狗子挑战高空气球跳伞，它吓得抱紧我’，播放量直接破万！",
        "chat": {
            "怎么起直播标题？": "《花200块租巨型气球跳伞，结果飘到小区楼顶！》",
            "带什么道具涨粉？": "带发光手环+宠物，镜头怼近气球上的宠物脸，播放量直接翻倍！",
            "怎么互动弹幕？": "让弹幕投票决定你往哪个方向飘，互动性拉满！"
        }
    },
    "🎮 游戏玩家": {
        "short_3": "新手关卡，轻松通关！",
        "long_3": "这是1星新手关卡！气球是基础坐骑，无debuff干扰，目标：平稳落地，解锁‘入门玩家’成就！",
        "short_6": "这是A+级关卡！",
        "long_6": "气球是你的飞行坐骑，大风是‘干扰debuff’，目标：避开高楼（障碍物），成功落地解锁‘气球勇士’成就！",
        "short_9": "S级隐藏关卡！",
        "long_9": "巨型气球是史诗级坐骑，宠物是‘辅助伙伴’，高空是‘高难度地图’，解锁条件：带宠物落地，奖励‘脑洞王者’成就！",
        "chat": {
            "有哪些成就？": "入门玩家、气球勇士、脑洞王者、流量之王（直播破万）！",
            "怎么避开障碍物？": "选平原地形，避开城市高楼，减少碰撞debuff！",
            "坐骑升级？": "巨型气球＞中型气球，卡通材质颜值高但风阻大！"
        }
    },
    "🚨 安全顾问": {
        "short_3": "安全！放心跳！",
        "long_3": "生存概率99%！低空+中型气球+平原，无任何风险，带瓶水就行，不用额外准备！",
        "short_6": "注意防风！带点零食！",
        "long_6": "生存概率80%，但大风可能让你飘去陌生地方，建议带点零食和手机充电宝，落地前先定位！",
        "short_9": "宠物要系安全带！",
        "long_9": "生存概率70%，高空温度低，记得给宠物穿小外套，同时带够零食，飘的时间会比预期久！",
        "chat": {
            "必备求生装备？": "充电宝、零食、保暖外套、定位器，缺一不可！",
            "宠物安全注意？": "给宠物系安全绳，避免高空受惊挣脱！",
            "失温怎么办？": "带暖宝宝贴在衣服里，高空温度比地面低10-15℃！"
        }
    }
}

# 3. 结局模板
end_templates = [
    "你带着普通气球，在低空平稳飘到平原落地，全程毫无波澜，适合保守派～",
    "你选了巨型卡通气球+高空大风，被吹得左右晃，但最终安全落地，直播收获5000点赞！",
    "宠物同行+巨型气球，狗狗帮你稳住了气球绳，飘到郊区平原，还和狗狗拍了超治愈的合照～",
    "大风把你吹到城市楼顶，好在带了降落伞，安全落地还被路人拍上本地热搜！",
    "快速充气氦气让你10秒就充满气球，提前落地，避开了后续的强风，运气爆棚！",
    "带自拍杆直播跳伞，标题够吸睛，直接冲上同城热门，收获10万播放量！",
    "高空+无buff，你飘了30分钟才落地，又饿又冷，下次记得听安全顾问的带零食！",
    "卡通材质气球风阻太大，你飘得很慢，但沿途风景超美，拍了好多好看的照片～",
    "上升气流buff帮你省了氦气，轻松飘到目标高度，还偶遇了一群飞鸟，超浪漫！",
    "80kg体重+中型气球，浮力差点不够，好在低空风小，有惊无险落地！"
]

# ===================== 核心功能函数 =====================
def get_difficulty_level():
    """判断当前场景难度等级（3/6/9星）"""
    level = 6  # 默认6星
    # 3星条件：中型气球+低空+无buff
    if "中型气球" in balloon_size_var.get() and "低空" in height_var.get() and buff_var.get() == "无":
        level = 3
    # 9星条件：巨型气球+高空+宠物同行
    elif "巨型气球" in balloon_size_var.get() and "高空" in height_var.get() and "宠物同行" in buff_var.get():
        level = 9
    return level

def generate_scene():
    """生成场景预览、难度评级、图片匹配"""
    try:
        # 1. 拼接场景文案
        scene_text = (
            f"{weight_var.get()}+{balloon_size_var.get()}+{balloon_material_var.get()}+{helium_var.get()}+"
            f"{weather_var.get()}+{location_var.get()}+{height_var.get()}+{equipment_var.get()}+{buff_var.get()}"
        )
        scene_label.config(text=scene_text)

        # 2. 难度评级
        level = get_difficulty_level()
        if level == 3:
            star_text = "⭐⭐⭐（保守派）"
        elif level == 6:
            star_text = "⭐⭐⭐⭐⭐⭐（趣味版）"
        else:
            star_text = "⭐⭐⭐⭐⭐⭐⭐⭐⭐（脑洞天花板）"
        star_label.config(text=star_text)

        # 3. 匹配卡通图片（提示：替换为本地图片路径，建议准备5张png）
        try:
            if "巨型气球" in balloon_size_var.get():
                img = tk.PhotoImage(file="giant_balloon.png")  # 需自行准备
            elif "卡通材质" in balloon_material_var.get():
                img = tk.PhotoImage(file="cartoon_balloon.png")  # 需自行准备
            elif "宠物同行" in buff_var.get():
                img = tk.PhotoImage(file="pet_balloon.png")  # 需自行准备
            elif "大风" in weather_var.get():
                img = tk.PhotoImage(file="wind_balloon.png")  # 需自行准备
            else:
                img = tk.PhotoImage(file="normal_balloon.png")  # 需自行准备
            img_label.config(image=img)
            img_label.image = img  # 防止图片被垃圾回收
        except:
            # 图片加载失败时显示提示
            img_label.config(text="🎈 请将卡通气球图片放在代码同目录！")

        # 4. 生成AI简短发言
        level = get_difficulty_level()
        physicist_short = ai_lines["🔬 物理学家"][f"short_{level}"]
        blogger_short = ai_lines["🤪 吐槽博主"][f"short_{level}"]
        gamer_short = ai_lines["🎮 游戏玩家"][f"short_{level}"]
        safety_short = ai_lines["🚨 安全顾问"][f"short_{level}"]
        
        ai_physicist_short.config(text=physicist_short)
        ai_blogger_short.config(text=blogger_short)
        ai_gamer_short.config(text=gamer_short)
        ai_safety_short.config(text=safety_short)

        # 5. 生成结局
        generate_end()

        # 6. 绘制可视化图表
        draw_force_chart()
        draw_height_chart()

        # 显示所有结果区域
        result_frame.grid()
    except Exception as e:
        messagebox.showerror("生成失败", f"场景生成出错：{str(e)}")

def toggle_ai_detail(ai_type, label, btn):
    """切换AI详细/简短发言"""
    level = get_difficulty_level()
    if btn["text"] == "展开详情":
        # 显示详细发言
        detail_text = ai_lines[ai_type][f"long_{level}"]
        label.config(text=detail_text)
        btn["text"] = "收起详情"
    else:
        # 显示简短发言
        short_text = ai_lines[ai_type][f"short_{level}"]
        label.config(text=short_text)
        btn["text"] = "展开详情"

def ai_chat_popup(ai_type):
    """AI聊两句弹窗"""
    chat_win = tk.Toplevel(root)
    chat_win.title(f"{ai_type} - 聊两句")
    chat_win.geometry("400x300")
    chat_win.configure(bg="#F5F5DC")

    # 显示问题按钮
    chat_questions = ai_lines[ai_type]["chat"]
    row = 0
    for q, a in chat_questions.items():
        # 问题按钮
        btn = tk.Button(chat_win, text=q, bg="#FFE4B5", command=lambda ans=a: messagebox.showinfo("回复", ans))
        btn.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        row += 1

def generate_end():
    """生成结局文本"""
    level = get_difficulty_level()
    weight = weight_var.get()
    balloon = balloon_size_var.get()
    weather = weather_var.get()
    buff = buff_var.get()

    # 匹配结局
    end_text = end_templates[0]  # 默认结局
    if "巨型气球" in balloon and "宠物同行" in buff:
        end_text = end_templates[2]
    elif "大风" in weather and "城市" in location_var.get():
        end_text = end_templates[3]
    elif "自拍杆" in equipment_var.get():
        end_text = end_templates[5]
    elif level == 9:
        end_text = end_templates[8]
    elif "80kg" in weight and "中型气球" in balloon:
        end_text = end_templates[9]
    
    end_label.config(text=f"结局：{end_text}")

def draw_force_chart():
    """绘制受力对比柱状图"""
    # 1. 获取参数对应的力数据
    # 重力（N）：40kg=400，60kg=600，80kg=800
    if "40kg" in weight_var.get():
        gravity = 400
    elif "80kg" in weight_var.get():
        gravity = 800
    else:
        gravity = 600

    # 浮力（N）：中型=1500，巨型=3000
    buoyancy = 1500 if "中型气球" in balloon_size_var.get() else 3000

    # 风力（N）：大风=800，其他=200
    wind = 800 if "大风" in weather_var.get() else 200

    # 2. 绘制柱状图
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(["重力", "浮力", "风力"], [gravity, buoyancy, wind], color=["#FFC0CB", "#87CEEB", "#90EE90"])
    ax.set_ylabel("力的大小（N）")
    ax.set_title("受力对比图")
    # 添加注释
    if buoyancy > gravity:
        ax.text(0.5, buoyancy + 100, "浮力＞重力，不会自由落体！", ha="center")
    else:
        ax.text(0.5, buoyancy + 100, "浮力不足，注意安全！", ha="center")

    # 3. 嵌入Tkinter窗口
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

def draw_height_chart():
    """绘制高度-时间折线图"""
    # 1. 生成高度数据（0-120秒）
    time = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    # 不同场景高度变化
    if "低空" in height_var.get():
        height = [3000, 2800, 2600, 2500, 2500, 2500, 2500, 2500, 2400, 2300, 2200, 2100, 2000]
    elif "高空" in height_var.get() and "大风" in weather_var.get():
        height = [10000, 9800, 9600, 9500, 9700, 9900, 9800, 9700, 9600, 9500, 9400, 9300, 9200]
    else:
        height = [10000, 9900, 9800, 9700, 9700, 9700, 9700, 9600, 9500, 9400, 9300, 9200, 9100]

    # 2. 绘制折线图
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(time, height, color="#FF6347", linewidth=2)
    ax.set_xlabel("时间（秒）")
    ax.set_ylabel("高度（米）")
    ax.set_title("高度-时间变化图")
    # 标注关键节点
    ax.annotate("开始充气", xy=(10, height[1]), xytext=(15, height[1]+200), arrowprops=dict(arrowstyle="->"))
    ax.annotate("停止下落", xy=(30, height[3]), xytext=(35, height[3]+200), arrowprops=dict(arrowstyle="->"))
    # 添加吐槽文案
    ax.text(60, max(height)-500, "你看这曲线，像不像你跌宕起伏的冒险！", ha="center")

    # 3. 嵌入Tkinter窗口
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, padx=10, pady=10)

def save_scene():
    """保存场景到本地json文件"""
    try:
        scene_data = {
            "weather": weather_var.get(),
            "location": location_var.get(),
            "height": height_var.get(),
            "balloon_size": balloon_size_var.get(),
            "helium": helium_var.get(),
            "balloon_material": balloon_material_var.get(),
            "weight": weight_var.get(),
            "equipment": equipment_var.get(),
            "buff": buff_var.get()
        }
        with open("scene.json", "w", encoding="utf-8") as f:
            json.dump(scene_data, f, ensure_ascii=False, indent=2)
        tip_label.config(text="✅ 场景已保存到scene.json！")
    except Exception as e:
        messagebox.showerror("保存失败", f"场景保存出错：{str(e)}")

def load_scene():
    """加载本地保存的场景"""
    try:
        if os.path.exists("scene.json"):
            with open("scene.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            # 回显参数
            weather_var.set(data["weather"])
            location_var.set(data["location"])
            height_var.set(data["height"])
            balloon_size_var.set(data["balloon_size"])
            helium_var.set(data["helium"])
            balloon_material_var.set(data["balloon_material"])
            weight_var.set(data["weight"])
            equipment_var.set(data["equipment"])
            buff_var.set(data["buff"])
            tip_label.config(text="✅ 已加载历史场景！")
        else:
            tip_label.config(text="⚠️ 暂无保存的场景～")
    except Exception as e:
        messagebox.showerror("加载失败", f"场景加载出错：{str(e)}")

# ===================== 界面布局 =====================
# 1. 标题区域
title_label = tk.Label(root, text="🎈 高空氦气球大冒险 🎈", font=("微软雅黑", 18, "bold"), bg="#F5F5DC")
title_label.grid(row=0, column=0, columnspan=4, pady=10)

# 2. 场景编辑器区域（参数选择）
editor_frame = tk.LabelFrame(root, text="场景编辑器", font=("微软雅黑", 12), bg="#F5F5DC", padx=10, pady=10)
editor_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="w")

# 2.1 环境参数
tk.Label(editor_frame, text="🌤️ 环境参数", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=0, column=0, sticky="w")
# 天气
tk.Label(editor_frame, text="天气：", bg="#F5F5DC").grid(row=1, column=0, sticky="w")
weather_menu = ttk.OptionMenu(editor_frame, weather_var, "晴天（☀️ 适合拍照）", "晴天（☀️ 适合拍照）", "大风（💨 风筝模式）", "多云（⛅ 不晒）")
weather_menu.grid(row=1, column=1, sticky="w")
# 地理位置
tk.Label(editor_frame, text="位置：", bg="#F5F5DC").grid(row=1, column=2, sticky="w")
location_menu = ttk.OptionMenu(editor_frame, location_var, "平原（🌾 软着陆）", "平原（🌾 软着陆）", "城市（🏙️ 可能挂高楼）")
location_menu.grid(row=1, column=3, sticky="w")
# 高度
tk.Label(editor_frame, text="高度：", bg="#F5F5DC").grid(row=1, column=4, sticky="w")
height_menu = ttk.OptionMenu(editor_frame, height_var, "低空（3000m 新手）", "低空（3000m 新手）", "高空（10000m 进阶）")
height_menu.grid(row=1, column=5, sticky="w")

# 2.2 设备参数
tk.Label(editor_frame, text="🎈 设备参数", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=2, column=0, sticky="w", pady=5)
# 气球规格
tk.Label(editor_frame, text="气球规格：", bg="#F5F5DC").grid(row=3, column=0, sticky="w")
tk.Radiobutton(editor_frame, text="中型气球（🎈🎈 堪比汽车）", variable=balloon_size_var, value="中型气球（🎈🎈 堪比汽车）", bg="#F5F5DC").grid(row=3, column=1, sticky="w")
tk.Radiobutton(editor_frame, text="巨型气球（🎈🎈🎈 比足球场大）", variable=balloon_size_var, value="巨型气球（🎈🎈🎈 比足球场大）", bg="#F5F5DC").grid(row=3, column=2, sticky="w")
# 氦气配置
tk.Label(editor_frame, text="氦气配置：", bg="#F5F5DC").grid(row=3, column=3, sticky="w")
tk.Radiobutton(editor_frame, text="普通氦气（3罐）", variable=helium_var, value="普通氦气（3罐）", bg="#F5F5DC").grid(row=3, column=4, sticky="w")
tk.Radiobutton(editor_frame, text="快速充气氦气（✨ 10秒充满）", variable=helium_var, value="快速充气氦气（✨ 10秒充满）", bg="#F5F5DC").grid(row=3, column=5, sticky="w")
# 气球材质
tk.Label(editor_frame, text="气球材质：", bg="#F5F5DC").grid(row=4, column=0, sticky="w")
tk.Radiobutton(editor_frame, text="抗压尼龙（✅ 耐造）", variable=balloon_material_var, value="抗压尼龙（✅ 耐造）", bg="#F5F5DC").grid(row=4, column=1, sticky="w")
tk.Radiobutton(editor_frame, text="卡通材质（🐻 宠物脸，风阻大）", variable=balloon_material_var, value="卡通材质（🐻 宠物脸，风阻大）", bg="#F5F5DC").grid(row=4, column=2, sticky="w")

# 2.3 人体参数
tk.Label(editor_frame, text="👤 人体参数", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=5, column=0, sticky="w", pady=5)
# 体重
tk.Label(editor_frame, text="体重：", bg="#F5F5DC").grid(row=6, column=0, sticky="w")
tk.Radiobutton(editor_frame, text="40kg（轻 像羽毛）", variable=weight_var, value="40kg（轻 像羽毛）", bg="#F5F5DC").grid(row=6, column=1, sticky="w")
tk.Radiobutton(editor_frame, text="60kg（中 标准）", variable=weight_var, value="60kg（中 标准）", bg="#F5F5DC").grid(row=6, column=2, sticky="w")
tk.Radiobutton(editor_frame, text="80kg（重 需大球）", variable=weight_var, value="80kg（重 需大球）", bg="#F5F5DC").grid(row=6, column=3, sticky="w")
# 装备
tk.Label(editor_frame, text="装备：", bg="#F5F5DC").grid(row=6, column=4, sticky="w")
tk.Radiobutton(editor_frame, text="带降落伞（🪂 保命）", variable=equipment_var, value="带降落伞（🪂 保命）", bg="#F5F5DC").grid(row=6, column=5, sticky="w")
tk.Radiobutton(editor_frame, text="带自拍杆（📸 直播流量密码）", variable=equipment_var, value="带自拍杆（📸 直播流量密码）", bg="#F5F5DC").grid(row=6, column=6, sticky="w")

# 2.4 脑洞buff
tk.Label(editor_frame, text="✨ 脑洞buff", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=7, column=0, sticky="w", pady=5)
tk.Radiobutton(editor_frame, text="无", variable=buff_var, value="无", bg="#F5F5DC").grid(row=8, column=1, sticky="w")
tk.Radiobutton(editor_frame, text="上升气流（🌀 免费搭便车）", variable=buff_var, value="上升气流（🌀 免费搭便车）", bg="#F5F5DC").grid(row=8, column=2, sticky="w")
tk.Radiobutton(editor_frame, text="宠物同行（🐶 带狗跳，加负重）", variable=buff_var, value="宠物同行（🐶 带狗跳，加负重）", bg="#F5F5DC").grid(row=8, column=3, sticky="w")

# 2.5 功能按钮
tk.Button(editor_frame, text="生成场景", bg="#FFA500", font=("微软雅黑", 10), command=generate_scene).grid(row=9, column=0, padx=5, pady=10)
tk.Button(editor_frame, text="保存场景", bg="#90EE90", font=("微软雅黑", 10), command=save_scene).grid(row=9, column=1, padx=5, pady=10)
tk.Button(editor_frame, text="加载场景", bg="#87CEEB", font=("微软雅黑", 10), command=load_scene).grid(row=9, column=2, padx=5, pady=10)
tip_label = tk.Label(editor_frame, text="💡 选完参数点击「生成场景」开始冒险！", bg="#F5F5DC", fg="#696969")
tip_label.grid(row=9, column=3, columnspan=4, pady=10)

# 3. 场景预览区域
result_frame = tk.LabelFrame(root, text="场景结果", font=("微软雅黑", 12), bg="#F5F5DC", padx=10, pady=10)
result_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=5, sticky="w")
result_frame.grid_remove()  # 初始隐藏

# 3.1 场景基本信息
tk.Label(result_frame, text="📝 场景描述：", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=0, column=0, sticky="w")
scene_label = tk.Label(result_frame, text="", bg="#F5F5DC", wraplength=800)
scene_label.grid(row=0, column=1, columnspan=3, sticky="w")

tk.Label(result_frame, text="⭐ 难度评级：", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=1, column=0, sticky="w")
star_label = tk.Label(result_frame, text="", bg="#F5F5DC")
star_label.grid(row=1, column=1, sticky="w")

tk.Label(result_frame, text="🖼️ 场景预览：", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=2, column=0, sticky="w")
img_label = tk.Label(result_frame, text="请生成场景后查看图片", bg="#F5F5DC")
img_label.grid(row=2, column=1, sticky="w")

# 3.2 AI议会区域
tk.Label(result_frame, text="🤖 AI议会：", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=3, column=0, sticky="w", pady=5)

# 物理学家卡片
physicist_frame = tk.Frame(result_frame, bg="#F0F8FF", bd=1, relief="solid")
physicist_frame.grid(row=4, column=0, columnspan=4, padx=5, pady=3, sticky="w")
tk.Label(physicist_frame, text="🔬 物理学家：", bg="#F0F8FF", font=("微软雅黑", 10, "bold")).grid(row=0, column=0, sticky="w")
ai_physicist_short = tk.Label(physicist_frame, text="", bg="#F0F8FF", wraplength=600)
ai_physicist_short.grid(row=0, column=1, sticky="w")
tk.Button(physicist_frame, text="展开详情", bg="#E6E6FA", command=lambda: toggle_ai_detail("🔬 物理学家", ai_physicist_short, physicist_btn)).grid(row=0, column=2, padx=5)
physicist_btn = tk.Button(physicist_frame, text="聊两句", bg="#FFE4E1", command=lambda: ai_chat_popup("🔬 物理学家"))
physicist_btn.grid(row=0, column=3, padx=5)

# 吐槽博主卡片
blogger_frame = tk.Frame(result_frame, bg="#F0F8FF", bd=1, relief="solid")
blogger_frame.grid(row=5, column=0, columnspan=4, padx=5, pady=3, sticky="w")
tk.Label(blogger_frame, text="🤪 吐槽博主：", bg="#F0F8FF", font=("微软雅黑", 10, "bold")).grid(row=0, column=0, sticky="w")
ai_blogger_short = tk.Label(blogger_frame, text="", bg="#F0F8FF", wraplength=600)
ai_blogger_short.grid(row=0, column=1, sticky="w")
tk.Button(blogger_frame, text="展开详情", bg="#E6E6FA", command=lambda: toggle_ai_detail("🤪 吐槽博主", ai_blogger_short, blogger_btn)).grid(row=0, column=2, padx=5)
blogger_btn = tk.Button(blogger_frame, text="聊两句", bg="#FFE4E1", command=lambda: ai_chat_popup("🤪 吐槽博主"))
blogger_btn.grid(row=0, column=3, padx=5)

# 游戏玩家卡片
gamer_frame = tk.Frame(result_frame, bg="#F0F8FF", bd=1, relief="solid")
gamer_frame.grid(row=6, column=0, columnspan=4, padx=5, pady=3, sticky="w")
tk.Label(gamer_frame, text="🎮 游戏玩家：", bg="#F0F8FF", font=("微软雅黑", 10, "bold")).grid(row=0, column=0, sticky="w")
ai_gamer_short = tk.Label(gamer_frame, text="", bg="#F0F8FF", wraplength=600)
ai_gamer_short.grid(row=0, column=1, sticky="w")
tk.Button(gamer_frame, text="展开详情", bg="#E6E6FA", command=lambda: toggle_ai_detail("🎮 游戏玩家", ai_gamer_short, gamer_btn)).grid(row=0, column=2, padx=5)
gamer_btn = tk.Button(gamer_frame, text="聊两句", bg="#FFE4E1", command=lambda: ai_chat_popup("🎮 游戏玩家"))
gamer_btn.grid(row=0, column=3, padx=5)

# 安全顾问卡片
safety_frame = tk.Frame(result_frame, bg="#F0F8FF", bd=1, relief="solid")
safety_frame.grid(row=7, column=0, columnspan=4, padx=5, pady=3, sticky="w")
tk.Label(safety_frame, text="🚨 安全顾问：", bg="#F0F8FF", font=("微软雅黑", 10, "bold")).grid(row=0, column=0, sticky="w")
ai_safety_short = tk.Label(safety_frame, text="", bg="#F0F8FF", wraplength=600)
ai_safety_short.grid(row=0, column=1, sticky="w")
tk.Button(safety_frame, text="展开详情", bg="#E6E6FA", command=lambda: toggle_ai_detail("🚨 安全顾问", ai_safety_short, safety_btn)).grid(row=0, column=2, padx=5)
safety_btn = tk.Button(safety_frame, text="聊两句", bg="#FFE4E1", command=lambda: ai_chat_popup("🚨 安全顾问"))
safety_btn.grid(row=0, column=3, padx=5)

# 3.3 数据可视化区域
tk.Label(result_frame, text="📊 数据可视化：", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=8, column=0, sticky="w", pady=5)
chart_frame = tk.Frame(result_frame, bg="#F5F5DC")
chart_frame.grid(row=9, column=0, columnspan=4, sticky="w")

# 3.4 结局区域
tk.Label(result_frame, text="🏁 冒险结局：", bg="#F5F5DC", font=("微软雅黑", 10, "bold")).grid(row=10, column=0, sticky="w", pady=5)
end_label = tk.Label(result_frame, text="", bg="#F5F5DC", wraplength=800, font=("微软雅黑", 10))
end_label.grid(row=10, column=1, columnspan=3, sticky="w")

# 3.5 截图提示
tk.Label(result_frame, text="💡 按PrintScreen键截图分享你的脑洞场景！", bg="#F5F5DC", fg="#696969").grid(row=11, column=0, columnspan=4, pady=10)

# ===================== 运行主循环 =====================
if __name__ == "__main__":
    # 解决matplotlib中文显示问题
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 显示中文
    plt.rcParams["axes.unicode_minus"] = False    # 显示负号
    root.mainloop()