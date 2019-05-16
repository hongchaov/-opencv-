'''
在这个例子中，我们演示了如何使用Opencv3和PyQt5创建简单的相机查看器
作者：Berrouba.A
最后编辑：2018年2月21日
'''
# 进口一些PyQt5模块
import sys
import numpy as np
# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

# import Opencv module
import cv2

from ui_main_window import *

class MainWindow(QWidget):
    # 类的构造函数
    def __init__(self):
        # 调用QWidget构造函数
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 创建一个计时器
        self.timer = QTimer()
        # 设置control_bt回调点击功能
        self.timer.timeout.connect(self.viewCam)
        # 设置control_bt回调函数点击
        self.ui.control_bt.clicked.connect(self.controlTimer)

    # 视摄像头
    def viewCam(self):
        # 以BGR格式读取图像
        ret, image = self.cap.read()
        # 将图像转换为RGB格式
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 获得图像的相关信息
        height, width, channel = image.shape
        step = channel * width
        # 从图像创建QImage
        qImg = QImage(image.data, width, height, step, QImage.Format_RGB888)
        # 在img_label显示图像
        self.ui.image_label.setPixmap(QPixmap.fromImage(qImg))

    # 启动/停止计时器
    def controlTimer(self):
        # if如果计时器停止
        if not self.timer.isActive():
            # 创建视频拍摄
            #self.cap = cv2.VideoCapture(0)
            blue_val = 114

            # 从网络摄像头捕获视频
            cap = cv2.VideoCapture(0)

            while (True):
                # 逐帧捕获
                ret, frame = cap.read()

                cv2.imshow("original", frame)
                # 将BGR转换为HSV
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # 限定在HSV蓝色的范围
                blue_lower = np.array([blue_val - 10, 100, 100])
                blue_upper = np.array([blue_val + 10, 255, 255])

                # T阈值HSV图像以仅获得所选颜色
                blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

                # Bitwise-AND屏蔽原始图像
                blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)

                # 结构元素
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

                # 形态学结束
                blue_closing = cv2.morphologyEx(blue_res, cv2.MORPH_CLOSE, kernel)

                # 转换为黑白图像
                blue_gray = cv2.cvtColor(blue_closing, cv2.COLOR_BGR2GRAY)
                (thresh2, blue_bw) = cv2.threshold(blue_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

                # 计算像素变化
                blue_black = cv2.countNonZero(blue_bw)
                if blue_black > 18000:
                    print("BLUE")

                # 按q退出
                if cv2.waitKey(3) & 0xFF == ord('q'):
                    break

            # 启动定时器
            self.timer.start(20)
            # 更新control_bt文本
            self.ui.control_bt.setText("停止")
        # if如果启动计时器
        else:
            # 停止计时器
            self.timer.stop()
            # 发布视频捕获
            self.cap.release()
            # 更新control_bt文本
            self.ui.control_bt.setText("开始")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 创建并显示主窗口
    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())