from segmentpy._taskManager.opening_design import Ui_Dialog
from PySide2.QtWidgets import QDialog
from tqdm import tqdm
import os


class opening_logic(QDialog, Ui_Dialog):
    def __init__(self, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle('Welcome to SegmentPy Beta 0.1')
        self.setStyleSheet("border-image: url({});".format(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'img', 'LRCS.png')))
        self.log.setText('Scanning available devices...')
        self.progressBar.setValue(0)

    def load_gpus(self):
        from tensorflow.python.client import device_lib
        l = []
        local_devices = device_lib.list_local_devices()
        self.progressBar.setRange(0, 100)
        # write devices
        for i, x in tqdm(enumerate(local_devices)):
            self.progressBar.setValue(i / len(local_devices) * 100)
            if x.device_type == 'GPU' or x.device_type == "XLA_GPU":
                _gpu = int(x.name.split(':')[-1])
                if _gpu not in l:
                    self.log.setText('Found GPU: {}'.format(_gpu))
                    l.append(int(x.name.split(':')[-1]))
            else:
                # CPU
                self.log.setText('Cannot find available GPUs, use CPU instead...')

        loggerDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
        if not os.path.exists(loggerDir):
            os.makedirs(loggerDir)
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log', 'device.txt'), 'w') as f:
            for dv in l:
                f.write('{}\n'.format(dv))


