import sys
import glob
from pathlib import Path
from dataclasses import dataclass, field
from datetime import date

##
## Define Paths
##
SCRIPT_DIR = Path(__file__).resolve().parent
KICAD_DIR = SCRIPT_DIR.parent
SYM_DIR = KICAD_DIR / "symbols"
REVIEW_DIR = KICAD_DIR / "reviews"
FP_DIR = KICAD_DIR / "footprints"

##
## Class & Dict for storing indexed symbols
##
@dataclass
class Sym:
    name            : str
    library         : str
    library_line    : int
    template        : str | None
    properties      : dict[str, str] = field(default_factory=dict)

##
##  Class for automatic check results
##
@dataclass
class Results:
    number          : str
    description     : str
    result          : str
    detail          : str = ""



##
##  Traverses all .kicad_sym files in ../symbols/ and stores all symbols with their:
##  Name, Library, Library file line (for quicker future lookups) and template.
##
def index_symbols() -> dict[str, Sym]:
    sym_index: dict[str, Sym] = {}
    sym_files = sorted(SYM_DIR.glob("*.kicad_sym"))
    for sym_file in sym_files:
        lib_templates = []
        with sym_file.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                # If line is symbol definition, save symbol name:
                if line.startswith('\t(symbol "'):
                    sym_name = line.split('"')[1]
                    sym_line = line_no
                # If line is symbol reference, save symbol reference:
                elif line.startswith('\t\t(property "Reference"'):
                    sym_ref = line.split('"')[3]
                    # If duplicate, create warning and continue:
                    if sym_name in sym_index:
                        ## To-Do: Insert warning here.
                        continue
                    # If sym is template:
                    if sym_name.startswith('000_'):
                        lib_templates.append(sym_name) # add to templates list:
                        sym_index[sym_name] = Sym(sym_name, sym_file.stem, sym_line, sym_name)
                    # If library has no template:
                    elif len(lib_templates) == 0:
                        sym_index[sym_name] = Sym(sym_name, sym_file.stem, sym_line, None)
                    # If library only has 1 template:
                    elif len(lib_templates) == 1:
                        sym_index[sym_name] = Sym(sym_name, sym_file.stem, sym_line, lib_templates[0])
                    # If library has multiple templates, match on reference:
                    elif len(lib_templates) > 1:
                        # If multiple lib templates, identify based on Reference:
                        template_match = f"000_{sym_ref}_Template"
                        if template_match in lib_templates:
                            sym_index[sym_name] = Sym(sym_name, sym_file.stem, sym_line, template_match)
                        else:
                            sym_index[sym_name] = Sym(sym_name, sym_file.stem, sym_line, None)
    return sym_index

##
##  The footprint library names in KiCad are defined by the footprint lib table,
##  and may not match the directory name.
##  Thus, map library names to directory paths.
##
def index_footprints() -> dict[str, Path]:
    fp_index: dict[str, Path] = {}
    table_file = KICAD_DIR / "ninjalib-fp-table"

    with table_file.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("(lib "):
                parts = line.split('"')
                name, uri = parts[1], parts[5]
                fp_index[name] = Path(uri.replace("${NINJALIB}", str(KICAD_DIR)))
    return fp_index

def read_properties(sym: Sym) -> dict[str, str]:
    properties: dict[str, str] = {}
    sym_file = SYM_DIR / f"{sym.library}.kicad_sym"
    with sym_file.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            # Skip up to and including the symbol definition line:
            if line_no <= sym.library_line:
                continue
            # If end of symbol definition:
            if line.startswith('\t)'):
                break
            # If property definition within symbol definition:
            if line.startswith('\t\t(property "'):
                parts = line.split('"')
                properties[parts[1]] = parts[3]
    return properties

def sym_template_field_check(sym: Sym, template: Sym | None) -> Results:
    desc = "All template fields present in symbol"
    num = "1.1"
    if template is None:
        return Results(num, desc, "FAIL", "No template found")
    missing = template.properties.keys() - sym.properties.keys()
    if missing:
        return Results(num, desc, "FAIL", f"Missing fields: {', '.join(sorted(missing))}")
    return Results(num, desc, "PASS")

def sym_extra_field_check(sym: Sym, template: Sym | None) -> Results:
    desc = "No extra fields in symbol"
    num = "1.2"
    if template is None:
        return Results(num, desc, "FAIL", "No template found")
    extra = sym.properties.keys() - template.properties.keys()
    # filter out internal "ki_*" fields:
    extra = {name for name in extra if not name.startswith("ki_")}
    if extra:
        return Results(num, desc, "FAIL", f"Extra fields: {', '.join(sorted(extra))}")
    return Results(num, desc, "PASS")

def sym_footprint_exists(sym: Sym, fp_index: dict[str, Path]) -> Results:
    num = "1.3"
    desc = "Footprint file exists"
    if "Footprint" not in sym.properties:
        return Results(num, desc, "FAIL", "Missing Footprint property")
    footprint = sym.properties.get("Footprint")
    if footprint == "":
        return Results(num, desc, "FAIL", "Footprint property empty")
    if ":" not in footprint:
        return Results(num, desc, "FAIL", f"Footprint has no library prefix: {footprint}")
    fp_lib, fp_name = footprint.split(':', 1)
    fp_lib_dir = fp_index.get(fp_lib)
    if fp_lib_dir is None:
        return Results(num, desc, "FAIL", f"Footprint library not in ninjalib-fp-table: {fp_lib}")
    if not (fp_lib_dir / f"{fp_name}.kicad_mod").is_file():
        return Results(num, desc, "FAIL", f"Footprint file not found: {fp_lib}:{fp_name}")
    return Results(num, f"Footprint file `{fp_name}.kicad_mod` exists", "PASS")

def sym_pin_count_match_fp(sym: Sym, fp_index: dict[str, Path]) -> Results:
    desc = "Pin count in symbol matches pin count in footprint"
    ## Future work

def sym_height_match_fp(sym: Sym, fp_index: dict[str, Path]) -> Results:
    desc = "H_max_um in symbol matches H_max in footprint"
    ## Future work

def sym_3d_model_exists(sym: Sym, fp_index: dict[str, Path]) -> Results:
    desc = "3D Model file exists"
    ## Future work

def sym_datasheet_exists(sym: Sym) -> Results:
    desc = "Datasheet file exists"
    ## Future work

def find_project_symbols(project_dir: Path):
    pass
    # future work

###
### .md report building functions
###
def table_rows(rows: list[tuple[str, str, str]]) -> str:
    return "\n".join(f"| {a} | {b} | {c} |" for a, b, c in rows)

def find_reports(folder: Path, sym_name: str) -> list[Path]:
    return sorted(folder.glob(f"????-??-??_{glob.escape(sym_name)}.md"))

# Makes columns in md tables same width:
def balance_md_tables(report: str) -> str:
    r_lines = report.splitlines()

    tab_start = None
    tab_end = None

    for line_no, line in enumerate(r_lines):
        if line.startswith("|"): # if md table
            if tab_start is None:
                tab_start = line_no
                continue
        if tab_start is not None and not line.startswith("|"):
            # Found end of table
            tab_end = line_no

            # Find widest word in each column:
            table = [] # List of cells for each row
            c_widths = []
            for row in r_lines[tab_start:tab_end]:
                row = row.strip()       # Removes trailing/leading whitespace
                row = row.strip("|")    # Removes trailing/leading "|"
                cells = row.split("|")  # Split row into cells
                table.append(cells)

                if c_widths == []:
                    for c in cells:
                        c_widths.append(len(c))
                else:
                    for pos, c in enumerate(cells):
                        if len(c) > c_widths[pos]:
                            c_widths[pos] = len(c)
            # c_widths now contain max widths of each cell
            for i in range(tab_start, tab_end):
                cells = table[i - tab_start]

                is_separator = True # The |---|---|... row
                for c in cells:
                    if c.strip("-") != "":
                        is_separator = False

                new_cells = []
                for pos in range(len(cells)):
                    if is_separator:
                        new_cells.append("-" * c_widths[pos])
                    else:
                        new_cells.append(cells[pos].ljust(c_widths[pos]))

                r_lines[i] = "|" + "|".join(new_cells) + "|"

            tab_start = None

    return "\n".join(r_lines) + "\n"

# Creates one line command for f3d to get step model dimensions & position:
# Avoids creating f3d dependency in script.
def model_bbox_command(step_file: Path | None) -> str:
    if step_file is None:
        return "No 3D model referenced by the footprint."
    return (f'f3d "{step_file}" --verbose=debug '
            f'--output "$env:TEMP\\f3d.png" | Select-String "bounding box"')
           
def review_component(sym_name: str, sym_index: dict[str, Sym], fp_index: dict[str, Path]) -> Path | None:
    sym = sym_index.get(sym_name)
    sym_template = sym_index.get(sym.template)
    sym.properties = read_properties(sym)

    if sym.properties.get("Review_Status") in ("Approved", "In Production"):
        return None # Sym already approved, no review performed.
    if find_reports(REVIEW_DIR / "pending", sym_name):
        return None # Report already exists in /pending/
    if find_reports(REVIEW_DIR / "approved", sym_name):
        return None # Report already exists in /approved/
    if sym.library in ("ninja_tp", "ninja_symbol"):
        return None # Non-revieable symbols
    sym_template.properties = read_properties(sym_template)

    checks: list[Results] = [
        sym_template_field_check(sym, sym_template),
        sym_extra_field_check(sym, sym_template),
        sym_footprint_exists(sym, fp_index),
    ]

    check_rows = table_rows([(c.number, c.description, c.result) for c in checks])
    check_errors = [f"{c.number}: {c.detail}" for c in checks if c.result == "FAIL"]
    check_output = "\n".join(check_errors) if check_errors else "No errors."

    properties = [(name, f"`{value}`", "Y/N/NA")
                      for name, value in sym.properties.items()
                      if not name.startswith("ki_")]

    property_rows = table_rows(properties)

    template_text = (SCRIPT_DIR / "review_template.md").read_text(encoding="utf-8")

    # Locate 3D-model:
    # Future work.


    report = template_text
    report = report.replace("%%SYMBOL_NAME%%", sym.name)
    report = report.replace("%%LIBRARY%%", sym.library)
    report = report.replace("%%TEMPLATE%%", sym.template)
    report = report.replace("%%CHECK_ROWS%%", check_rows)
    report = report.replace("%%CHECK_OUTPUT%%", check_output)
    report = report.replace("%%PROPERTY_ROWS%%", property_rows)
    today = date.today().isoformat()
    report = report.replace("%%DATE%%", today)

    report = balance_md_tables(report)

    out_dir = REVIEW_DIR / "pending"
    out_dir.mkdir(parents=True, exist_ok=True) # Create dir if missing
    out_file = out_dir / f"{today}_{sym.name}.md"
    out_file.write_text(report, encoding="utf-8", newline="\n")

    return out_file

##
## Project Parsing Functions
##
def syms_in_schematic(schematic: Path) -> list[str]:
    sym_list = []
    with schematic.open("r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("\t\t(symbol "):
                lib_name, sym_name = line.split('"')[1].split(":", 1)
                sym_list.append(sym_name)
    return sym_list


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8") # Files contain "Ω"
    if not SYM_DIR.is_dir():
        sys.exit(f"Symbols folder not found: {SYM_DIR}")

    # Create index of all symbols:
    sym_index = index_symbols()
    # Create index of footprint libraries:
    fp_index = index_footprints()

    test_sym_name = "FB_120Ω_0603_H950"

    #print(review_component(test_sym_name, sym_index, fp_index))
    syms = syms_in_schematic(SCRIPT_DIR / "nsim_lpb.kicad_sch")

    for sym in syms:
        review_component(sym, sym_index, fp_index)

    return 0 # Success

if __name__ == "__main__":
    sys.exit(main())