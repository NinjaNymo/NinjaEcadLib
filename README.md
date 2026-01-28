# NinjaEcadLib
A repository for ECAD component libraries

## Component Colors

| Preview                                                           | Hex Code  | Name                  | Use                               | Source                        |
| :---                                                              | :---      | :---                  | :---                              | :---                          |
| ![](https://img.shields.io/badge/%20-DEDEDE?style=for-the-badge)  | `DEDEDE`  | **Substrate White**   | Resistor substrate, Pin 1 Mark    | Altium (increased luminance)  |
| ![](https://img.shields.io/badge/%20-CCCCCC?style=for-the-badge)  | `CCCCCC`  | **Terminal Grey**     | Leads, terminals                  | Altium                        |
| ![](https://img.shields.io/badge/%20-333333?style=for-the-badge)  | `333333`  | **Casing Black**      | Molded packages, INDC, RESC       | Altium                        |
| ![](https://img.shields.io/badge/%20-4D4D4D?style=for-the-badge)  | `4D4D4D`  | **Plastic Black**     | Connectors                        | Custom                        |
| ![](https://img.shields.io/badge/%20-614537?style=for-the-badge)  | `614537`  | **Capacitor Brown**   | CAPC                              | KiCad                         |
| ![](https://img.shields.io/badge/%20-F5D578?style=for-the-badge)  | `F5D578`  | **Plating Gold**      | Gold plated leads                 | Custom                        |

### Changing STEP Model Colors
The following example shows how two color _entities_ with ID `#316` and `#317` are defined using the `COLOUR_RGB` keyword with _normalized_ RGB values (aka. _"RBG 0-1"_ or _"Unit RGB"_):

```
#316=COLOUR_RGB('',0.2,0.2,0.2);
#317=COLOUR_RGB('',0.8,0.8,0.8);
```

Other entities in the STEP file will then reference those color entity IDs:

```
#313=FILL_AREA_STYLE_COLOUR('',#316);
#314=FILL_AREA_STYLE_COLOUR('',#317);
```

Thus, to manually change colors, modify the RGB values in the `COLOUR_RGB` keyword.

_* While the STEP format only requires colors to be defined once, some STEP model generators will define the same color multiple times. Thus, even if a model only has one color, multiple `COLOUR_RGB` keywords may exist and will have to be changed to re-color the entire model._

## Chip Component Dimensions
```
├───────────────L───────────────┤
┌───────┬───────────────┬───────┐   ┬
│       │               │       │   │
│       │               │       │   │
│       │               │       │   W
│       │               │       │   │
│       │               │       │   │
└───────┴───────────────┴───────┘   ┴
├──TL───┤
```

|   Imperial    |   Metric  |   L [mm]  |   W [mm]  |   TL [mm] |
|   :---        |   :---    |   :---    |   :---    |   :---    |
|   0201        |   0603    |   0.60    |   0.30    |   0.15    |
|   0402        |   1005    |   1.00    |   0.50    |   0.20    |
|   0603        |   1608    |   1.60    |   0.80    |   0.30    |
|   0805        |   2012    |   2.00    |   1.20    |   0.40    |
|   0806        |   2016    |   2.00    |   1.60    |   0.40    |
|   1008        |   2520    |   2.50    |   2.00    |   0.40    |
|   1206        |   3216    |   3.20    |   1.60    |   0.40    |
|   1210        |   3225    |   3.20    |   2.50    |   0.40    |




