# Data Quality Summary

## 1. Null Rates (Final Dataset)

| Column | Null % |
|--------|--------|
| console | 0.00% |
| genre | 0.00% |
| publisher | 0.00% |
| developer | 0.01% |
| critic_score | 0.00% |
| total_sales | 0.00% |
| na_sales | 29.11% |
| jp_sales | 63.15% |
| pal_sales | 32.94% |
| other_sales | 19.52% |
| log_sales | 0.00% |


## 2. Class Balance

### Console Distribution

| console   |   count |
|:----------|--------:|
| DS        |    2152 |
| PS2       |    2097 |
| PS3       |    1310 |
| WII       |    1281 |
| X360      |    1264 |
| PSP       |    1257 |
| PS        |    1126 |
| PC        |     939 |
| PS4       |     891 |
| XB        |     822 |
| GBA       |     820 |
| PSV       |     638 |
| 3DS       |     543 |
| GC        |     527 |
| XONE      |     517 |
| N64       |     279 |
| NS        |     247 |
| SNES      |     196 |
| SAT       |     175 |
| WIIU      |     139 |
| 2600      |     126 |
| DC        |      49 |
| NES       |      47 |
| GB        |      46 |
| GEN       |      27 |
| NG        |      12 |
| PSN       |       9 |
| WS        |       7 |
| SCD       |       5 |
| XBL       |       5 |
| 3DO       |       4 |
| VC        |       3 |
| GBC       |       3 |
| PCE       |       2 |
| WW        |       1 |
| GG        |       1 |
| OSX       |       1 |
| MOB       |       1 |
| PCFX      |       1 |

### Genre Distribution

| genre            |   count |
|:-----------------|--------:|
| ACTION           |    2686 |
| SPORTS           |    2484 |
| MISC             |    1834 |
| ADVENTURE        |    1683 |
| ROLE-PLAYING     |    1414 |
| SHOOTER          |    1377 |
| RACING           |    1349 |
| SIMULATION       |    1004 |
| PLATFORM         |     903 |
| FIGHTING         |     856 |
| STRATEGY         |     692 |
| PUZZLE           |     630 |
| ACTION-ADVENTURE |     257 |
| VISUAL NOVEL     |     197 |
| MUSIC            |     138 |
| MMO              |      30 |
| PARTY            |      28 |
| EDUCATION        |       4 |
| BOARD GAME       |       3 |
| SANDBOX          |       1 |

## 3. Outlier Treatment

- **total_sales:** Values <= 0 removed; no capping/winsorizing applied. Log transformation reduces impact of extreme values.
- **critic_score:** Missing values imputed with median; score range confirmed to be within 0–100.
- **Regional sales (na_sales, jp_sales, pal_sales, other_sales):** Retained as-is. Further outlier investigation may be performed during EDA.

## 4. Data Schema

```
<class 'pandas.core.frame.DataFrame'>
Index: 17570 entries, 0 to 17569
Data columns (total 11 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   console       17570 non-null  object 
 1   genre         17570 non-null  object 
 2   publisher     17570 non-null  object 
 3   developer     17568 non-null  object 
 4   critic_score  17570 non-null  float64
 5   total_sales   17570 non-null  float64
 6   na_sales      12455 non-null  float64
 7   jp_sales      6475 non-null   float64
 8   pal_sales     11782 non-null  float64
 9   other_sales   14141 non-null  float64
 10  log_sales     17570 non-null  float64
dtypes: float64(7), object(4)
memory usage: 1.6+ MB

```

**Data types per column:**

|              | 0       |
|:-------------|:--------|
| console      | object  |
| genre        | object  |
| publisher    | object  |
| developer    | object  |
| critic_score | float64 |
| total_sales  | float64 |
| na_sales     | float64 |
| jp_sales     | float64 |
| pal_sales    | float64 |
| other_sales  | float64 |
| log_sales    | float64 |

