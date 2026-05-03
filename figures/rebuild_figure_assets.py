from __future__ import annotations

import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Iterable


ROOT = Path(r"D:\22017\Documents\毕业设计\myXDU_Project")
OUTPUT_DIR = ROOT / "figures"

FONT = "Microsoft YaHei"
BG = "#F8FAFC"
INK = "#0F172A"
MUTED = "#475569"
SHADOW = "#D8E1EB"

BLUE = "#2F80ED"
BLUE_FILL = "#EAF3FF"
AMBER = "#D99A00"
AMBER_FILL = "#FFF5CC"
PURPLE = "#8E44AD"
PURPLE_FILL = "#F2E8FF"
PINK = "#E83E8C"
PINK_FILL = "#FFE1EF"
INDIGO = "#4C6EF5"
INDIGO_FILL = "#E6ECFF"
GREEN = "#2F9E44"
GREEN_FILL = "#E8F8EC"
TEAL = "#0F766E"
TEAL_FILL = "#DCFCE7"
SLATE = "#94A3B8"
SLATE_FILL = "#F1F5F9"


def rounded_rect(x: int, y: int, w: int, h: int, fill: str, stroke: str,
                 rx: int = 24, stroke_width: int = 3, shadow: bool = True) -> list[dict]:
    shapes: list[dict] = []
    if shadow:
        shapes.append(
            {
                "type": "rect",
                "x": x + 8,
                "y": y + 10,
                "w": w,
                "h": h,
                "rx": rx,
                "fill": SHADOW,
                "stroke": "none",
                "stroke_width": 0,
            }
        )
    shapes.append(
        {
            "type": "rect",
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "rx": rx,
            "fill": fill,
            "stroke": stroke,
            "stroke_width": stroke_width,
        }
    )
    return shapes


def text_block(x: int, y: int, lines: Iterable[str], size: int = 26,
               fill: str = INK, weight: str = "normal", align: str = "center",
               line_gap: int = 12) -> dict:
    return {
        "type": "text",
        "x": x,
        "y": y,
        "lines": list(lines),
        "font_size": size,
        "fill": fill,
        "weight": weight,
        "align": align,
        "line_gap": line_gap,
    }


def arrow(x1: int, y1: int, x2: int, y2: int, color: str = MUTED, width: int = 4) -> dict:
    return {
        "type": "line",
        "x1": x1,
        "y1": y1,
        "x2": x2,
        "y2": y2,
        "color": color,
        "width": width,
        "arrow_end": True,
    }


def polyline(points: list[tuple[int, int]], color: str = MUTED, width: int = 4) -> dict:
    return {
        "type": "polyline",
        "points": points,
        "color": color,
        "width": width,
        "arrow_end": True,
    }


def label_chip(x: int, y: int, w: int, h: int, text: str, fill: str, stroke: str,
               size: int = 22) -> list[dict]:
    return rounded_rect(x, y, w, h, fill, stroke, rx=18, stroke_width=2, shadow=False) + [
        text_block(x + w // 2, y + h // 2, text.splitlines(), size=size, fill=stroke, weight="bold")
    ]


def feature_pill(x: int, y: int, w: int, h: int, title: str, desc: str,
                 fill: str, stroke: str) -> list[dict]:
    return rounded_rect(x, y, w, h, fill, stroke, rx=18, stroke_width=2, shadow=False) + [
        text_block(x + w // 2, y + h // 2 - 16, [title], size=24, fill=stroke, weight="bold"),
        text_block(x + w // 2, y + h // 2 + 16, [desc], size=18, fill=INK, weight="bold"),
    ]


def build_specs() -> dict[str, dict]:
    specs: dict[str, dict] = {}

    specs["8.短训GRU1"] = {
        "width": 1180,
        "height": 360,
        "background": BG,
        "shapes": [
            *rounded_rect(40, 102, 160, 150, BLUE_FILL, BLUE, rx=22),
            text_block(120, 177, ["输入特征", "维度：5"], size=28, weight="bold"),
            arrow(200, 177, 245, 177),
            *rounded_rect(250, 78, 390, 205, AMBER_FILL, AMBER, rx=24),
            text_block(445, 144, ["单层 GRU", "隐式联合跟踪各类协方差", "维度：80"], size=27, weight="bold"),
            *label_chip(642, 146, 128, 38, "隐状态映射", "#FFF0D8", AMBER, size=18),
            arrow(640, 177, 760, 177),
            *rounded_rect(770, 95, 230, 170, SLATE_FILL, SLATE, rx=22),
            text_block(885, 180, ["FC 输出层", "维度：80 → 160 → 32"], size=26, weight="bold"),
            arrow(1000, 177, 1045, 177),
            *rounded_rect(1050, 95, 110, 170, GREEN_FILL, GREEN, rx=22),
            text_block(1105, 180, ["卡尔曼增益", "Kₜ", "维度：32"], size=24, weight="bold"),
        ],
    }

    common_multi_shapes = [
        *rounded_rect(40, 212, 150, 150, BLUE_FILL, BLUE, rx=22),
        arrow(190, 287, 248, 287),
        *rounded_rect(250, 200, 200, 174, SLATE_FILL, SLATE, rx=22),
        text_block(350, 282, ["FC 输入层", "多路特征提取"], size=25, weight="bold"),
        arrow(450, 287, 520, 287),
        *rounded_rect(520, 200, 250, 174, PINK_FILL, PINK, rx=22),
        arrow(770, 240, 850, 150),
        arrow(770, 287, 850, 240),
        arrow(770, 334, 860, 452),
        *rounded_rect(850, 70, 330, 180, PURPLE_FILL, PURPLE, rx=24),
        *rounded_rect(870, 372, 310, 170, INDIGO_FILL, INDIGO, rx=24),
        arrow(1015, 250, 1015, 372),
        *label_chip(955, 270, 126, 54, "降维映射\n64 → 16", "#F5E8FF", PURPLE, size=19),
        arrow(1180, 160, 1335, 255),
        arrow(1180, 458, 1335, 332),
        *rounded_rect(1340, 208, 170, 160, SLATE_FILL, SLATE, rx=22),
        arrow(1510, 288, 1562, 288),
    ]

    specs["9.短训GRU2"] = {
        "width": 1760,
        "height": 600,
        "background": BG,
        "shapes": [
            *common_multi_shapes,
            text_block(115, 287, ["输入特征", "维度：5"], size=30, weight="bold"),
            text_block(645, 285, ["GRU 层", "跟踪状态噪声（Q）", "维度：64"], size=26, weight="bold"),
            text_block(1015, 160, ["GRU 层", "跟踪预测协方差（Σ）", "维度：64"], size=26, weight="bold"),
            text_block(1025, 455, ["GRU 层", "跟踪残差协方差（S）", "维度：64 → 16"], size=25, weight="bold"),
            text_block(1425, 286, ["FC 输出层", "维度：32"], size=26, weight="bold"),
            *rounded_rect(1560, 208, 170, 160, GREEN_FILL, GREEN, rx=22),
            text_block(1645, 286, ["卡尔曼增益", "Kₜ"], size=28, weight="bold"),
            *label_chip(785, 212, 54, 34, "Q", "#FFF0F6", PINK, size=20),
            *label_chip(1210, 96, 128, 40, "预测协方差", "#F5E8FF", PURPLE, size=18),
            *label_chip(1202, 418, 128, 40, "残差协方差", "#E8EDFF", INDIGO, size=18),
        ],
    }

    specs["7.短+长训GRU3"] = {
        "width": 1780,
        "height": 600,
        "background": BG,
        "shapes": [
            *common_multi_shapes,
            text_block(115, 287, ["输入特征", "F₂, F₄, Conf", "维度：13"], size=28, weight="bold"),
            text_block(645, 285, ["GRU 层", "跟踪状态噪声（Q）", "维度：64"], size=26, weight="bold"),
            text_block(1015, 160, ["GRU 层", "跟踪预测协方差（Σ）", "维度：64"], size=26, weight="bold"),
            text_block(1025, 455, ["GRU 层", "跟踪残差协方差（S）", "维度：64 → 16"], size=25, weight="bold"),
            text_block(1425, 286, ["FC 输出层", "维度：32"], size=26, weight="bold"),
            *rounded_rect(1560, 208, 190, 160, GREEN_FILL, GREEN, rx=22),
            text_block(1655, 286, ["卡尔曼增益", "修正量 ΔKₜ"], size=27, weight="bold"),
            *label_chip(785, 212, 54, 34, "Q", "#FFF0F6", PINK, size=20),
            *label_chip(1210, 96, 128, 40, "预测协方差", "#F5E8FF", PURPLE, size=18),
            *label_chip(1202, 418, 128, 40, "残差协方差", "#E8EDFF", INDIGO, size=18),
        ],
    }

    specs["32.KalmanNet架构-横向排版"] = {
        "width": 1600,
        "height": 620,
        "background": BG,
        "shapes": [
            *rounded_rect(50, 60, 520, 500, BLUE_FILL, BLUE, rx=34),
            text_block(310, 115, ["输入层"], size=34, weight="bold"),
            text_block(310, 180, ["F₂：观测残差", "Δyₜ = 当前观测值 - 先验观测预测值"], size=27, weight="bold"),
            *feature_pill(95, 270, 170, 92, "Δx", "中心 X 坐标差值", "#FFFFFF", BLUE),
            *feature_pill(95, 375, 170, 92, "Δy", "中心 Y 坐标差值", "#FFFFFF", BLUE),
            *feature_pill(95, 480, 170, 92, "Δa", "目标宽高比差值", "#FFFFFF", BLUE),
            *feature_pill(300, 375, 170, 92, "Δh", "目标高度差值", "#FFFFFF", BLUE),
            text_block(520, 282, ["4 维差分", "特征输入"], size=22, fill=MUTED, weight="bold"),
            arrow(570, 310, 675, 310),
            *rounded_rect(690, 145, 340, 330, AMBER_FILL, AMBER, rx=28),
            text_block(860, 240, ["中间架构层"], size=34, weight="bold"),
            *label_chip(760, 285, 200, 54, "架构 2：3 个 GRU", "#FFF8E1", AMBER, size=24),
            *label_chip(760, 360, 90, 44, "GRU Q", "#FFFFFF", AMBER, size=18),
            *label_chip(880, 360, 90, 44, "GRU Σ", "#FFFFFF", AMBER, size=18),
            *label_chip(820, 418, 90, 44, "GRU S", "#FFFFFF", AMBER, size=18),
            text_block(1098, 270, ["全连接", "非线性映射"], size=22, fill=MUTED, weight="bold"),
            arrow(1030, 310, 1140, 310),
            *rounded_rect(1155, 175, 370, 250, GREEN_FILL, GREEN, rx=34),
            text_block(1340, 260, ["输出层"], size=34, weight="bold"),
            text_block(1340, 355, ["卡尔曼增益  Kₜ"], size=30, weight="bold"),
        ],
    }

    specs["31.系统流程图"] = {
        "width": 2400,
        "height": 1550,
        "background": BG,
        "shapes": [
            *rounded_rect(760, 40, 880, 128, "#143E68", "#143E68", rx=28),
            text_block(1200, 104, ["系统输入：视频流"], size=38, fill="#FFFFFF", weight="bold"),
            arrow(1200, 168, 1200, 242, color=SLATE, width=5),
            *rounded_rect(890, 250, 620, 112, BLUE_FILL, BLUE, rx=24),
            text_block(1200, 306, ["YOLOX 目标检测"], size=38, weight="bold"),
            arrow(1200, 362, 1200, 430, color=SLATE, width=5),
            *rounded_rect(120, 430, 2160, 930, "#FFFFFF", SLATE, rx=34),
            text_block(1200, 480, ["ByteTrack 算法"], size=42, weight="bold"),
            *rounded_rect(230, 560, 360, 170, BLUE_FILL, BLUE, rx=26),
            text_block(410, 645, ["历史活跃轨迹", "t−1 时刻轨迹状态"], size=31, weight="bold"),
            *rounded_rect(720, 560, 460, 170, TEAL_FILL, TEAL, rx=26),
            text_block(950, 640, ["卡尔曼状态预测", "输出先验估计  x̂ₜ|ₜ₋₁"], size=30, weight="bold"),
            *rounded_rect(1320, 560, 430, 170, PURPLE_FILL, PURPLE, rx=26),
            text_block(1535, 640, ["置信度划分", "高置信度框 / 低置信度框"], size=30, weight="bold"),
            *rounded_rect(1860, 540, 280, 110, "#F8F4FF", PURPLE, rx=24),
            text_block(2000, 595, ["首次匹配"], size=30, weight="bold"),
            *rounded_rect(1860, 710, 280, 110, "#EEF2FF", INDIGO, rx=24),
            text_block(2000, 765, ["二次匹配"], size=30, weight="bold"),
            *rounded_rect(640, 790, 620, 430, "#E9FFF5", TEAL, rx=30),
            text_block(950, 835, ["KalmanNet 模块"], size=34, weight="bold"),
            *label_chip(730, 900, 130, 54, "FC 输入层", "#FFFFFF", TEAL, size=22),
            *label_chip(890, 900, 120, 54, "GRU Q", "#FFFFFF", PINK, size=22),
            *label_chip(1040, 900, 120, 54, "GRU Σ", "#FFFFFF", PURPLE, size=22),
            *label_chip(815, 985, 120, 54, "GRU S", "#FFFFFF", INDIGO, size=22),
            *label_chip(965, 985, 130, 54, "FC 输出层", "#FFFFFF", TEAL, size=22),
            *rounded_rect(740, 1080, 420, 100, "#FFFFFF", TEAL, rx=22, shadow=False),
            text_block(950, 1130, ["输出卡尔曼残差增益  ΔKₜ"], size=28, weight="bold"),
            *rounded_rect(1490, 930, 480, 190, "#F8FAFF", INDIGO, rx=28),
            text_block(1730, 1022, ["轨迹管理", "新建轨迹 / 活跃轨迹 / 丢失轨迹"], size=31, weight="bold"),
            *label_chip(1680, 840, 190, 42, "剩余轨迹进入二次匹配", "#FFFFFF", SLATE, size=18),
            *label_chip(1615, 470, 170, 42, "检测结果 yₜ", "#FFFFFF", BLUE, size=18),
            *label_chip(1030, 742, 172, 42, "先验估计送入匹配", "#FFFFFF", TEAL, size=18),
            arrow(590, 645, 720, 645),
            polyline([(1180, 645), (1245, 645), (1245, 525), (1910, 525), (1910, 540)], color=MUTED, width=4),
            polyline([(1535, 730), (1535, 770), (1860, 770)], color=PURPLE, width=4),
            polyline([(2000, 650), (2000, 710)], color=SLATE, width=4),
            arrow(950, 790, 950, 730),
            arrow(2000, 820, 1730, 930),
            polyline([(1730, 1120), (1730, 1260), (1200, 1260), (1200, 1380)], color=INDIGO, width=5),
            *label_chip(990, 1230, 150, 42, "活跃轨迹集合", "#FFFFFF", INDIGO, size=18),
            *rounded_rect(720, 1380, 960, 120, "#143E68", "#143E68", rx=28),
            text_block(1200, 1440, ["系统输出：连续多目标轨迹数据流"], size=38, fill="#FFFFFF", weight="bold"),
        ],
    }

    return specs


def svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_svg(spec: dict, path: Path) -> None:
    width = spec["width"]
    height = spec["height"]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{MUTED}"/>',
        "</marker>",
        "</defs>",
        f'<rect width="{width}" height="{height}" fill="{spec["background"]}"/>',
    ]

    for shape in spec["shapes"]:
        if shape["type"] == "rect":
            stroke = shape["stroke"]
            stroke_width = shape["stroke_width"]
            lines.append(
                f'<rect x="{shape["x"]}" y="{shape["y"]}" width="{shape["w"]}" height="{shape["h"]}" '
                f'rx="{shape["rx"]}" fill="{shape["fill"]}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
            )
        elif shape["type"] == "line":
            marker = ' marker-end="url(#arrow)"' if shape.get("arrow_end") else ""
            lines.append(
                f'<line x1="{shape["x1"]}" y1="{shape["y1"]}" x2="{shape["x2"]}" y2="{shape["y2"]}" '
                f'stroke="{shape["color"]}" stroke-width="{shape["width"]}" stroke-linecap="round"{marker}/>'
            )
        elif shape["type"] == "polyline":
            marker = ' marker-end="url(#arrow)"' if shape.get("arrow_end") else ""
            points = " ".join(f"{x},{y}" for x, y in shape["points"])
            lines.append(
                f'<polyline points="{points}" fill="none" stroke="{shape["color"]}" '
                f'stroke-width="{shape["width"]}" stroke-linejoin="round" stroke-linecap="round"{marker}/>'
            )
        elif shape["type"] == "text":
            anchor = {"center": "middle", "left": "start", "right": "end"}[shape["align"]]
            font_weight = "700" if shape["weight"] == "bold" else "400"
            line_height = int(shape["font_size"] + shape["line_gap"])
            offset = -((len(shape["lines"]) - 1) * line_height) / 2
            lines.append(
                f'<text x="{shape["x"]}" y="{shape["y"]}" fill="{shape["fill"]}" '
                f'font-family="{FONT}" font-size="{shape["font_size"]}" font-weight="{font_weight}" '
                f'text-anchor="{anchor}" dominant-baseline="middle">'
            )
            for idx, content in enumerate(shape["lines"]):
                dy = offset + idx * line_height
                lines.append(f'<tspan x="{shape["x"]}" dy="{dy if idx == 0 else line_height}">{svg_escape(content)}</tspan>')
                offset = 0
            lines.append("</text>")

    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")


POWERSHELL_RENDERER = r"""
param(
    [string]$SpecPath,
    [string]$OutPath
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

function Get-Color {
    param([string]$Hex)
    return [System.Drawing.ColorTranslator]::FromHtml($Hex)
}

function New-RoundRectPath {
    param(
        [float]$X,
        [float]$Y,
        [float]$W,
        [float]$H,
        [float]$R
    )
    $path = New-Object System.Drawing.Drawing2D.GraphicsPath
    $d = $R * 2
    $path.AddArc($X, $Y, $d, $d, 180, 90)
    $path.AddArc($X + $W - $d, $Y, $d, $d, 270, 90)
    $path.AddArc($X + $W - $d, $Y + $H - $d, $d, $d, 0, 90)
    $path.AddArc($X, $Y + $H - $d, $d, $d, 90, 90)
    $path.CloseFigure()
    return $path
}

function Draw-ArrowHead {
    param(
        $Graphics,
        [float]$X1,
        [float]$Y1,
        [float]$X2,
        [float]$Y2,
        [string]$Color,
        [float]$Width
    )
    $angle = [Math]::Atan2($Y2 - $Y1, $X2 - $X1)
    $length = 14 + $Width
    $spread = 0.52
    $p1 = New-Object System.Drawing.PointF($X2, $Y2)
    $p2 = New-Object System.Drawing.PointF(
        [float]($X2 - $length * [Math]::Cos($angle - $spread)),
        [float]($Y2 - $length * [Math]::Sin($angle - $spread))
    )
    $p3 = New-Object System.Drawing.PointF(
        [float]($X2 - $length * [Math]::Cos($angle + $spread)),
        [float]($Y2 - $length * [Math]::Sin($angle + $spread))
    )
    $brush = New-Object System.Drawing.SolidBrush((Get-Color $Color))
    $Graphics.FillPolygon($brush, @($p1, $p2, $p3))
    $brush.Dispose()
}

function Draw-TextBlock {
    param(
        $Graphics,
        $Shape
    )
    $style = if ($Shape.weight -eq 'bold') { [System.Drawing.FontStyle]::Bold } else { [System.Drawing.FontStyle]::Regular }
    $font = New-Object System.Drawing.Font('Microsoft YaHei', [float]$Shape.font_size, $style, [System.Drawing.GraphicsUnit]::Pixel)
    $brush = New-Object System.Drawing.SolidBrush((Get-Color $Shape.fill))
    $format = New-Object System.Drawing.StringFormat
    switch ($Shape.align) {
        'left' { $format.Alignment = [System.Drawing.StringAlignment]::Near }
        'right' { $format.Alignment = [System.Drawing.StringAlignment]::Far }
        default { $format.Alignment = [System.Drawing.StringAlignment]::Center }
    }
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $lineHeight = [float]$Shape.font_size + [float]$Shape.line_gap
    $startY = [float]$Shape.y - ((($Shape.lines.Count - 1) * $lineHeight) / 2.0)
    $i = 0
    foreach ($line in $Shape.lines) {
        $rect = New-Object System.Drawing.RectangleF -ArgumentList ([float]$Shape.x - 320), ($startY + $i * $lineHeight - $lineHeight / 2), 640, ($lineHeight + 6)
        if ($Shape.align -eq 'left') {
            $rect = New-Object System.Drawing.RectangleF -ArgumentList ([float]$Shape.x), ($startY + $i * $lineHeight - $lineHeight / 2), 720, ($lineHeight + 6)
        }
        $Graphics.DrawString([string]$line, $font, $brush, $rect, $format)
        $i += 1
    }
    $brush.Dispose()
    $font.Dispose()
    $format.Dispose()
}

$spec = Get-Content -Raw -Encoding UTF8 $SpecPath | ConvertFrom-Json
$bmp = New-Object System.Drawing.Bitmap([int]$spec.width, [int]$spec.height)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear((Get-Color $spec.background))

foreach ($shape in $spec.shapes) {
    switch ($shape.type) {
        'rect' {
            $path = New-RoundRectPath $shape.x $shape.y $shape.w $shape.h $shape.rx
            $brush = New-Object System.Drawing.SolidBrush((Get-Color $shape.fill))
            $g.FillPath($brush, $path)
            $brush.Dispose()
            if ($shape.stroke -ne 'none' -and [float]$shape.stroke_width -gt 0) {
                $pen = New-Object System.Drawing.Pen((Get-Color $shape.stroke), [float]$shape.stroke_width)
                $g.DrawPath($pen, $path)
                $pen.Dispose()
            }
            $path.Dispose()
        }
        'line' {
            $pen = New-Object System.Drawing.Pen((Get-Color $shape.color), [float]$shape.width)
            $pen.StartCap = [System.Drawing.Drawing2D.LineCap]::Round
            $pen.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
            $g.DrawLine($pen, [float]$shape.x1, [float]$shape.y1, [float]$shape.x2, [float]$shape.y2)
            if ($shape.arrow_end) {
                Draw-ArrowHead $g $shape.x1 $shape.y1 $shape.x2 $shape.y2 $shape.color $shape.width
            }
            $pen.Dispose()
        }
        'polyline' {
            $points = New-Object 'System.Collections.Generic.List[System.Drawing.PointF]'
            foreach ($point in $shape.points) {
                $points.Add((New-Object System.Drawing.PointF([float]$point[0], [float]$point[1])))
            }
            $pen = New-Object System.Drawing.Pen((Get-Color $shape.color), [float]$shape.width)
            $pen.LineJoin = [System.Drawing.Drawing2D.LineJoin]::Round
            $pen.StartCap = [System.Drawing.Drawing2D.LineCap]::Round
            $pen.EndCap = [System.Drawing.Drawing2D.LineCap]::Round
            $g.DrawLines($pen, $points.ToArray())
            if ($shape.arrow_end -and $points.Count -ge 2) {
                $a = $points[$points.Count - 2]
                $b = $points[$points.Count - 1]
                Draw-ArrowHead $g $a.X $a.Y $b.X $b.Y $shape.color $shape.width
            }
            $pen.Dispose()
        }
        'text' {
            Draw-TextBlock $g $shape
        }
    }
}

$directory = Split-Path -Parent $OutPath
if (-not (Test-Path $directory)) {
    New-Item -ItemType Directory -Force -Path $directory | Out-Null
}

$bmp.Save($OutPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bmp.Dispose()
"""


def render_png(spec: dict, path: Path) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        spec_path = tmp_path / "spec.json"
        ps1_path = tmp_path / "render.ps1"
        spec_path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
        ps1_path.write_text(POWERSHELL_RENDERER, encoding="utf-8")
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ps1_path),
                str(spec_path),
                str(path),
            ],
            check=True,
        )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    specs = build_specs()
    for name, spec in specs.items():
        render_svg(spec, OUTPUT_DIR / f"{name}.svg")
        render_png(spec, OUTPUT_DIR / f"{name}.png")
    shutil.copy2(Path(__file__), OUTPUT_DIR / Path(__file__).name)
    print(f"generated {len(specs)} figures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
