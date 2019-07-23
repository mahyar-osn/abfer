import sys
import os
import argparse
import pyabf

import csv
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# sns.set(style="whitegrid")


class ProgramArguments(object):
    pass


def color_fader(c1, c2, mix=0):
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1 - mix) * c1 + mix * c2)


class ABFer(object):

    def __init__(self, file_name):
        self._file_name = file_name
        self._abf = pyabf.ABF(file_name)
        self._sweep_count = self._abf.sweepCount
        self._channel_count = self._abf.channelCount
        self._protocol = self._abf.protocol

    def get_sweep_count(self):
        return self._sweep_count

    def get_channel_count(self):
        return self._channel_count

    def plot_abf_qt(self):
        from pyqtgraph.Qt import QtGui, QtCore
        import pyqtgraph as pg

        app = QtGui.QApplication([])
        win = pg.GraphicsWindow(title="Plot : {}".format(self._protocol))
        win.resize(800, 600)
        win.nextRow()

        col = 1
        row = 1
        for sweep in range(self._sweep_count):
            for channel in range(self._channel_count):
                self._abf.setSweep(sweepNumber=sweep, channel=channel)
                p = win.addPlot(x=self._abf.sweepX, y=self._abf.sweepY,
                                name="Sweep {} Channel {}".format(sweep + 1, channel + 1),
                                title="Sweep {} Channel {}".format(sweep + 1, channel + 1), row=row, col=col)
                p.setLabel("left", self._abf.sweepLabelY)
                if row == self._sweep_count:
                    p.setLabel("bottom", self._abf.sweepLabelX)

                col += 1
                if col == 3:
                    col = 1
            row += 1

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def plot_abf_qt_temp_for_isan(self):
        from pyqtgraph.Qt import QtGui, QtCore
        import pyqtgraph as pg
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        app = QtGui.QApplication([])
        win = pg.GraphicsWindow(title="Basic plotting examples")
        win.resize(1000, 600)
        win.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        p1 = win.addPlot(title="")
        self._abf.setSweep(sweepNumber=7, channel=1)
        p1.plot()
        fileName = 'D:\\sparc\\misc\\stellate_isan.png'
        img = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap(fileName))
        img.scale(1, -1)
        img.setZValue(-100)  # make sure image is behind other data
        p1.addItem(img)

        # p1 = win.addPlot(title="")
        # self._abf.setSweep(sweepNumber=6, channel=1)
        # p1.plot(x=self._abf.sweepX, y=self._abf.sweepY)
        # p1.showGrid(x=True, y=True)

        self._abf.setSweep(sweepNumber=0, channel=1)
        p2 = win.addPlot(x=self._abf.sweepX, y=self._abf.sweepY, pen=(60, 166, 188))
        p2.showGrid(x=True, y=True)
        win.nextRow()

        p3 = win.addPlot(title="")
        self._abf.setSweep(sweepNumber=1, channel=1)
        p3.plot(x=self._abf.sweepX, y=self._abf.sweepY, pen=pg.mkPen(60, 166, 188, width=2), name="Red curve")
        self._abf.setSweep(sweepNumber=2, channel=1)
        p3.plot(x=self._abf.sweepX, y=self._abf.sweepY, pen=(60, 166, 188), name="Green curve")
        self._abf.setSweep(sweepNumber=3, channel=1)
        p3.plot(x=self._abf.sweepX, y=self._abf.sweepY, pen=(60, 166, 188), name="Blue curve")
        p3.showGrid(x=True, y=True)

        # win.nextRow()

        p4 = win.addPlot(title="")
        self._abf.setSweep(sweepNumber=5, channel=1)
        p4.plot(x=self._abf.sweepX, y=self._abf.sweepY, pen=(60, 166, 188), symbolBrush=(255, 161, 223), symbolPen='w')
        p4.showGrid(x=True, y=True)
        lr = pg.LinearRegionItem([1.1, 5])
        lr.setZValue(-1)
        p4.addItem(lr)

        qGraphicsGridLayout = win.ci.layout
        qGraphicsGridLayout.setColumnStretchFactor(0, 1)
        qGraphicsGridLayout.setRowStretchFactor(0, 2)
        # qGraphicsGridLayout.setColumnStretchFactor(1, 2)

        # p4 = win.addPlot(title="")
        # self._abf.setSweep(sweepNumber=6, channel=1)
        # p4.plot(x=self._abf.sweepX, y=self._abf.sweepY)
        # p4.showGrid(x=True, y=True)
        #
        # p6 = win.addPlot(title="")
        # self._abf.setSweep(sweepNumber=1, channel=0)
        # p6.plot(x=self._abf.sweepX, y=self._abf.sweepY)
        # p6.showGrid(x=True, y=True)

        # win.nextRow()

        # p7 = win.addPlot(title="")
        # self._abf.setSweep(sweepNumber=1, channel=0)
        # p7.plot(x=self._abf.sweepX, y=self._abf.sweepY)
        # p7.showGrid(x=True, y=True)

        # x2 = np.linspace(-100, 100, 1000)
        # data2 = np.sin(x2) / x2
        # p8 = win.addPlot(title="Region Selection")
        # p8.plot(data2, pen=(255, 255, 255, 200))
        # lr = pg.LinearRegionItem([400, 700])
        # lr.setZValue(-10)
        # p8.addItem(lr)

        # p9 = win.addPlot(title="Zoom on selected region")
        # p9.plot(data2)
        #
        # def updatePlot():
        #     p9.setXRange(*lr.getRegion(), padding=0)
        #
        # def updateRegion():
        #     lr.setRegion(p9.getViewBox().viewRange()[0])
        #
        # lr.sigRegionChanged.connect(updatePlot)
        # p9.sigXRangeChanged.connect(updateRegion)
        # updatePlot()

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def plot_abf(self):
        plt.figure(figsize=(8, 5))
        plt.title(self._protocol)
        plt.ylabel(self._abf.sweepLabelY)
        plt.xlabel(self._abf.sweepLabelX)
        for sweep in range(self._sweep_count):
            for channel in range(self._channel_count):
                self._abf.setSweep(sweepNumber=sweep, channel=channel)
                plt.plot(self._abf.sweepX, self._abf.sweepY, alpha=.5, label="Sweep {} Channel {}"
                         .format(sweep + 1, channel + 1))

        # self._abf.setSweep(sweepNumber=4, channel=0)
        # n = len(self._abf.sweepY)
        # c1 = '#0026ff'
        # c2 = '#f80045'
        # fig, ax = plt.subplots(figsize=(8, 5))
        # for i in range(n - 1):
            # ax.plot(self._abf.sweepX, self._abf.sweepY, color=color_fader(c1, c2, x / n), linewidth=4)
            # ax.scatter(self._abf.sweepX[x], self._abf.sweepY[x], color=color_fader(c1, c2, x / n), marker='x')
            # index = i
            # next_index = i + 1
            # x = [self._abf.sweepX[index], self._abf.sweepX[next_index]]
            # y = [self._abf.sweepY[index], self._abf.sweepY[next_index]]
            # ax.plot(x, y, color=color_fader(c1, c2, i / n), linewidth=1)

        plt.legend()
        # plt.savefig('D:\\sparc\\test.png', transparent=True, dpi=600)
        plt.show()

        print('done')

    def save_to_csv(self, file_path):
        file_name = os.path.basename(self._file_name).split('.')[0]
        for channel in range(self._channel_count):
            x = self._create_array_for_channel(channel)
            individual_file = file_name + '_channel_{}.csv'.format(channel + 1)
            sweep_headers = ['Sweep ' + str(x) + '_' + self._abf.sweepLabelY for x in range(self._sweep_count)]
            header = [self._abf.sweepLabelX] + sweep_headers

            with open(os.path.join(file_path, individual_file), 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow(header)
                csv_writer.writerows(x)

    def _create_array_for_channel(self, channel=0):
        n_rows = self._abf.data.shape[1] // self._sweep_count
        n_cols = self._sweep_count
        x = np.zeros((n_rows, n_cols + 1))
        x[:, 0] = self._abf.sweepX
        for column in range(n_cols):
            self._abf.setSweep(sweepNumber=column, channel=channel)
            x[:, column + 1] = self._abf.data[channel, n_rows * column:(column + 1) * n_rows]

        return x


def _main():
    args = parse_args()
    if os.path.exists(args.input_file):
        abf = ABFer(args.input_file)
    else:
        raise FileNotFoundError('File {} does  not exists.'.format(args.input_file))
    if args.output_path is None:
        output_csv = os.path.split(args.input_file)[0]
    else:
        output_csv = args.output_path
    if args.plot:
        # abf.plot_abf()
        # abf.plot_abf_qt_temp_for_isan()
        abf.plot_abf()
    if args.save:
        abf.save_to_csv(output_csv)


def parse_args():
    parser = argparse.ArgumentParser(description="An IO helper to read, process, and plot ABF file formats.")
    parser.add_argument("-F", "--input_file", type=str, metavar='', required=True,
                        help="Location of the input ABF file.")
    parser.add_argument("-P", "--plot", metavar='', help="Plots all the data and channels.")
    parser.add_argument("-S", "--save", metavar='', help="Save data to CSV.")
    parser.add_argument("-O", "--output_path", metavar='', help="Specify path to save CSV.")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


def _hacky():
    path = 'D:\\sparc\\experimental_data\\Tompkins\\Sample_4_010518\\ephys\\cell_3\\abf'
    filenames = os.listdir(path)

    output_path = 'D:\\sparc\\experimental_data\\Tompkins\\Sample_4_010518\\ephys\\cell_3\\csv'

    for filename in filenames:
        abf_file = os.path.join(path, filename)
        abf = ABFer(abf_file)
        print('Saving CSV for file {}'.format(filename))
        abf.save_to_csv(output_path)

    print('Done.')


if __name__ == '__main__':
    """ MAIN: """
    _main()

    """ Hacky: """
    # _hacky()
