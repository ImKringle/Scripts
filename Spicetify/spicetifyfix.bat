@echo off
Rem This script just grabs old Spicetify data for when Spotify updates and removes the client - Requires spicetify is installed!
echo Restoring Spicetify Backup
Spicetify backup apply
echo Updating Spicetify
Spicetify upgrade
echo Restoring Backup Data
Spicetify restore backup
echo Applying Update and Install
Spicetify apply
echo All commands exectuted. Opening Spotify!
start "" "C:\Users\dylan\AppData\Roaming\Spotify\Spotify.exe"
