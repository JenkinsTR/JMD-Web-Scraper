@ECHO OFF

REM Set master local expansion and command extensions.
REM USE ONCE
@SetLocal enableextensions EnableDelayedExpansion

CLS

ECHO [97m[102m=======================================================================[0m
ECHO                    Selenium web scraper                                          
ECHO             (c)2023 JMDigital. All Rights Reserved.            
ECHO [97m[102m=======================================================================[0m
ECHO.

SET CWD=%~dp0

PUSHD "%CWD%"

REM # UNIQUE TIME MACRO
SET "mm=%DATE:~4,2%"
SET "dd=%DATE:~7,2%"
SET "yy=%DATE:~10,4%"
FOR /f "tokens=1-4 delims=:. " %%A IN ("%time: =0%") DO @SET UNIQUE=%yy%-%dd%-%mm%-%%A%%B-%%C%%D

SET "STARTTIME=%TIME%"
SET ReturnCode=

FOR /F "usebackq tokens=* delims=" %%G IN ("terms.txt") DO (
	
	ECHO [36mScraping for [1m"%%G"[0m . . .
	ECHO.
	IF EXIST "%CWD%%%G" ECHO [33mWARNING: Search term folder already exists at "%CWD%%%G" && ECHO Skipping...[0m
	IF NOT EXIST "%CWD%%%G" python scrape.py %%G
	ECHO.
	IF NOT EXIST "%CWD%%%G" ECHO [92mDone![0m
)

ECHO [92mCompleted all scrapes at[0m [1m%UNIQUE%[0m

PAUSE
EXIT
