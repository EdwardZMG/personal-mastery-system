# Edward Growth System - 快速部署指南

## 前置要求

### 1. 服务器准备（阿里云/腾讯云轻量应用服务器）
- 系统：Ubuntu 22.04 LTS
- 配置：2核CPU / 2GB内存 / 50GB存储
- 费用：约¥50/月

### 2. 获取4个关键凭证

#### 凭证1: 飞书群Webhook URL
1. 打开飞书，创建新群或进入现有群
2. 点击右上角"..." → "添加机器人" → "自定义机器人"
3. 设置机器人名称为"Edward成长系统"
4. 复制Webhook地址（格式：`https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx`）

#### 凭证2: Server酱SendKey（微信推送）
1. 访问 https://sct.ftqq.com/
2. 使用微信扫码登录
3. 登录后复制SendKey（格式：`SCTxxxxxxxxxxxxxxxxxxx`）
4. 关注"方糖"公众号接收微信消息

#### 凭证3: 飞书企业应用凭证
1. 访问 https://open.feishu.cn/
2. 点击"创建企业自建应用"
3. 填写应用名称"Edward成长系统"、描述、图标
4. 进入应用管理页面，复制：
   - App ID: `cli_xxxxxxxxxxxxxxxx`
   - App Secret: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. 在"权限管理"中开通以下权限：
   - `im:message`（发送消息）
   - `contact:user.base:readonly`（读取用户信息）
6. 发布应用（选择"仅企业内部可用"）

#### 凭证4: 你的飞书Open ID
1. 在飞书应用中，点击"版本管理与发布" → "创建版本"
2. 在"事件与回调"中，临时订阅"接收消息"事件
3. 向应用发送任意消息，从调试日志中查看你的Open ID
4. 或者使用飞书API测试工具查询自己的Open ID（格式：`ou_xxxxxxxxxxxxxxxx`）

## 部署步骤

### Step 1: 上传代码到服务器

```bash
# 本地打包
cd C:\Users\admin\Documents\Qoder\2026-10-11\14fabd93
tar -czf edward-growth.tar.gz backend/ database/

# 上传到服务器（替换your_server_ip为你的服务器IP）
scp edward-growth.tar.gz root@your_server_ip:/opt/

# SSH登录服务器
ssh root@your_server_ip
```

### Step 2: 解压并配置

```bash
# 服务器上执行
cd /opt
tar -xzf edward-growth.tar.gz
mv backend edward-growth
cd edward-growth

# 安装Python和依赖
apt update
apt install -y python3.10 python3.10-venv python3-pip postgresql postgresql-contrib redis-server

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
vim .env
```

在`.env`文件中填入4个凭证：
```ini
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx
SERVERJIANG_SENDKEY=SCTxxxxxxxxxxxxxxxxxxx
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_USER_OPEN_ID=ou_xxxxxxxxxxxxxxxx
DATABASE_URL=postgresql://edward:your_password@localhost:5432/edward_growth
```

### Step 3: 配置数据库

```bash
# 启动PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# 创建数据库和用户
sudo -u postgres psql
CREATE USER edward WITH PASSWORD 'your_password';
CREATE DATABASE edward_growth OWNER edward;
\q

# 导入schema
psql -U edward -d edward_growth -f ../database/schema.sql
```

### Step 4: 启动服务

```bash
# 测试运行
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 浏览器访问 http://your_server_ip:8000/docs 查看API文档
```

### Step 5: 配置systemd开机自启

```bash
# 复制service文件
cp edward-growth.service /etc/systemd/system/

# 重载systemd
systemctl daemon-reload

# 启动服务
systemctl start edward-growth
systemctl enable edward-growth

# 查看状态
systemctl status edward-growth
```

### Step 6: （可选）配置Nginx反向代理和HTTPS

```bash
# 安装Nginx
apt install -y nginx

# 创建Nginx配置
cat > /etc/nginx/sites-available/edward-growth <<EOF
server {
    listen 80;
    server_name growth.edward.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# 启用配置
ln -s /etc/nginx/sites-available/edward-growth /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx

# 配置HTTPS（使用Let's Encrypt）
apt install -y certbot python3-certbot-nginx
certbot --nginx -d growth.edward.com
```

## 测试推送

```bash
# 测试所有推送渠道
curl -X POST "http://localhost:8000/test-push/" \
  -H "Content-Type: application/json" \
  -d '{"message": "测试推送成功！"}'
```

你应该收到：
- ✅ 飞书群消息（如果配置了Webhook）
- ✅ 微信消息（如果配置了Server酱）
- ✅ 飞书私聊消息（如果配置了自定义Bot）

## 监控和维护

```bash
# 查看日志
journalctl -u edward-growth -f

# 重启服务
systemctl restart edward-growth

# 查看服务状态
systemctl status edward-growth

# 更新代码
cd /opt/edward-growth
git pull  # 如果使用git
systemctl restart edward-growth
```

## 常见问题

### Q: 收不到飞书消息？
A: 检查：
1. Webhook URL是否正确
2. 飞书应用的权限是否开通
3. Open ID是否正确
4. 查看日志：`journalctl -u edward-growth -f`

### Q: 收不到微信消息？
A: 检查：
1. ServerJiang SendKey是否正确
2. 是否关注了"方糖"公众号
3. ServerJiang账户是否有剩余额度

### Q: 定时任务不执行？
A: 检查：
1. scheduler是否在main.py中正确启动
2. 服务器时区是否为Asia/Shanghai
3. 查看日志确认任务是否触发

## 下一步

部署成功后，你将每天收到3次推送：
- ☀️ 6:00 AM - 晨间提醒
- 🌞 12:30 PM - 午间复盘
- 🌙 9:00 PM - 晚间总结

每周日20:00收到周复盘提醒，每月1日9:00收到月度里程碑检查。

**开始行动吧，Edward！**
