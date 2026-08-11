from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUTPUT_PATH = ASSETS / "stack.svg"

svg = """<svg
    width="1000"
    height="350"
    viewBox="0 0 1000 350"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
>
    <style>
        .background {
            fill: #0d1117;
        }

        .border {
            stroke: #30363d;
        }

        .title {
            fill: #58a6ff;
            font-family: "Courier New", monospace;
            font-size: 22px;
            font-weight: bold;
        }

        .prompt {
            fill: #7ee787;
            font-family: "Courier New", monospace;
            font-size: 19px;
            font-weight: bold;
        }

        .command {
            fill: #c9d1d9;
            font-family: "Courier New", monospace;
            font-size: 19px;
        }

        .comment {
            fill: #58a6ff;
            font-family: "Courier New", monospace;
            font-size: 17px;
            font-weight: bold;
        }

        .label {
            fill: #8b949e;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        .colon {
            fill: #6e7681;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        .value {
            fill: #c9d1d9;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        .accent {
            fill: #d2a8ff;
            font-family: "Courier New", monospace;
            font-size: 16px;
        }

        .cursor {
            fill: #7ee787;
            animation: blink 1s step-end infinite;
        }

        .divider {
            stroke: #21262d;
            stroke-width: 1;
        }

        @keyframes blink {
            0%, 49% {
                opacity: 1;
            }

            50%, 100% {
                opacity: 0;
            }
        }

        @media (prefers-color-scheme: light) {
            .background {
                fill: #ffffff;
            }

            .border,
            .divider {
                stroke: #d0d7de;
            }

            .title,
            .comment {
                fill: #0969da;
            }

            .prompt {
                fill: #1a7f37;
            }

            .command,
            .value {
                fill: #24292f;
            }

            .label,
            .colon {
                fill: #57606a;
            }

            .accent {
                fill: #8250df;
            }

            .cursor {
                fill: #1a7f37;
            }
        }
    </style>

    <!-- Ventana -->
    <rect
        x="10"
        y="10"
        width="980"
        height="330"
        rx="14"
        class="background border"
        stroke-width="2"
    />

    <!-- Botones -->
    <circle cx="38" cy="38" r="7" fill="#ff5f56"/>
    <circle cx="62" cy="38" r="7" fill="#ffbd2e"/>
    <circle cx="86" cy="38" r="7" fill="#27c93f"/>

    <!-- Título -->
    <text
        x="500"
        y="45"
        text-anchor="middle"
        class="title"
    >
        jamesVLK@github
    </text>

    <!-- Comando -->
    <text
        x="55"
        y="84"
        class="prompt"
    >
        jamesVLK@github:~$
    </text>

    <text
        x="305"
        y="84"
        class="command"
    >
        cat stack.txt
    </text>

    <!-- ========================= -->
    <!-- CORE -->
    <!-- ========================= -->

    <text
        x="85"
        y="120"
        class="comment"
    >
        # core
    </text>

    <!-- Languages -->
    <text
        x="105"
        y="150"
        class="label"
    >
        languages
    </text>

    <text
        x="315"
        y="150"
        class="colon"
    >
        :
    </text>

    <text
        x="337"
        y="150"
        class="value"
    >
        C · C++ · Java · C#
    </text>

    <!-- Web Services -->
    <text
        x="105"
        y="180"
        class="label"
    >
        web-services
    </text>

    <text
        x="315"
        y="180"
        class="colon"
    >
        :
    </text>

    <text
        x="337"
        y="180"
        class="accent"
    >
        HTML · CSS · JS · REST · SOAP
    </text>

    <!-- Foundations -->
    <text
        x="105"
        y="210"
        class="label"
    >
        foundations
    </text>

    <text
        x="315"
        y="210"
        class="colon"
    >
        :
    </text>

    <text
        x="337"
        y="210"
        class="value"
    >
        Algorithms · Data Structures · SQL
    </text>

    <!-- Separador -->
    <line
        x1="85"
        y1="225"
        x2="915"
        y2="225"
        class="divider"
    />

    <!-- ========================= -->
    <!-- ENGINEERING -->
    <!-- ========================= -->

    <text
        x="85"
        y="248"
        class="comment"
    >
        # engineering
    </text>

    <!-- Software Engineering -->
    <text
        x="105"
        y="274"
        class="label"
    >
        software-engineering
    </text>

    <text
        x="315"
        y="274"
        class="colon"
    >
        :
    </text>

    <text
        x="337"
        y="274"
        class="accent"
    >
        UML · C4 · Requirements · Design Patterns
    </text>

    <!-- Future Focus -->
    <text
        x="105"
        y="300"
        class="label"
    >
        future-focus
    </text>

    <text
        x="315"
        y="300"
        class="colon"
    >
        :
    </text>

    <text
        x="337"
        y="300"
        class="value"
    >
        Cybersecurity · AI
    </text>

    <!-- Prompt final -->
    <text
        x="55"
        y="329"
        class="prompt"
    >
        jamesVLK@github:~$
    </text>

    <rect
        x="305"
        y="312"
        width="11"
        height="21"
        rx="1"
        class="cursor"
    />
</svg>
"""

OUTPUT_PATH.write_text(svg, encoding="utf-8")

print(f"Listo :D -> {OUTPUT_PATH}")