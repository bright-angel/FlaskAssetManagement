# 项目名称

## 项目介绍

这是一个基于 Flask 的资产管理系统，使用 Flask-SQLAlchemy 进行数据库操作，Flask-WTF 处理表单，以及 Flask-Login 进行用户认证和权限管理。该系统允许用户管理资产、角色和权限，提供了清晰的用户界面和简单的操作流程。

ps: deepseek+手工调教出的，没基础的情况踩了好多坑。。。
## 特性

- 用户认证与授权
- 资产管理（增、删、改、查）
- 角色与权限管理
- 响应式用户界面（基于 Flask-Bootstrap）
- 支持多用户和角色
- 使用环境变量配置项目

## 技术栈

- Python 3.x
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-WTF 1.2.1
- Flask-Login 0.6.3
- Bootstrap-Flask 2.5.0
- python-dotenv 1.0.0

## 安装与配置

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录下创建一个 `.env` 文件，添加以下内容：

```
# 基础配置
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///app.db
SECURITY_PASSWORD_SALT=your_password_salt_here

# 管理员账户配置
ADMIN_USERNAME=admin
ADMIN_PASSWORD=adminpassword
```

## 使用

### 启动项目

在终端中运行以下命令启动 Flask 开发服务器：

```bash
flask run
```

然后在浏览器中访问 `http://127.0.0.1:5000`。

### 用户登录

- 访问 `/register` 进行用户注册。
- 注册后，使用您的凭据登录。

### 资产管理

在登录后，您可以通过导航栏访问资产管理模块，执行资产的创建、修改、删除和查看等操作。




### 注意事项：

1. **项目名称和链接**：请将 `项目名称` 和 GitHub 链接替换为您的实际项目名称和链接。
2. **环境变量**：根据您项目的实际配置，修改 `.env` 文件中的内容。
3. **数据库**：如果您使用其他类型的数据库，请确保相应的连接字符串正确。
4. **联系方式**：提供您的联系信息，以便用户能够与您联系。

希望这个模板能够满足您的需求！如果您还有其他问题，欢迎随时询问。
