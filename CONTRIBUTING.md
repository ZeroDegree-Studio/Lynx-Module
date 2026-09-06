# Contributing to Lynx Module Market

> How to publish a module package to the Lynx module repository.

[English](#english) · [中文](#中文)

---

## English

### Quick Path

1. **Pack** your module into `.lmp` — Module Workbench → select module → "导出 .lmp", or call `export_package` API. The package must contain `manifest.yaml` (the protocol core) — see [`MODULE_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)
2. **Fork** this repository
3. **Add the package** at `packages/<module_id>/<module_id>-<version>.lmp`
4. **Open a Pull Request** — CI regenerates `index.json` automatically after merge

### Naming Conventions

| Item | Rule |
|------|------|
| `module_id` | letters/digits/underscores/hyphens, starts with a letter, globally unique; reserved prefixes like `tool:` / `skill:` are forbidden |
| `version` | semver `MAJOR.MINOR.PATCH` |
| Package path | `packages/<module_id>/<module_id>-<version>.lmp` |
| Do **not** change | `module_id` when updating; bump `version` instead |

### Review Criteria

Maintainers check:

1. ✅ Package opens as zip, contains a valid `manifest.yaml` (parses per the module protocol)
2. ✅ Install passes: checksums verified, zip-slip protection not circumvented, no ID conflict
3. ✅ Declared `permissions` match actual behavior (file write / execute / network)
4. ✅ No malicious content (data exfiltration, destructive commands, credential harvesting)
5. ✅ No hardcoded local paths or embedded credentials
6. ✅ `checksums.sha256` inside the package matches content (regenerate before submitting if you edited files)
7. ✅ Not a duplicate (same `module_id` must bump `version` instead)
8. ✅ License compatible (declare in `manifest.yaml`; default `MIT`)

PRs that fail review will receive a comment explaining what to fix.

### Testing Before PR

1. In the Module Workbench, use "导入 .lmp" to install your package locally
2. Verify the module appears in the capability tree and runs (use 沙箱测试 where available)
3. Export it again and confirm the round-trip produces a working package

### PR Title Format

```
[module] <module_id> by <author>
```

Example: `[module] code-reviewer by alice`

### Updating an Existing Module

1. **Do not** change the `module_id`
2. Bump `version` (semver)
3. Submit a PR adding the new package file (old versions may be kept for rollback or removed per maintainer guidance)

### Removing a Module

Open a PR deleting the package file(s), explain why. Maintainers merge after confirming you're the original author.

### License

- **This repository** (tooling, docs): [MIT License](LICENSE)
- **Each module** carries its own license via `manifest.yaml` `license` field

### Code of Conduct

- Be respectful in PR discussions
- No spam, no advertising, no malicious content
- Maintainers reserve the right to reject any PR

### Need Help?

- Open an issue with the `question` label
- Or read the module protocol: [`MODULE_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)

---

## 中文

### 快速路径

1. **打包**：模块工作台 → 选中模块 → 「导出 .lmp」（或调 `export_package` API）。包内必须含 `manifest.yaml`（协议核心）— 规范见 [`MODULE_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)
2. **Fork** 本仓库
3. **放包**：`packages/<module_id>/<module_id>-<version>.lmp`
4. **提 Pull Request** — 合并后 CI 自动重新生成 `index.json`

### 命名规范

| 项目 | 规则 |
|------|------|
| `module_id` | 字母/数字/下划线/连字符，字母开头，全局唯一；禁止 `tool:` / `skill:` 等保留前缀 |
| `version` | 语义版本 `MAJOR.MINOR.PATCH` |
| 包路径 | `packages/<module_id>/<module_id>-<version>.lmp` |
| 更新时**不要** | 改 `module_id`；应提升 `version` |

### 审核标准

维护者会检查：

1. ✅ 包可正常以 zip 打开，含合法 `manifest.yaml`（按模块协议解析通过）
2. ✅ 安装通过：校验和验证、zip-slip 防护未被绕过、无 ID 冲突
3. ✅ 声明的 `permissions` 与实际行为一致（写文件/执行/网络）
4. ✅ 无恶意内容（数据外泄、破坏性命令、窃取凭证）
5. ✅ 无硬编码本地路径、无内嵌凭证
6. ✅ 包内 `checksums.sha256` 与内容一致（提交前重新导出即可保证）
7. ✅ 不是重复提交（相同 `module_id` 应提升 `version`）
8. ✅ 许可证兼容（`manifest.yaml` 里声明，默认 `MIT`）

审核未通过的 PR 会收到评论说明需要修改什么。

### 提 PR 前本地测试

1. 模块工作台用「导入 .lmp」本地安装你的包
2. 确认模块出现在能力树并可运行（能用沙箱测试的先沙箱测试）
3. 再导出一次，确认往返打包产出可用

### PR 标题格式

```
[module] <module_id> by <作者>
```

示例：`[module] code-reviewer by alice`

### 更新已有模块

1. **不要**改 `module_id`
2. 提升 `version`（语义版本）
3. 提 PR 添加新包文件（旧版本可保留回滚，或按维护者指引删除）

### 删除模块

提 PR 删除对应包文件，在描述里说明原因。维护者确认你是原作者后合并。

### 许可证

- **本仓库**（工具、文档）：[MIT License](LICENSE)
- **每个模块**通过 `manifest.yaml` 的 `license` 字段自带许可证

### 行为准则

- PR 讨论中保持尊重
- 不发垃圾信息、广告、恶意内容
- 维护者保留无理由拒绝任何 PR 的权利

### 需要帮助？

- 提 issue 并打 `question` 标签
- 或读模块协议：[`MODULE_FORMAT.md`](https://github.com/ZeroDegree-Studio/LYNX/blob/main/docs/MODULE_FORMAT.md)
