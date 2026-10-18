"""
KiCad's position file looks like this:

Ref,Val,Package,PosX,PosY,Rot,Side
"C1","10u","CAPC3216X180N",88.250000,-97.300000,90.000000,top
"C2","1u","CAPC1005X60N",90.100000,-98.600000,-90.000000,top


JLC expects position files that looks like this:

Designator,Mid X,Mid Y,Rotation,Layer
C1,88.25,-97.3,90.0,top
C10,99.6,-97.8,0.0,top
C11,112.75,-89.95,180.0,top

Let's transform!
"""

import sys
import csv
from pathlib import Path

def format_positions(in_path: Path, out_path: Path):
    with open(in_path, newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        rows = []

        for row in reader:
            # Remove quotes from KiCad's Ref
            designator = row["Ref"].strip('"')

            # Fetch KiCad's position as floats.
            # Floats are printed without trailing zeroes by default.
            mid_x = float(row["PosX"])
            mid_y = float(row["PosY"])

            # Fix KiCad's "negative" rotation angles.
            # I.e. make -90 into 270.
            rotation = float(row["Rot"])
            if rotation < 0:
                rotation += 360

            # KiCad's "Side" and JLC's "Layer" has the same format:
            layer = row["Side"]

            # Add row to rows as dict with correct header names:
            rows.append({
                "Designator"    : designator,
                "Mid X"         : mid_x,
                "Mid Y"         : mid_y,
                "Rotation"      : rotation,
                "Layer"         : layer
            })

        # Write output:
    with open(out_path, "w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=["Designator", "Mid X", "Mid Y", "Rotation", "Layer"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows into {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: kicad_to_jlc_positions.py <input.csv> <project_dir>")
        sys.exit(1)

    source           = Path(sys.argv[1])
    project_name     = Path(sys.argv[2]).name # Pull project name from folder name

    destination = source.parent / f"{project_name}_jlc_cpl.csv"

    format_positions(source, destination)

    # Delete the input file:
    source.unlink()