from numpy import *
import matplotlib.pyplot as plt
import io_utils as io

def plot_joints(arr2d):  # Plots all joints throughout all timesteps
    timesteps = arange(len(arr2d))
    for row_index in range(len(arr2d[0])):
        plt.plot(timesteps, arr2d[:, row_index], '-,')
    plt.xlabel('Timesteps')
    plt.ylabel('Joint angles')
    plt.show()

#First argument is the 2D array to be sampled from
#Second argument is the desired new number of timesteps
def downsampling(arr2d, new_ts):
    num_ts = len(arr2d)
    if num_ts % new_ts != 0:
        print("The old number of timesteps must be a multiple of the new number of timesteps")
    else:
        multiple = int(num_ts / new_ts)
        new_arr2d = arr2d[::multiple, :]
        #print("The time sequence has been reduced from {} to {}".format(num_ts,new_ts))

    return new_arr2d

#Appends two sequences horizontally (with the same number of timestepts, adds more joints)
def stack_seq_joints(arr1, arr2):
    if len(arr1) != len(arr2):
        print("The arrays must have the same number of rows")
    else:
        joint_extended_arr = hstack((arr1, arr2))
        #print(joint_extended_arr)
    return joint_extended_arr

#Appends two sequences vertically (with the same number joints, adds more timesteps)
def stack_seq_ts(arr1, arr2):
    if len(arr1[0]) != len(arr2[0]):
        print("The arrays must have the same number of columns")
    else:
        ts_extended_arr = vstack((arr1, arr2))
        #print(ts_extended_arr)
    return ts_extended_arr

#Repeat a still position many times, thus creating a "pause" trajectory
#The argument must be a 2D array of one row (the angle of each joint, at a given timestep)
def make_pause(arr1d, ts):
    arr2d = repeat(arr1d, ts, axis=0)
    return arr2d

#Given two still positions, it creates a trajectory of length "ts" between the two positions
#The interpolated points are equidistant from each other
#The positions must be 1D arrays
def interpolate(pos1, pos2, interpolation_ts):
        print("pos1: {} pos2: {} interpolation_ts: {}".format(pos1, pos2, interpolation_ts))
        if len(pos1) != len(pos2):
            print("The two positions must have the same number of joints")
        traj = zeros([interpolation_ts, len(pos1)], dtype='float') #Initialized 2D array
        col = array([])
        for i in range(len(pos1)):
            col = linspace(pos1[i], pos2[i], interpolation_ts)
            traj[:,i] = col
        return traj

#Similar to interpolate(), but offers the possibility of interpolating only within a given timestep window
#Two extra timesteps are given, which demarcate that window. Outside the window, joint values are repeated (pause)
#interp_window_begin and interp_window_end are indexes
def interpolate2(pos1, pos2, cycle_length, interp_ts):
    if len(pos1) != len(pos2):
        print("The two positions must have the same number of joints")

    #Create interpolated range
    traj = zeros([interp_ts, len(pos1)], dtype='float')  # Initialized 2D array. OK so far######
    for i in range(len(pos1)):
        col = linspace(pos1[i], pos2[i], interp_ts)
        traj[:, i] = col

    #Create pause
    pause_ts = cycle_length - interp_ts
    pause = make_pause([pos2], pause_ts)

    #Attach pause to all the previous
    whole_arr = stack_seq_ts(traj, pause)

    return whole_arr

#Plot joints from a 2d sequence, which belongs to a 3d dataset
def dataset_plot(arr3d, seq_index, *joints):

    #arr3d can be a path to an .npy file, or a 3d array
    if type(arr3d) == str:
        arr3d = io.npy_to_array(arr3d)

    #Select the specific sequence
    seq = arr3d[seq_index]

    #Plot all, or specific joints
    if len(joints) == 0:
        plot_joints(seq)
    else:
        selected_array = seq[:,list(joints)]
        plot_joints(selected_array)











