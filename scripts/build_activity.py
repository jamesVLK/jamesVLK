from pathlib import Path
from datetime import date, timedelta
from html import escape
import json


# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "activity.json"
OUTPUT_PATH = ROOT / "assets" / "activity.svg"


# ============================================================
# CARGAR DATA
# ============================================================

with DATA_PATH.open("r", encoding="utf-8") as file:
    data = json.load(file)

days = data["days"]

if not days:
    raise RuntimeError("activity.json no tiene días :c")


# ============================================================
# PREPARAR FECHAS
# ============================================================

days_map = {
    date.fromisoformat(day["date"]): day["count"]
    for day in days
}

start_date = min(days_map)
end_date = max(days_map)

# Python:
# lunes = 0 ... domingo = 6
#
# Nosotros queremos:
# domingo = 0 ... sábado = 6
def github_weekday(d):
    return (d.weekday() + 1) % 7


# Completamos hasta domingo al inicio
calendar_start = start_date - timedelta(
    days=github_weekday(start_date)
)

# Y hasta sábado al final
calendar_end = end_date + timedelta(
    days=6 - github_weekday(end_date)
)

weeks = (
    (calendar_end - calendar_start).days // 7
) + 1


# ============================================================
# NIVELES DE COLOR
# ============================================================

def contribution_level(count):
    if count == 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 9:
        return 3

    return 4


# ============================================================
# HELPERS
# ============================================================

def plural(value, singular, plural_word=None):
    if value == 1:
        return singular

    return plural_word or singular + "s"


def month_iterator(start, end):
    current = date(start.year, start.month, 1)

    while current <= end:
        yield current

        if current.month == 12:
            current = date(
                current.year + 1,
                1,
                1
            )
        else:
            current = date(
                current.year,
                current.month + 1,
                1
            )


# ============================================================
# DATA PARA STATS
# ============================================================

total = data["total_contributions"]
active_days = data["active_days"]

current_streak = data["current_streak"]["length"]
longest_streak = data["longest_streak"]["length"]

best_day_date = data["best_day"]["date"]
best_day_count = data["best_day"]["count"]

best_date_obj = date.fromisoformat(best_day_date)


# ============================================================
# LAYOUT
# ============================================================

SVG_WIDTH = 1000
SVG_HEIGHT = 430

HEATMAP_X = 115
HEATMAP_Y = 145

CELL = 11
GAP = 3
STEP = CELL + GAP


# ============================================================
# HEATMAP
# ============================================================

cells = []

current = calendar_start

while current <= calendar_end:

    delta = (current - calendar_start).days

    week = delta // 7
    weekday = github_weekday(current)

    x = HEATMAP_X + week * STEP
    y = HEATMAP_Y + weekday * STEP

    count = days_map.get(current, 0)
    level = contribution_level(count)

    extra_class = ""

    if current == best_date_obj:
        extra_class = " best"

    tooltip = (
        f"{current.isoformat()} — "
        f"{count} "
        f"{plural(count, 'contribution')}"
    )

    cells.append(
        f'''
        <rect
            x="{x}"
            y="{y}"
            width="{CELL}"
            height="{CELL}"
            rx="2"
            class="day level{level}{extra_class}"
        >
            <title>{escape(tooltip)}</title>
        </rect>
        '''
    )

    current += timedelta(days=1)


# ============================================================
# ETIQUETAS DE MESES
# ============================================================

MONTHS = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

month_labels = []

last_x = -999

for month_date in month_iterator(
    start_date,
    end_date
):
    week_index = (
        month_date - calendar_start
    ).days // 7

    x = HEATMAP_X + week_index * STEP

    # evita que dos meses queden demasiado pegados
    if x - last_x < 38:
        continue

    month_labels.append(
        f'''
        <text
            x="{x}"
            y="130"
            class="month"
        >
            {MONTHS[month_date.month - 1]}
        </text>
        '''
    )

    last_x = x


# ============================================================
# SVG
# ============================================================

svg = f"""<svg
    width="{SVG_WIDTH}"
    height="{SVG_HEIGHT}"
    viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
>
    <style>

        /* ==================================================
           BASE
        ================================================== */

        .background {{
            fill: #0d1117;
        }}

        .border {{
            stroke: #30363d;
        }}

        .divider {{
            stroke: #21262d;
            stroke-width: 1;
        }}


        /* ==================================================
           TERMINAL
        ================================================== */

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


        /* ==================================================
           HEATMAP
        ================================================== */

        .month,
        .weekday,
        .legend {{
            fill: #8b949e;
            font-family: "Courier New", monospace;
            font-size: 13px;
        }}

        .level0 {{
            fill: #161b22;
        }}

        .level1 {{
            fill: #0e4429;
        }}

        .level2 {{
            fill: #006d32;
        }}

        .level3 {{
            fill: #26a641;
        }}

        .level4 {{
            fill: #39d353;
        }}

        .day {{
            transition: opacity 0.2s;
        }}

        .best {{
            stroke: #d2a8ff;
            stroke-width: 1.5;
        }}

        .heatmap {{
            animation: reveal 0.8s ease-out both;
        }}


        /* ==================================================
           STATS
        ================================================== */

        .stat-label {{
            fill: #8b949e;
            font-family: "Courier New", monospace;
            font-size: 15px;
        }}

        .stat-value {{
            fill: #c9d1d9;
            font-family: "Courier New", monospace;
            font-size: 15px;
        }}

        .stat-accent {{
            fill: #d2a8ff;
            font-family: "Courier New", monospace;
            font-size: 15px;
        }}

        .muted {{
            fill: #6e7681;
            font-family: "Courier New", monospace;
            font-size: 12px;
        }}


        /* ==================================================
           CURSOR
        ================================================== */

        .cursor {{
            fill: #7ee787;
            animation: blink 1s step-end infinite;
        }}


        /* ==================================================
           ANIMACIONES
        ================================================== */

        @keyframes blink {{
            0%, 49% {{
                opacity: 1;
            }}

            50%, 100% {{
                opacity: 0;
            }}
        }}

        @keyframes reveal {{
            from {{
                opacity: 0;
                transform: translateY(5px);
            }}

            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}


        /* ==================================================
           LIGHT MODE
        ================================================== */

        @media (prefers-color-scheme: light) {{

            .background {{
                fill: #ffffff;
            }}

            .border {{
                stroke: #d0d7de;
            }}

            .divider {{
                stroke: #d8dee4;
            }}

            .title {{
                fill: #0969da;
            }}

            .prompt {{
                fill: #1a7f37;
            }}

            .command,
            .stat-value {{
                fill: #24292f;
            }}

            .month,
            .weekday,
            .legend,
            .stat-label,
            .muted {{
                fill: #57606a;
            }}

            .stat-accent {{
                fill: #8250df;
            }}

            .level0 {{
                fill: #ebedf0;
            }}

            .level1 {{
                fill: #9be9a8;
            }}

            .level2 {{
                fill: #40c463;
            }}

            .level3 {{
                fill: #30a14e;
            }}

            .level4 {{
                fill: #216e39;
            }}

            .cursor {{
                fill: #1a7f37;
            }}
        }}

    </style>


    <!-- ==================================================
         VENTANA
    ================================================== -->

    <rect
        x="10"
        y="10"
        width="980"
        height="410"
        rx="14"
        class="background border"
        stroke-width="2"
    />


    <!-- botones -->

    <circle
        cx="38"
        cy="38"
        r="7"
        fill="#ff5f56"
    />

    <circle
        cx="62"
        cy="38"
        r="7"
        fill="#ffbd2e"
    />

    <circle
        cx="86"
        cy="38"
        r="7"
        fill="#27c93f"
    />


    <!-- título -->

    <text
        x="500"
        y="45"
        text-anchor="middle"
        class="title"
    >
        jamesVLK@github
    </text>


    <!-- ==================================================
         COMANDO
    ================================================== -->

    <text
        x="55"
        y="88"
        class="prompt"
    >
        jamesVLK@github:~$
    </text>

    <text
        x="305"
        y="88"
        class="command"
    >
        ./activity --last-year
    </text>


    <!-- ==================================================
         MESES
    ================================================== -->

    {"".join(month_labels)}


    <!-- ==================================================
         DÍAS
    ================================================== -->

    <text
        x="72"
        y="{HEATMAP_Y + STEP + 9}"
        class="weekday"
    >
        Mon
    </text>

    <text
        x="72"
        y="{HEATMAP_Y + STEP * 3 + 9}"
        class="weekday"
    >
        Wed
    </text>

    <text
        x="72"
        y="{HEATMAP_Y + STEP * 5 + 9}"
        class="weekday"
    >
        Fri
    </text>


    <!-- ==================================================
         HEATMAP
    ================================================== -->

    <g class="heatmap">

        {"".join(cells)}

    </g>


    <!-- ==================================================
         LEYENDA
    ================================================== -->

    <text
        x="720"
        y="265"
        class="legend"
    >
        less
    </text>

    <rect
        x="765"
        y="254"
        width="11"
        height="11"
        rx="2"
        class="level0"
    />

    <rect
        x="782"
        y="254"
        width="11"
        height="11"
        rx="2"
        class="level1"
    />

    <rect
        x="799"
        y="254"
        width="11"
        height="11"
        rx="2"
        class="level2"
    />

    <rect
        x="816"
        y="254"
        width="11"
        height="11"
        rx="2"
        class="level3"
    />

    <rect
        x="833"
        y="254"
        width="11"
        height="11"
        rx="2"
        class="level4"
    />

    <text
        x="855"
        y="265"
        class="legend"
    >
        more
    </text>


    <!-- separador -->

    <line
        x1="70"
        y1="285"
        x2="930"
        y2="285"
        class="divider"
    />


    <!-- ==================================================
         STATS
    ================================================== -->

    <text
        x="85"
        y="318"
        class="stat-label"
    >
        contributions
    </text>

    <text
        x="245"
        y="318"
        class="stat-accent"
    >
        {total}
    </text>


    <text
        x="355"
        y="318"
        class="stat-label"
    >
        active-days
    </text>

    <text
        x="490"
        y="318"
        class="stat-value"
    >
        {active_days}
    </text>


    <text
        x="585"
        y="318"
        class="stat-label"
    >
        current-streak
    </text>

    <text
        x="755"
        y="318"
        class="stat-value"
    >
        {current_streak} {plural(current_streak, "day")}
    </text>


    <text
        x="85"
        y="350"
        class="stat-label"
    >
        longest-streak
    </text>

    <text
        x="245"
        y="350"
        class="stat-value"
    >
        {longest_streak} {plural(longest_streak, "day")}
    </text>


    <text
        x="355"
        y="350"
        class="stat-label"
    >
        best-day
    </text>

    <text
        x="455"
        y="350"
        class="stat-accent"
    >
        {best_day_date}
    </text>

    <text
        x="585"
        y="350"
        class="muted"
    >
        {best_day_count} contributions
    </text>


    <!-- ==================================================
         PROMPT FINAL
    ================================================== -->

    <text
        x="55"
        y="397"
        class="prompt"
    >
        jamesVLK@github:~$
    </text>

    <rect
        x="305"
        y="380"
        width="11"
        height="21"
        rx="1"
        class="cursor"
    />

</svg>
"""


# ============================================================
# GUARDAR
# ============================================================

OUTPUT_PATH.write_text(
    svg,
    encoding="utf-8"
)

print("======================================")
print(" Activity SVG generado :D")
print("======================================")
print(f"Semanas          : {weeks}")
print(f"Contribuciones   : {total}")
print(f"Días activos     : {active_days}")
print(f"Racha actual     : {current_streak}")
print(f"Racha máxima     : {longest_streak}")
print(f"Mejor día        : {best_day_date} ({best_day_count})")
print()
print(f"Guardado en -> {OUTPUT_PATH}")