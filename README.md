# OpenCode Skills Registry

多系统 OpenCode skills 同步管理仓库。

## 🚀 快速开始

### 安装 ocm (OpenCode Manager)

```bash
curl -fsSL https://raw.githubusercontent.com/xingshizhai/opencode-skills/main/tools/install.sh | bash
```

或者手动安装：

```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/.opencode-skills
ln -s ~/.opencode-skills/tools/ocm /usr/local/bin/ocm
```

### 初始化系统

```bash
ocm init
```

### 同步 skills

```bash
ocm sync
```

## 📋 常用命令

| 命令 | 说明 |
|-----|------|
| `ocm init` | 初始化当前系统的 manifest |
| `ocm sync` | 双向同步 skills |
| `ocm push` | 推送本地 skills 到仓库 |
| `ocm pull` | 从仓库拉取 skills |
| `ocm list` | 查看本机 skills |
| `ocm list-all` | 查看所有系统的 skills |
| `ocm copy <系统>:<skill>` | 从其他系统复制 skill |
| `ocm status` | 查看状态 |

## 🔄 工作流程

```
┌─────────────┐      ocm push      ┌─────────────────┐      ocm pull      ┌─────────────┐
│   MacBook   │ ─────────────────► │  GitHub Repo    │ ◄───────────────── │   Desktop   │
│  (新增skill)│                    │  (中央仓库)      │                    │  (获取skill) │
└─────────────┘                    └─────────────────┘                    └─────────────┘
```

### 1. 添加新 skill

```bash
# 在任意系统上创建/修改 skill
mkdir -p ~/.opencode/skills/my-new-skill
echo "# My New Skill" > ~/.opencode/skills/my-new-skill/SKILL.md

# 同步到中央仓库
ocm push
```

### 2. 在其他系统获取

```bash
# 在另一台机器上
ocm pull

# 查看新 skill
ocm list
```

### 3. 从其他系统复制 skill

```bash
# 查看所有系统的 skills
ocm list-all

# 从 server 系统复制 skill
ocm copy server:linux-only-skill
```

## 📁 目录结构

```
opencode-skills/
├── README.md              # 本文件
├── skills/                # 所有 skills
│   ├── esp32-developer/  # ESP32 开发 skill
│   └── skill-creator/    # Skill 创建工具
├── manifests/             # 各系统配置
│   ├── Mac.lan.json      # Mac 系统配置
│   └── server.json       # 服务器配置
└── tools/
    ├── ocm               # 主管理脚本
    └── install.sh        # 安装脚本
```

## 🖥️ 支持的系统

- ✅ macOS
- ✅ Linux
- ✅ Windows (WSL)

## ⚙️ 自动同步

### macOS (LaunchAgent)

```bash
# 每小时自动同步
cp ~/.opencode-skills/tools/com.opencode.sync.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.opencode.sync.plist
```

### Linux (Systemd Timer)

```bash
# 启用定时同步
systemctl --user enable ocm-sync.timer
systemctl --user start ocm-sync.timer
```

## 📝 Manifest 格式

每个系统的配置保存在 `manifests/<hostname>.json`：

```json
{
  "system": {
    "name": "Mac.lan",
    "hostname": "Mac.lan",
    "os": "macos",
    "arch": "arm64"
  },
  "skills": [
    {
      "name": "esp32-developer",
      "version": "1.0.0",
      "auto_update": true
    }
  ]
}
```

## 🤝 添加新系统

1. 在新系统上安装 ocm：
   ```bash
   curl -fsSL ... | bash
   ```

2. 初始化并推送：
   ```bash
   ocm init
   ocm push
   ```

3. 在其他系统同步：
   ```bash
   ocm pull
   ```

## 🐛 故障排查

| 问题 | 解决方案 |
|-----|---------|
| `ocm: command not found` | 检查 PATH 或重新运行 install.sh |
| `Permission denied` | 运行 `chmod +x ~/.opencode-skills/tools/ocm` |
| `git pull failed` | 检查 SSH key 是否已添加到 GitHub |
| 同步冲突 | 手动解决冲突后重新 push |

## 🔐 SSH 配置

确保每台机器都有 GitHub SSH 访问权限：

```bash
ssh-keygen -t ed25519 -C "$(hostname)"
cat ~/.ssh/id_ed25519.pub
# 添加到 GitHub: Settings > SSH and GPG keys
```

## 📄 License

MIT License - 见 LICENSE 文件
