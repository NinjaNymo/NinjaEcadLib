# JLC PCBA Cost Analysis

Empirical cost model for small-batch JLCPCB assembly derived in **October 2026**.

## Tl;Dr Findings:
* Economic PCBA has a **fixed cost of ~$10** + ~$0.0017 per joint + $3.10 per extended part.
* Standard PCBA has a **fixed cost of ~$35** + ~$0.0032 per joint + $1.55 loading fee for **all** parts.
* 4-Layer Economic PCBA is **not a cost up** as long as the PCB is kept **entirely standard** (green etc.).
* **Changing a 4-layer stackup** (such as adding black mask) **adds a fixed $25** engineering fee **if combined with PCBA**.
* 2-layers allow **some stackup modification** without forcing standard PCBA or adding other engineering fees.
* **Component attrition** (aka "wasted" components) is essentially 0 for basic and extended promotional parts as they do not have a MOQ. However, attrition increases on standard PCBA as almost all loaded parts will have some attrition. **Very design specific**.

## Design Notes:
* Economic PCBA requires 2~3 corner non-plated tooling holes; Ø1.152mm.
* Standard PCBA requires fiducals and 2 5mm side rails.

JLC will add either if missing.

## Cost Model:
**Disclaimer:** This is very approximate, JLC prices change rapidly, use at own risk.

```
ECONOMIC PCBA cost model:
N      = qty bare boards
Nas    = qty assembled boards
Nce    = qty unique extended parts
Np     = qty of pads/solder joints
A      = 1 = component attrition factor


PCB    ≈ $1 x N                           promotional prices

PCBA   ≈ $9.79                            setup $8.24 + stencil $1.55
       + $0.83 + $0.016 x Nas             nitrogen reflow
       + $0.15 + $0.0017 x Np x Nas       assembly
       + $3.09 x Nce                      extended loading fee
       + SUM(part price) x Nas x A        total component cost
```
```
STANDARD PCBA cost model:
N      = qty bare boards
Nas    = qty assembled boards
Nc     = qty unique parts (both basic and extended)
A      = 1 = component attrition factor

PCB    ≈ $1 x N                           promotional prices
PCBA   ≈ $34.02                           setup $25.75 + stencil $8.27
       + $1.55 x Nc                       loading fee
       + $0.0032 x Np x Nas               assembly
       + $0.51                            packaging
       + SUM(part price) x N x A          total component cost

Note:
A set to 1 for simplicity. However, the examples used showed an A ~ 1.25.
```

## Method:

A 100x50mm board was used in all examples. The baseline has ~15 BOM lines, ~20 total components, ~40 total pads aka. solder joints.

First, parameters such as BOM lines, PCB quantity, PCBA quantity was changed to to nail fixed costs vs scaled costs on economic PCBA with a 2-layer board.

Then, 4-layers was introduced, and the tests repeated.

Finally, soldermask changes were introduced to see effect on cost.

Raw data from the experiments can be found in [`jlc_pcba_cost_analysis_data.csv`](jlc_pcba_cost_analysis_data.csv).