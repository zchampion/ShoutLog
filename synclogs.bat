@echo off
echo Make sure you're running this from the Dropbox source.\n

set /p driveletter="Give the Drive letter: "

robocopy %CD% %driveletter%:\shoutlogs\ /mir /xf "synclogs.bat"

timeout /t -1
