# OpenCode Skills

Git 托管的 OpenCode skills 仓库。

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
```

### 2. 链接到 OpenCode

**Linux/Mac (推荐):**
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

# 使用 Git Worktree（推荐，无需管理员权限）
cd ~/projects/opencode-skills
git worktree add ~/.opencode/skills

# 或者使用管理员权限创建 Junction Point
# cmd /c "mklink /J %USERPROFILE%\.opencode\skills %USERPROFILE%\projects\opencode-skills\skills"
```

### 3. 验证

```bash
ls ~/.opencode/skills/
```

## 日常使用

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
# cp -r ~/.opencode/skills.backup.20260224/my-skill ~/projects/opencode-skills/skills/
# cd ~/projects/opencode-skills && git add . && git commit && git push
```

**Windows:**
```bash
# 备份并替换
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d)
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
cd ~/projects/opencode-skills
git worktree add ~/.opencode/skills

# 合并原有 skill（可选）
# cp -r ~/.opencode/skills.backup.20260224/my-skill ~/.opencode/skills/
# cd ~/projects/opencode-skills && git add . && git commit && git push
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
└── skills -> ~/projects/opencode-skills/skills   # Linux/Mac: 软链接
└── skills/                     # Windows: Git Worktree 目录
```

## 跨平台说明

**Linux/Mac:**
- 使用软链接，修改实时生效
- 切换 Git 分支时，OpenCode 自动使用当前分支的 skills

**Windows:**
- 使用 Git Worktree，无需管理员权限
- 在主仓库目录执行 Git 操作
- Worktree 自动同步到最新代码

两者功能完全一致，只是链接方式不同。

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

**Q: 软链接失效？**
A: 重新创建：
```bash
rm ~/.opencode/skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
```

**Q: Windows 上无法创建软链接？**
A: 使用 Git Worktree（推荐，无需管理员权限）：
```bash
cd ~/projects/opencode-skills
git worktree add ~/.opencode/skills
```

**Q: Windows 上 Git Worktree 如何更新？**
A: 在仓库主目录操作：
```bash
cd ~/projects/opencode-skills
git pull
```
Worktree 会自动同步。

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
