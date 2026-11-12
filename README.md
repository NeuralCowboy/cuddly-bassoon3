# 问卷截图与 CSV 分析工具

这个仓库包含飞书贴图工具的桌面入口和一个独立的 CSV 问答示例。

| 入口 | 用途 | 当前状态 |
| --- | --- | --- |
| [飞书贴图整合工具.py](./飞书贴图整合工具.py) | 在内容日志与转化日志模式之间切换，用于整理问卷和截图 | 已提供 Tkinter 启动器，完整处理需要另行取得对应模块 |
| [main.py](./main.py) 与 [utils.py](./utils.py) | 在 Streamlit 中上传 CSV，用自然语言请求回答、表格或图表 | 实验示例，运行还需要 Streamlit 和兼容的 LangChain 依赖 |

## 飞书贴图工具

内容日志模式面向受访者、平台、题号和截图的匹配。转化日志模式面向购买平台、题号截图及原始文字的归位。完整工具的两种模式分别由以下模块实现。

- 内容日志：`飞书截图校验上传工具_Link增强版.py`
- 转化日志：`转化日志贴图项目/转化日志贴图工具.py`

取得对应模块后，按上面的相对路径放置。使用带 Tkinter 的 Python，在仓库目录安装 [飞书工具依赖](./requirements.txt) 并启动入口。

```sh
python -m pip install -r requirements.txt
python 飞书贴图整合工具.py
```

## CSV 问答示例

页面支持上传 CSV、预览数据，并请求文字回答、表格、条形图、折线图或散点图。在具备兼容的 Streamlit 和 LangChain 运行环境后，从仓库目录执行 `python -m streamlit run main.py`，再在侧栏填写自己的 OpenAI API Key。CSV 依赖尚未锁定，`requirements.txt` 对应飞书工具。

## 数据与配置

飞书 App ID、App Secret、表格地址、文件夹 token 和模型密钥由使用者在本地配置。提交代码前应移除这些值，以及实际问卷、受访者截图和导出的业务数据。CSV 示例会把用户提问及模型处理所需的数据发送至模型接口。
