# Dataset Composer

This python package allows us to create datasets from cyclic robot trajectories. For example, we may want to create several sequences of robot movements in which the robot is repeatedly touching or grabbing an object and coming back to its home position. The tools will help us edit and create such datasets, at least with regard to the data processing part between the raw data collection, and the use of a dataset by a neural network. 

## Data requirements

The robot movements (trajectories) must be previously recorded as two-dimensional numpy arrays, in which the columns correspond to the angles of different robot joints, and the rows correspond to the values of such joints at progressive timesteps. A specific robot movement is here called a "primitive". The raw data corresponding to different primitives must have been recorded and saved as separate numpy 2D arrays or .npy files. 
No labels are included in the initial, nor finished, saved data. 

## How the code is structured

The code is organized in classes, which are defined in main.py, and supported by functions from utils.py and io_utils.py. An extra demonstration module is  included: demo.py.   

All classes inherit from *TimeSequence* and work therefore in a similar manner. An object is created from some saved .npy data or 2D array, storing the trajectory as an attribute called "ts_array" (2D numpy array). Most methods in TimeSequence and the other classes act then as getters or setters of the ts_array stored in each object. Class "DataSet" works somewhat differently; its ts_array attribute is not a 2D, but a 3D array (the third dimension corresponds to the different time sequences that make up the whole dataset). 

Objects from class *Primitive* are constructed from numpy arrays or paths to .npy files. They are the main building blocks for the datasets. Tags can be attached to Primitive objects, this way specifying variations or distinctions that we might want to make between similar primitives. 

Objects from class *Customized* take Primitive objects as arguments. They are useful to create pauses or interpolations between positions. 

Class *DataSet* takes primitive objects as arguments. It composes and saves a dataset.  

## Tools/functions of Data Composer

### From **TimeSequence** (thus, inherited by all classes)
(I will describe only the functions whose purpose are not obvious from the name)

*get_ts_array()*

*get_shape()*

*get_number_of_joints()*

*get_number_of_timesteps()*

*get_one_joint(index)*

*plot_joints(*args)*: Very useful to make sure that the process is going well. All joints, or just a few specified ones, can be plotted.

*downsampling(new_ts)*

*add_joints(extra_joints)*

*add_timesteps(extra_ts)*


### From **Primitive**

*get_variation()*: Gets the tag or note associated with a Primitive object, if there is any.

### From **Customized**

*get_array()*

*create_pause(ts)*: Repeats a still position many times, thus creating a "pause" trajectory.

*pos_interpolate(pos1, pos2, ts)*: Given two still positions, it creates a trajectory of length "ts" between the two positions. The interpolated points are equidistant from each other.

### From **DataSet**

*seq_composer(num_cycles, *prob_repeat)*: Creates a single sequence composed by "num_cycles" cycles, with potentially different probabilities of appearance for each primitive. 

*traj_interpolate(arr2d, cycle_length, interp_ts, joints_lst)*: Optional. Only after a sequence has been made with seq_composer. It interpolates "ts" timesteps at the beginning of each cycle

*dataset_composer(num_seq, num_cycles, interpolate, *prob_repeat)*: Returns a 3D array, consisting in the dataset, with shape: "num_seq" x "seq_len" x "num_joints". With "interpolate" set to True, it will apply interpolation at the beginning of specified joint sequences.

*dataset_plot(seq_index, *joints)*: Once a dataset already exists, it allows us to plot just one specific sequence (or a few joints from it). 

*save_as_npy(path_traj)*

The demonstration in demo.py will greatly help understand the workflow. 

## Future work

Exception handling will be added. 



