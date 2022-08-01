from numpy import *


def npy_to_array(path):
    arr = load(path)
    return arr

#For the .toml file when using libpvrnn. 3D array (dataset with several trajectories)
def array_to_npy(dataset, path):
    save(path, dataset)
    print("Dataset saved in ", path)

#To get Torobo (robot or simulator) to move, in Torobopy. "positions" is a 2D array (only one trajectory)
def array_to_npz(arr, path):
    joint_names = []
    positions = arr
    velocities = []
    efforts = []
    timestamps = []
    fps = 0
    savez_compressed(path, joint_names=joint_names, positions=positions, velocities=velocities,
                     efforts=efforts, timestamps=timestamps, fps=fps)


