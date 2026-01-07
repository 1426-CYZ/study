class InputListener:
    def __init__(self):
        self.pending_input = None

    def add_check_point(self, message: str = None):
        if message:
            print(f"\n{message}")
        try:
            user_input = input("（按回车继续，或输入问题/选项/输入“追问”来打断讨论）：").strip()
            if user_input:
                self.pending_input = user_input
                return True
        except (EOFError, KeyboardInterrupt):
            self.pending_input = "退出"
            return True
        return False

    def has_input(self):
        return self.pending_input is not None

    def get_input(self):
        if self.pending_input:
            result = self.pending_input
            self.pending_input = None
            return result
        return None

    def clear(self):
        self.pending_input = None

