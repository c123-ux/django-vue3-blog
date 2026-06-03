@echo off
chcp 65001 >nul
echo ========================================
echo 博客系统增强功能启动脚本
echo ========================================
echo.

echo [1/5] 检查并安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 依赖安装失败！
    pause
    exit /b 1
)
echo ✓ 依赖安装完成
echo.

echo [2/5] 执行数据库迁移...
python manage.py migrate
if %errorlevel% neq 0 (
    echo 数据库迁移失败！
    pause
    exit /b 1
)
echo ✓ 数据库迁移完成
echo.

echo [3/5] 创建Elasticsearch索引（可选）...
python manage.py search_index --rebuild
if %errorlevel% neq 0 (
    echo Elasticsearch索引创建失败（可能Elasticsearch未启动，不影响其他功能）
) else (
    echo ✓ Elasticsearch索引创建完成
)
echo.

echo [4/5] 启动Celery Worker（新窗口）...
start "Celery Worker" cmd /k "celery -A blog_backend worker -l info --pool=solo"
echo ✓ Celery Worker已启动
echo.

echo [5/5] 启动Django后端...
python manage.py runserver

pause