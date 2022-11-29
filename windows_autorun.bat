@echo off
title docker_spinup_windows
set dockerimage=dimage
set container=mysql-db
set volume=mysql-vol-cap
::set volume=test
set sql_pword=pw
set database=hyperopt
set wcardPath=wcards/rnd/tests/

set problemCard=%1
set /A timeout=%2

if [%problemCard%] == [] CALL :print_usage || GOTO :eof
if [%timeout%] == [] CALL :print_usage || GOTO :eof


docker volume ls -q | findstr %volume% >nul 2>&1
if %errorlevel% == 1 docker volume create %volume% >nul 2>&1

docker build -t %dockerimage% .

docker stop %container% >nul 2>&1
docker rm %container% >nul 2>&1
docker run -d -p 3306:3306 --name=%container% -v %volume%:/var/lib/mysql --mount type=tmpfs,destination=/mnt/ramdisk -e MYSQL_ROOT_PASSWORD=%sql_pword% %dockerimage%

set finalPath=%wcardPath%%problemCard%

docker exec -i %container% sh -c "python3 -u src/wrapper.py %finalPath% %timeout%"

goto :eof


:print_usage
echo USAGE:
echo .\windows_autorun.bat problemcard timeout
echo Example .\windows_autorun.bat test1.wcard 2
EXIT /B 1