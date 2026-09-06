@echo off
chcp 65001 > nul
title BanglaBhasha Compiler Live Demo
echo =========================================================
echo    🇧🇩 BanglaBhasha Compiler — Interactive Live Demo
echo =========================================================
echo.
echo [1/2] ব্রাউজারে ডেমো প্লেগ্রাউন্ড চালু করা হচ্ছে...
start http://localhost:5000
echo.
echo [2/2] লোকাল সার্ভার শুরু হচ্ছে (http://localhost:5000)...
echo সার্ভার বন্ধ করতে Ctrl + C চাপুন।
echo.
set PYTHONIOENCODING=utf-8
python server.py
pause
