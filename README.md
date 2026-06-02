## 本地部署
## 1.配置python3.14
- `git clone` 到本地
- 进入`...\web\notes`目录下

## 2. 配置虚拟环境
```powershell
python -m venv venv

.\venv\Scripts\Activate.ps1
```

## 3. 安装依赖包
```powershell
pip install -r requirements.txt
```

## 4. 初始化数据库
```powershell
$env:FLASK_APP="app.py"
flask init-db
```

## 5. 运行
```powershell
python app.py
# 或者
py app.py
# 或者
flask run
```
启动后，默认可以通过浏览器访问 `http://127.0.0.1:5000`
