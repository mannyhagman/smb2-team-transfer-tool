# Ferrea's Team Transfer Tool
A tool to transfer teams between saves in Super Mega Baseball 2

Built into a Windows executable using PyInstall with the --onefile option.

**This tool is still in a beta state. It has been tested and should function as expected, however there are no guarantees that use of this tool will not corrupt or destroy your save data. Taking backups manually is highly recommended.**

# Installation
Simply download the standalone binaries from the latest release.

Depending on your PC settings, the tool may be blocked. To solve this, right click on the executable, select Properties, then select Unblock, then apply the changes.

![Alt text](https://raw.githubusercontent.com/JudgeZarbi/smb2-team-transfer-tool/master/images/image1.png)

# Usage

**Before using this tool, you should close Super Mega Baseball 2. You could potentially corrupt your save file if you use this tool while Super Mega Baseball 2 is running.**

It is recommended that you create a folder to store the tool and the .team files in. This allows you to organise them any way you wish. The tool will search for .team files in the folder it is located and any folders inside the same folder. For example:

![Alt text](https://raw.githubusercontent.com/JudgeZarbi/smb2-team-transfer-tool/master/images/image2.png)

In addition, you can manually take a backup of your save data if you wish before using this tool. You can find this (as well as the automatic backup made by the tool when importing teams) by entering `%USERPROFILE%\AppData\Local\Metalhead\Super Mega Baseball 2\` into your file browser address bar and looking inside the folder in that location.

To quit the program at any point if you wish to stop, use <kbd>Ctrl</kbd>-<kbd>C</kbd>.

## Exporting teams
Type <kbd>2</kbd> to enter export mode, then type the name of the team you wish to export.

![Alt text](https://raw.githubusercontent.com/JudgeZarbi/smb2-team-transfer-tool/master/images/image3.png)

If there are multiple teams with a name, such as if you've made a copy of a built-in team, simply follow the instructions and select the team that you wish to export.

![Alt text](https://raw.githubusercontent.com/JudgeZarbi/smb2-team-transfer-tool/master/images/image4.png)

Once you have made your selection, the program will output a .team file in the same folder as the executable is located. This contains your team data that you can share for other people to import.

![Alt text](https://raw.githubusercontent.com/JudgeZarbi/smb2-team-transfer-tool/master/images/image5.png)

## Importing teams
When selecting to import teams, the program automatically makes a backup of your save data in case of any problems. It will however only keep one backup file, so if importing a lot of teams, it is recommended to regularly take backups when the import is confirmed.

Type <kbd>1</kbd> to enter import mode, and then the program will produce a list of up to 10 team files. If you have more than 10 files, you can navigate between pages by typing n for next page and p for previous page, and choosing the file that you wish to import with the number key.

![Alt text](https://raw.githubusercontent.com/JudgeZarbi/smb2-team-transfer-tool/master/images/image6.png)

# Miscellanea
The .team file is in JSON format, and as such is editable in a text editor if you so choose, but there is no guarantee that a manually edited .team file will work.
