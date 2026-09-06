# Lynx Module Market

> The official community repository for sharing Lynx module packages (`.lmp`).

[English](#english) · [中文](#中文)

---

## English

### What is a Module?

A **module** is a Lynx capability package: tools, skills, UI panels, controllers, or collections — all mounted into one capability tree via a unified `manifest.yaml` protocol. "Everything is a module": skills, tools and controllers are all module kinds.

Modules are distributed as **`.lmp` packages** (zip container) with built-in integrity protection: per-file SHA-256 checksums and zip-slip path protection on install.

- **Import** — use the Module Workbench's "Import .lmp" dialog
- **Export** — any module can be packed into a distributable `.lmp`
- **Share** — publish your `.lmp` here for the global community

### Repository Structure

```
Lynx-Module/
├── README.md                     # This file
├── CONTRIBUTING.md               # How to publish a module
├── LICENSE                       # Repository license (MIT)
├── index.json                    # Auto-generated module index (GitHub Actions)
├── tools/
│   └── generate_index.py         # Index generator (reads manifest.yaml from .lmp)
└── packages/
    └── <module_id>/
        └── <module_id>-<version>.lmp
```

### Index Format

`index.json` is regenerated on every push by GitHub Actions. The client reads it via raw URL (with optional mirror):

```json
{
  "version": "1",
  "updated_at": "...",
  "modules": [
    {
      "module_id": "code-reviewer",
      "name": "代码审查",
      "author": "lynx",
      "version": "1.2.0",
      "kind": "py-skill",
      "description": "...",
      "permissions": ["read_file"],
      "official": true,
      "license": "MIT",
      "size_bytes": 12345,
      "sha256": "...",
      "download_url": "packages/code-reviewer/code-reviewer-1.2.0.lmp"
    }
  ]
}
```

### Contributing a Module

1. **Pack** your module: Module Workbench → select module → "导出 .lmp" (or `export_package` API)
2. **Fork** this repository
3. **Add the package** at `packages/<module_id>/<module_id>-<version>.lmp`
4. **Open a Pull Request** — see [CONTRIBUTING.md](CONTRIBUTING.md) for review criteria

Full module protocol: [`docs/MODULE_FORMAT.md` in the main repo](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)

### Related

- **Lynx main repository**: [ZeroDegree-Studio/LYNX](https://github.com/ZeroDegree-Studio/LYNX)
- **Skill community**: [ZeroDegree-Studio/Lynx-Skill](https://github.com/ZeroDegree-Studio/Lynx-Skill)
- **Spore market**: [ZeroDegree-Studio/lynx-spore-market](https://github.com/ZeroDegree-Studio/lynx-spore-market)
- **ZeroDegree Studio**: [zerodegree.cc](https://zerodegree.cc)

---

## 中文

### 什么是模块？

**模块**（Module）是 Lynx 的能力包：工具、技能、界面面板、控制器或集合——通过统一的 `manifest.yaml` 协议挂载进能力树。"一切皆模块"：技能、工具、控制器都是模块的一种 kind。

模块以 **`.lmp` 包**（zip 容器）分发，自带完整性防护：安装时逐文件 SHA-256 校验 + zip-slip 路径防护。

- **导入** — 模块工作台的「导入 .lmp」对话框
- **导出** — 任何模块都能打包成可分发的 `.lmp`
- **共享** — 把你的 `.lmp` 发布到这里，供全球用户使用

### 仓库结构

```
Lynx-Module/
├── README.md                     # 本文件
├── CONTRIBUTING.md               # 如何发布模块
├── LICENSE                       # 仓库许可证（MIT）
├── index.json                    # 自动生成的模块索引（GitHub Actions）
├── tools/
│   └── generate_index.py         # 索引生成器（直接从 .lmp 内读 manifest.yaml）
└── packages/
    └── <module_id>/
        └── <module_id>-<version>.lmp
```

### 索引格式

每次 push 后 GitHub Actions 自动重新生成 `index.json`。客户端通过 raw 地址读取（支持镜像）：

```json
{
  "version": "1",
  "updated_at": "...",
  "modules": [
    {
      "module_id": "code-reviewer",
      "name": "代码审查",
      "author": "lynx",
      "version": "1.2.0",
      "kind": "py-skill",
      "description": "...",
      "permissions": ["read_file"],
      "official": true,
      "license": "MIT",
      "size_bytes": 12345,
      "sha256": "...",
      "download_url": "packages/code-reviewer/code-reviewer-1.2.0.lmp"
    }
  ]
}
```

### 发布模块

1. **打包**：模块工作台 → 选中模块 → 「导出 .lmp」（或 `export_package` API）
2. **Fork** 本仓库
3. **放包**：`packages/<module_id>/<module_id>-<version>.lmp`
4. **提 Pull Request** — 审核标准见 [CONTRIBUTING.md](CONTRIBUTING.md)

模块协议全文：主仓库 [`docs/MODULE_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)

### 相关链接

- **Lynx 主仓库**：[ZeroDegree-Studio/LYNX](https://github.com/ZeroDegree-Studio/LYNX)
- **技能社区**：[ZeroDegree-Studio/Lynx-Skill](https://github.com/ZeroDegree-Studio/Lynx-Skill)
- **孢子市场**：[ZeroDegree-Studio/lynx-spore-market](https://github.com/ZeroDegree-Studio/lynx-spore-market)
- **零度工作室**：[zerodegree.cc](https://zerodegree.cc)
