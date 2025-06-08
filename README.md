#install uv
PowerShell:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

#confirm install
cmd:
uv -V

#set up script running environment
go to the unzip folder
cmd:
uv sync

#start websocket server
go to the unzip folder
cmd:
uv run ./server2.py