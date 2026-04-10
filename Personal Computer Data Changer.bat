@echo off
chcp 65001 >nul
color 08
title PassCtool - By BLT x Venqus

:: Password Prompt
set /p pass="Enter password: "
if "%pass%" NEQ "blt" exit

:menu
cls
echo.
echo ****************
echo       PCT
echo ****************
echo.
echo 1) List Users on PC
echo 2) Create a New User
echo 3) Change a User's Password
echo 4) Delete a User Account
echo.
set /p input="© "

:: Option 1 - List users
if "%input%" == "1" (
    title List Users
    net user
    pause
    goto menu
)

:: Option 2 - Create new user
if "%input%" == "2" (
    call :checkadmin
    cls
    title User Creation
    set /p user="Enter new username: "
    set /p password="Enter new password: "
    net user %user% %password% /add
    echo.
    echo New user created with credentials:
    echo %user% : %password%
    pause
    goto menu
)

:: Option 3 - Change password
if "%input%" == "3" (
    call :checkadmin
    cls
    set /p username="Target user: "
    set /p password="New password: "
    net user %username% %password%
    pause
    goto menu
)

:: Option 4 - Denied action
if "%input%" == "4" (
    cls
    echo You're not allowed to do that.
    pause
    goto menu
)

goto menu

:checkadmin
net session >nul
if %errorlevel% NEQ 0 (
    cls
    echo.
    echo Please run this script as administrator.
    pause
    exit /b
)
