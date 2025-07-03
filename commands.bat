@echo off

if "%1"=="" (
    echo Usage: commands.bat [run^|migrate^|createsuperuser^|shell]
    goto :eof
)

if "%1"=="run" (
    python manage.py runserver
) else if "%1"=="migrate" (
    python manage.py migrate
) else if "%1"=="createsuperuser" (
    python manage.py createsuperuser
) else if "%1"=="shell" (
    python manage.py shell
) else (
    echo Unknown command: %1
    echo Usage: commands.bat [run^|migrate^|createsuperuser^|shell]
)
