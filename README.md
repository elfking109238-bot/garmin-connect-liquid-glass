# Garmin Connect Liquid Glass

给现有 Garmin Connect 中国站换上柔和的液态玻璃外观：薄荷绿、桃粉和淡蓝渐变，半透明白色圆角卡片、轻阴影与清晰的导航状态。

**独立社区项目，非 Garmin 官方产品；未获 Garmin 赞助、认可或关联。** 不提供独立健康面板，不连接 Garmin API。原站的数据、布局、图表和操作继续由原站提供。

## 适用范围

仅匹配 **`https://connectus.garmin.cn/app/*`**。不匹配登录页、其他域名或其他网站。
国际站 `connect.garmin.com`、其他中国站地址、手机端及其他浏览器未测试，不承诺兼容。

v0.2.1 的主要修复是侧栏悬停黑角与滚动条深色边框，同时保留浅蓝选中状态和键盘焦点框。

## 下载与安装（Windows Edge）

1. 从本仓库的 **Releases → v0.2.1** 下载 `garmin-connect-liquid-glass-v0.2.1-extension.zip` 和 `SHA256SUMS`。
2. 可用 PowerShell 的 `Get-FileHash -Algorithm SHA256` 检查 ZIP，和 `SHA256SUMS` 中的值比较。
3. 将 ZIP 解压到希望长期保留的文件夹。该文件夹内应直接包含 `manifest.json` 和 `skin.css`。
4. 在 Edge 打开“扩展 → 管理扩展”。如果需要使用本地侧载，用户须自行决定是否开启“开发人员模式”；它允许加载本地非商店扩展。
5. 点击“加载解压缩的扩展”，选中第 3 步的文件夹。确认名称为 **Garmin Connect Liquid Glass**，版本为 **0.2.1**。
6. 刷新已登录的 Garmin 页面。无需输入新的 Garmin 凭据，也无需授权任何新 Garmin API。

这是 GitHub 源码与下载包发布，**不是浏览器扩展商店上架**。浏览器可能提示“读取和更改 connectus.garmin.cn 上的数据”；此站点访问能力用于加载 CSS，不能描述为没有网站访问权限。

安装流程可参考 [Microsoft Edge 官方侧载说明](https://learn.microsoft.com/en-us/microsoft-edge/extensions/getting-started/extension-sideloading)。请保留解压后的文件夹供浏览器和后续更新使用。

### 停用或卸载

在 Edge“管理扩展”中关闭或移除 **Garmin Connect Liquid Glass**，然后刷新 Garmin 页面。也可以仅停用样式，而继续使用原站。关闭扩展后的恢复尚未在本版本的实际安装环境中单独实测。

### 已有 UserCSS 扩展

可改用仓库中的 `garmin-liquid-glass.user.css`，只在兼容 UserCSS 的样式管理器内导入，并核对作用范围。此导入方式尚未实测。建议一次只启用一种安装方式，避免重复叠加。

## 隐私与权限

- 运行包仅包含 CSS、Manifest 和说明文件；没有 JavaScript、后台进程、API 调用或遥测。
- 不读取或导出 cookies、密码、令牌、账户信息或健康数据；不包含远程图片、字体、`@import` 或其他联网资源。
- Manifest 仅将 CSS 加载到上述 Garmin 路径，没有额外的 cookies、storage、tabs 或 scripting API 权限。
- 项目不分发真实页面截图、个人数据、Garmin 字体/图标/logo 或参考图片。官网自身显示的内容仍来自官网。

## 已验证与已知限制

已在 Windows Edge 桌面视口验证首页、心率单日/周视图、导航、图表工具提示、弹出菜单和帮助弹窗。安装后刷新、另开首页和心率页均会自动应用，验证时没有临时注入 CSS。

已验证侧栏主项和子项悬停、按下、选中、展开/收起、点击跳转及键盘焦点；黑角修复有效。

未逐页验证整个 Garmin 网站，未实测完整重启浏览器后的行为、扩展停用恢复、其他浏览器、移动视口或所有辅助技术。透明度降级和不支持模糊效果的回退规则已编写，但未覆盖实测所有系统。

Garmin 更改组件名称后，选择器可能需要维护。模糊效果可能增加低性能设备的渲染负担。窄卡片中原站本来存在的文字省略行为仍会保留。项目不提供健康或医疗解释。

## 源码与构建

需要 Python 3.10+，仅使用标准库，无需安装依赖。

```sh
python tools/build.py --check
python tools/build.py
```

- `styles/theme-tokens.css`：颜色、圆角、阴影和透明度。
- `styles/site.css`：根据原站组件前缀编写的选择器，不依赖生成的类名哈希尾码。
- `extension/`：可加载的纯 CSS 扩展。
- `garmin-liquid-glass.user.css`：完整的站点限定 UserCSS。
- `tools/build.py`：校验作用范围并生成确定性的 ZIP 和 SHA256SUMS。
- `dist/`：本地生成的下载包，不放入 Git 历史。

修改源 CSS 后重新构建，在 Edge 的扩展卡片上点击“重新加载”，再刷新 Garmin。构建脚本只操作本仓库，不会自动改动其他已安装目录。

## License / Third-party materials

自写 CSS、构建工具和项目文档按 [MIT License](LICENSE) 发布。第三方品牌与原站资产不包含在此许可中，见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

English: A CSS-only, unofficial appearance skin for the existing Garmin Connect China web app. Exact scope: `https://connectus.garmin.cn/app/*`. No scripts, telemetry, API integration or bundled Garmin assets. Windows Edge is the tested browser; international Garmin domains are not supported by the manifest.
