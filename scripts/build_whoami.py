from pathlib import Path
from PIL import Image
import base64
import io

# Aca para tener las rutas base :D
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

AVATAR_PATH = ASSETS / "avatar.png"  
OUTPUT_PATH = ASSETS / "whoami.svg"

# Acá estamos cargando el avatar
img = Image.open(AVATAR_PATH).convert("RGBA")

# para mejorar la imagen :D
gray = img.convert("L")
mask = gray.point(lambda p: 0 if p > 245 else 255)
bbox = mask.getbbox()

if bbox:
    left, top, right, bottom = bbox
    pad = 40
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(img.width, right + pad)
    bottom = min(img.height, bottom + pad)
    img = img.crop((left, top, right, bottom))

# Redimensionamos para que entre bonito
max_size = (280, 280)
img.thumbnail(max_size, Image.Resampling.LANCZOS)

# quitar fondo claro y convertir líneas a color "terminal / github"
target_rgb = (201, 209, 217)  # #c9d1d9

pixels = img.load()
for y in range(img.height):
    for x in range(img.width):
        r, g, b, a = pixels[x, y]
        lum = int(0.299 * r + 0.587 * g + 0.114 * b)

        # fondo claro => transparente
        if lum > 245:
            pixels[x, y] = (0, 0, 0, 0)
        else:
            # mientras más oscuro el trazo, más visible
            alpha = 255 - lum
            alpha = max(90, min(255, alpha + 70))
            pixels[x, y] = (target_rgb[0], target_rgb[1], target_rgb[2], alpha)

# centramos en un canva transparente
canvas = Image.new("RGBA", (320, 280), (0, 0, 0, 0))
offset_x = (canvas.width - img.width) // 2
offset_y = (canvas.height - img.height) // 2
canvas.alpha_composite(img, (offset_x, offset_y))

# convertimos a base64 para incrustarlo dentro del SVG
buffer = io.BytesIO()
canvas.save(buffer, format="PNG")
avatar_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

# se construye ya el svg final
svg = f"""<svg
    width="1000"
    height="390"
    viewBox="0 0 1000 390"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
>
    <style>
        .background {{
            fill: #0d1117;
        }}

        .border {{
            stroke: #30363d;
        }}

        .panel {{
            fill: #0b1220;
            stroke: #30363d;
        }}

        .title {{
            fill: #58a6ff;
            font-family: "Courier New", monospace;
            font-size: 22px;
            font-weight: bold;
        }}

        .prompt {{
            fill: #7ee787;
            font-family: "Courier New", monospace;
            font-size: 19px;
            font-weight: bold;
        }}

        .command {{
            fill: #c9d1d9;
            font-family: "Courier New", monospace;
            font-size: 19px;
        }}

        .label {{
            fill: #8b949e;
            font-family: "Courier New", monospace;
            font-size: 17px;
        }}

        .value {{
            fill: #c9d1d9;
            font-family: "Courier New", monospace;
            font-size: 17px;
        }}

        .accent {{
            fill: #d2a8ff;
            font-family: "Courier New", monospace;
            font-size: 17px;
        }}

        .mini {{
            fill: #6e7681;
            font-family: "Courier New", monospace;
            font-size: 13px;
        }}

        .cursor {{
            fill: #7ee787;
            animation: blink 1s step-end infinite;
        }}

        @keyframes blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}

        @media (prefers-color-scheme: light) {{
            .background {{
                fill: #ffffff;
            }}

            .border {{
                stroke: #d0d7de;
            }}

            .panel {{
                fill: #f6f8fa;
                stroke: #d0d7de;
            }}

            .title {{
                fill: #0969da;
            }}

            .prompt {{
                fill: #1a7f37;
            }}

            .command,
            .value {{
                fill: #24292f;
            }}

            .label,
            .mini {{
                fill: #57606a;
            }}

            .accent {{
                fill: #8250df;
            }}

            .cursor {{
                fill: #1a7f37;
            }}
        }}
    </style>

    <!-- marco principal -->
    <rect
        x="10"
        y="10"
        width="980"
        height="370"
        rx="14"
        class="background border"
        stroke-width="2"
    />

    <!-- botoncitos tipo mac/terminal -->
    <circle cx="38" cy="38" r="7" fill="#ff5f56"/>
    <circle cx="62" cy="38" r="7" fill="#ffbd2e"/>
    <circle cx="86" cy="38" r="7" fill="#27c93f"/>

    <!-- título -->
    <text x="500" y="45" text-anchor="middle" class="title">
        jamesVLK@github
    </text>

    <!-- panel izquierdo del retrato -->
    <rect
        x="40"
        y="72"
        width="330"
        height="240"
        rx="12"
        class="panel"
        stroke-width="1.5"
    />

    <image
    href="data:image/png;base64,{avatar_b64}"
    x="52"
    y="80"
    width="306"
    height="224"
    preserveAspectRatio="xMidYMid meet"
/>

    <!-- bloque derecho -->
    <text x="410" y="95" class="prompt">
        jamesVLK@github:~$
    </text>

    <text x="650" y="95" class="command">
        whoami
    </text>

    <text x="440" y="145" class="label">
        Name
    </text>

    <text x="610" y="145" class="value">
        James Valentín
    </text>

    <text x="440" y="185" class="label">
        Studies
    </text>

    <text x="610" y="185" class="value">
        Informatics Engineering @ PUCP
    </text>

    <text x="440" y="225" class="label">
        Focus
    </text>

    <text x="610" y="225" class="accent">
        Software Engineering
    </text>

    <text x="610" y="255" class="accent">
        Algorithms &amp; Data Structures
    </text>

    <text x="610" y="285" class="accent">
        Backend Development
    </text>

    <text x="610" y="315" class="accent">
        Databases
    </text>

    <!-- prompt final -->
    <text x="55" y="355" class="prompt">
        jamesVLK@github:~$
    </text>

    <rect
        x="275"
        y="338"
        width="11"
        height="21"
        rx="1"
        class="cursor"
    />
</svg>
"""

OUTPUT_PATH.write_text(svg, encoding="utf-8")
print(f"Listo :D se generó -> {{OUTPUT_PATH}}")