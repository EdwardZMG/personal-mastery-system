# Edward 智能成长系统 - 完整部署指南 v5.0

##  前置准备清单

在开始部署前，请准备好以下信息：

### 必需凭证

- [ ] **飞书群Webhook URL**
  - 创建飞书群 → 添加自定义机器人 → 复制Webhook URL
  - 格式：`https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

- [ ] **Server酱SendKey**（微信推送）
  - 访问 https://sct.ftqq.com/
  - 微信登录 → Dashboard → 复制SendKey
  - 格式：`SCTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

- [ ] **飞书企业自建应用凭证**（方案A）
  - 访问 https://open.feishu.cn/
  - 创建企业自建应用 → 获取App ID和App Secret
  - App ID格式：`cli_xxxxxxxxxxxxxxxx`
  - App Secret格式：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

- [ ] **Edward的飞书Open ID**
  - 在飞书中找到自己的Open ID
  - 格式：`ou_xxxxxxxxxxxxxxxx`

### 服务器环境

- [ ] **Linux服务器**（推荐Ubuntu 22.04）
  - 阿里云/腾讯云轻量应用服务器
  - 配置：2核2G+
  - 成本：约¥50/月

- [ ] **域名**（可选，用于HTTPS）
  - 例如：`bot.edward-growth.com`

---

## 🚀 快速部署（30分钟）

### 步骤1：上传代码到服务器

```bash
# SSH登录服务器
ssh root@your-server-ip

# 创建应用目录
mkdir -p /opt/edward-growth
cd /opt/edward-growth

# 上传代码（使用scp或Git）
# 方式1：使用scp从本地上传
scp -r /path/to/edward-growth-bot/* root@your-server-ip:/opt/edward-growth/

# 方式2：使用Git（如果已推送到GitHub）
git clone https://github.com/your-repo/edward-growth-bot.git .
```

### 步骤2：安装依赖

```bash
# 安装Python 3.10+
apt update && apt upgrade -y
apt install python3 python3-pip python3-venv -y

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤3：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

**填入以下信息：**

```env
# 飞书应用凭证（必填）
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 飞书机器人Webhook（必填，方案B）
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Edward的飞书Open ID（必填）
EDWARD_OPEN_ID=ou_xxxxxxxxxxxxxxxx

# Server酱SendKey（必填，方案C）
SERVER_JIANG_KEY=SCTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# 日志配置
LOG_LEVEL=INFO

# 推送时间配置
MORNING_PUSH_TIME=06:00
NOON_PUSH_TIME=12:30
EVENING_PUSH_TIME=21:00
WEEKLY_REVIEW_TIME=20:00
MONTHLY_CHECK_TIME=09:00

# 学习周期配置
LEARNING_CYCLE_DAYS=90
START_DAY=1
```

### 步骤4：测试运行

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行应用
python -m app.main
```

**访问测试：**
```bash
# 在另一个终端测试
curl http://localhost:8000/
curl http://localhost:8000/health

# 手动触发推送测试
curl -X POST http://localhost:8000/push/morning
curl -X POST http://localhost:8000/push/noon
curl -X POST http://localhost:8000/push/evening
```

**检查飞书和微信是否收到消息！**

### 步骤5：配置Systemd服务（生产环境）

```bash
# 创建service文件
nano /etc/systemd/system/edward-growth.service
```

**内容如下：**

```ini
[Unit]
Description=Edward Growth Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/edward-growth
Environment="PATH=/opt/edward-growth/venv/bin"
ExecStart=/opt/edward-growth/venv/bin/python -m app.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**启动服务：**

```bash
# 重新加载systemd
systemctl daemon-reload

# 启用服务（开机自启）
systemctl enable edward-growth

# 启动服务
systemctl start edward-growth

# 查看服务状态
systemctl status edward-growth

# 查看日志
journalctl -u edward-growth -f
```

### 步骤6：配置Nginx反向代理（可选，推荐）

```bash
# 安装Nginx
apt install nginx -y

# 创建Nginx配置
nano /etc/nginx/sites-available/edward-growth
```

**内容如下：**

```nginx
server {
    listen 80;
    server_name bot.your-domain.com;  # 替换为你的域名

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**启用配置：**

```bash
# 创建软链接
ln -s /etc/nginx/sites-available/edward-growth /etc/nginx/sites-enabled/

# 测试配置
nginx -t

# 重新加载Nginx
systemctl reload nginx
```

**配置HTTPS（推荐）：**

```bash
# 安装Certbot
apt install certbot python3-certbot-nginx -y

# 获取SSL证书
certbot --nginx -d bot.your-domain.com

# 自动续期测试
certbot renew --dry-run
```

---

## 🧪 测试验证

### 测试1：API健康检查

```bash
curl http://localhost:8000/health
# 应返回：{"status": "healthy"}
```

### 测试2：手动触发推送

```bash
# 晨间推送
curl -X POST http://localhost:8000/push/morning

# 午间推送
curl -X POST http://localhost:8000/push/noon

# 晚间推送
curl -X POST http://localhost:8000/push/evening
```

**检查：**
- ✅ 飞书群是否收到消息？
- ✅ 微信是否收到消息？

### 测试3：查看日志

```bash
# 查看应用日志
journalctl -u edward-growth -f

# 或查看实时日志
tail -f /var/log/edward-growth.log
```

---

## 🔧 故障排查

### 问题1：服务无法启动

```bash
# 查看详细错误
journalctl -u edward-growth -n 100

# 检查端口是否被占用
netstat -tulpn | grep 8000

# 检查环境变量
cat .env
```

**解决方案：**
- 确保`.env`文件中的凭证正确
- 确保端口8000未被占用
- 检查Python依赖是否安装完整

### 问题2：飞书消息发送失败

```bash
# 检查App ID和App Secret是否正确
cat .env | grep FEISHU_APP

# 检查EDWARD_OPEN_ID是否正确
cat .env | grep EDWARD_OPEN_ID

# 测试飞书API
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_xxx","app_secret":"xxx"}'
```

**解决方案：**
- 确认飞书应用权限已开通
- 确认EDWARD_OPEN_ID正确
- 检查网络连接

### 问题3：微信推送失败

```bash
# 检查Server酱SendKey是否正确
cat .env | grep SERVER_JIANG_KEY

# 测试Server酱API
curl "https://sctapi.ftqq.com/SCTxxxxxxxx.send?title=test&desp=test"
```

**解决方案：**
- 确认SendKey正确
- 确认已关注Server酱服务号
- 检查免费额度是否用完

### 问题4：定时任务不执行

```bash
# 检查scheduler是否运行
ps aux | grep scheduler

# 手动触发测试
curl -X POST http://localhost:8000/push/morning

# 查看日志
journalctl -u edward-growth -f | grep "Triggering"
```

**解决方案：**
- 确保应用正在运行
- 检查系统时间是否正确
- 检查时区设置

---

## 📊 监控与维护

### 监控服务状态

```bash
# 查看服务状态
systemctl status edward-growth

# 查看资源使用
htop

# 查看端口占用
netstat -tulpn | grep 8000
```

### 查看日志

```bash
# 实时日志
journalctl -u edward-growth -f

# 最近100行日志
journalctl -u edward-growth -n 100

# 错误日志
journalctl -u edward-growth -p err
```

### 备份数据

```bash
# 备份环境变量
cp .env .env.backup.$(date +%Y%m%d)

# 备份数据库（如果使用PostgreSQL）
pg_dump edward_growth_db > backup_$(date +%Y%m%d).sql

# 备份日志
tar -czf logs-backup-$(date +%Y%m%d).tar.gz /var/log/edward-growth/
```

### 更新代码

```bash
cd /opt/edward-growth
source venv/bin/activate

# 拉取最新代码
git pull

# 安装新依赖
pip install -r requirements.txt

# 重启服务
systemctl restart edward-growth

# 查看状态
systemctl status edward-growth
```

---

## 🎯 下一步行动

### 立即做的（今天）

1. **获取凭证**
   - 飞书群Webhook URL
   - Server酱SendKey
   - 飞书应用App ID + App Secret
   - Edward的飞书Open ID

2. **部署到服务器**
   - 按照上述步骤1-5操作
   - 测试推送是否正常

3. **验证功能**
   - 手动触发三次推送
   - 确认飞书和微信都收到消息

### 本周做的

1. **配置飞书Bot事件订阅**（方案A增强）
   - 在飞书开放平台配置事件订阅
   - 实现双向互动

2. **完善数据库**
   - 安装PostgreSQL
   - 导入schema.sql
   - 连接应用到数据库

3. **测试完整流程**
   - 用户注册
   - 接收推送
   - 记录学习
   - 查看仪表盘

### 本月做的

1. **前端开发**
   - Web App（Next.js）
   - Mobile App（React Native）

2. **AI模型训练**
   - 推荐算法优化
   - NLP模型微调
   - 知识图谱构建

3. **产品化准备**
   - 多用户支持
   - 订阅系统
   - 支付集成

---

## 📞 技术支持

### 文档资源

- 飞书开放平台：https://open.feishu.cn/document
- FastAPI文档：https://fastapi.tiangolo.com/
- PostgreSQL文档：https://www.postgresql.org/docs/
- Server酱文档：https://sct.ftqq.com/doc

### 常见问题

**Q: 如何获取Edward的飞书Open ID？**
A: 在飞书开放平台 → 应用管理 → 权限管理 → 查看用户ID

**Q: 推送时间如何修改？**
A: 编辑`.env`文件中的`MORNING_PUSH_TIME`等参数，然后重启服务

**Q: 如何添加新的学习内容？**
A: 通过API `/content/create` 或直接插入数据库`learning_content`表

**Q: 如何查看用户学习数据？**
A: 通过API `/analytics/dashboard` 或直接查询数据库视图`user_dashboard_summary`

---

## ✅ 部署检查清单

- [ ] 服务器已购买并配置
- [ ] Python 3.10+已安装
- [ ] 代码已上传到服务器
- [ ] 依赖已安装
- [ ] `.env`文件已配置
- [ ] 服务已启动并运行
- [ ] 飞书推送测试成功
- [ ] 微信推送测试成功
- [ ] Systemd服务已配置
- [ ] Nginx反向代理已配置（可选）
- [ ] HTTPS已配置（可选）
- [ ] 日志监控已设置
- [ ] 备份策略已制定

---

## 🎉 恭喜！

完成以上步骤后，你的**Edward智能成长系统**就已经部署成功了！

**明天早上6:00，你会自动收到第一条晨间推送！**

祝你学习愉快，早日实现1亿美金梦想！🚀
