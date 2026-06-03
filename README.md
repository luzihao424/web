# 校园闲置时光胶囊 (Campus Idle Time Capsule)

“闲置换故事，旧物藏回忆。” —— 这是一个温暖的、以故事与情感为导向的校园闲置物品流转与回忆寄存平台。

---

## 🎨 视觉风格说明
本项目的前台界面采用了 **「治愈系复古日记 (Healing Retro Diary)」** 视觉设计系统：
*   **治愈配色**：暖沙纸张底色配合复古焦糖主色，辅以温馨的玫瑰红作为情感激活色。
*   **拍立得照片卡片**：闲置物品以拍立得物理相框展现，支持悬浮微偏转与柔和阴影动效。
*   **复古日记信纸**：物品故事详情页呈现为手账日记本信纸，配有红色分割竖线。
*   **马卡龙手写便签墙**：时光胶囊墙呈现为精美的手写便签网格，顶部带半透明粘胶效果。

---

## 🛠️ 本地部署与运行指南

### 1. 新建本地文件夹与克隆代码
在准备存放项目的磁盘路径下，先创建好一个文件夹并拉取代码：

1. **新建文件夹**：在你的电脑上创建一个工作空间目录，例如 `D:\workspace`。
2. **打开终端**：进入该目录下，在此处打开你的终端（推荐使用 `PowerShell` 或 `Git Bash`）。
3. **克隆代码**：在终端内输入以下命令，从 GitHub 拉取项目代码：
   ```bash
   git clone https://github.com/luzihao424/web.git
   ```
4. **进入工作目录**：
   ```bash
   cd web
   ```

### 2. 安装指定版本的 Python (3.14.0)
本项目开发并运行在 **Python 3.14.0** 环境下。请务必安装对应版本以避免依赖库不兼容问题：

*   **方式 A：通过命令行快捷安装（Windows 推荐）**
    ```powershell
    winget install Python.Python.3.14 --version 3.14.0
    ```
*   **方式 B：官网下载安装包**
    前往 [Python 3.14.0 官方下载页面](https://www.python.org/downloads/release/python-3140/) 下载对应的系统安装包，并在安装时勾选 **"Add python.exe to PATH"**。

### 3. 创建与激活虚拟环境
请在终端中切换到项目子目录 `notes` 下，再创建和激活虚拟环境：

1. **进入 notes 目录**：
   ```bash
   cd notes
   ```
2. **创建虚拟环境**：
   ```powershell
   py -m venv .venv
   ```
3. **激活虚拟环境**：
   *   **PowerShell 终端**：
       ```powershell
       .\.venv\Scripts\Activate.ps1
       ```
    *   **CMD (命令提示符) 终端**：
        ```cmd
        .venv\Scripts\activate.bat
        ```
   *(激活成功后，你的命令行前缀会出现 `(.venv)` 字样)*

    > 💡 **PowerShell 报错“在此系统上禁止运行脚本”的解决方法**：
    > 如果激活时遇到该安全策略报错，请先在终端运行以下命令允许当前窗口执行脚本，然后再运行激活命令：
    > ```powershell
    > Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
    > ```

### 4. 安装项目依赖
虚拟环境激活后，可以使用以下命令一键安装已锁定版本的顶层依赖：

*   **默认官方源安装**：
    ```powershell
    pip install -r requirements.txt
    ```
*   **国内镜像加速安装（推荐中国大陆用户使用清华源，下载速度极快）**：
    ```powershell
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```
> **提示**：我们已精简并锁定了虚拟环境实际用到的顶层依赖（如 `supabase`、`Flask-SQLAlchemy`、`Flask-Login` 等），并特别针对 Python 3.14 锁定了兼容库 `websockets==15.0.1`。


### 5. 初始化本地 SQLite 数据库
运行以下命令以在本地创建和初始化数据库表结构：
```powershell
$env:FLASK_APP="app.py"
flask init-db
```
若需要进行数据库表结构迁移（升级）：
```powershell
flask db upgrade
```

### 6. 启动运行
运行服务主程序：
```powershell
python app.py
```
启动后，即可在浏览器中访问本地预览地址：`http://127.0.0.1:5000`

---

## 🔑 管理员后台 (Admin Panel)

本项目配备了完整的管理员后台管理系统（地址为 `/admin/`，仅对管理员账户开放）。

### 1. 如何指定管理员？
在项目部署并启动后，你可以在激活了虚拟环境的终端中，运行以下命令将指定的注册学生设为管理员：
```powershell
flask set-admin <学生学号>
```
*   **示例**：
    ```powershell
    flask set-admin 423470231
    ```

### 2. 管理后台核心模块
*   **数据可视化看板**：总用户数、总发布物品数、历史流转故事统计及流转模式图表。
*   **学生账号管理**：查看全站学生账户，支持模糊检索、封禁与注销操作。
*   **闲置物品审核**：审核全站发布的物品，支持强制下架不合规物品。
*   **故事墙审核**：对匿名流转成功后的日记故事进行置顶推荐或隐藏处理。
