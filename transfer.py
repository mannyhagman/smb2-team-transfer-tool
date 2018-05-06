import sqlite3
import zlib
import os
import json
import uuid
import sys
import math
import shutil

# SMB2 saves GUIDs in blob form, which Python makes bytes
# Convert it to UUID form to save to file
# then check if the type is guid coming back.
class BytesEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return {
                "_type": "guid",
                "value": uuid.UUID(bytes=obj).hex
            }
        return super(BytesEncoder, self).default(obj)

class BytesDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if '_type' not in obj:
            return obj
        type = obj['_type']
        if type == 'guid':
            return uuid.UUID(obj['value']).bytes
        return obj

def export_team(c):

    while True:
        print('Type the name of the team you wish to export.')
        team_name = input('--> ')
        c.execute('SELECT * FROM t_teams WHERE teamName = ? COLLATE NOCASE', (team_name,))
        team_choices = c.fetchall()
        if len(team_choices) == 0:
            print('No teams exist with the name ' + team_name + '. Please try again.')
        else:
            break
    for item in team_choices[:]:
        if item[1] is not None:
            team_choices.remove(item)

    if len(team_choices) > 1:
        while True:
            print('There are multiple teams with that name, please choose one.')
            print('Note the highest-numbered teams are the most recently created.')
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
                team_guid = team_choices[choice-1][0]
                break
    else:
        print('Found a team! Using found team.')
        team_guid = team_choices[0][0]

    data = {}

    # t_teams
    c.execute('SELECT * FROM t_teams WHERE GUID = ?', (team_guid,))
    team_data = c.fetchone()
    data['team_data'] = team_data

    # t_baseball_players
    c.execute('SELECT * FROM t_baseball_players WHERE teamGUID = ?', (team_guid,))
    player_guids = []
    player_data = c.fetchall()
    for item in player_data:
        player_guids.append(item[0])

    data['player_data'] = player_data

    # t_baseball_player_local_ids
    player_ids = []
    for guid in player_guids:
        c.execute('SELECT * FROM t_baseball_player_local_ids WHERE GUID = ?', (guid,))
        new_id = c.fetchone()
        player_ids.append((new_id[0], guid))
    data['player_ids'] = player_ids

    # t_baseball_player_attributes
    player_attr_data_all = []
    for id_ in player_ids:
        c.execute('SELECT * FROM t_baseball_player_attributes WHERE baseballPlayerLocalID = ?', (id_[0],))
        player_attr_data = c.fetchall()
        player_attr_data_all.append(player_attr_data)
    data['player_attr_data'] = player_attr_data_all

    #t_lineups
    c.execute('SELECT * FROM t_lineups WHERE teamGUID = ?', (team_guid,))
    lineup_data = c.fetchone()
    lineup_guid = lineup_data[0]
    data['lineup_data'] = lineup_data

    #t_batting_orders
    c.execute('SELECT * FROM t_batting_orders WHERE lineupGUID = ?', (lineup_guid,))
    order_data = c.fetchall()
    data['order_data'] = order_data

    #t_pitching_rotations
    c.execute('SELECT * FROM t_pitching_rotations WHERE lineupGUID = ?', (lineup_guid,))
    rotation_data = c.fetchall()
    data['rotation_data'] = rotation_data

    #t_defensive_positions
    c.execute('SELECT * FROM t_defensive_positions WHERE lineupGUID = ?', (lineup_guid,))
    dpos_data = c.fetchall()
    data['dpos_data'] = dpos_data

    #t_team_local_ids
    c.execute('SELECT * FROM t_team_local_ids WHERE GUID = ?', (team_guid,))
    team_id_data = c.fetchone()
    data['team_id_data'] = team_id_data

    #t_team_attributes
    c.execute('SELECT * FROM t_team_attributes WHERE teamLocalID = ?', (team_id_data[0],))
    team_attr_data = c.fetchall()
    data['team_attr_data'] = team_attr_data

    #t_team_logos
    c.execute('SELECT * FROM t_team_logos WHERE teamGUID = ?', (team_guid,))
    logo_data = c.fetchall()
    logo_guids = []
    for item in logo_data:
       logo_guids.append(item[0])
    data['logo_data'] = logo_data

    #t_team_logo_attributes
    logo_attrs_all = []
    for guid in logo_guids:
        c.execute('SELECT * FROM t_team_logo_attributes WHERE teamLogoGUID = ?', (guid,))
        logo_attrs = c.fetchall()
        logo_attrs_all.append(logo_attrs)
    data['logo_attrs'] = logo_attrs_all

    if (os.path.isfile(team_name + '.team')):
        number = 0
        exists = True
        while exists:
            if (os.path.isfile(team_name + '_' + str(number) + '.team')):
                pass
                number += 1
            else:
                fname = team_name + '_' + str(number) + '.team'
                exists = False
    else:
        fname = team_name + '.team'

    f = open(fname, 'w')
    f.write(json.dumps(data, cls=BytesEncoder))
    f.close()

def import_team(save, c):

    # Back up original save data
    shutil.copy2(os.path.join(save[0], save[1]), os.path.join(save[0], 'savedata_backup.sav'))
    print('Backup of savedata made to savedata_backup.sav')

    # Search for team files
    team_files = []
    for root, dirs, files in os.walk('.'):
        for fileName in files:
            if(fileName[-5:] == '.team'):
                relDir = os.path.relpath(root, '.')
                relFile = os.path.join(relDir, fileName)
                if relFile[:2] == './' or relFile[:2] == '.\\':
                    relFile = relFile[2:]
                team_files.append(relFile)

    team_files = sorted(team_files)
    if(len(team_files) == 0):
        return
    # List pages of the team files
    cur_page = 1
    while True:
        allowable_options = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'n', 'p']
        max_pages = math.ceil(len(team_files)/10)
        items_on_last_page = len(team_files) % 10
        if (items_on_last_page == 0):
            items_on_last_page = 10
        if (cur_page == max_pages):
            print('Page ' + str(cur_page) + ' of team files')
            print('Choose an option.')
            for i in range(0, items_on_last_page):
                print(str(i) + '. ' + team_files[10*(cur_page-1) + i])
            if (cur_page > 1):
                print('p. Previous page')
            choice = input('--> ').strip().lower()
            if (choice in allowable_options):
                if (choice == 'n'):
                    print('You are already on the last page.')
                elif (choice == 'p'):
                    if (cur_page == 1):
                        print('You are already on the first page.')
                    else:
                        cur_page -= 1
                else:
                    team_load = team_files[10*(cur_page-1) + int(choice)]
                    break
            else:
                print('That is not a valid option. Please try again.')
        else:
            print('Page ' + str(cur_page) + ' of team files')
            print('Choose an option.')
            for i in range(0, 10):
                print(str(i) + '. ' + team_files[10*(cur_page-1) + i])
            if (cur_page > 1):
                print('p. Previous page')
            if (cur_page < max_pages):
                print('n. Next page')
            choice = input('--> ').strip()
            if (choice in allowable_options):
                if (choice == 'n'):
                    cur_page += 1
                elif (choice == 'p'):
                    if (cur_page == 1):
                        print('You are already on the first page.')
                    else:
                        cur_page -= 1
                else:
                    team_load = team_files[10*(cur_page-1) + int(choice)]
                    break
            else:
                print('That is not a valid option. Please try again.')

        print('')

    with open(team_load) as team_file:
        data = json.loads(team_file.read(), cls=BytesDecoder)

    # t_teams
    team_data = data['team_data']
    c.execute('INSERT INTO t_teams VALUES (?, ?, ?, ?, ?, ?, ?, ?)', team_data)

    # t_baseball_players
    player_data = data['player_data']
    c.executemany('INSERT INTO t_baseball_players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', player_data)

    # t_baseball_player_local_ids
    space = False
    number = 3000
    while not space:
        c.execute('SELECT MAX(localID) FROM t_baseball_player_local_ids WHERE localID < ?', (number,))
        max_val = c.fetchone()[0]
        if max_val < 2500:
            next_val = 2500
            space = True
        elif (max_val < (number-22)):
            next_val = max_val + 1
            space = True
        else:
            number += 10
    player_ids_dict = {}
    player_ids = data['player_ids']
    player_ids_new = []
    for id in player_ids:
        # Do mapping from old ID to new ID
        player_ids_dict[id[0]] = next_val
        player_ids_new.append((next_val, id[1]))
        next_val += 1

    c.executemany('INSERT INTO t_baseball_player_local_ids VALUES (?, ?)', player_ids_new)

    # t_baseball_player_attributes
    player_attr_data = data['player_attr_data']
    for player in player_attr_data:
        for item in player:
            c.execute('INSERT INTO t_baseball_player_attributes VALUES (?, ?, ?, ?, ?, ?, ?)', [player_ids_dict[item[0]]] + item[1:])

    #t_lineups
    lineup_data = data['lineup_data']
    c.execute('INSERT INTO t_lineups VALUES (?, ?, ?)', lineup_data)

    #t_batting_orders
    order_data = data['order_data']
    c.executemany('INSERT INTO t_batting_orders VALUES (?, ?, ?)', order_data)

    #t_pitching_rotations
    rotation_data = data['rotation_data']
    c.executemany('INSERT INTO t_pitching_rotations VALUES (?, ?, ?)', rotation_data)

    #t_defensive_positions
    dpos_data = data['dpos_data']
    c.executemany('INSERT INTO t_defensive_positions VALUES (?, ?, ?)', dpos_data)

    #t_team_local_ids
    c.execute('SELECT MAX(localID) FROM t_team_local_ids')
    next_team_val = int(c.fetchone()[0]) + 1

    team_id_data = data['team_id_data']

    c.execute('INSERT INTO t_team_local_ids VALUES (?, ?)', (next_team_val, team_id_data[1]))

    #t_team_attributes
    team_attr_data = data['team_attr_data']
    for team_attr in team_attr_data:
        c.execute('INSERT INTO t_team_attributes VALUES (?, ?, ?, ?, ?, ?, ?)', [next_team_val] + team_attr[1:])

    #t_team_logos
    logo_data = data['logo_data']
    c.executemany('INSERT INTO t_team_logos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', logo_data)

    #t_team_logo_attributes
    logo_attrs = data['logo_attrs']
    for guid in logo_attrs:
        c.executemany('INSERT INTO t_team_logo_attributes VALUES (?, ?, ?, ?, ?, ?, ?)', guid)



def main():

    print("Ferrea's SMB2 Team Transfer Tool 0.1 beta")

    #This is for easier Linux testing for me
    #in_fname = 'savedata.sav'

    save_files = []

    for root, dirs, files in os.walk(os.path.expanduser('~\AppData\local\Metalhead\Super Mega Baseball 2')):
        for name in files:
            if (name == 'savedata.sav'):
                save_files.append((root, name))

    if len(save_files) > 1:
        print('Multiple save files! Quitting to avoid problems.')
        print('Press Enter to exit.')
        input('')
        sys.exit(0)
    elif (len(save_files) == 0):
        print('No save data found.')
        print('Press Enter key to exit.')
        input('')
        sys.exit(0)

    in_fname = os.path.join(save_files[0][0], save_files[0][1])

    try:
        with open(in_fname, 'rb') as in_data:
            in_file = in_data.read()
        print('Found save data file.')
    except FileNotFoundError:
        print('No save data found.')
        print('Press Enter key to exit.')
        input('')
        sys.exit(1)

    decomp_in_file = zlib.decompress(in_file)
    f = open('database.sqlite', 'wb')
    f.write(decomp_in_file)
    f.close()

    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()

    success = False
    while not success:
        print('Do you wish to import or export data?')
        print('1. Import')
        print('2. Export')
        decision = input('--> ')
        if (decision.strip() == '1'):
            success = True
            try:
                import_team(save_files[0], c)
                conn.commit()
                conn.close()
                with open('database.sqlite', 'rb') as new_data:
                    new_save = new_data.read()
                zlib_save = zlib.compress(new_save)
                f = open(os.path.join(save_files[0][0], 'savedata_new.sav'), 'wb')
                f.write(zlib_save)
                f.close()
                os.replace(os.path.join(save_files[0][0], 'savedata_new.sav'), os.path.join(save_files[0][0], save_files[0][1]))
            except sqlite3.IntegrityError:
                print('There has been a problem with the database.')
                print('Are you trying to add a team that already exists?')
                print('Press Enter to exit.')
                input('')
                sys.exit(0)
            except KeyboardInterrupt:
                conn.close()
                raise KeyboardInterrupt from None
        elif (decision.strip() == '2'):
            success = True
            try:
                export_team(c)
                conn.close()
            except KeyboardInterrupt:
                conn.close()
                raise KeyboardInterrupt from None
        else:
            print('You did not type 1 or 2. Please try again.')

    os.remove('database.sqlite')

    print('Done! Press enter to exit.')
    input('')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('')
        print('Quitting!')
        os.remove('database.sqlite')
        print('Press Enter to close.')
        input('')
        sys.exit(0)
