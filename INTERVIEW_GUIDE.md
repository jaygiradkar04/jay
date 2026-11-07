# Interview Guide: Finance Concepts for Banking Analytics

Each topic has: **Intuition → Maths → Worked example → What interviewers ask → Pitfalls.**
Numbers match the notebook `Financial_Modeling_Toolkit.ipynb`, so you can say "I built this and got X".

---

## 1. Time Value of Money (TVM)

**Intuition.** A dollar today beats a dollar tomorrow: you can invest it, and inflation and risk erode the later one. Discounting converts future money to today's money.

**Maths**
- Future value: FV = PV(1 + r)^n
- Present value: PV = FV / (1 + r)^n
- Level annuity (payment C, n periods): PV = C · [1 − (1 + r)^−n] / r
- Perpetuity: PV = C / r. Growing perpetuity: PV = C₁ / (r − g), needs r > g.
- Effective annual rate: EAR = (1 + APR/m)^m − 1

**Example.** $10,000 at 5% for 10 years: 10,000 × 1.05^10 = **$16,288.95**.
$1,000/yr for 20 years at 7%: 1,000 × (1 − 1.07^−20)/0.07 = **$10,594.01**.
6% APR compounded monthly: (1.005)^12 − 1 = **6.17% EAR**.

**Interview Qs.** Why does a higher discount rate lower PV? Difference between APR and APY/EAR? Value a bond or a stock using these formulas (a bond is an annuity + a lump sum, a stock is a growing perpetuity).

**Pitfalls.** Mixing annual rates with monthly periods. Using r ≤ g in the growing perpetuity.

---

## 2. Loan Amortization

**Intuition.** Fixed payment each month. Interest is charged on the *remaining balance*, so early payments are mostly interest.

**Maths.** With monthly rate r = APR/12 and n months:

P = L · r / [1 − (1 + r)^−n]

Each month: interest_t = r × balance_(t−1); principal_t = P − interest_t; balance_t = balance_(t−1) − principal_t.

**Example.** L = $400,000, 6.5%, 30 years: r = 0.005417, n = 360 → **P = $2,528.27**.
Month 1: interest = 400,000 × 0.005417 = $2,166.67, principal = **$361.60** (only 14% of the payment).
Total interest over life = $510,178 (more than the loan). Adding $300/month cuts the term by 7.6 years and saves ~$149,581.

**Why a bank cares.** Prepayment shortens asset life and reduces expected interest income (prepayment risk). Mortgage-backed securities are priced on prepayment assumptions.

**Interview Qs.** Why is early payment mostly interest? How does prepayment affect a bank's duration? Fixed vs variable rate: who bears interest-rate risk? (Fixed: the bank, unless hedged.)

---

## 3. Capital Budgeting: NPV, IRR, Payback

**Intuition.** Do the project's discounted cash flows exceed its cost?

**Maths**
- NPV = Σ CFₜ / (1 + r)^t (t = 0 is the initial outlay, negative). **Accept if NPV > 0.**
- IRR: the r that makes NPV = 0. Accept if IRR > hurdle rate (usually the WACC).
- Payback: time until cumulative cash flow turns positive (ignores time value and later cash flows).
- Profitability index: PV of inflows / initial cost.

**Example.** Cash flows −1,000, 400, 500, 600 at 10%:
NPV = −1,000 + 363.64 + 413.22 + 450.79 = **$227.65**; IRR = **21.65%**.

**Interview Qs.**
- *Why prefer NPV over IRR?* NPV is in dollars of value created and assumes reinvestment at the cost of capital. IRR assumes reinvestment at the IRR itself, can give multiple answers when cash flows change sign more than once, and can rank mutually exclusive projects of different size wrongly.
- *What if projects have unequal lives?* Equivalent annual annuity.
- *What does a positive NPV mean?* Value added to shareholders today.

---

## 4. Bonds, Duration and Convexity

**Intuition.** A bond is a stream of coupons plus principal. When market yields rise, existing bonds are worth less. Banks hold large bond books, so this is their core interest-rate risk.

**Maths**
- Price = Σ C/(1 + y/m)^(mt) + F/(1 + y/m)^(mT)
- YTM: the y that equates price to the cash flows (solved numerically).
- Macaulay duration D = Σ t · PV(CFₜ) / Price (the weighted-average time to receive cash, in years)
- Modified duration D_mod = D / (1 + y/m)
- Price change ≈ −D_mod · Δy + ½ · Convexity · (Δy)²

**Example.** 10-year, 5% coupon, semi-annual, yield 5% (so price = 1,000): D = 7.99 years, D_mod = 7.80, convexity = 73.6.
A +100bp rise: −7.80% + ½(73.6)(0.01)² = −7.80% + 0.37% = **−7.43%** (exact: −7.44%).
A −100bp fall: +7.80% + 0.37% = +8.17% (exact: +8.18%). Convexity helps you in both directions: prices rise more than they fall.

**Key relationships.** Price and yield move inversely. Longer maturity and lower coupon mean higher duration. Zero-coupon bond duration = maturity.

**Interview Qs.** Why are long bonds riskier? What is DV01 (dollar change per 1bp = price × D_mod × 0.0001)? How would a bank hedge duration mismatch (swaps, matching asset and liability durations)? What is the difference between duration gap and repricing gap?

---

## 5. Risk, Return and CAPM

**Maths**
- Return: R = (P₁ − P₀ + D) / P₀. Annualised from daily: μ × 252; σ × √252.
- Variance σ² = E[(R − μ)²]. Covariance and correlation ρ = Cov(A,B) / (σ_A σ_B).
- **Beta** β = Cov(R_i, R_m) / Var(R_m): the slope from regressing the stock's returns on the market's.
- **CAPM:** E[R_i] = r_f + β (E[R_m] − r_f). The bracket is the market risk premium (MRP).
- **Sharpe ratio** = (R_p − r_f) / σ_p. **Treynor** = (R_p − r_f) / β. **Jensen's alpha** = actual return − CAPM return.

**Example.** r_f = 4%, β = 1.2, MRP = 5.5%: E[R] = 4% + 1.2 × 5.5% = **10.6%**. That is the cost of equity used in WACC.

**Systematic vs idiosyncratic.** Total variance = β²σ_m² + σ²_idio. Diversification removes idiosyncratic risk, so only β is rewarded. R² of the regression = share of risk that is systematic.

**Interview Qs.** What does β = 0 mean? Can beta be negative (yes, e.g. gold sometimes)? CAPM assumptions and weaknesses (single factor, one period, rational investors, unobservable market portfolio; Fama-French adds size and value factors). What is the difference between Sharpe and Treynor? (Total risk vs systematic risk.)

---

## 6. Portfolio Theory (Markowitz)

**Intuition.** Assets that don't move together reduce portfolio risk without reducing expected return: the one "free lunch".

**Maths**
- Two assets: σ_p² = w₁²σ₁² + w₂²σ₂² + 2w₁w₂ρσ₁σ₂
- N assets: σ_p² = wᵀΣw, and μ_p = wᵀμ
- Optimisation: minimise wᵀΣw subject to wᵀμ = target and Σw = 1 (add w ≥ 0 for long-only). Plotting the solutions for each target gives the **efficient frontier**.
- **Tangency portfolio** maximises (μ_p − r_f)/σ_p. Combining it with the risk-free asset gives the Capital Market Line.

**Example.** 50/50 mix of A (σ=20%) and B (σ=30%), ρ = 0.3:
σ_p² = 0.25(0.04) + 0.25(0.09) + 2(0.25)(0.3)(0.2)(0.3) = 0.01 + 0.0225 + 0.009 = 0.0415 → **σ_p = 20.4%**, less than the 25% average of the two. At ρ = 1 there would be no benefit; at ρ = −1 you could remove all risk.

**Interview Qs.** Why do optimisers give extreme weights (they exploit estimation error in μ; fix with constraints, shrinkage, Black-Litterman)? Systematic vs diversifiable risk? What does the frontier look like when you add a risk-free asset?

---

## 7. Value at Risk (VaR) and Expected Shortfall (ES)

**Definition.** VaR at 99%, 1 day = the loss that will be exceeded only 1% of days. ES = the average loss *given* the loss exceeds VaR.

**Maths**
- Parametric (normal): VaR = V · (z_α σ − μ), z₉₉ = 2.326, z₉₅ = 1.645.
- Normal ES = V · (σ φ(z)/(1 − α) − μ), where φ is the normal density.
- Time scaling: VaR_T = VaR_1 · √T (assumes independent returns).
- Historical: take the (1 − α) percentile of past P&L. Monte Carlo: simulate a model.
- Backtesting: count exceptions; at 99% expect ~1% (about 2.5 days a year). Basel's traffic-light test punishes banks with more.

**Example.** $10M portfolio, daily σ = 1.5%: 1-day VaR(99%) = 10M × 2.326 × 0.015 = **$348,945**; 10-day = ×√10 = **$1.10M**.

**Method comparison.**
| Method | Pros | Cons |
|---|---|---|
| Parametric | Fast, closed-form | Assumes normality, understates fat tails |
| Historical | No distribution assumption | Only as good as the window; ghost effects |
| Monte Carlo | Handles options, non-linear risk | Model dependent, slow |

**Why ES replaced VaR in Basel FRTB.** VaR says nothing about how bad losses are *beyond* the threshold, and it isn't sub-additive (diversification can appear to increase VaR). ES is a coherent risk measure.

**Interview Qs.** Explain VaR to a non-technical manager. Limitations of VaR? Why ES? How do you backtest it? Difference between VaR and stress testing (stress = specific extreme scenario).

---

## 8. Credit Risk: PD, LGD, EAD, Expected Loss

**Maths**
- **Expected Loss = PD × LGD × EAD**
- PD: probability of default over a horizon (12 months for IFRS 9 Stage 1, lifetime for Stage 2/3).
- LGD = 1 − recovery rate. EAD = drawn balance + CCF × undrawn commitment.
- **Logistic regression** for PD: ln(p/(1−p)) = β₀ + β₁x₁ + … → p = 1/(1 + e^−(β₀+βx)). A coefficient is the change in log-odds per unit of x; e^β is the odds multiplier.
- **Unexpected loss** is the volatility of losses around EL. Capital covers UL; provisions cover EL. Basel IRB formulas compute capital from PD, LGD, EAD and a correlation factor.

**Example.** PD 2%, LGD 40%, EAD $100,000 → **EL = $800** (0.8% of the exposure).
Risk-based pricing (notebook): minimum rate = funding cost 3.5% + opex 1.0% + PD × LGD + target margin 1.0%. For a 2% PD loan: 3.5 + 1.0 + 0.8 + 1.0 = **6.3%**; for a 19.8% PD loan, **13.4%**.

**Model evaluation.**
- **AUC/ROC**: probability the model ranks a random defaulter above a random non-defaulter (0.5 = random, 1 = perfect). **Gini = 2·AUC − 1.** Mine: AUC 0.83.
- **KS statistic**: max gap between the cumulative distributions of defaulters and non-defaulters (0.51 in the notebook).
- **Calibration**: predicted PD ≈ actual default rate by decile. Discrimination (ranking) and calibration are different; you need both.
- Other metrics: Population Stability Index (PSI) for drift, Weight of Evidence/Information Value for scorecard variables.

**Accounting: IFRS 9 / CECL.**
- IFRS 9 stages: **Stage 1** performing (12-month ECL), **Stage 2** significant increase in credit risk (lifetime ECL), **Stage 3** credit-impaired (lifetime ECL, interest on net balance).
- CECL (US GAAP) requires lifetime expected losses from day one.
- ECL is forward looking: weight macro scenarios (base, downside, upside).

**Interview Qs.** Walk through building a PD model (data, target definition, variable selection, train/test split, validation, monitoring). Why can't you just use accuracy for imbalanced defaults (6.9% default rate: predicting "no default" gives 93% accuracy)? How do you handle class imbalance (class weights, resampling, use AUC/precision-recall)? Difference between EL and UL? Through-the-cycle vs point-in-time PD? What is a "default" (Basel: 90 days past due or unlikely to pay)?

---

## 9. Cost of Capital and DCF Valuation

**Maths**
- Cost of equity (CAPM): r_e = r_f + β · MRP
- After-tax cost of debt: r_d (1 − t) (interest is tax deductible)
- **WACC** = E/V · r_e + D/V · r_d (1 − t)
- **FCFF** = EBIT (1 − t) + D&A − CapEx − ΔNWC
- **Enterprise value** = Σ FCFFₜ/(1 + WACC)^t + TV/(1 + WACC)^N
- **Terminal value (Gordon)** = FCFF_N (1 + g) / (WACC − g)
- Equity value = EV − debt + cash; per-share value = equity value / shares.
- Alternative terminal value: exit multiple, TV = EBITDA_N × multiple.

**Example (notebook, hypothetical company).** r_e = 10.6%; E = 3,600, D = 600; r_d = 6%, tax 25%:
WACC = 0.857 × 10.6% + 0.143 × 4.5% = **9.73%**.
Year-5 FCFF = 356.1 → TV = 356.1 × 1.025 / (0.0973 − 0.025) = **5,048**; PV(TV) = 5,048/1.0973⁵ = **3,173**, which is **73% of EV (4,338)**. Equity = 4,338 − 600 + 150 = 3,888 → **$38.88/share** vs market $36.

**Sensitivity.** Moving WACC from 9.7% to 8.7% lifts value/share from $38.9 to $46.0 (+18%). A 1pp change in discount rate is worth more than most operating assumptions, which is why you show a grid.

**Interview Qs.**
- *Walk me through a DCF in 2 minutes.* Forecast FCFF, discount at WACC, add terminal value, subtract net debt, divide by shares.
- *Why use FCFF at WACC rather than FCFE at cost of equity?* Both are valid if consistent; FCFF/WACC is unaffected by capital structure changes in the forecast.
- *How does debt affect WACC?* Cheaper after-tax debt lowers WACC at first, but raises r_e (higher beta from leverage) and distress costs; the optimal structure balances these.
- *Unlever / relever beta:* β_U = β_L / [1 + (1 − t) D/E].
- *Why is DCF dangerous?* Terminal value dominates; small input changes swing the answer; garbage-in garbage-out.
- *Sanity checks:* g below long-run GDP growth, implied exit multiple reasonable, TV share under ~75%, WACC > g.
- **Banks are different:** you don't value a bank with FCFF because debt is raw material, not financing. Use a **dividend discount / residual income** model: Value = book equity × (P/B justified by (ROE − g)/(r_e − g)).

---

## 10. Monte Carlo Simulation

**Intuition.** Replace single-point assumptions with distributions, run the model thousands of times, and read off probabilities.

**Method.** (1) Pick uncertain inputs and distributions. (2) Draw N samples. (3) Run the model per draw. (4) Summarise: mean, percentiles, probability of exceeding a target. Standard error of the mean shrinks as σ/√N.

**Example (notebook).** 10,000 draws on growth, margin, beta and terminal growth give a median of **$38.8/share**, a 5th–95th percentile range of **$26–$56**, and a **62.9% probability** that value exceeds the $36 market price.

**Pitfalls.** Inputs are often correlated (don't sample independently when they aren't); distribution choices drive the answer; results look more precise than they are.

---

## 11. Bank-Specific Concepts (very likely in your interviews)

| Concept | Definition / formula |
|---|---|
| Net Interest Margin | (Interest income − interest expense) / average earning assets |
| Net Interest Income sensitivity | ΔNII for ±100bp parallel shifts; main IRRBB metric |
| ROE and DuPont | ROE = (NI/Rev) × (Rev/Assets) × (Assets/Equity) = margin × turnover × leverage |
| Efficiency ratio | Non-interest expense / revenue (lower is better) |
| CET1 ratio | Common equity tier 1 / risk-weighted assets (Basel minimum 4.5% plus buffers, ~7% or more) |
| Leverage ratio | Tier 1 capital / total exposure (minimum 3%) |
| LCR | High-quality liquid assets / net cash outflows over 30 days stressed ≥ 100% |
| NSFR | Available stable funding / required stable funding ≥ 100% |
| Funds transfer pricing (FTP) | Internal rate charged to business lines for funding, so each product shows true margin |
| Loan-to-deposit ratio | Loans / deposits; funding and liquidity indicator |
| Provision coverage | Allowance for credit losses / non-performing loans |
| Basel pillars | 1: minimum capital (credit, market, operational risk); 2: supervisory review (ICAAP); 3: disclosure |

**Example (DuPont).** Net income/revenue 25%, revenue/assets 4%, assets/equity 11x → ROE = 0.25 × 0.04 × 11 = **11%**. High leverage drives bank ROE, which is why regulators set capital floors.

**Interest-rate risk in the banking book (IRRBB).** Banks borrow short (deposits) and lend long, so they have a duration gap. Rising rates reduce the economic value of equity (EVE) when asset duration exceeds liability duration. Measure with repricing gap, duration gap and NII/EVE simulation.

**Three lines of defence.** Business owns risk, risk management and compliance oversee, internal audit provides independent assurance. **Model risk (SR 11-7):** development, independent validation, and ongoing monitoring of every model such as your PD scorecard.

---

## 12. Quick-fire Interview Answers

1. **"What is the single most important idea in finance?"** Value = PV of future cash flows, adjusted for risk.
2. **"Stock vs bond valuation?"** Bond: contractual cash flows, discount at yield. Stock: uncertain cash flows, discount at cost of equity.
3. **"Rates go up. What happens to a bank?"** Asset values fall (bond book), NII usually rises if asset-sensitive, deposit costs rise, prepayments slow, credit risk increases.
4. **"How would you explain your project to a non-technical person?"** "I built Python models that answer how much a loan costs, how risky a portfolio is, what a company is worth, and how much to set aside for loans that go bad."
5. **"What would you do differently with real data?"** Out-of-time validation, monitoring for drift, macro-linked PDs, documentation for model risk.
6. **"Biggest weakness of your DCF?"** Terminal value is ~73% of EV and highly sensitive to WACC and g, hence the sensitivity grid and Monte Carlo.
7. **"Why is correlation important?"** It determines how much diversification you get, and it spikes in a crisis, which is why VaR can fail when you most need it.

---

## Study plan (2 weeks)
- **Days 1–3:** Sections 1–4 (TVM, loans, NPV, bonds). Re-derive each formula by hand once.
- **Days 4–6:** Sections 5–7 (CAPM, portfolio, VaR). Re-run notebook modules and change parameters to see effects.
- **Days 7–9:** Section 8 (credit risk) and Section 11 (bank concepts): your differentiator given your bank job.
- **Days 10–12:** Section 9–10 (WACC, DCF, Monte Carlo). Practise a 2-minute DCF walk-through aloud.
- **Days 13–14:** Mock interviews with Section 12, plus explain each notebook module in 60 seconds.
