from __future__ import annotations
from time import sleep
import glob
import os
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np


class Mat2Img:
    DATA_ROOT = Path.home().joinpath("data.cresis.ku.edu")
    def __init__(self, season_path):
        self.season: Path= Mat2Img.DATA_ROOT.joinpath(season_path)
        self.echo_data: None | h5py.File = None

    def load_data(self, matfile_path):
        self.echo_data = h5py.File(matfile_path, "r")

    def plot_image(self, save_img: Path = None):
        data: np.ndarray = self.echo_data["Data"]
        data: np.ndarray = 10 * np.log10(data).T

        x_min, x_max = 0, data.shape[1] - 1
        y_min, y_max = (lambda y: (y.min(), y.max()))(self.echo_data["Time"][()].squeeze())

        fig, ax = plt.subplots()
        cax = ax.imshow(data, cmap='gray_r', extent=(x_min, x_max, y_min, y_max), aspect='auto')

        if save_img is not None:
            plt.axis('off')
            img_path = f'{save_img.parent.absolute()}/Image{save_img.stem[4:]}.jpg'
            print(f"Saving image to: {img_path}")
            fig.savefig(img_path, bbox_inches='tight', pad_inches=0, dpi=300)
        else:
            print("Image not passed. Plotting the echogram...")
            plt.axis('on')
            # Add a colorbar to the plot
            cbar = fig.colorbar(cax, ax=ax, orientation='vertical')
            cbar.set_label('Echogram Intensity')

            # Add labels and a title
            ax.set_xlabel('Range line')
            ax.set_ylabel('Two way travel time (us)')
            ax.set_title(f'Echogram frame')
            # Show the plot
            plt.show()

if __name__ == '__main__':
    obj = Mat2Img("data/rds/2023_Antarctica_BaslerMKB/")
    for top, dirs, files in os.walk(obj.season / "CSARP_standard"):
        for dir in dirs:
            temp_dir = obj.season / "CSARP_standard" / dir
            print(f"Changing dir to {dir}...")
            for f in glob.glob("*.mat", root_dir=temp_dir):
                matfile = temp_dir / f
                # print(matfile.parent.absolute())
                obj.load_data(matfile)
                obj.plot_image(save_img=matfile)
                sleep(0.5)
