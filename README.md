# OpenCode Skills

Git 托管的 OpenCode skills 仓库。

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
```

### 2. 链接到 OpenCode

**Linux/Mac:**
```bash
# 备份原有 skills（如果有）
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d) 2>/dev/null || true

# 创建软链接
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
```

**Windows:**
```bash
# 备份原有 skills（如果有）
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d) 2>/dev/null || true

# 使用 Git Worktree
cd ~/projects/opencode-skills
git worktree add ~/.opencode/skills
```

### 3. 验证

```bash
ls ~/.opencode/skills/
```

## 日常使用

### Linux/Mac

```bash
# 编辑 skill
vim ~/projects/opencode-skills/skills/esp32-developer/SKILL.md

# 提交变更
cd ~/projects/opencode-skills
git add .
git commit -m "feat: update skill"
git push

# 拉取更新
git pull
```

### Windows

```bash
# 编辑 skill（在主仓库目录）
notepad ~/projects/opencode-skills/skills/esp32-developer/SKILL.md

# 提交变更
cd ~/projects/opencode-skills
git add .
git commit -m "feat: update skill"
git push

# 拉取更新（worktree 自动同步）
git pull
```

## 多机器同步

### 场景1：全新机器

**Linux/Mac:**
```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
```

**Windows:**
```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
cd ~/projects/opencode-skills
git worktree add ~/.opencode/skills
```

### 场景2：已有 skills

**Linux/Mac:**
```bash
# 备份并替换
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d)
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills

# 合并原有 skill（可选）
cp -r ~/.opencode/skills.backup.20260224/my-skill ~/projects/opencode-skills/skills/
cd ~/projects/opencode-skills
git add . && git commit && git push
```

**Windows:**
```bash
# 备份并替换
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d)
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
cd ~/projects/opencode-skills
git worktree add ~/.opencode/skills

# 合并原有 skill（可选）
cp -r ~/.opencode/skills.backup.20260224/my-skill ~/.opencode/skills/
cd ~/projects/opencode-skills
git add . && git commit && git push
```

## 目录结构

```
~/projects/opencode-skills/      # Git 仓库
├── skills/                      # OpenCode 使用的 skills
│   ├── esp32-developer/
│   ├── skill-creator/
│   └── requirements-manager/
└── tools/                       # 辅助工具

~/.opencode/
└── skills/                       # 链接到仓库 skills 目录
```

## 添加新 skill

```bash
mkdir ~/projects/opencode-skills/skills/my-skill
cat > ~/projects/opencode-skills/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: "Description of what this skill does"
---

# My Skill

Content here...
EOF

cd ~/projects/opencode-skills
git add skills/my-skill/
git commit -m "feat: add my-skill"
git push
```

## 常见问题

**Q: OpenCode 不识别新 skill？**
A: 确保包含 SKILL.md 和 YAML frontmatter：
```yaml
---
name: skill-name
description: "description"
---
```

**Q: 软链接失效？**（Linux/Mac）
A: 重新创建：
```bash
rm ~/.opencode/skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
```

**Q: Windows 上无法创建软链接？**
A: 使用 Git Worktree：
```bash
cd ~/projects/opencode-skills
git worktree add ~/.opencode/skills
```

**Q: Windows 上如何更新？**
A: 在主仓库目录操作，worktree 自动同步：
```bash
cd ~/projects/opencode-skills
git pull
```

**Q: Git 冲突？**
A: 标准冲突处理：
```bash
git pull
# 手动解决冲突
git add .
git commit -m "merge: resolve conflicts"
git push
```

---

MIT License
