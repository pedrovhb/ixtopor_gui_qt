import sys
from main_window import Ui_MainWindow
from ixtopor import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    ixtopor = Ixtopor(ui)

    def keyPressEvent(keyEvent):

        if keyEvent.isAutoRepeat():
            return

        if keyEvent.key() == Qt.Key_Right:
            ui.btnRight.animateClick(10e9)
        if keyEvent.key() == Qt.Key_Up:
            ui.btnUp.animateClick(10e9)
        if keyEvent.key() == Qt.Key_Left:
            ui.btnLeft.animateClick(10e9)
        if keyEvent.key() == Qt.Key_Down:
            ui.btnDown.animateClick(10e9)

        if keyEvent.key() == Qt.Key_Z:
            ui.btnBaseCcw.animateClick(10e9)
        if keyEvent.key() == Qt.Key_X:
            ui.btnBaseCw.animateClick(10e9)
        if keyEvent.key() == Qt.Key_A:
            ui.btnClawCcw.animateClick(10e9)
        if keyEvent.key() == Qt.Key_S:
            ui.btnClawCw.animateClick(10e9)


    def keyReleaseEvent(keyEvent):

        if keyEvent.isAutoRepeat():
            return

        if keyEvent.key() == Qt.Key_Right:
            ui.btnRight.animateClick(0)
        if keyEvent.key() == Qt.Key_Up:
            ui.btnUp.animateClick(0)
        if keyEvent.key() == Qt.Key_Left:
            ui.btnLeft.animateClick(0)
        if keyEvent.key() == Qt.Key_Down:
            ui.btnDown.animateClick(0)

        if keyEvent.key() == Qt.Key_Z:
            ui.btnBaseCcw.animateClick(0)
        if keyEvent.key() == Qt.Key_X:
            ui.btnBaseCw.animateClick(0)
        if keyEvent.key() == Qt.Key_A:
            ui.btnClawCcw.animateClick(0)
        if keyEvent.key() == Qt.Key_S:
            ui.btnClawCw.animateClick(0)


    window.keyPressEvent = keyPressEvent
    window.keyReleaseEvent = keyReleaseEvent

    # ui.toolButton.clicked.connect(lambda x: print('ok'))
    ui.actionSalvar.triggered.connect(lambda x: print('não salvei'))

    ui.btnPlayPause.pressed.connect(lambda: ixtopor.play_commands())

    ui.dialLinearSpeed.valueChanged.connect(ixtopor.updateLinearSpeed)
    ui.dialClawSpeed.valueChanged.connect(ixtopor.updateClawSpeed)
    ui.dialBaseSpeed.valueChanged.connect(ixtopor.updateBaseSpeed)

    ui.sliderTemperature.valueChanged.connect(ixtopor.updateTemperature)

    ui.btnRight.pressed.connect(lambda: ixtopor.set_flag_linear(flag_right))
    ui.btnRight.released.connect(lambda: ixtopor.clear_flag_linear(flag_right))
    ui.btnUp.pressed.connect(lambda: ixtopor.set_flag_linear(flag_up))
    ui.btnUp.released.connect(lambda: ixtopor.clear_flag_linear(flag_up))
    ui.btnLeft.pressed.connect(lambda: ixtopor.set_flag_linear(flag_left))
    ui.btnLeft.released.connect(lambda: ixtopor.clear_flag_linear(flag_left))
    ui.btnDown.pressed.connect(lambda: ixtopor.set_flag_linear(flag_down))
    ui.btnDown.released.connect(lambda: ixtopor.clear_flag_linear(flag_down))

    ui.btnBaseCw.pressed.connect(lambda: ixtopor.set_flag_rotation(flag_base_cw))
    ui.btnBaseCw.released.connect(lambda: ixtopor.clear_flag_rotation(flag_base_cw))
    ui.btnBaseCcw.pressed.connect(lambda: ixtopor.set_flag_rotation(flag_base_ccw))
    ui.btnBaseCcw.released.connect(lambda: ixtopor.clear_flag_rotation(flag_base_ccw))
    ui.btnClawCw.pressed.connect(lambda: ixtopor.set_flag_rotation(flag_claw_cw))
    ui.btnClawCw.released.connect(lambda: ixtopor.clear_flag_rotation(flag_claw_cw))
    ui.btnClawCcw.pressed.connect(lambda: ixtopor.set_flag_rotation(flag_claw_ccw))
    ui.btnClawCcw.released.connect(lambda: ixtopor.clear_flag_rotation(flag_claw_ccw))

    '''def update_text():
    cursor_position = ui.textEdit.textCursor()  # type: QTextCursor
    parsed_text = ide.parse_text(ui.textEdit.toPlainText())
    print(parsed_text)
    ui.textEdit.blockSignals(True)
    ui.textEdit.setHtml(parsed_text)
    print(cursor_position)
    cursor_position.setPosition(cursor_position.position() + 1)
    ui.textEdit.setTextCursor(cursor_position)
    ui.textEdit.blockSignals(False)'''

    def textEditUpdate():
        status = ixtopor.parse_commands(ui.textEdit.toPlainText())
        ui.textBrowser.setText('\n'.join(status))


    ui.textEdit.textChanged.connect(textEditUpdate)

    window.show()
    sys.exit(app.exec_())