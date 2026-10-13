# Review: `%%SYMBOL_NAME%%` 

**Library:** `%%LIBRARY%%` | **Template:** `%%TEMPLATE%%` | **Date:** %%DATE%%

**Review Status:** `Preliminary`

---

## 1 — Automated Checks

| # | Check | Result |
|---|---|---|
%%CHECK_ROWS%%

```
%%CHECK_OUTPUT%%
```

---

## 2 — Symbol Properties

Fields from the template, values from the symbol under review.

| Field | Value | Approved |
|---|---|---|
%%PROPERTY_ROWS%%

---

## 3 — Symbol

| # | Check | Approved |
|---|---|---|
| 3.1 | Pin numbers & names match datasheet | Y/N/NA |
| 3.2 | Pin electrical types correct | Y/N/NA |
| 3.3 | Symbol graphical representation correct | Y/N/NA |

---

## 4 — Footprint

| # | Check | Approved |
|---|---|---|
| 4.1 | Pad size correct | Y/N/NA |
| 4.2 | Pad pitch correct | Y/N/NA |
| 4.3 | Pad numbering correct | Y/N/NA |
| 4.4 | Solder mask margin 0.05mm | Y/N/NA |
| 4.5 | Courtyard on 50µm grid | Y/N/NA |
| 4.6 | Fab layer body outline matches component dimensions | Y/N/NA |
| 4.7 | Fab layer `${REFERENCE}` text size proportional to body | Y/N/NA |
| 4.8 | No silkscreen reference designator | Y/N/NA |
| 4.9 | Footprint name matches IPC-7351 convention | Y/N/NA |
| 4.10 | If symmetric footprint, pin 1 mark correct | Y/N/NA |

---

## 5 — 3D Model

Bounding box (mm) extraction with f3d. Replace `".step"` with model path (including `" "`) and run command in terminal:

```
f3d ".step" --verbose=debug --output "$env:TEMP\f3d.png" | Select-String "bounding box"
```


| # | Check | Approved |
|---|---|---|
| 5.1 | STEP model aligns with footprint pads | Y/N/NA |
| 5.2 | Model height matches `H_max_um` | Y/N/NA |
| 5.3 | Model origin at footprint center | Y/N/NA |

---

## 6 — Notes

_(Reviewer notes, exceptions, issues found)_
