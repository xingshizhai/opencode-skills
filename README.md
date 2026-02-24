# OpenCode Skills Registry

多系统 OpenCode skills 同步管理仓库。

## 📦 两种管理方式

本仓库提供 **两种** 管理工具，满足不同需求：

### 1. 🚀 opm (OpenCode Package Manager) - 推荐
**Git Native** 方式，直接管理 skills，简单透明。

适合：
- ✅ 喜欢直接控制 Git 的用户
- ✅ 需要清晰变更历史的用户
- ✅ 熟悉 Git 工作流的用户

```bash
# 编辑 skill
vim ~/.opencode/skills/esp32-developer/SKILL.md

# 查看变更
opm status
opm diff

# 提交
opm add esp32-developer
opm commit "feat: add new feature"
opm push
```

### 2. 🔧 ocm (OpenCode Manager) - 传统
**双向同步** 方式，自动处理 manifest 和多系统同步。

适合：
- 多系统环境（Mac + Linux + Server）
- 需要自动同步的用户
- 旧用户保持兼容

---

## 🚀 快速开始 (opm 方式)

### 1. 初始化

```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/opencode-skills

# 创建软链接（让 OpenCode 使用 git 仓库中的 skills）
rm -rf ~/.opencode/skills
ln -s ~/opencode-skills/skills ~/.opencode/skills

# 添加到 PATH
echo 'export PATH="$HOME/opencode-skills/tools:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 2. 日常使用

```bash
# 查看状态
opm status

# 编辑 skill（直接在 ~/.opencode/skills/ 编辑）
vim ~/.opencode/skills/esp32-developer/SKILL.md

# 查看变更
opm diff

# 提交变更
opm add esp32-developer
opm commit "feat: update skill"
opm push

# 获取最新变更
opm pull
```

---

## 📋 opm 命令参考

| 命令 | 说明 | 示例 |
|-----|------|------|
| `opm status` | 查看哪些 skills 有变更 | `opm status` |
| `opm diff` | 查看具体变更内容 | `opm diff` |
| `opm add <skill>` | 暂存指定 skill 的变更 | `opm add esp32-developer` |
| `opm commit <msg>` | 提交变更 | `opm commit "update skill"` |
| `opm push` | 推送到远程仓库 | `opm push` |
| `opm pull` | 拉取最新变更 | `opm pull` |
| `opm log [n]` | 查看提交历史 | `opm log 10` |
| `opm list` | 列出所有 skills | `opm list` |
| `opm sync` | 快速同步（pull + status）| `opm sync` |

---

## 🔧 ocm (传统方式)

如果你需要多系统自动同步功能，使用 `ocm`：

### 安装

```bash
curl -fsSL https://raw.githubusercontent.com/xingshizhai/opencode-skills/main/tools/install.sh | bash
```

### 常用命令

| 命令 | 说明 |
|-----|------|
| `ocm init` | 初始化当前系统的 manifest |
| `ocm sync` | 双向同步 skills |
| `ocm status` | 查看状态 |

---

## 📁 目录结构

```
~/opencode-skills/              # Git 仓库（Registry）
├── .git/                       # Git 版本控制
├── README.md                   # 本文件
├── LICENSE
├── skills/                     # 🔥 所有 skills
│   ├── esp32-developer/        # ESP32 开发 skill
│   │   ├── SKILL.md           # Skill 定义（必需）
│   │   ├── scripts/           # 脚本（可选）
│   │   ├── references/        # 参考资料（可选）
│   │   └── assets/            # 资源文件（可选）
│   └── skill-creator/          # Skill 创建工具
├── manifests/                  # 各系统配置（ocm 使用）
│   └── Mac.json               # 系统 manifest
└── tools/
    ├── opm                    # 🔥 新的包管理器（推荐）
    ├── ocm                    # 传统管理器
    └── install.sh             # 安装脚本

~/.opencode/                    # OpenCode 主目录
└── skills -> ~/opencode-skills/skills   # 🔗 软链接
```

---

## 🔄 工作流程对比

### opm 方式（Git Native）

```
编辑 skill ──→ opm status ──→ opm add ──→ opm commit ──→ opm push
    ↑                                                      │
    └────────────────── opm pull ──────────────────────────┘
```

简单直接，就是标准 Git 工作流。

### ocm 方式（双向同步）

```
┌─────────────┐      ocm sync      ┌─────────────────┐      ocm sync      ┌─────────────┐
│   MacBook   │ ─────────────────► │  GitHub Repo    │ ◄───────────────── │   Desktop   │
│  (新增skill)│                    │  (中央仓库)      │                    │  (获取skill) │
└─────────────┘                    └─────────────────┘                    └─────────────┘
```

适合多系统自动同步。

---

## 🛠️ 添加新 Skill

使用 `skill-creator` skill：

```bash
# 确保 skill-creator 已安装
cd ~/opencode-skills

# 使用创建脚本
python skills/skill-creator/scripts/init_skill.py my-new-skill --path skills/

# 编辑 SKILL.md
vim skills/my-new-skill/SKILL.md

# 提交
opm add my-new-skill
opm commit "feat: add my-new-skill"
opm push
```

---

## 🖥️ 多系统同步

### 在新系统上设置

```bash
# 1. 克隆仓库
git clone git@github.com:xingshizhai/opencode-skills.git ~/opencode-skills

# 2. 创建软链接
rm -rf ~/.opencode/skills
ln -s ~/opencode-skills/skills ~/.opencode/skills

# 3. 添加到 PATH
echo 'export PATH="$HOME/opencode-skills/tools:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 4. 完成！
opm list
```

### 同步变更

```bash
# 系统 A：推送变更
opm add my-skill
opm commit "update"
opm push

# 系统 B：拉取变更
opm pull
```

---

## 🐛 故障排查

### opm 问题

| 问题 | 解决方案 |
|-----|---------|
| `opm: command not found` | 检查 PATH：`export PATH="$HOME/opencode-skills/tools:$PATH"` |
| `Not a git repository` | 运行 `cd ~/opencode-skills && git init` |
| `Permission denied` | `chmod +x ~/opencode-skills/tools/opm` |

### OpenCode 问题

| 问题 | 解决方案 |
|-----|---------|
| Skill 未生效 | 检查软链接：`ls -la ~/.opencode/skills` |
| 找不到 skill | 确认 skill 目录下有 `SKILL.md` |

### Git 问题

| 问题 | 解决方案 |
|-----|---------|
| `git pull failed` | 检查 SSH key：`cat ~/.ssh/id_ed25519.pub` |
| 合并冲突 | 手动解决后 `git add . && git commit` |

---

## 🔐 SSH 配置

确保有 GitHub SSH 访问权限：

```bash
# 生成密钥
ssh-keygen -t ed25519 -C "$(hostname)"

# 复制公钥
cat ~/.ssh/id_ed25519.pub
# 添加到 GitHub: Settings > SSH and GPG keys > New SSH key

# 测试连接
ssh -T git@github.com
```

---

## 📄 License

MIT License - 见 LICENSE 文件
