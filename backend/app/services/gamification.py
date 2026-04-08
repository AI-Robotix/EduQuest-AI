def update_progress(user, is_correct: bool, reward_coins: int) -> None:
    if is_correct:
        user.coins += reward_coins
        user.streak += 1
    else:
        user.coins += max(2, reward_coins // 5)
        user.streak = 0
    user.level = 1 + user.coins // 150
