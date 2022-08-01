
# This demo shows a realistic use of the package, based on real data taken from a Torobo robot.

# Recorded data:
# Two separate arm robot movements (primitives) have been previously recorded and saved as two .npy files. One corresponds
# to the robot touching an object with the right hand, and subsequently with the left hand (here called "touch" primitive).
# The other primitive is identical to the first for the first half, but for the second half it lifts and drops down the object
# (we will call it "lift" primitive). In addition, the "touch" primitive was recorded when the objected was located
# on the left side of the robot, whereas the "lift" primitive was recorded from the right side of the robot.
# The head positions (note: just "positions", not time sequence trajectories) for the left and right side of the robot are
# also available as .npy files.

# Task:
# We aim to create long sequences by concatenating the two primitives, which will appear with different probabilities.
# There will be pauses between the primitives (periods at which the last position of a primitive stays constant for many
# timesteps). Head positions will be added to each primitive, so that the robot performs the "touch" primitive while
# "looking" left, and the "lift" primitive while looking right.
# Also, we do not want the robot to produce sudden head movements from one primitive to another. Thus, we will add position
# interpolations for the head movements.
# Finally, a dataset, consisting of several such time sequences, will be generated and saved as an .npy file.
# Other features, such as plotting, will be demonstrated throughout the process.


from main import *

path_touch = 'venv/dataset_demo/touch_left.npy'
path_lift = 'venv/dataset_demo/lift_right.npy'

#Two Primitive objects are created
prim_touch = Primitive(path_touch)
prim_lift = Primitive(path_lift)

# # (Optional) Use some TimeSequence methods to inspect the primitives and plot their trajectories

# print("Number of joints of touch primitive: ", prim_touch.get_number_of_joints())
# print("Number of timesteps of touch primitive: ", prim_touch.get_number_of_timesteps())
# print("Number of joints of lift primitive: ", prim_lift.get_number_of_joints())
# print("Number of timesteps of lift primitive: ", prim_lift.get_number_of_timesteps())
# prim_touch.plot_joints()
# prim_lift.plot_joints()
# # Notice that we find 400 timesteps in touch primitive and 600 timesteps in lift primitive

# Make head trajectories for each primitive. (Thus far, we only have head "positions").
head_left_pos = io.npy_to_array("venv/dataset_demo/head_left.npy")
head_left_traj = Customized(head_left_pos)
head_left_traj.create_pause(prim_touch.get_number_of_timesteps()) #Now, its "ts_array" is a pause trajectory of head angles
head_right_pos = io.npy_to_array("venv/dataset_demo/head_right.npy")
head_right_traj = Customized(head_right_pos)
head_right_traj.create_pause(prim_lift.get_number_of_timesteps())

# The head trajectories are added to their corresponding primitives
prim_touch.add_joints(head_left_traj.get_ts_array())
prim_lift.add_joints(head_right_traj.get_ts_array())

# # (Optional) Plot the trajectories of each newly composed primitive, considering only the head joints.
# # First of all, how many dimensions (joints) were the head trajectories composed of?
# print("Number of joints of head (left trajectory): ", head_left_traj.get_number_of_joints())
# print("Number of joints of head (right trajectory): ", head_right_traj.get_number_of_joints())
# prim_touch.plot_joints(12,13)
# prim_lift.plot_joints(12,13)

# Recall that the two primitives have different lengths:
print("Number of timesteps of touch primitive: ", prim_touch.get_number_of_timesteps())
print("Number of timesteps of lift primitive: ", prim_lift.get_number_of_timesteps())

# Let us assume that we want the two primitives to have the same length. In any case, we wanted to downsample them.
prim_touch.downsampling(50)
prim_lift.downsampling(50)

# Create some pauses and add them at the beginning of each primitive
pause_touch = Customized(prim_touch.ts_array[0])
pause_touch.create_pause(10) #A pause of 10 timesteps
prim_touch.ts_array = pause_touch.add_timesteps(prim_touch.ts_array)
pause_lift = Customized(prim_lift.ts_array[0])
pause_lift.create_pause(10) #A pause of 10 timesteps
prim_lift.ts_array = pause_lift.add_timesteps(prim_lift.ts_array)

# At this point, we might be satisfied with the current state of each primitive. Let us finally create a dataset.
# We want a dataset of 6 sequences, each composed of 40 random cycles (primitives).
# "touch" cycles will appear with a probability of 20%; "lift" cycles will have an 80% probability.
# We also want to enable the feature "interpolation". This will be set to True, and further prompts will be outputted.
ds = DataSet(prim_touch, prim_lift) #The DataSet object is created with the two primitives
ds.dataset_composer(6, 40, True, 20, 80)

# Let us "eyeball" whether the sequences were composed correctly, by plotting one of them
ds.dataset_plot(0)

# # If we want to save the dataset as an .npy file:
# path = '(path where you want to save the dataset)'
# ds.save_as_npy(path)












