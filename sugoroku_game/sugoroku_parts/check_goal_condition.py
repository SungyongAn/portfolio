# ゴール条件を満たしているかの判定
def check_goal_condition(goal_condition, tatget_position)
    if goal_condition == False:
        tatget_position = 1
    else:
        tatget_position = "Goal"
    return tatget_position
