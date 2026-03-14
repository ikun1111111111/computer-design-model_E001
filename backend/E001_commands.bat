@echo off
REM E-001 用户档案系统 - 快速命令脚本
REM 使用方法：双击运行或命令行执行

echo ============================================================
echo E-001 用户档案系统 - 快速命令
echo ============================================================
echo.
echo 请选择要执行的命令:
echo.
echo [1] 运行模型验证测试（无需数据库）
echo [2] 执行数据库迁移
echo [3] 回滚数据库迁移
echo [4] 运行 API 测试（需要 MySQL 和服务）
echo [5] 启动后端服务
echo [6] 查看帮助
echo.
set /p choice="请输入选项 (1-6): "

if "%choice%"=="1" goto test_models
if "%choice%"=="2" goto migrate
if "%choice%"=="3" goto rollback
if "%choice%"=="4" goto test_api
if "%choice%"=="5" goto start_server
if "%choice%"=="6" goto help
goto end

:test_models
echo.
echo 运行模型验证测试...
python tests/test_e001_user_models_simple.py
goto end

:migrate
echo.
echo 执行数据库迁移...
python app/db/migrations/001_create_user_tables.py
goto end

:rollback
echo.
echo 回滚数据库迁移...
python app/db/migrations/001_create_user_tables.py --rollback
goto end

:test_api
echo.
echo 运行 API 测试...
python tests/test_e001_api.py
goto end

:start_server
echo.
echo 启动后端服务...
python run.py
goto end

:help
echo.
echo ============================================================
echo 帮助信息
echo ============================================================
echo.
echo 手动执行命令:
echo   - 模型测试：python tests/test_e001_user_models_simple.py
echo   - 数据库迁移：python app/db/migrations/001_create_user_tables.py
echo   - 迁移回滚：python app/db/migrations/001_create_user_tables.py --rollback
echo   - API 测试：python tests/test_e001_api.py
echo   - 启动服务：python run.py
echo.
echo 文档位置:
echo   - API 使用指南：docs/E001_API 使用指南.md
echo   - 项目集成说明：docs/E001_项目集成说明.md
echo   - 完成报告：reports/E001_完成报告.md
echo.
goto end

:end
echo.
pause
