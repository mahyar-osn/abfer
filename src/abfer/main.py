import os
import argparse
import pyabf

import csv
import numpy as np
import matplotlib.pyplot as plt


class ProgramArguments(object):
    pass


class ABFReade(object):

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
        plt.legend()
        plt.show()

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
        abf = ABFReade(args.input_file)
    if args.output_path is None:
        output_csv = os.path.split(args.input_file)[0]
    if args.plot:
        abf.plot_abf()
    if args.save:
        abf.save_to_csv(output_csv)
    else:
        raise FileNotFoundError('File {} does  not exists.'.format(args.input_file))


def parse_args():
    parser = argparse.ArgumentParser(description="An IO helper to read, process, and plot ABF file formats.")
    parser.add_argument("input_file", help="Location of the input ABF file.")
    parser.add_argument("plot", help="Plots all the data and channels.")
    parser.add_argument("--output_path", help="Specify path to save CSV.")
    parser.add_argument("save", help="Save data to CSV.")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == '__main__':
    _main()
