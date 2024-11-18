import matplotlib.pyplot as plt
import numpy as np
import scipy
import h5py
from pathlib import Path

DATA_ROOT = Path.home().joinpath("data.cresis.ku.edu")
season = DATA_ROOT.joinpath("data/rds/2023_Antarctica_BaslerMKB/")

echo_fn = season / "CSARP_standard/20240111_02/Data_20240111_02_003.mat"
layer_fn = season / "CSARP_layerData/20240111_02/Data_20240111_02_003.mat"

#TODO
# ----------------------- LAYER SECTION ------------------------------- #
print(echo_fn)
print(layer_fn.exists())
# layers = scipy.io.loadmat(layer_fn.__str__())
# print(layers["twtt"].shape)

# surface = layers["layerData"][0][0]     [0][0]      [0][0]      [1][0]      [0][0]
# # bottom = layers["layerData"][0][1]     [0][0]      [0][0]      [1][0]      [0][0]
# print(mdata["GPS_time"].shape, mdata["Time"][()].squeeze().shape, np.array(range(mdata["Time"].shape[1])).shape)
# surface = np.interp(surface.squeeze(), np.array(range(mdata["Time"].shape[1])), mdata["Time"][()].squeeze())
# surface = np.interp(mdata["GPS_time"][0],surface, mdata["GPS_time"][0])
# print(surface.shape)
# mdata_elcomp = scipy.io.loadmat("/home/p1utoze/Downloads/Data_20240111_02_003-elcomp.mat")

# print(mdata_elcomp["mdata"]["Data"][0][0].shape)
#
# print(np.array_equal(mdata["Data"], mdata_elcomp["mdata"]["Data"][0][0].T))

# ----------------------------------------------------------------------------- #
mdata = h5py.File(echo_fn, "r")
# Create a figure and an axes
fig, ax = plt.subplots()
print(mdata.keys())

data: np.ndarray = mdata["Data"]
data: np.ndarray = 10 * np.log10(data).T
print(data.shape, data.min(), data.max())
print(mdata["Time"][()].shape)
x_min, x_max = 0, data.shape[1] - 1
y_min, y_max = (lambda y: (y.min(), y.max()))(mdata["Time"][()].squeeze())

print(x_min, x_max, y_min, y_max)
# Plot the echogram data using a 256 grayscale colormap
cax = ax.imshow(data, cmap='gray_r', extent=(x_min, x_max, y_min, y_max), aspect='auto')

plt.axis('off')
fig.savefig(f'Image{echo_fn.stem[4:]}.jpg', bbox_inches='tight', pad_inches=0, dpi=300)

plt.axis('on')
# Add a colorbar to the plot
cbar = fig.colorbar(cax, ax=ax, orientation='vertical')
cbar.set_label('Echogram Intensity')

# Add labels and a title
ax.set_xlabel('Range')
ax.set_ylabel('Depth')
ax.set_title('Echogram Plot')
# Show the plot
plt.show()
