import keyboard
import re
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6 import QtCore
import sys

# 定义敏感信息列表（支持正则匹配）
sensitive_patterns = [
    r'\b\d{18}\b',  # 18位身份证号
    r'\b\d{11}\b',  # 11位手机号
    r'password',  # 关键词示例
]

input_buffer = ""  # 用于存储用户输入

def check_sensitive_info(text):
    """检查输入文本是否包含敏感信息"""
    for pattern in sensitive_patterns:
        if re.search(pattern, text):
            return True, pattern
    return False, None

def on_key_event(event):
    global input_buffer
    print(f"键盘输入:{event.name}")
    print(f"键盘缓冲:{input_buffer}")

    if str(event.name) == "enter":
        is_sensitive, pattern = check_sensitive_info(input_buffer)
        if is_sensitive:
            app = QApplication.instance() or QApplication(sys.argv)
            msg_box = QMessageBox()
            msg_box.setWindowTitle("警告")
            if str(pattern) == r"\b\d{11}\b":
                et = "手机号"
            elif str(pattern) == r"\b\d{18}\b":
                et = "身份证号"
            else:
                et = pattern
            msg_box.setText(f"检测到敏感信息: {et}\n请注意隐私!")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setWindowFlags(msg_box.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # 强制置顶
            result = msg_box.exec_()

            if result == QMessageBox.No:
                input_buffer = re.sub(pattern, "*" * len(pattern), input_buffer)
                print(f"修改后输入: {input_buffer}")
        input_buffer = ""  # 清空缓冲区
    elif event.name == "backspace":
        input_buffer = input_buffer[:-1]  # 删除最后一个字符
    elif len(event.name) == 1:
        input_buffer += event.name

# 监听所有键盘输入
keyboard.on_press(on_key_event)

print("正在监听键盘输入，按 Ctrl+C 退出。")
keyboard.wait()
