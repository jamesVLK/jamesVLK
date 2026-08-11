from pathlib import Path
from datetime import datetime, UTC
import json
import re

import requests
from bs4 import BeautifulSoup


# ============================================================
# CONFIG
# ============================================================

USERNAME = "jamesVLK"

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_PATH = DATA_DIR / "activity.json"

URL = f"https://github.com/users/{USERNAME}/contributions"


# ============================================================
# SACAR EL NÚMERO DEL TOOLTIP DE GITHUB
# ============================================================

def get_contribution_count(soup, cell):
    """
    GitHub pone algo como:
        "5 contributions on August 10th."
        "1 contribution on August 10th."
        "No contributions on August 10th."

    Nosotros solo queremos el numerito :v
    """

    cell_id = cell.get("id")

    text = ""

    # normalmente GitHub conecta cada cuadrito con un <tool-tip>
    if cell_id:
        tooltip = soup.find("tool-tip", attrs={"for": cell_id})

        if tooltip:
            text = tooltip.get_text(" ", strip=True)

    # fallback por si GitHub cambia algo y mete el texto directamente
    if not text:
        text = cell.get("aria-label", "")

    if "no contributions" in text.lower():
        return 0

    match = re.search(
        r"([\d,]+)\s+contribution",
        text,
        flags=re.IGNORECASE
    )

    if not match:
        return 0

    return int(match.group(1).replace(",", ""))


# ============================================================
# DESCARGAR CALENDARIO
# ============================================================

def fetch_days():
    print(f"Buscando actividad de @{USERNAME}...")
    print(URL)

    response = requests.get(
        URL,
        headers={
            "User-Agent": "jamesVLK-profile-readme/1.0"
        },
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Estos son literalmente los cuadraditos del calendario de GitHub
    cells = soup.select(
        "td.ContributionCalendar-day[data-date]"
    )

    if not cells:
        raise RuntimeError(
            "No encontré los cuadritos del calendario :c "
            "GitHub pudo haber cambiado su HTML."
        )

    days = []

    for cell in cells:
        date = cell.get("data-date")

        if not date:
            continue

        count = get_contribution_count(soup, cell)

        days.append({
            "date": date,
            "count": count
        })

    # porsiacaso GitHub nos los manda desordenados xd
    days.sort(key=lambda item: item["date"])

    return days


# ============================================================
# RACHA ACTUAL
# ============================================================

def calculate_current_streak(days):
    if not days:
        return {
            "length": 0,
            "start": None,
            "end": None
        }

    index = len(days) - 1

    # Si hoy todavía tiene 0, no dejamos que "hoy"
    # mate una racha que terminó ayer.
    if days[index]["count"] == 0:
        index -= 1

    end_index = index
    streak = 0

    while index >= 0 and days[index]["count"] > 0:
        streak += 1
        index -= 1

    if streak == 0:
        return {
            "length": 0,
            "start": None,
            "end": None
        }

    start_index = index + 1

    return {
        "length": streak,
        "start": days[start_index]["date"],
        "end": days[end_index]["date"]
    }


# ============================================================
# RACHA MÁS LARGA
# ============================================================

def calculate_longest_streak(days):
    longest = 0
    current = 0

    current_start = None
    longest_start = None
    longest_end = None

    for day in days:

        if day["count"] > 0:

            if current == 0:
                current_start = day["date"]

            current += 1

            if current > longest:
                longest = current
                longest_start = current_start
                longest_end = day["date"]

        else:
            current = 0
            current_start = None

    return {
        "length": longest,
        "start": longest_start,
        "end": longest_end
    }


# ============================================================
# ESTADÍSTICAS
# ============================================================

def build_activity_data(days):
    total = sum(day["count"] for day in days)

    active_days = sum(
        1
        for day in days
        if day["count"] > 0
    )

    best_day = max(
        days,
        key=lambda day: day["count"]
    )

    current_streak = calculate_current_streak(days)
    longest_streak = calculate_longest_streak(days)

    return {
        "username": USERNAME,

        "generated_at": datetime.now(UTC).isoformat(),

        "range": {
            "start": days[0]["date"],
            "end": days[-1]["date"]
        },

        "total_contributions": total,

        "active_days": active_days,

        "average_per_active_day": (
            round(total / active_days, 2)
            if active_days > 0
            else 0
        ),

        "current_streak": current_streak,

        "longest_streak": longest_streak,

        "best_day": best_day,

        "days": days
    }


# ============================================================
# MAIN
# ============================================================

def main():
    days = fetch_days()

    data = build_activity_data(days)

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print()
    print("======================================")
    print(" GitHub activity cargada :D")
    print("======================================")
    print(f"Días leídos        : {len(days)}")
    print(f"Contribuciones     : {data['total_contributions']}")
    print(f"Días activos       : {data['active_days']}")
    print(
        f"Racha actual       : "
        f"{data['current_streak']['length']} días"
    )
    print(
        f"Racha más larga    : "
        f"{data['longest_streak']['length']} días"
    )
    print(
        f"Mejor día          : "
        f"{data['best_day']['date']} "
        f"({data['best_day']['count']})"
    )
    print()
    print(f"Guardado en -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()