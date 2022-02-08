import Servo
from Runner import Runner, Operation, Sequence

#   DEGREES

degStates = {}

degStates["heater"]     = 0
degStates["d_mag"]      = 0
degStates["d_final"]    = 0
degStates["b_mag"]      = 0
degStates["b_final"]    = 0
degStates["d1"]         = 0
degStates["d2"]         = 0

#   SERVOS

servos = {}

servos["d_arm"] = Servo("d_arm", 0)
servos["d_cyl"] = Servo("d_cyl", 0)
servos["d_mag"] = Servo("d_mag", 0)

servos["b_arm"] = Servo("b_arm", 0)
servos["b_mag"] = Servo("b_mag", 0)
servos["dress_1"] = Servo("dress_1", 0)
servos["dress_2"] = Servo("dress_2", 0)

#   OPERATIONS

ops = {}

ops["dog_to_mag"]       = Operation(100, servos["d_Arm_S"].goto, "d_mag")
ops["dog_to_heater"]    = Operation(100, servos["d_Arm_S"].goto, "heater")
ops["dog_to_bread"]     = Operation(100, servos["d_Arm_S"].goto, "d_final")
ops["dog_down"]         = Operation(100, servos["d_Cyl_S"].down, None)
ops["dog_up"]           = Operation(100, servos["d_Cyl_S"].up, None)
ops["next_dog"]         = Operation(100, servos["d_Mag_S"].next, None)

#TODO ops["cook_dog"]         = Operation(Heater on, None)

ops["bread_to_mag"]     = Operation(100, servos["b_Arm_S"].goto, "b_mag")
ops["bread_to_d1"]      = Operation(100, servos["b_Arm_S"].goto, "d1")
ops["bread_to_d2"]      = Operation(100, servos["b_Arm_S"].goto, "d2")
ops["bread_to_dog"]     = Operation(100, servos["b_Arm_S"].goto, "b_final")
ops["next_bread"]       = Operation(100, servos["b_Mag_S"].next, None)

ops["dress1_push"]      = Operation(100, servos["dress_1"].push, None)
ops["dress1_release"]   = Operation(100, servos["dress_1"].release, None)
ops["dress2_push"]      = Operation(100, servos["dress_2"].push, None)
ops["dress2_release"]   = Operation(100, servos["dress_2"].release, None)

#   SEQUENCES

dog_seq = ["dog_to_mag", "dog_down", "dog_up", "dog_to_heater", "dog_down", "cook_dog", "dog_up", "dog_to_bread", "dog_down", "dog_up", "next_dog"]

bread_seq1 = ["bread_to_mag", "next_bread", "bread_to_d1", "bread_to_dog"]
bread_seq1 = ["bread_to_mag", "next_bread", "bread_to_d2", "bread_to_dog"]

dog = Runner("dog_runner", dog_seq)
bread1 = Runner("bread_runner", bread_seq1)
bread2 = Runner("bread_runner", bread_seq1)