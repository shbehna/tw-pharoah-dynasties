"""Campaign AI targets: where AI armies go (not whether the AI goes to war).

- a distance penalty when the AI gives tasks to its armies, so nearby targets win over far ones
- task priorities rescaled: lower for targets anywhere on the map, higher for neighbouring
  targets and for the defence of the AI's own territory
"""

from __future__ import annotations

import collections

from lib.data import Overlay

FEATURE = "ai"

PERSONALITIES = "cai_personalities_tables"
TMS_VARIABLES = "cai_task_management_system_variable_group_junctions_tables"
GENERATOR_PRIORITIES = "cai_task_management_system_task_generator_groups_generators_junctions_tables"
GENERATOR_PREFIX = "TASK_GENERATOR_"  # after CAI_TMS_ or CAI_TMS_GDS_
LEGACY_PREFIX = "troy_"

NO_PENALTY_TURNS = "ALLOCATOR_PRE_SCORING_TASK_PRIORITY_DISTANCE_SCALING_NO_SCALING_WITHIN_TURNS_DISTANCE"
MIN_SCORE = "ALLOCATOR_SCORING_DISTANCE_SCALING_RETAINED_MINIMUM_SCORE_PROPORTION_NONRECRUITING"
MIN_SCORE_RECRUITING = "ALLOCATOR_SCORING_DISTANCE_SCALING_RETAINED_MINIMUM_SCORE_PROPORTION_RECRUITING"


def apply(overlay: Overlay, settings) -> None:
    s = settings
    _distance(overlay, s)
    _priorities(overlay, s)


def _distance(overlay: Overlay, s) -> None:
    values = {
        NO_PENALTY_TURNS: s.AI_DISTANCE_NO_PENALTY_TURNS,
        MIN_SCORE: s.AI_DISTANCE_MIN_SCORE,
        MIN_SCORE_RECRUITING: s.AI_DISTANCE_MIN_SCORE_RECRUITING,
    }
    groups = set()
    for row in list(overlay.rows(TMS_VARIABLES)):
        if row["variable_key"] in values:
            overlay.put(TMS_VARIABLES, dict(row, value=values[row["variable_key"]]), FEATURE)
            groups.add(row["group_key"])
    overlay.note(FEATURE, f"Distance penalty for AI army tasks ({len(groups)} variable groups, every AI personality): "
                          f"no penalty within {s.AI_DISTANCE_NO_PENALTY_TURNS:g} turns; a target at the far end "
                          f"of the range keeps {s.AI_DISTANCE_MIN_SCORE:g} of its score "
                          f"({s.AI_DISTANCE_MIN_SCORE_RECRUITING:g} for armies that are recruiting).")


def _generator_groups(overlay: Overlay) -> set[str]:
    """Task generator groups used by the game's AI personalities (Troy leftovers excluded).

    Some of them are Troy groups that Pharaoh personalities use in special situations (last stand,
    no regions left).
    """
    profiles = {row["task_management_system_task_generation_profile"] for row in overlay.rows(PERSONALITIES)
                if not row["key"].startswith(LEGACY_PREFIX)}
    groups = {row["default_generator_group"]
              for row in overlay.rows("cai_personalities_task_management_system_task_generator_profiles_tables")
              if row["key"] in profiles}
    groups |= {row["generator_group_key"]
               for row in overlay.rows("cai_personalities_tms_task_generator_profiles_strategic_contexts_junctions_tables")
               if row["task_generator_profile_key"] in profiles}
    groups |= {row["task_generator_group"]
               for row in overlay.rows("cai_personalities_tms_task_generator_profile_faction_statuses_junctions_tables")
               if row["task_generator_policy_key"] in profiles}
    return groups


def _priorities(overlay: Overlay, s) -> None:
    multipliers = s.AI_TASK_PRIORITY_MULTIPLIERS
    values = s.AI_TASK_PRIORITY_VALUES
    both = set(multipliers) & set(values)
    if both:
        raise ValueError(f"AI tasks both in AI_TASK_PRIORITY_MULTIPLIERS and AI_TASK_PRIORITY_VALUES: {sorted(both)}")
    groups = _generator_groups(overlay)
    changed = collections.Counter()
    for row in list(overlay.rows(GENERATOR_PRIORITIES)):
        if row["task_generator_group_key"] not in groups or GENERATOR_PREFIX not in row["task_generator_key"]:
            continue
        name = row["task_generator_key"].split(GENERATOR_PREFIX, 1)[1]
        if name in multipliers:
            priority = float(row["priority"]) * multipliers[name]
        elif name in values:
            priority = values[name]
        else:
            continue
        overlay.put(GENERATOR_PRIORITIES, dict(row, priority=priority), FEATURE)
        changed[name] += 1
    unused = sorted((set(multipliers) | set(values)) - set(changed))
    if unused:
        raise ValueError(f"AI tasks not found in the game's task generator groups: {unused}")
    parts = [f"{name} x{multipliers[name]:g}" for name in multipliers]
    parts += [f"{name} = {values[name]:g}" for name in values]
    overlay.note(FEATURE, f"AI army task priorities in {len(groups)} task generator groups "
                          f"({sum(changed.values())} rows): {', '.join(parts)}.")
