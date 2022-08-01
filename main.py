from numpy import *
import utils
import io_utils as io
import random


class TimeSequence:

    def __init__(self, ts_array):
        # A numpy array, usually of two dimensions. Rows correspond to joint angles; columns, to timesteps.
        self.ts_array = ts_array

    def get_ts_array(self):
        return self.ts_array

    def get_shape(self):
        print(self.ts_array.shape)
        return self.ts_array.shape

    def get_number_of_joints(self):
        return len(self.ts_array[0])

    def get_number_of_timesteps(self):
        return len(self.ts_array)

    def get_one_joint(self, index, verbose=False):  # index: from 0-th to n-th -1
        if verbose:
            print(self.ts_array[:,index])
        return self.ts_array[:,index]

    def plot_joints(self, *args):

        if len(args) == 0:
            utils.plot_joints(self.ts_array)
        else:
            selected_array = self.ts_array[:,list(args)]
            utils.plot_joints(selected_array)

    def downsampling(self, new_ts):
        self.ts_array = utils.downsampling(self.ts_array, new_ts)

    #Appends extra joints at the end, column-wise
    def add_joints(self, extra_joints):
        self.ts_array = utils.stack_seq_joints(self.ts_array, extra_joints)

    #Appends extra timesteps at the end, row-wise
    def add_timesteps(self, extra_ts):
        self.ts_array = utils.stack_seq_ts(self.ts_array, extra_ts)
        return self.ts_array


class Primitive(TimeSequence):

    # prim may be either a path to an .npy file, or a numpy array
    # variation: any kind of tag that the user may want to add, to distinguish similar primitives from each other
    def __init__(self, prim, *variation):
        if type(prim) == str:
            self.ts_array = io.npy_to_array(prim)
        else:
            self.ts_array = prim
        self.variation = variation

    def get_variation(self):
        return self.variation


#Useful when starting from single positions of the robot, rather than from trajectories
class Customized(Primitive):

    def __init__(self, *ts_array):
        if len(ts_array) == 0:
            self.ts_array = array([])
        else:
            self.ts_array = ts_array

    def get_array(self):
        print(self.ts_array)
        return self.ts_array

    #Repeat a still position many times, thus creating a "pause" trajectory
    #The argument must be a 2D array of one element (the angle of each joint, at a given timestep)
    def create_pause(self, ts):
        pos = self.ts_array
        self.ts_array = repeat(pos, ts, axis=0)
        return self.ts_array

    #Given two still positions, it creates a trajectory of length "ts" between the two positions
    #The interpolated points are equidistant from each other.
    def pos_interpolate(self, pos1, pos2, ts):
        self.ts_array = io.interpolate(pos1, pos2, ts)


#In this class, sequences are created based on primitives
class DataSet(TimeSequence):

    def __init__(self, *prims):
        self.ts_array = array([]) #The array that will contain the dataset
        self.primitives = array(prims, dtype=Primitive) #An array that contains the primitives
        lst = [] #Empty list that will contain 2D arrays
        self.dict_prob = {} #A dictionary containing the probabilities of repeating, and the corresponding 2D arrays
        for i in range(len(prims)):
            lst.append(prims[i].ts_array)
        self.primitives_arr = array(lst) #An array that contains the sequences (2D arrays) of the primitives

    #Creates a sequence of primitives
    #"num_cycles" corresponds to the number of cycles
    #"prob_repeat" corresponds to the probabilities (%) of appearing, for each corresponding primitive
    def seq_composer(self, num_cycles, *prob_repeat):

        array_lst = random.choices(self.primitives_arr, weights=(prob_repeat), k=num_cycles) #A list of 2D arrays
        arr_stacked = array_lst[0]
        for i in range(1,len(array_lst)):
            arr_stacked = utils.stack_seq_ts(arr_stacked, array_lst[i])

        return arr_stacked #Returns a 2D array

    #Optional. Only after a sequence has been made with seq_composer
    #Interpolates ts timesteps at the beginning of each cycle
    def traj_interpolate(self, arr2d, cycle_length, interp_ts, joints_lst):

        #Create a 2d array representing the columns to change
        selected_joints = arr2d[:,joints_lst]

        for i in range(len(selected_joints)):
            if i == 0:
                continue
            if i % cycle_length == 0:
                pos1 = selected_joints[i-1]
                pos2 = selected_joints[i + cycle_length - 1]
                interp_arr2d = utils.interpolate2(pos1, pos2, cycle_length, interp_ts)
                arr2d[i:(i+cycle_length),joints_lst] = interp_arr2d

        return arr2d

    #Returns a 3D array, consisting in the dataset
    #The shape will be: num_seq x seq_len x num_joints
    #interpolate=True: it will apply interpolation at the beginning of specified joint sequences
    def dataset_composer(self, num_seq, num_cycles, interpolate, *prob_repeat):

        dataset = self.seq_composer(num_cycles, *prob_repeat)
        for i in range(num_seq-1):
            new_seq = self.seq_composer(num_cycles, *prob_repeat)
            dataset = concatenate((dataset, new_seq), axis=0)

        dataset = dataset.reshape(num_seq, int(dataset.shape[0]/num_seq), dataset.shape[1]) #3D array
        print("The shape of the new dataset is: ", dataset.shape)

        # INTERPOLATION ENABLED
        if interpolate:
            interp_ts = int(input("Please, enter the number of interpolated timesteps: "))
            interp_joints_str = input("Please, enter the indexes of the interpolated joints, separated by commas: ")
            interp_joints_str_lst = interp_joints_str.split(',')
            interp_joints_ints = [int(x) for x in interp_joints_str_lst]

            for i in range(len(dataset)):
                dataset[i] = self.traj_interpolate(dataset[i], int(len(dataset[0])/num_cycles), interp_ts, interp_joints_ints)

        self.ts_array = dataset
        return dataset

    def dataset_plot(self, seq_index, *joints):
        utils.dataset_plot(self.ts_array, seq_index, *joints)

    def save_as_npy(self, path_traj):
        io.array_to_npy(self.ts_array, path_traj)



# The datasets are created inside this "main" function
def main():

    pass


if __name__ == "__main__":
    main()


