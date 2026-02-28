# OpenCode Skills

Git 托管的 OpenCode skills 仓库。

## 快速开始

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

```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
```

### 场景2：已有 skills

```bash
# 备份并替换
mv ~/.opencode/skills ~/.opencode/skills.backup.$(date +%Y%m%d)
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills

# 合并原有 skill（可选）
# cp -r ~/.opencode/skills.backup.20260224/my-skill ~/projects/opencode-skills/skills/
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
└── skills -> ~/projects/opencode-skills/skills   # 软链接
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

**Q: 软链接失效？**
A: 重新创建：
```bash
rm ~/.opencode/skills
ln -s ~/projects/opencode-skills/skills ~/.opencode/skills
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
