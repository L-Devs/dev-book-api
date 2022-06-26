@echo off
cmd /k "cd /d %cd%\env\scripts & activate & cd /d %cd%\dev_book_api & pip install django"