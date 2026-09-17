# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This is not a software project — it's a personal KiCad ECAD library ("NinjaLib"): schematic symbols, PCB footprints, and 3D STEP models for electronic components. There is no build, lint, or test tooling; changes are authored/verified by opening the libraries in KiCad (version 7+/10 symbol format) and are validated visually rather than by any automated command.

## Repository layout

- `kicad/symbols/*.kicad_sym` — one symbol library file per component category (`ninja_resistor`, `ninja_capacitor`, `ninja_diode`, `ninja_connector`, `ninja_ic`, `ninja_ic_power`, `ninja_osc`).
- `kicad/footprints/*.pretty/` — one footprint library folder per package family (`ninja_capc`, `ninja_resc`, `ninja_sot`, `ninja_soic`, `ninja_sop`, `ninja_custom`), each containing `.kicad_mod` files.
- `kicad/ninjalib-sym-table` / `kicad/ninjalib-fp-table` — the KiCad library tables that must list every symbol/footprint library above or KiCad won't load it. **When adding a new `.kicad_sym` file or `.pretty` folder, register it here too.**
- `step/<package-family>/*.step` — 3D models, organized into folders matching package families (`bga`, `capc`, `custom`, `dfn`, `header`, `indc`, `ledc`, `resc`, `soic`, `sop`, `sot`).
- `kicad/README.md` — KiCad path-variable and library setup instructions (`NINJALIB`, `NINJASTEP`, `NINJADATASHEET`).
- `README.md` — standardized 3D-model color palette (STEP `COLOUR_RGB` entities) and IPC-7351 chip package dimension reference.
- `kicad/footprints/package_codes.md` — maps IPC-7351 footprint names to manufacturer-specific package codes.

## Conventions to follow when adding parts

**Symbol naming:**
- Passives (resistors/capacitors) are named `<Value>_<Package>_<Tolerance-or-Dielectric>_<Rating>_<Manufacturer>_H<HeightUnits>`, e.g. `R_10k_0402_1%_TKF_H400`, `C_100n_0402_X7R_50V_H500`.
- ICs, diodes, connectors, and oscillators are named after the manufacturer part number, e.g. `TPS25210L`, `USBLC6-2SC6`, `TYPE-C-31-M-12`.

**Templates:** each symbol library starts with a `000_..._Template`/`000_..._template` symbol defining the standard property schema for that category.
- In `ninja_resistor.kicad_sym`, real parts use `(extends "000_R_Template")` — a live KiCad inheritance link, so shared graphics/pins update from the template automatically.
- In `ninja_capacitor.kicad_sym`, value symbols use `(extends "C")`, the generic base capacitor symbol.
- In the other libraries (diode, ic, ic_power, connector, osc), the `000_..._template` is only a copy-paste starting point — each real part is a fully standalone, hand-drawn symbol (no `extends` link), because these parts have unique graphics/pinouts.

**Standard properties** on parts (fields present but often left blank until known): `Reference`, `Value`, `Footprint`, `Datasheet`, `Description`, `Manufacturer`, `Manufacturer_PN`, category-specific fields (e.g. `Type`, `V_r_max`, `I_f_max_ma`, `IC_Category`, `V_type`), `T_min`, `T_max`, `H_max`, `Package`, `Ninja_ID`, `JLC_Package`/`JLC_PACKAGE`, `JLC_PN`.

**Footprint references** inside a symbol use `<footprint-library>:<footprint-name>`, e.g. `ninja_sot:SOT95P280X145-6N`.

**Datasheets** are never stored in this repo (copyright). Symbols reference them via `file://${NINJADATASHEETs}/<manufacturer>_<part-number>_<revision>_<publication-date>.pdf`; revision is omitted if not provided, and part-family name is used instead of part number when a datasheet covers multiple parts.

**Footprint/package naming** follows IPC-7351 (e.g. `RESC1608X55`, `SOIC127P600X175-8`); an `N` suffix denotes the nominal (IPC "N") density variant. See `kicad/footprints/package_codes.md` for the mapping to vendor-specific package codes.

**STEP model colors** are set via `COLOUR_RGB` entities referenced by `FILL_AREA_STYLE_COLOUR` entities in the STEP file; the standardized palette (hex + normalized RGB) is documented in the root `README.md` and should be reused rather than picking new colors ad hoc. Note a color entity may be defined multiple times in one file, so all occurrences may need changing to recolor a model fully.

## Notes

- `*.bak` files next to `.kicad_sym` files are KiCad's own local backups; they're gitignored and not part of the library.
