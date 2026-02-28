# OpenCode Skills

Git托管的OpenCode技能仓库，用于跨机器同步和管理OpenCode技能。

## 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
```

Windows用户可使用Git Bash（推荐）或PowerShell，路径根据实际情况调整。

### 2. 链接到OpenCode

**所有平台（推荐使用Git Bash）：**

```bash
# 备份原有skills（如果存在）
mv ~/.config/opencode/skills ~/.config/opencode/skills.backup.$(date +%Y%m%d) 2>/dev/null || true

# 使用Git Worktree链接
cd ~/projects/opencode-skills
git worktree add ~/.config/opencode/skills
```

**Windows PowerShell：**

```powershell
# 备份原有skills（如果存在）
Move-Item $env:USERPROFILE\.config\opencode\skills $env:USERPROFILE\.config\opencode\skills.backup$(Get-Date -Format "yyyyMMdd") -ErrorAction SilentlyContinue

# 使用Git Worktree链接
cd $env:USERPROFILE\projects\opencode-skills
git worktree add $env:USERPROFILE\.config\opencode\skills
```

### 3. 验证

```bash
ls ~/.config/opencode/skills/
```

## 日常使用

### 编辑和更新技能

**在主仓库目录操作：**

```bash
# 编辑技能文件
cd ~/projects/opencode-skills
# 使用你喜欢的编辑器编辑 skills/目录下的文件

# 提交变更
git add .
git commit -m "feat: update skill"
git push

# 拉取更新（worktree自动同步）
git pull
```

**Windows注意：** 在Git Bash中`~`映射到`/c/Users/用户名`，但某些系统可能是`/c/User/用户名`。如果路径不匹配，请使用完整路径。

## 目录结构

```
~/projects/opencode-skills/      # Git主仓库
├── skills/                      # 技能目录
│   ├── esp32-developer/        # ESP32开发技能
│   ├── skill-creator/          # 技能创建器
│   └── requirements-manager/    # 依赖管理器
├── tools/                       # 辅助工具
└── manifests/                   # 清单文件

~/.config/opencode/skills/       # OpenCode实际使用的技能目录（worktree链接）
```

## 添加新技能

```bash
# 在主仓库创建技能目录
mkdir ~/projects/opencode-skills/skills/your-skill-name

# 创建SKILL.md文件（必须包含YAML frontmatter）
cat > ~/projects/opencode-skills/skills/your-skill-name/SKILL.md << 'EOF'
---
name: your-skill-name
description: "技能描述"
---

# 技能名称

技能内容...
EOF

# 提交并推送
cd ~/projects/opencode-skills
git add skills/your-skill-name/
git commit -m "feat: add your-skill-name"
git push
```

## 多机器同步

### 全新机器

```bash
# 克隆仓库
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills

# 链接到OpenCode
cd ~/projects/opencode-skills
git worktree add ~/.config/opencode/skills
```

### 已有技能迁移

```bash
# 备份原有技能
mv ~/.config/opencode/skills ~/.config/opencode/skills.backup.$(date +%Y%m%d)

# 克隆并链接
git clone git@github.com:xingshizhai/opencode-skills.git ~/projects/opencode-skills
cd ~/projects/opencode-skills
git worktree add ~/.config/opencode/skills

# 合并原有自定义技能（可选）
cp -r ~/.config/opencode/skills.backup.*/custom-skill ~/projects/opencode-skills/skills/
git add . && git commit && git push
```

## 常见问题

**Q: Windows上路径错误，OpenCode找不到技能？**
A: Windows系统可能存在`/c/User`和`/c/Users`路径差异。检查：
1. 使用`git worktree list`查看现有worktree路径
2. 确保worktree创建在`~/.config/opencode/skills`（对应`/c/Users/用户名/.config/opencode/skills`）
3. 如果路径不正确，删除并重新创建worktree：
```bash
cd ~/projects/opencode-skills
git worktree remove ~/.config/opencode/skills --force
git worktree add ~/.config/opencode/skills
```

**Q: OpenCode不识别新技能？**
A: 确保SKILL.md文件包含正确的YAML frontmatter：
```yaml
---
name: skill-name
description: "技能描述"
---
```

**Q: Windows上路径错误？**
A: 检查OpenCode实际使用的配置目录。默认在`%USERPROFILE%\.config\opencode\`，使用`git worktree list`查看现有worktree路径。

**Q: Git冲突如何处理？**
A: 在主仓库目录解决冲突：
```bash
git pull
# 手动解决冲突后
git add .
git commit -m "merge: resolve conflicts"
git push
```

**Q: Worktree已存在怎么办？**
A: 删除现有worktree并重新创建：
```bash
cd ~/projects/opencode-skills
git worktree remove ~/.config/opencode/skills --force
git worktree add ~/.config/opencode/skills
```

---

MIT License