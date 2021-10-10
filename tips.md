# django 有关命令

### 1. 建立虚拟环境
```python
python3 -m venv <venvname>
```

### 2. 如果没有 virtualenv
```.env
pip install -user virtualenv

```

### 3. 命令创建 django 项目

```.env
django-admin.py startprooject <project-name> .
```

### 4. 创建应用程序

```.env
python3 manage.py startapp <app-name>
```

### 可能需要安装的包
```.env
pip install django-simpleui
pip install django-mdeditor  # 用于后台编辑
pip install markdown # 用于前端显示
pip install Pygments # 用于前端显示markdown里面写的代码的高亮
editor.md 开源的前端的编辑器的源码，这个在GitHub上，下载解压（好像也有官网）
pip install static3

pip install django-embed-video


```