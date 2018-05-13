def _get_team_guid(c):
    """User chooses a team, GUID is returned for use in the DB"""
    while True:
        print('Type the name of the team you wish to export.')
        team_name = input('--> ')
        c.execute('SELECT * FROM t_teams WHERE teamType = 1 AND '
                  ' teamName = ? COLLATE NOCASE',
                  (team_name,))
        team_choices = c.fetchall()
        if len(team_choices) == 0:
            print('No teams exist with the name ' +
                  team_name +
                  '. Please try again.')
        else:
            break
    for item in team_choices[:]:
        if item[1] is not None:
            team_choices.remove(item)

    if len(team_choices) > 1:
        while True:
            print('There are multiple teams with that name, '
                  'please choose one.')
            print('Note the highest-numbered teams '
                  'are the most recently created.')
            count = 0
            for item in team_choices:
                count += 1
                print(str(count) + '. ' + item[2])
            try:
                choice = int(input('--> '))
            except ValueError:
                print('That was not a valid number. Please try again.')
            if (choice < 1 or choice > count):
                print('That was not a valid choice. Please try again.')
            else:
                return team_choices[choice-1][0]
    else:
        print('Found a team! Using found team.')
        return team_choices[0][0]
