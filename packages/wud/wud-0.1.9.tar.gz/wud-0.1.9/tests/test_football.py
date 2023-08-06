from wud.football import team_name_revise


def test_team_name_revise():
    assert team_name_revise('Chelsea FC', 'footballapi', 'livescore') == 'Chelsea'
    assert team_name_revise('Tottenham Hotspur', 'livescore', 'short') == 'Spurs'
    
    assert team_name_revise("Man Utd", 'short', 'livescore') == "Manchester United"
    
    assert team_name_revise("Nankatsu", 'footballapi', 'livescore') == "Nankatsu"