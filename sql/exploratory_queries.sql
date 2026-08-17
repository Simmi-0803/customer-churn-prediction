-- ============================================
-- CHURN PROJECT - SQL ANALYSIS
-- ============================================

-- Setup: create and select the database
CREATE DATABASE churn_project;
USE churn_project;
SELECT * FROM churn LIMIT 10;
-- ============================================
-- Query 1: Churn rate by Contract type
-- ============================================
-- Insight: Month-to-month customers churn at nearly 15x the rate of 
-- two-year contract customers (42.71% vs 2.85%). Contract length is 
-- one of the strongest predictors of churn.
SELECT 
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM churn
GROUP BY Contract;


-- ============================================
-- Query 2: Churn rate by tenure buckets
-- ============================================
-- Insight: Churn is highest among customers in their first 12 months 
-- (47.68%), dropping steadily to 28.71% (13-24 months), 20.39% (25-48 
-- months), and just 9.51% for long-tenured customers (49+ months). 
-- Nearly half of new customers churn within their first year, making 
-- early-tenure retention the single highest-impact area to focus on.

SELECT 
    CASE 
        WHEN tenure <= 12 THEN '0-12 months'
        WHEN tenure <= 24 THEN '13-24 months'
        WHEN tenure <= 48 THEN '25-48 months'
        ELSE '49+ months'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM churn
GROUP BY tenure_group
ORDER BY tenure_group;


-- ============================================
-- Query 3: Average MonthlyCharges — churned vs not
-- ============================================

-- Insights: Churned customers pay a higher average MonthlyCharges (₹74.44) 
-- than retained customers (₹61.31), suggesting price sensitivity plays a 
-- role in churn. However, churned customers have a LOWER avg_total_charges 
-- (₹1531.80 vs ₹2555.34) — this is explained by tenure: churned customers 
-- leave earlier, so despite paying more per month, they haven't been 
-- around long enough to accumulate high total charges. This confirms 
-- TotalCharges is really just a proxy for tenure, not an independent driver.

SELECT 
    Churn,
    COUNT(*) AS total_customers,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2) AS avg_total_charges
FROM churn
GROUP BY Churn;

-- ============================================
-- Query 4: Churn rate by InternetService type
-- ============================================

-- Insight: Fiber optic customers churn at 41.89% — over 2x the rate of DSL 
-- customers (19.00%) and nearly 6x the rate of customers with no internet 
-- service (7.43%). Despite fiber being the premium, higher-revenue product, 
-- it has the highest churn, pointing to possible service quality issues, 
-- pricing dissatisfaction, or strong competitive pressure specifically in 
-- the fiber segment — worth investigating with customer feedback data.

SELECT 
    InternetService,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM churn
GROUP BY InternetService;