"""Campaign AI targets."""

# Where AI armies go, not whether the AI goes to war: wars and aggressiveness are unchanged.
# Distance penalty when the AI gives tasks to its armies. In vanilla, 159 of the 163 Pharaoh AI
# personalities use a profile without any penalty (a far target keeps its full score).
# Targets closer than this many turns of movement are not penalised (vanilla 4; 5 for the
# other 4 personalities).
AI_DISTANCE_NO_PENALTY_TURNS = 2
# Proportion of its score a target at the far end of the range keeps (vanilla 1.0 = no penalty;
# the other 4 personalities: 0.2 and 0.1), for armies that are not recruiting / that are.
AI_DISTANCE_MIN_SCORE = 0.2
AI_DISTANCE_MIN_SCORE_RECRUITING = 0.1
# Multipliers for the priority of AI army tasks, for every culture (each keeps its own values).
# Keys are task generator names without their "CAI_TMS_[GDS_]TASK_GENERATOR_" prefix.
AI_TASK_PRIORITY_MULTIPLIERS = {
    # Targets anywhere on the map
    "ATTACK_ENEMY_LAST_SETTLEMENT": 0.02,  # vanilla 1000-1500, the highest priority of all
    "ATTACK_ALL_ENEMY_SETTLEMENTS_IF_HAVENT_EXPANDED_RECENTLY": 0.25,  # vanilla 2-20
    "ATTACK_ALL_ENEMY_MAIN_THREAT_SETTLEMENTS": 0.5,  # vanilla 7-18
    "ATTACK_ALL_ENEMY_SETTLEMENTS": 0.5,  # vanilla 0.5-1
    "WAR_COORDINATION_ATTACK_FORCES": 0.25,  # helping an ally, vanilla 50-75
    "WAR_COORDINATION_ATTACK_REGIONS": 0.25,
    # Neighbouring targets
    "ATTACK_REGIONS_NEIGHBOURNIG_OWN_REGIONS_ENEMY": 3,  # vanilla 0.8-5
    "ATTACK_PROVINCES_NEIGHBOURNIG_OWN_REGIONS_ENEMY": 3,  # vanilla 1-9
    "ATTACK_PROVINCES_NEIGHBOURNIG_OWN_PROVINCES_ENEMY": 3,  # vanilla 0.7-7
    "ATTACK_NEIGHBOURING_WAR_REGIONS": 3,  # vanilla 1-2.6
    "COMPLETE_PROVINCE": 5,  # vanilla 0.6
    # Defence of own territory
    "DEFEND_BESIEGED_SETTLEMENT": 4,  # vanilla 2-10
    "ACTIVELY_DEFEND_THREATENED_REGIONS": 4,  # vanilla 0.5-0.75
    "DEFEND_OWNED_REGIONS": 4,  # vanilla 0.25
    "ACTIVELY_DEFEND_CAPITAL": 4,  # vanilla 0.25
    "RECAPTURE_RECENTLY_LOST_TERRITORY": 4,  # vanilla 0.25
    "DEFEND_REGIONS_NEIGHBOURING_ENEMY": 3,  # vanilla 1.25-3
    "ACTIVELY_DEFEND_REGIONS_NEIGHBOURING_ENEMY_MAIN_THREAT": 2,  # vanilla 3-8
    "ACTIVELY_DEFEND_REGIONS_NEIGHBOURING_MAIN_THREAT": 2,  # vanilla 1.5-7
}
# Priorities set to a fixed value, for tasks that vanilla turns off (priority 0).
AI_TASK_PRIORITY_VALUES = {
    "CONSOLIDATE_BORDERS": 3,  # vanilla 0
}
