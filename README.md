# Customer Churn Prediction

Predicting telecom customer churn using machine learning, with SQL-based analysis and a Power BI dashboard for business stakeholders.

## Problem

Customer churn directly impacts revenue, and acquiring a new customer typically costs more than retaining an existing one. This project identifies which customers are likely to churn and what drives that behaviour, so retention efforts can be targeted rather than broad.

## Dataset

IBM Telco Customer Churn — 7,043 customers, 21 features.
Target variable: `Churn` (26.5% churned, 73.5% retained).

`TotalCharges` was stored as text with blank-space entries for 11 new customers — invisible to `.isnull()` and silently coerced on conversion. Caught during type inspection and handled explicitly.

## Key Findings

| Finding | Evidence |
|---|---|
| Contract length is the strongest churn signal | Month-to-month customers churn at 42.71% vs 2.85% for two-year contracts — a 15x difference |
| Churn concentrates in the first year | 47.68% churn rate in months 0-12, dropping to 9.51% after 49 months |
| Fiber optic customers churn disproportionately | 41.89% vs 19.00% for DSL and 7.43% for no internet service |
| Higher monthly charges correlate with churn | Churned customers averaged $74.44/month vs $61.31 for retained |
| Support add-ons reduce churn | OnlineSecurity and TechSupport both showed strong negative coefficients |

Findings were validated two ways — visual EDA in Python and independent SQL aggregate queries — with consistent results.

## Modelling

Three models were compared on the churn class specifically, since overall accuracy is misleading on imbalanced data.

| Model | Precision | Recall | F1 | Accuracy |
|---|---|---|---|---|
| Logistic Regression (baseline) | 0.65 | 0.56 | 0.60 | 80% |
| **Logistic Regression (balanced)** | 0.50 | **0.79** | 0.62 | 74% |
| Random Forest (balanced) | 0.64 | 0.49 | 0.55 | 79% |

**Selected model:** balanced Logistic Regression. Despite lower headline accuracy, it catches 79% of actual churners versus 56% for the baseline. In a churn context, a missed churner costs a lost customer while a false alarm costs a retention offer — so recall is prioritised.

**Notable result:** Random Forest underperformed on recall despite being the more complex model. Its majority-voting mechanism dampens the effect of class weighting, pulling predictions back toward the majority class.

## Feature Importance

Strongest retention driver: two-year contracts (coefficient -1.42), nearly 3x the magnitude of the top churn driver.

Strongest churn drivers: fiber optic internet (+0.46) and electronic check payment (+0.41).

Electronic check as a churn signal did not surface during visual EDA — the model identified it independently.

## Dashboard

![Churn Dashboard](images/dashboard.png)

Customers are segmented into Low (<0.3), Medium (0.3–0.6), and High (>0.6) risk bands, with a ranked table of high-risk customers for retention teams to action. 488 customers are flagged High against 374 actual churners in the test set — the model over-flags by design, consistent with the recall-first threshold choice above.

## Project Structure

```
churn_prediction/
├── data/
│ ├── WA_Fn-UseC_-Telco-Customer-Churn.csv
│ └── churn_predictions.csv
├── images/
│ └── dashboard.png
├── notebooks/
│ ├── 1_eda.ipynb
│ └── 2_modeling.ipynb
├── sql/
│ └── exploratory_queries.sql
├── churn_dashboard.pbix
├── .gitignore
└── README.md
```

## Tools

Python (pandas, scikit-learn, seaborn, matplotlib) · MySQL · Power BI