# OpenCVPyqt04.py
# Demo04 of GUI by PyQt5
# Copyright 2023 Youcans, XUPT
# Crated：2023-01-31

import sys
import cv2 as cv
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from uiDemo3 import Ui_MainWindow  # 导入 uiDemo5.py 中的 Ui_MainWindow 界面类


class MyMainWindow(QMainWindow, Ui_MainWindow):  # 继承 QMainWindow 类和 Ui_MainWindow 界面类
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)  # 初始化父类
        self.setupUi(self)  # 继承 Ui_MainWindow 界面类

        self.pushButton_1.clicked.connect(self.click_pushButton_1)  # 点击 pushButton_1 触发
        self.pushButton_2.clicked.connect(self.click_pushButton_2)  # 点击 pushButton_2 触发
        self.pushButton_4.clicked.connect(self.saveSlot)
        #self.pushButton_3.clicked.connect(self.close)  # 点击 pushButton_3 关闭窗口
        self.pushButton_3.clicked.connect(self.click_pushButton_3)  # 点击 pushButton_3 关闭窗口
        return

    def click_pushButton_1(self):
        img = self.openSlot()
        qImg = self.cvToQImage(img)  # 转为 PyQt 图像格式
        self.label.setPixmap(QPixmap.fromImage(qImg))

        return

    def click_pushButton_3(self):
        pixmap = self.label.pixmap()
        if pixmap is not None:
            img = self.qPixmapToCV(pixmap)

        if img is None:
            img = self.button_2()
            # return  # If no image is loaded, then exit the function

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # Convert to grayscale image
        print("click_pushButton_3", img.shape, gray.shape)

        # Apply binary thresholding
        ret, binary_img = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

        qImg = self.cvToQImage(binary_img)  # Convert the binary image to PyQt image format
        self.label.setPixmap(QPixmap.fromImage(qImg))

        return






    def click_pushButton_2(self):
        pixmap = self.label.pixmap()
        if pixmap is not None:
            img = self.qPixmapToCV(pixmap)

        if img is None:
            img = self.button_2()
            #return  # 如果没有加载图像，则退出函数

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)  # 转换为灰度图像
        print("click_pushButton_2", img.shape, gray.shape)
        qImg = self.cvToQImage(gray)  # 将灰度图像转换为 PyQt 图像格式
        self.label.setPixmap(QPixmap.fromImage(qImg))

        return
    def button_2(self):
        img = self.openSlot()
        return img
    def openSlot(self, flag=1):  # 读取图像文件
        # OpenCV 读取图像文件
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "../images/", "*.png *.jpg *.tif")
        if flag == 0 or flag == "gray":
            img = cv.imread(fileName, cv.IMREAD_GRAYSCALE)  # 读取灰度图像
        else:
            img = cv.imread(fileName, cv.IMREAD_COLOR)  # 读取彩色图像
        print(fileName, img.shape)
        return img

    def saveSlot(self):  # 保存图像文件
        # 检查 QLabel 是否有 QPixmap 设置
        pixmap = self.label.pixmap()
        if pixmap is not None:
            # 弹出保存文件的对话框
            saveName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", '*.jpg')
            if saveName:
                # 将 QPixmap 转换为 QImage 并保存
                image = pixmap.toImage()
                image.save(saveName, "PNG")
                print(f"Image saved to {saveName}")
        else:
            print("No image to save in the QLabel.")

    def cvToQImage(self, image):  # OpenCV图像 转换为 PyQt图像
        # 8-bits unsigned, NO. OF CHANNELS=1
        row, col, pix = image.shape[0], image.shape[1], image.strides[0]
        channels = 1 if len(image.shape) == 2 else image.shape[2]
        if channels == 3:  # CV_8UC3
            qImg = QImage(image.data, col, row, pix, QImage.Format_RGB888)
            return qImg.rgbSwapped()
        elif channels == 1:
            qImg = QImage(image.data, col, row, pix, QImage.Format_Indexed8)
            return qImg
        else:
            QtCore.qDebug("ERROR: numpy.ndarray could not be converted to QImage. Channels = %d" % image.shape[2])
            return QImage()

    def qPixmapToCV(self, qPixmap):  # PyQt图像 转换为 OpenCV图像
        print("qPixmap is not None:", qPixmap is not None)
        if qPixmap is None:
            return None

        qImg = qPixmap.toImage()
        print("qImg is not Null:", qImg.isNull())
        if qImg.isNull():
            return None

        if qImg.depth() == 0:
            print("Error: QImage depth is zero, cannot convert to OpenCV image.")
            return None
        if qImg.isNull():
            print("Error: QImage is null.")
            return None

            # 确保 QImage 使用的是合适的格式
        if qImg.format() != QImage.Format_RGB32:
            qImg = qImg.convertToFormat(QImage.Format_RGB32)
        shape = (qImg.height(), qImg.bytesPerLine() * 8 // qImg.depth())
        shape += (4,)
        ptr = qImg.bits()
        ptr.setsize(qImg.byteCount())
        image = np.array(ptr, dtype=np.uint8).reshape(shape)  # 定义 OpenCV 图像
        image = image[..., :3]
        return image

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    myWin = MyMainWindow()  # 实例化 MyMainWindow 类，创建主窗口
    myWin.show()  # 在桌面显示控件 myWin
    sys.exit(app.exec_())  # 结束进程，退出程序
