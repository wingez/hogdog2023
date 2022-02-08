import Servo
from Sequencer import Operation, Sequence

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

#   OPERATIONS

ops = {}

ops["dog_to_mag"]       = Operation(servos["d_Arm_S"].goto, "d_mag")
ops["dog_to_heater"]    = Operation(servos["d_Arm_S"].goto, "heater")
ops["dog_to_bread"]     = Operation(servos["d_Arm_S"].goto, "d_final")
ops["dog_down"]         = Operation(servos["d_Cyl_S"].down, None)
ops["dog_up"]           = Operation(servos["d_Cyl_S"].up, None)
ops["next_dog"]         = Operation(servos["d_Mag_S"].next, None)

ops["bread_to_mag"]     = Operation(servos["b_Arm_S"].goto, "b_mag")
ops["bread_to_d1"]      = Operation(servos["b_Arm_S"].goto, "d1")
ops["bread_to_d2"]      = Operation(servos["b_Arm_S"].goto, "d2")
ops["bread_to_dog"]     = Operation(servos["b_Arm_S"].goto, "b_final")
ops["next_bread"]       = Operation(servos["b_MAg_S"].next, None)

#   SEQUENCES

seqs = {}

seqs["init"] = Sequence(["dog_to_mag", "bread_to_mag"], 100)
seqs["get_dog"] = Sequence(["dog_down", "bread_to_mag"], 100)
seqs["s2"] = Sequence(["dog_up", "bread_to_mag"], 100)