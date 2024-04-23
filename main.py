import tkinter as tk
import csv
import random
import time
import math

class Option:
    def __init__(self, name):
        self.name = name

class RouletteWheel:
    def __init__(self, options):
        self.options = options
        self.pointer_angle = 0
        self.speed = 20  # 初始化旋轉速度為 20 單位
        self.acceleration = 0.1  # 減少加速度
        self.rotation_time = 100000  # 旋轉時間為 10 秒，單位為毫秒

    def spin(self):
        self.speed = random.uniform(20, 26)  # 隨機設置旋轉速度，範圍為 2~5 單位
        self.acceleration = 0.1  # 減少加速度
        self.rotate_pointer(0)  # 開始旋轉指針

    def rotate_pointer(self, angle):
        self.pointer_angle += self.speed
        self.speed -= self.acceleration
        if self.speed <= 0:
            # 停止旋轉後顯示今晚吃的選項
            selected_option = self.options[int((self.pointer_angle % 360) / (360 / len(self.options)))]
            self.game.display_selected_option(selected_option)
            return
        self.game.rotate_pointer(angle=self.pointer_angle)
        # 使用遞迴，每 0.01 秒重新繪製指針
        self.game.root.after(20, self.rotate_pointer, self.pointer_angle)

    def stop_rotation_after_time(self):
        self.game.root.after(self.rotation_time, self.stop_rotation)

    def stop_rotation(self):
        self.speed = 0
        self.rotate_pointer(self.pointer_angle)  # 絲滑停止旋轉

class RouletteGame:
    def __init__(self, options_file):
        self.options = self.load_options(options_file)
        self.root = tk.Tk()
        self.root.title("Russian Roulette")

        self.font = ("Noto Sans TC Medium", 8)  # 設置字型
        self.but_font = ("Noto Sans TC Medium", 20)  # 設置字型

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        self.wheel = RouletteWheel(self.options)
        self.pointer = self.canvas.create_line(200, 200, 200, 50, arrow=tk.LAST, fill="red", width=5)
        self.wheel.game = self

        # 繪製輪盤
        self.draw_wheel()

        self.selected_option_label = tk.Label(self.root, text="", font=self.but_font)
        self.selected_option_label.pack(pady=10)  # 改為使用 pack 並增加一些間距

        self.start_button = tk.Button(self.root, text="開始", command=self.start_game)
        self.start_button.pack(pady=10)  # 改為使用 pack 並增加一些間距

    def load_options(self, filename):
        options = []
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                options.append(Option(row[0]))
        return options

    def start_game(self):
        self.selected_option_label.config(text="")
        self.wheel.spin()
        self.wheel.stop_rotation_after_time()

    def rotate_pointer(self, angle=0):
        self.canvas.delete(self.pointer)
        rotated_pointer = self.rotate_line(200, 200, 150, angle)
        self.pointer = self.canvas.create_line(*rotated_pointer, arrow=tk.LAST, fill="red", width=5)

    def rotate_line(self, x1, y1, length, angle):
        x2 = x1 + length * math.cos(math.radians(angle))
        y2 = y1 - length * math.sin(math.radians(angle))
        return x1, y1, x2, y2

    def draw_wheel(self):
        # 輪盤中心座標和半徑
        x, y = 200, 200
        radius = 150

        # 繪製輪盤
        num_options = len(self.options)
        angle_step = 360 / num_options
        start_angle = 0  # 從正上方開始繪製
        for option in self.options:
            start_rad = math.radians(start_angle)
            end_rad = math.radians(start_angle + angle_step)

            # 計算區段的起點和終點坐標
            x1 = x + radius * math.cos(start_rad)
            y1 = y - radius * math.sin(start_rad)
            x2 = x + radius * math.cos(end_rad)
            y2 = y - radius * math.sin(end_rad)

            # 繪製輪盤區段
            arc_id = self.canvas.create_arc(x - radius, y - radius, x + radius, y + radius, start=start_angle, extent=angle_step,
                                    style=tk.PIESLICE, outline='black', width=2)

            # 在區段中心位置添加文字
            text_angle = (start_angle + start_angle + angle_step) / 2  # 文字所在的角度
            text_x = x + 0.7 * radius * math.cos(math.radians(text_angle))  # 文字的 x 座標
            text_y = y - 0.7 * radius * math.sin(math.radians(text_angle))  # 文字的 y 座標
            self.canvas.create_text(text_x, text_y, text=option.name, font=self.font)  # 顯示選項名稱

            # 更新角度
            start_angle += angle_step

    def display_selected_option(self, option):
        self.selected_option_label.config(text=f"今天吃{option.name}")

if __name__ == "__main__":
    game = RouletteGame("options.csv")
    game.root.mainloop()
