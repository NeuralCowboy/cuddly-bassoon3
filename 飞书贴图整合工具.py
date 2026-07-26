# -*- coding: utf-8 -*-
"""
飞书贴图整合工具
================
统一入口：先选择内容日志版或转化日志版，再进入对应的原有工具界面。

两套工具的核心功能、配置文件和输出行为保持不变：
- 内容日志版 -> 飞书截图校验上传工具_Link增强版.py
- 转化日志版 -> 转化日志贴图项目/转化日志贴图工具.py
"""

import argparse
import importlib.util
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Any, List, Optional


if getattr(sys, "frozen", False):
    APP_DIR = Path(sys.executable).resolve().parent
    RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR)).resolve()
else:
    APP_DIR = Path(__file__).resolve().parent
    RESOURCE_DIR = APP_DIR

CONTENT_TOOL_PATH = RESOURCE_DIR / "飞书截图校验上传工具_Link增强版.py"
CONVERSION_TOOL_PATH = RESOURCE_DIR / "转化日志贴图项目" / "转化日志贴图工具.py"

MODES = {
    "content": {
        "title": "内容日志版",
        "subtitle": "进入飞书贴图项目 Link 增强版",
        "path": CONTENT_TOOL_PATH,
        "module_name": "content_log_link_tool",
    },
    "conversion": {
        "title": "转化日志版",
        "subtitle": "进入转化日志贴图项目",
        "path": CONVERSION_TOOL_PATH,
        "module_name": "conversion_log_tool",
    },
}


def load_tool_module(mode: str) -> Any:
    info = MODES[mode]
    path = Path(info["path"])
    if not path.exists():
        raise FileNotFoundError(f"找不到工具文件:{path}")
    module_name = str(info["module_name"])
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载工具模块:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def launch_mode(mode: str, argv: Optional[List[str]] = None) -> int:
    module = load_tool_module(mode)
    if argv:
        return int(module.main(argv))
    return int(module.launch_gui())


class ModeChooser(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("飞书贴图整合工具")
        self.geometry("900x540")
        self.minsize(760, 460)
        self.configure(bg="#07111F")
        self._animated_panels = []
        self._build()

    def _build(self) -> None:
        style = ttk.Style(self)
        try:
            if "clam" in style.theme_names():
                style.theme_use("clam")
        except Exception:
            pass

        self.font = "Microsoft YaHei UI"
        style.configure("Root.TFrame", background="#07111F")

        header = tk.Canvas(self, height=150, bg="#07111F", highlightthickness=0)
        header.pack(fill="x")
        header.bind("<Configure>", self._draw_header)
        self.header_canvas = header

        body = ttk.Frame(self, style="Root.TFrame", padding=(28, 28))
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._choice_card(
            body,
            column=0,
            title="内容日志版",
            eyebrow="CONTENT LOG",
            subtitle="适合上传内容日志 Day1 / Day2。AI 会自动把截图和问卷记录对齐，并在多张截图中选择更像主界面广告的图片作为截图主图。",
            button_text="进入内容日志版",
            accent="#38BDF8",
            accent_dark="#0E7490",
            panel_bg="#0B1B2E",
            features=("识别截图属于哪位受访者", "自动匹配平台和评价序号", "区分截图主图和补充截图", "生成可复核的内容日志结果"),
            mode="content",
        )
        self._choice_card(
            body,
            column=1,
            title="转化日志版",
            eyebrow="CONVERSION LOG",
            subtitle="适合上传转化日志。AI 会识别购买平台和题目截图，把 E1、E2、E17、E20 及 DT-FM 原始文字放到正确列。",
            button_text="进入转化日志版",
            accent="#22C55E",
            accent_dark="#15803D",
            panel_bg="#0B2319",
            features=("识别 TT / IG 购买平台", "自动归位每个题号截图", "同步 DT-FM 原始文字", "生成可复核的转化日志结果"),
            mode="conversion",
        )
        self._animate_panels()

    def _draw_header(self, event: tk.Event) -> None:
        canvas = self.header_canvas
        canvas.delete("all")
        width = max(1, event.width)
        height = max(1, event.height)
        for i in range(0, width, 18):
            shade = "#07111F" if (i // 18) % 2 else "#091827"
            canvas.create_rectangle(i, 0, i + 18, height, fill=shade, outline=shade)
        for y, color in ((28, "#123B5D"), (76, "#104334"), (118, "#1E293B")):
            canvas.create_line(0, y, width, y + 12, fill=color, width=1)
        canvas.create_oval(width - 210, -70, width + 90, 210, outline="#164E63", width=2)
        canvas.create_oval(width - 145, -35, width + 35, 145, outline="#14532D", width=2)
        canvas.create_text(34, 34, anchor="nw", text="FEISHU IMAGE OPS",
                           fill="#67E8F9", font=("Consolas", 10, "bold"))
        canvas.create_text(34, 60, anchor="nw", text="飞书贴图整合工具",
                           fill="#F8FAFC", font=(self.font, 24, "bold"))
        canvas.create_text(36, 102, anchor="nw", text="选择上传类型，系统将路由到对应的日志处理工作台",
                           fill="#A7B7C8", font=(self.font, 11))
        canvas.create_text(width - 36, 36, anchor="ne", text="AI ROUTER ONLINE",
                           fill="#86EFAC", font=("Consolas", 10, "bold"))
        canvas.create_text(width - 36, 64, anchor="ne", text="CONTENT  /  CONVERSION",
                           fill="#CBD5E1", font=("Consolas", 10))

    def _choice_card(self, parent: ttk.Frame, column: int, title: str, eyebrow: str, subtitle: str,
                     button_text: str, accent: str, accent_dark: str, panel_bg: str,
                     features: tuple, mode: str) -> None:
        card = tk.Frame(
            parent,
            bg=panel_bg,
            highlightbackground=accent,
            highlightcolor=accent,
            highlightthickness=1,
            padx=24,
            pady=22,
        )
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 14) if column == 0 else (14, 0))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(5, weight=1)

        tk.Label(card, text=eyebrow, bg=panel_bg, fg=accent, font=("Consolas", 10, "bold")).grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(card, text=title, bg=panel_bg, fg="#F8FAFC", font=(self.font, 20, "bold")).grid(
            row=1, column=0, sticky="w", pady=(8, 0)
        )
        tk.Frame(card, bg=accent, height=3).grid(row=2, column=0, sticky="ew", pady=(14, 16))
        tk.Label(
            card,
            text=subtitle,
            bg=panel_bg,
            fg="#B6C3D1",
            font=(self.font, 11),
            wraplength=330,
            justify="left",
        ).grid(row=3, column=0, sticky="w")

        scan_panel = self._scan_panel(card, accent, panel_bg, title)
        scan_panel.grid(row=4, column=0, sticky="ew", pady=(20, 4))

        feature_box = tk.Frame(card, bg=panel_bg)
        feature_box.grid(row=5, column=0, sticky="new", pady=(16, 16))
        feature_box.columnconfigure(0, weight=1)
        for row, text in enumerate(features):
            item = tk.Frame(feature_box, bg=panel_bg)
            item.grid(row=row, column=0, sticky="ew", pady=4)
            tk.Label(item, text="●", bg=panel_bg, fg=accent, font=("Consolas", 10, "bold")).pack(side="left")
            tk.Label(item, text=text, bg=panel_bg, fg="#D7E1EA", font=(self.font, 10)).pack(
                side="left", padx=(8, 0)
            )

        button = self._canvas_button(card, button_text, accent, accent_dark, lambda: self._open_mode(mode))
        button.grid(row=6, column=0, sticky="ew")

    def _scan_panel(self, parent: tk.Widget, accent: str, panel_bg: str, title: str) -> tk.Canvas:
        canvas = tk.Canvas(parent, height=78, bg=panel_bg, highlightthickness=0)
        panel = {"canvas": canvas, "accent": accent, "title": title, "phase": len(self._animated_panels) * 18}
        self._animated_panels.append(panel)
        canvas.bind("<Configure>", lambda _event, item=panel: self._draw_scan_panel(item))
        return canvas

    def _draw_scan_panel(self, panel: dict) -> None:
        canvas = panel["canvas"]
        accent = panel["accent"]
        title = panel["title"]
        phase = int(panel["phase"])
        width = max(1, canvas.winfo_width())
        canvas.delete("all")
        canvas.create_rectangle(0, 0, width, 78, fill="#071827", outline=accent, width=1)
        canvas.create_text(14, 14, anchor="nw", text="AI CHECKFLOW", fill=accent, font=("Consolas", 9, "bold"))
        canvas.create_text(14, 38, anchor="nw", text="读取截图  →  匹配记录  →  输出结果",
                           fill="#D7E1EA", font=(self.font, 10, "bold"))
        for x in range(16, width - 14, 38):
            canvas.create_line(x, 64, x + 16, 64, fill="#24435A", width=2)
        dot_x = 18 + (phase % max(1, width - 52))
        canvas.create_oval(dot_x, 58, dot_x + 12, 70, fill=accent, outline=accent)
        canvas.create_text(width - 14, 14, anchor="ne", text="READY", fill="#86EFAC", font=("Consolas", 9, "bold"))
        badge = "内容日志智能路由" if "内容" in title else "转化日志智能路由"
        canvas.create_text(width - 14, 39, anchor="ne", text=badge, fill="#A7B7C8", font=(self.font, 9))

    def _animate_panels(self) -> None:
        for panel in self._animated_panels:
            panel["phase"] = int(panel["phase"]) + 5
            self._draw_scan_panel(panel)
        self.after(90, self._animate_panels)

    def _canvas_button(self, parent: tk.Widget, text: str, accent: str, base: str, command) -> tk.Canvas:
        canvas = tk.Canvas(parent, height=56, bg=parent.cget("bg"), highlightthickness=0, cursor="hand2")
        state = {"hover": False}

        def draw(_event=None) -> None:
            width = max(1, canvas.winfo_width())
            canvas.delete("all")
            fill = accent if state["hover"] else base
            text_fill = "#06111F" if state["hover"] else "#FFFFFF"
            canvas.create_rectangle(0, 0, width, 56, fill=fill, outline=accent, width=2)
            canvas.create_rectangle(5, 5, width - 5, 51, outline="#FFFFFF", width=1)
            canvas.create_text(
                width / 2,
                28,
                text=text,
                fill=text_fill,
                font=(self.font, 13, "bold"),
            )

        def enter(_event=None) -> None:
            state["hover"] = True
            draw()

        def leave(_event=None) -> None:
            state["hover"] = False
            draw()

        canvas.bind("<Configure>", draw)
        canvas.bind("<Enter>", enter)
        canvas.bind("<Leave>", leave)
        canvas.bind("<Button-1>", lambda _event: command())
        return canvas

    def _open_mode(self, mode: str) -> None:
        self._play_transition(mode)

    def _play_transition(self, mode: str) -> None:
        accent = "#38BDF8" if mode == "content" else "#22C55E"
        title = "正在进入内容日志工作台" if mode == "content" else "正在进入转化日志工作台"
        overlay = tk.Canvas(self, bg="#020817", highlightthickness=0)
        overlay.place(x=0, y=0, relwidth=1, relheight=1)

        def draw(frame: int = 0) -> None:
            width = max(1, overlay.winfo_width())
            height = max(1, overlay.winfo_height())
            overlay.delete("all")
            overlay.create_rectangle(0, 0, width, height, fill="#020817", outline="#020817")
            for y in range(0, height, 26):
                color = "#06162A" if (y // 26 + frame) % 2 else "#071E30"
                overlay.create_line(0, y, width, y + 18, fill=color, width=1)
            scan_y = (frame * 18) % max(1, height + 80) - 40
            overlay.create_rectangle(0, scan_y, width, scan_y + 48, fill=accent, outline=accent, stipple="gray25")
            overlay.create_text(width / 2, height / 2 - 30, text="AI ROUTING", fill=accent,
                                font=("Consolas", 16, "bold"))
            overlay.create_text(width / 2, height / 2 + 6, text=title, fill="#F8FAFC",
                                font=(self.font, 20, "bold"))
            overlay.create_text(width / 2, height / 2 + 44, text="读取配置  →  装载工作台  →  准备任务引擎",
                                fill="#A7B7C8", font=(self.font, 11))
            for i in range(18):
                x = width / 2 - 170 + i * 20
                active = i <= frame % 18
                overlay.create_rectangle(x, height / 2 + 78, x + 12, height / 2 + 86,
                                         fill=accent if active else "#1E293B", outline="")
            if frame < 24:
                self.after(35, lambda: draw(frame + 1))
            else:
                try:
                    self.destroy()
                    launch_mode(mode)
                except Exception as exc:  # noqa: BLE001
                    messagebox.showerror("启动失败", str(exc))

        draw()

    def _open_mode_old(self, mode: str) -> None:
        try:
            self.destroy()
            launch_mode(mode)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("启动失败", str(exc))


def launch_gui() -> int:
    ModeChooser().mainloop()
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="飞书贴图整合工具")
    parser.add_argument("--mode", choices=sorted(MODES), default="", help="content=内容日志版, conversion=转化日志版")
    parser.add_argument("--gui", action="store_true", help="启动选择界面(默认)")
    args, rest = parser.parse_known_args(argv)

    if args.mode:
        return launch_mode(args.mode, rest)
    return launch_gui()


if __name__ == "__main__":
    raise SystemExit(main())
