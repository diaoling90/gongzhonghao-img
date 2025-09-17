@echo off
chcp 65001 >nul
title 手机相册管理工具

:menu
cls
echo.
echo ========================================
echo           手机相册管理工具
echo ========================================
echo.
echo 请选择操作：
echo.
echo 1. 传输图片到手机
echo 2. 删除手机相册中的图片
echo 3. 查看手机相册中的数字文件夹
echo 4. 测试ADB连接
echo 5. 退出
echo.
set /p choice=请输入选择 (1-5): 

if "%choice%"=="1" goto transfer
if "%choice%"=="2" goto delete
if "%choice%"=="3" goto list
if "%choice%"=="4" goto test
if "%choice%"=="5" goto exit
echo 无效选择，请重新输入
pause
goto menu

:transfer
echo.
echo 请输入要传输的文件夹路径：
set /p folder_path=文件夹路径: 
if "%folder_path%"=="" (
    echo 文件夹路径不能为空
    pause
    goto menu
)
python phone_manager.py transfer "%folder_path%"
pause
goto menu

:delete
echo.
echo 请输入要删除的文件夹名称（只支持数字）：
set /p folder_name=文件夹名称: 
if "%folder_name%"=="" (
    echo 文件夹名称不能为空
    pause
    goto menu
)
python phone_manager.py delete "%folder_name%"
pause
goto menu

:list
echo.
python phone_manager.py list
pause
goto menu

:test
echo.
echo 测试ADB连接...
adb devices
echo.
echo 如果看到设备列表，说明连接正常
echo 如果没有设备，请检查：
echo 1. 手机是否连接
echo 2. 是否开启USB调试
echo 3. 是否授权USB调试
pause
goto menu

:exit
echo.
echo 感谢使用！
pause
exit
