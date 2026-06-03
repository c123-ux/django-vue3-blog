@echo off
chcp 65001 >nul
echo ========================================
echo   博客系统 - 快速启动脚本
echo ========================================
echo.

echo [1/2] 数据库迁移...
D:\PythonProject3\venv\Scripts\python.exe D:\PythonProject3\manage.py migrate --noinput

echo [2/2] 启动开发服务器...
echo.
echo ========================================
echo   后端服务已启动
echo   访问地址: http://127.0.0.1:8001
echo   按 Ctrl+C 停止服务
echo ========================================
echo.

D:\PythonProject3\venv\Scripts\python.exe D:\PythonProject3\manage.py runserver 8001 --noreload
