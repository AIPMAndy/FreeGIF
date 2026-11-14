<div align="center">

# FreeGIF ✳️

### 让每一张图动起来。

**免费 · 开源 · 手机即用 · 本地处理 · 无强制水印**

[**立即在线制作 GIF**](https://aipmandy.github.io/FreeGIF/) · [安装 Codex Skill](skills/freegif/SKILL.md) · [路线图](docs/ROADMAP.md)

</div>

---

## 这是做什么的？

上传一张图片，选择弹跳、漂浮、摇摆或呼吸缩放，再加文字，就能直接在浏览器导出 GIF。也支持两张图之间切换、动态标题和可选署名。无需登录、会员、后端服务或 AI API。

**全部 GIF 帧和编码都在浏览器本地完成，图片不会提交至我们的服务器。** 仅网站静态资源通过 GitHub Pages 加载。

### 已实现（V0.1）

| 功能 | 说明 |
| --- | --- |
| 手机与桌面 | 适配移动端的静态网页 |
| 六种模式 | 漂浮、弹跳、摇摆、呼吸、双图切换、打字标题 |
| 自定义 | 上传图片、文字、背景、可选署名 |
| 三种画幅 | 1:1、9:16、16:9；可设置尺寸、时长和帧率 |
| 真正的 GIF 文件 | 多帧 GIF89a 编码、循环播放、下载 |
| Python CLI + Codex Skill | 可批量自动化调用，本地生成 |
| 开源 | MIT，无强制水印、无账户或广告 SDK |

> 这不是 AI 生图模型。无法自动生成复杂的角色骨骼运动或视频大片，也不承诺生成物直接通过微信表情开放平台审核。

### 试用

[**FreeGIF 在线网站**](https://aipmandy.github.io/FreeGIF/)（GitHub Pages 部署成功后可用）。

也可以下载 `index.html`，在浏览器中直接打开；页面内包含自己的 CSS、Canvas 渲染器和 GIF89a 编码器，**没有 CDN 依赖**。

### Codex Skill 与 Python CLI

```bash
python -m pip install -r requirements.txt
python scripts/freegif.py --input photo.png --mode bounce --text "今天也要加油！" --output output.gif
python scripts/freegif.py --input before.png --input-b after.png --mode flip --output compare.gif
```

Skill 说明见 [skills/freegif/SKILL.md](skills/freegif/SKILL.md)。Python 3.10+，需要 Pillow；网页版不需要 Python。执行完成后请检查 GIF 是否正常播放、尺寸和帧数是否符合目标平台规格。

### 本地运行和验证

```bash
python3 -m http.server 8000
# 打开 http://localhost:8000
node tests/test-site.mjs
```

### GitHub Pages 发布

本仓库的 [工作流](.github/workflows/pages.yml) 会在推送到 main 后校验并部署网站。若首次发布尚未成功，请在仓库 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions**，再重跑工作流。不要把仓库创建成功误当成网站部署成功。

### 隐私与使用许可

图片、文本和 GIF 在浏览器本地处理；无用户上传接口、无登录、无强制水印。使用者应确认素材有合法使用权。GIF 调色板色深有限，照片可能有轻微色带；低内存手机请降低输出尺寸和帧数。代码 MIT 许可，详见 [LICENSE](LICENSE)。

### 灵感来源与差异化

受 [WoYun520/gif-factory](https://github.com/WoYun520/gif-factory) 启发。原项目主要面向 Agent/Codex 的高阶制作工作流；FreeGIF 提供**独立原创的零安装网页 + 本地 GIF 编码 + Python CLI**，不是原项目的完整移植或官方分支，不包含原作者的私有素材。感谢 MIT 开源社区。

---

由 **AI 酋长 Andy / 星觉科技** 发起。个人网站：[metaver.vip](https://metaver.vip/) · [GitHub](https://github.com/AIPMAndy)
