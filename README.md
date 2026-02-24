# OpenCode Skills

Git 托管的 OpenCode skills 仓库。

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
```

### 2. 链接到 OpenCode

```bash
# 备份原有 skills（如果有）
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d) 2>/dev/null || true

# 创建软链接
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
```

### 3. 验证

```bash
ls ~/.opencode/skills/
# 应该看到: esp32-developer, skill-creator, ...
```

---

## 🔄 日常使用

### 修改 skill

```bash
# 直接编辑
vim ~/projects/opencode-skills/skills/esp32-developer/SKILL.md

# 查看变更
cd ~/projects/opencode-skills
git status
git diff

# 提交
git add skills/esp32-developer/
git commit -m "feat: update esp32-developer"
git push
```

### 获取最新变更（另一台机器）

```bash
cd ~/projects/opencode-skills
git pull
```

---

## 🖥️ 多机器同步

### 场景 1：全新机器（首次设置）

如果该机器上还没有配置过 OpenCode skills：

```bash
# 1. 创建目录并克隆仓库
mkdir -p ~/projects
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills

# 2. 链接到 OpenCode
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills

# 3. 验证
ls ~/.opencode/skills/
```

### 场景 2：已有 skills 的机器

如果该机器已有 skills，想切换到 git 管理：

```bash
# 1. 备份原有 skills
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d)

# 2. 克隆仓库
mkdir -p ~/projects
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills

# 3. 链接到 OpenCode
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills

# 4. （可选）合并原有 skills
# 如果有想保留的 skill，从备份复制到仓库
# cp -r ~/.opencode/skills.backup.20240224/my-skill ~/projects/opencode-skills/skills/
# cd ~/projects/opencode-skills && git add . && git commit && git push
```

### 机器 A：修改并推送

```bash
# 编辑 skill
vim ~/projects/opencode-skills/skills/esp32-developer/SKILL.md

# 提交并推送
cd ~/projects/opencode-skills
git add .
git commit -m "feat: update skill"
git push
```

### 机器 B：拉取更新

```bash
cd ~/projects/opencode-skills
git pull
```

---

## 📁 目录结构

```
~/projects/opencode-skills/      # Git 仓库
├── .git/                        # Git 版本控制
├── skills/                      # 👈 OpenCode 使用的 skills
│   ├── esp32-developer/
│   └── skill-creator/
└── tools/                       # 辅助工具（可选）
    └── opm

~/.opencode/
└── skills -> ~/projects/opencode-skills/skills   # 🔗 软链接
```

---

## 📝 添加新 skill

```bash
# 1. 创建目录
mkdir ~/projects/opencode-skills/skills/my-skill

# 2. 创建 SKILL.md
cat > ~/projects/opencode-skills/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: "Description of what this skill does"
---

# My Skill

Content here...
EOF

# 3. 提交
cd ~/projects/opencode-skills
git add skills/my-skill/
git commit -m "feat: add my-skill"
git push
```

---

## 🔧 SSH 配置（首次设置）

```bash
# 1. 生成 SSH key
ssh-keygen -t ed25519 -C "$(hostname)"

# 2. 复制公钥到剪贴板
cat ~/.ssh/id_ed25519.pub
# 然后添加到 GitHub: Settings > SSH and GPG keys > New SSH key

# 3. 测试连接
ssh -T git@github.com
```

---

## ⚡ 快捷命令（可选）

添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
# Skills 快捷方式
alias skills='cd ~/projects/opencode-skills'
alias sk-status='cd ~/projects/opencode-skills && git status'
alias sk-pull='cd ~/projects/opencode-skills && git pull'
alias sk-push='cd ~/projects/opencode-skills && git add . && git commit && git push'
```

然后使用：

```bash
skills          # 进入仓库目录
sk-status       # 查看状态
sk-pull         # 拉取更新
sk-push         # 提交并推送（会提示输入 commit message）
```

---

## ❓ 常见问题

**Q: OpenCode 不识别新 skill？**  
A: 确保 skill 目录下有 `SKILL.md` 文件，且包含 YAML frontmatter：
```yaml
---
name: skill-name
description: "description"
---
```

**Q: 软链接失效？**  
A: 重新创建：
```bash
rm ~/.opencode/skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
```

**Q: 两台机器修改冲突？**  
A: 正常 git 冲突处理：
```bash
git pull                    # 获取远程变更
# 手动解决冲突文件
git add .
git commit -m "merge: resolve conflicts"
git push
```

---

## 📄 License

MIT
