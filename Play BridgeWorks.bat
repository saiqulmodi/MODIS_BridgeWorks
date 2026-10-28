@echo off
title MODIS BridgeWorks - Engineering Sandbox
start http://localhost:8000/qa-bank.html
python -m http.server 8000
