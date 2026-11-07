---
title: "Finance Concepts for Banking Analytics: Interview Guide"
subtitle: "Formulas, worked examples and real-world uses"
---

**How to use this guide.** Every topic follows the same layout: **Idea → Formula → Worked example → Real-world use → Interview questions.** The numbers match the notebook `Financial_Modeling_Toolkit.ipynb`, so you can say "I built this and got X."

# 1. Time Value of Money

**Idea.** A dollar today is worth more than a dollar tomorrow, because today's dollar can earn interest and tomorrow's is exposed to inflation and risk. Discounting converts future money into today's money.

**Formulas**

Future value and present value:

$$FV = PV\,(1+r)^{n} \qquad\qquad PV = \frac{FV}{(1+r)^{n}}$$

Annuity (equal payment $C$ each period for $n$ periods):

$$PV = C\cdot\frac{1-(1+r)^{-n}}{r}$$

Perpetuity and growing perpetuity (requires $r>g$):

$$PV = \frac{C}{r} \qquad\qquad PV = \frac{C_1}{r-g}$$

Effective annual rate from a quoted rate (APR) compounded $m$ times a year:

$$EAR = \left(1+\frac{APR}{m}\right)^{m}-1$$

**Worked example**

| Question | Calculation | Answer |
|---|---|---|
| $10,000 at 5% for 10 years | $10\text{,}000 \times 1.05^{10}$ | **\$16,288.95** |
| $1,000/yr for 20 years at 7% | $1\text{,}000\times\frac{1-1.07^{-20}}{0.07}$ | **\$10,594.01** |
| 6% APR compounded monthly | $(1.005)^{12}-1$ | **6.17% EAR** |

**Real-world use**

- **Savings and loan products.** A bank advertises "6% compounded monthly." The customer really earns 6.17%. Regulators require banks to show APR and APY so customers can compare products honestly.
- **Pricing a bond or a pension.** A bond's price is the PV of its coupons (an annuity) plus its face value. A pension fund discounts promised future payouts to see whether it has enough assets today.
- **Stock valuation.** The dividend discount model treats a stock as a growing perpetuity: price $=D_1/(r-g)$.

**Interview questions.** Why does a higher discount rate lower PV? What is the difference between APR and APY? How is a bond an annuity plus a lump sum?

# 2. Loan Amortization

**Idea.** A fixed-payment loan charges interest on the *remaining balance*, so early payments are mostly interest and later ones mostly principal.

**Formulas**

Level monthly payment on loan $L$, with monthly rate $r=APR/12$ and $n$ months:

$$P = L\cdot\frac{r}{1-(1+r)^{-n}}$$

Month-by-month split:

$$\text{interest}_t = r\cdot B_{t-1} \qquad \text{principal}_t = P-\text{interest}_t \qquad B_t = B_{t-1}-\text{principal}_t$$

**Worked example.** Loan $L=\$400\text{,}000$, 6.5% APR, 30 years ($r=0.005417$, $n=360$):

$$P = 400\text{,}000\cdot\frac{0.005417}{1-(1.005417)^{-360}} = \$2\text{,}528.27$$

Month 1: interest $=400\text{,}000\times0.005417=\$2\text{,}166.67$, so principal is only **\$361.60**, about 14% of the payment. Total interest over 30 years is **\$510,178**, more than the loan. An extra \$300/month shortens the loan by **7.6 years** and saves about **\$149,581**.

**Real-world use**

- **Mortgage and auto-loan desks** generate customer schedules with exactly this formula.
- **Prepayment risk.** When rates fall, borrowers refinance and repay early. The bank loses expected interest income and must reinvest at lower rates. Mortgage-backed securities are priced on prepayment assumptions for this reason.
- **Customer advice.** Showing a customer that a small extra payment saves six figures is a common retention and financial-wellness message.

**Interview questions.** Why is early payment mostly interest? Fixed versus variable rate: who bears the interest-rate risk? (With fixed rates, the bank does, unless it hedges.) How does prepayment change an asset's duration?

# 3. Capital Budgeting: NPV, IRR, Payback

**Idea.** Does a project's stream of discounted cash flows exceed what it costs? Banks decide on branches, technology and acquisitions this way.

**Formulas**

$$NPV = \sum_{t=0}^{T}\frac{CF_t}{(1+r)^{t}}$$

IRR is the rate that makes NPV zero:

$$0 = \sum_{t=0}^{T}\frac{CF_t}{(1+IRR)^{t}}$$

$$\text{Profitability index} = \frac{PV(\text{inflows})}{\text{initial cost}}$$

Decision rule: accept if $NPV>0$, or equivalently if $IRR>$ the hurdle rate (usually WACC).

**Worked example.** Cash flows $-1000,\;400,\;500,\;600$ at $r=10\%$:

$$NPV=-1000+\frac{400}{1.1}+\frac{500}{1.1^{2}}+\frac{600}{1.1^{3}} = -1000+363.64+413.22+450.79=\$227.65$$

Solving for the zero gives **IRR = 21.65%**, well above the 10% hurdle, so accept.

**Real-world use**

- **Technology investment.** A bank compares a \$2.0M digital-banking platform (cash flows rising to \$1.0M a year) with a \$1.5M branch expansion. At a 9% WACC, the platform has NPV \$1.0M versus \$0.4M for the branch (see the notebook), so it adds more value.
- **Corporate lending.** Credit analysts compute NPV and IRR of a borrower's project to judge whether it can service the loan.

**Interview questions.** Why prefer NPV over IRR? (NPV measures dollars of value created; IRR can give multiple answers when cash flows change sign more than once, and can mis-rank projects of different size.) How do you compare projects with unequal lives? (Equivalent annual annuity.)

# 4. Bonds, Duration and Convexity

**Idea.** A bond pays coupons then principal. When market yields rise, existing bonds lose value. Banks hold large bond portfolios, so this is a core interest-rate risk.

**Formulas**

Price at yield $y$, with $m$ payments a year and $T$ years:

$$P=\sum_{k=1}^{mT}\frac{C/m}{(1+y/m)^{k}}+\frac{F}{(1+y/m)^{mT}}$$

Macaulay duration (PV-weighted average time to receive the cash, in years), and modified duration:

$$D_{Mac}=\frac{1}{P}\sum_{t}t\cdot\frac{CF_t}{(1+y/m)^{mt}}\qquad\qquad D_{mod}=\frac{D_{Mac}}{1+y/m}$$

Price change for a yield change $\Delta y$:

$$\frac{\Delta P}{P}\;\approx\;-D_{mod}\,\Delta y\;+\;\tfrac12\,\text{Convexity}\,(\Delta y)^{2}$$

DV01 (dollar change per one basis point): $DV01 = P\cdot D_{mod}\cdot 0.0001$.

**Worked example.** 10-year, 5% coupon, semi-annual, yield 5%: price \$1,000, $D_{Mac}=7.99$ years, $D_{mod}=7.80$, convexity $=73.6$.

$$\Delta y=+1\%:\quad -7.80\%+\tfrac12(73.6)(0.01)^2=-7.43\%\quad(\text{exact}: -7.44\%)$$

$$\Delta y=-1\%:\quad +7.80\%+0.37\%=+8.17\%\quad(\text{exact}: +8.18\%)$$

Convexity helps in both directions: prices rise more than they fall.

**Real-world use**

- **Treasury and ALM.** A bank with \$5B of bonds at $D_{mod}=5$ loses about \$250M if yields jump 100bp. The ALM committee limits this with hedges (interest-rate swaps) or by shortening the portfolio.
- **2022–2023 bank failures.** Silicon Valley Bank held long-duration bonds funded by short-term deposits. Rates rose, bond values fell, deposits fled, and losses were realised. This is the standard case study for duration risk.
- **Trading desks** quote risk in DV01, not in price.

**Interview questions.** Why are long, low-coupon bonds riskier? What is the duration of a zero-coupon bond? (Its maturity.) How would you hedge a duration mismatch? What happened at SVB?

# 5. Risk, Return and CAPM

**Idea.** Investors are paid only for risk they cannot diversify away (market risk). Beta measures how much a stock moves with the market.

**Formulas**

$$\beta_i=\frac{\mathrm{Cov}(R_i,R_m)}{\mathrm{Var}(R_m)} \qquad\qquad E[R_i]=r_f+\beta_i\,\big(E[R_m]-r_f\big)$$

$$\text{Sharpe}=\frac{R_p-r_f}{\sigma_p}\qquad \text{Treynor}=\frac{R_p-r_f}{\beta_p}\qquad \alpha_{Jensen}=R_p-\big[r_f+\beta_p(R_m-r_f)\big]$$

Risk splits into two parts, and only the first is rewarded:

$$\sigma_i^{2}=\underbrace{\beta_i^{2}\sigma_m^{2}}_{\text{systematic}}+\underbrace{\sigma_{\varepsilon}^{2}}_{\text{idiosyncratic}}$$

Annualising daily data: return $\times252$, volatility $\times\sqrt{252}$.

**Worked example.** $r_f=4\%$, $\beta=1.2$, market risk premium $=5.5\%$:

$$E[R]=4\%+1.2\times5.5\%=10.6\%$$

This 10.6% is the **cost of equity** used in the WACC (section 9).

**Real-world use**

- **Cost of equity** for valuation, M&A and regulatory rate cases.
- **Fund evaluation.** A fund returning 12% with beta 1.5 when CAPM predicts 11% has alpha of +1%. A manager returning 12% with beta 0.5 has alpha of about +7%.
- **Risk reports.** Banks report the beta of their equity book to understand how much of the portfolio simply rides the market.

**Interview questions.** What does $\beta=0$ mean? Can beta be negative? What are CAPM's weaknesses? (Single factor, one period, unobservable market; Fama-French adds size and value.) Sharpe versus Treynor? (Total risk versus market risk.)

# 6. Portfolio Theory (Markowitz)

**Idea.** Assets that do not move together reduce portfolio risk without reducing expected return. This is the "free lunch" of diversification.

**Formulas**

Two assets with weights $w_1, w_2$ and correlation $\rho$:

$$\sigma_p^{2}=w_1^{2}\sigma_1^{2}+w_2^{2}\sigma_2^{2}+2\,w_1w_2\,\rho\,\sigma_1\sigma_2$$

$N$ assets (vector of weights $w$, covariance matrix $\Sigma$, expected returns $\mu$):

$$\mu_p=w^{\top}\mu \qquad\qquad \sigma_p^{2}=w^{\top}\Sigma\,w$$

Efficient frontier (for each target return, find the lowest-risk portfolio), and the tangency portfolio:

$$\min_{w}\; w^{\top}\Sigma w\quad\text{s.t.}\quad w^{\top}\mu=\mu_{target},\;\; \sum w_i=1 \qquad\qquad \max_{w}\;\frac{w^{\top}\mu-r_f}{\sqrt{w^{\top}\Sigma w}}$$

**Worked example.** A 50/50 mix of A ($\sigma=20\%$) and B ($\sigma=30\%$) with $\rho=0.3$:

$$\sigma_p^{2}=0.25(0.04)+0.25(0.09)+2(0.25)(0.3)(0.2)(0.3)=0.0415\;\Rightarrow\;\sigma_p=20.4\%$$

That is lower than the 25% simple average. With $\rho=1$ there is no benefit; with $\rho=-1$ risk can be eliminated.

**Real-world use**

- **Wealth management.** Advisors build a client portfolio on the efficient frontier for the client's risk tolerance: conservative clients get more bonds, aggressive clients more equity.
- **Bank loan books.** A bank lending to many industries is diversified. One concentrated in oil and gas is not: a price crash hits all borrowers together (high default correlation). Concentration limits come from this idea.
- **Robo-advisors** automate this optimisation.

**Interview questions.** Why do optimisers give extreme weights? (They exploit noise in estimated returns; fixes are constraints, shrinkage, Black-Litterman.) How does correlation behave in a crisis? (It rises, so diversification fails when needed most.)

# 7. Value at Risk (VaR) and Expected Shortfall (ES)

**Idea.** VaR answers: "What is the most I lose on 99% of days?" ES answers: "When I do have a bad day, how bad is it on average?"

**Formulas**

Parametric (normal) VaR for portfolio value $V$, mean $\mu$, volatility $\sigma$ per day, and confidence $\alpha$:

$$VaR_{\alpha}=V\,\big(z_{\alpha}\,\sigma-\mu\big),\qquad z_{0.95}=1.645,\; z_{0.99}=2.326$$

Expected shortfall (normal case) and time scaling:

$$ES_{\alpha}=V\left(\sigma\,\frac{\varphi(z_{\alpha})}{1-\alpha}-\mu\right)\qquad\qquad VaR_{T\text{ days}}=VaR_{1\text{ day}}\cdot\sqrt{T}$$

Historical VaR is simply the $(1-\alpha)$ percentile of past profit and loss. Monte Carlo VaR takes that percentile from simulated outcomes.

**Worked example.** A \$10M portfolio with daily volatility 1.5%:

$$VaR_{99\%,1\text{d}}=10\text{M}\times2.326\times0.015=\$348\text{,}945 \qquad VaR_{99\%,10\text{d}}=348\text{,}945\times\sqrt{10}=\$1.10\text{M}$$

Backtest: at 99% you expect losses to exceed VaR on about 1% of days (roughly 2 to 3 days a year).

**Real-world use**

- **Daily risk limits.** A trading desk is told "99% 1-day VaR must stay under \$5M." The risk team reports it every morning.
- **Regulatory capital.** Basel rules link market-risk capital to VaR (now ES), and a bank with too many backtest exceptions has to hold more capital (the "traffic-light" test).
- **Why ES.** VaR ignores how large losses are beyond the threshold, and it can penalise diversification. ES is the Basel FRTB standard.

| Method | Strength | Weakness |
|---|---|---|
| Parametric | Fast, closed form | Assumes normal returns, understates fat tails |
| Historical | No distribution assumption | Depends on the chosen window |
| Monte Carlo | Handles options and non-linear risk | Model-dependent, slower |

**Interview questions.** Explain VaR to a non-technical manager. What are its limits? How do you backtest it? How does VaR differ from stress testing? (Stress testing applies a specific extreme scenario.)

# 8. Credit Risk: PD, LGD, EAD and Expected Loss

**Idea.** The core of lending. A bank expects some borrowers to default, and must price loans and set aside money for that.

**Formulas**

$$EL = PD\times LGD\times EAD$$

where PD is the probability of default, $LGD=1-\text{recovery rate}$, and $EAD=\text{drawn balance}+CCF\times\text{undrawn limit}$.

Logistic regression model for PD (log-odds are linear in the borrower features):

$$\ln\frac{p}{1-p}=\beta_0+\beta_1x_1+\dots+\beta_kx_k \qquad\Longleftrightarrow\qquad p=\frac{1}{1+e^{-(\beta_0+\beta^{\top}x)}}$$

A coefficient $\beta_j$ is the change in log-odds per unit of $x_j$; $e^{\beta_j}$ is the odds multiplier.

Model quality:

$$\text{Gini}=2\,AUC-1\qquad\qquad KS=\max_{s}\,\big|F_{bad}(s)-F_{good}(s)\big|$$

Loans are priced so the rate covers funding, operating cost, expected loss and profit:

$$\text{min. rate}=\text{funding}+\text{opex}+PD\times LGD+\text{target margin}$$

**Worked example.** $PD=2\%$, $LGD=40\%$, $EAD=\$100\text{,}000$:

$$EL=0.02\times0.40\times100\text{,}000=\$800\quad(0.8\%\text{ of the loan})$$

Pricing (funding 3.5%, opex 1.0%, margin 1.0%): a 2% PD loan needs $3.5+1.0+0.8+1.0=6.3\%$. A 19.8% PD loan needs about **13.4%**. In the notebook, the scorecard reaches **AUC 0.83** on held-out data.

**Real-world use**

- **Credit cards and personal loans.** Lenders score applicants (FICO, income, debt-to-income) and approve, price or decline automatically using a PD model.
- **Loan-loss provisions.** Under **IFRS 9** and **CECL**, banks book expected loss as an allowance. IFRS 9 stages: **Stage 1** performing (12-month ECL), **Stage 2** significant increase in credit risk (lifetime ECL), **Stage 3** credit-impaired (lifetime ECL). In the 2020 COVID shock, banks raised provisions sharply because forecast PDs rose.
- **Capital.** Expected loss is covered by pricing and provisions; unexpected loss (the volatility around EL) is covered by capital. Basel IRB capital is computed from PD, LGD and EAD.

**Model validation checklist**

- **Discrimination:** AUC, Gini, KS (does it rank risky borrowers above safe ones?).
- **Calibration:** predicted PD close to actual default rate by risk decile.
- **Stability:** Population Stability Index to detect drift after launch.
- **Imbalance:** with a 6.9% default rate, a model predicting "nobody defaults" is 93% accurate but useless, so use AUC or precision-recall, not accuracy.

**Interview questions.** Walk through building a PD model (target definition, features, split, validation, monitoring). EL versus UL? Through-the-cycle versus point-in-time PD? What counts as default under Basel? (90 days past due or unlikely to pay.)

# 9. Cost of Capital and DCF Valuation

**Idea.** A company is worth the present value of the free cash flow it will generate for all its capital providers, discounted at its cost of capital.

**Formulas**

$$WACC=\frac{E}{V}\,r_e+\frac{D}{V}\,r_d\,(1-t)\qquad\qquad r_e=r_f+\beta\cdot MRP$$

$$FCFF=EBIT(1-t)+D\&A-CapEx-\Delta NWC$$

$$EV=\sum_{t=1}^{N}\frac{FCFF_t}{(1+WACC)^{t}}+\frac{TV}{(1+WACC)^{N}}\qquad\qquad TV=\frac{FCFF_N\,(1+g)}{WACC-g}$$

$$\text{Equity value}=EV-\text{Debt}+\text{Cash}\qquad\qquad \text{Value per share}=\frac{\text{Equity value}}{\text{Shares}}$$

Unlevering beta (to compare firms with different debt):

$$\beta_U=\frac{\beta_L}{1+(1-t)\,D/E}$$

**Worked example (hypothetical company in the notebook).** $r_e=10.6\%$, $E=3\text{,}600$, $D=600$, $r_d=6\%$, $t=25\%$:

$$WACC=0.857\times10.6\%+0.143\times6\%\times0.75=9.73\%$$

Year-5 free cash flow is \$356.1M and $g=2.5\%$:

$$TV=\frac{356.1\times1.025}{0.0973-0.025}=\$5\text{,}048\text{M}\qquad PV(TV)=\frac{5\text{,}048}{1.0973^{5}}=\$3\text{,}173\text{M}\;(73\%\text{ of }EV)$$

$EV=\$4\text{,}338$M, equity $=4\text{,}338-600+150=\$3\text{,}888$M, so **\$38.88 per share** versus a \$36 market price.

**Real-world use**

- **Mergers and acquisitions.** An acquirer values the target with a DCF, then compares it with the offer price. Bankers show a WACC versus growth grid (here, 1 percentage point lower WACC lifts value from \$38.9 to \$46.0).
- **Equity research and investing.** Analysts publish target prices from DCFs; investors compare to market price.
- **Credit analysis.** Lenders use FCFF forecasts to test whether a borrower can service debt.
- **Banks are different.** A bank's debt is raw material, not financing, so FCFF-DCF does not fit. Analysts value banks with a **dividend discount** or **residual income** model, using the justified price-to-book ratio:

$$\frac{P}{B}=\frac{ROE-g}{r_e-g}$$

**Interview questions.** Walk me through a DCF in two minutes. Why does terminal value dominate? How does more debt affect WACC? Sanity checks: growth below long-run GDP, WACC above $g$, implied exit multiple reasonable.

# 10. Monte Carlo Simulation

**Idea.** Replace single-number assumptions with probability distributions, run the model thousands of times, and read the answer as a distribution.

**Formulas**

Simulate an asset price (geometric Brownian motion), where $Z\sim N(0,1)$:

$$S_{t+\Delta t}=S_t\,\exp\!\Big[\big(\mu-\tfrac12\sigma^{2}\big)\Delta t+\sigma\sqrt{\Delta t}\,Z\Big]$$

Accuracy of an estimate from $N$ runs (standard error shrinks slowly):

$$SE=\frac{s}{\sqrt{N}}$$

**Worked example.** The notebook runs 10,000 DCFs, drawing growth, margin, beta and terminal growth at random. Result: median **\$38.8 per share**, 5th–95th percentile **\$26–\$56**, and a **62.9% probability** that value exceeds the \$36 market price.

**Real-world use**

- **Stress testing and capital planning.** Banks simulate thousands of interest-rate, unemployment and house-price paths to see the loss distribution for regulators.
- **Pricing complex derivatives** that have no closed-form formula.
- **Investment committees** prefer "63% chance the stock is undervalued" to a single point estimate.

**Pitfalls.** Inputs are often correlated, so sampling them independently understates risk. The answer is only as good as the chosen distributions.

# 11. Bank-Specific Concepts

| Concept | Formula or definition | Real-world meaning |
|---|---|---|
| Net interest margin (NIM) | $\dfrac{\text{interest income}-\text{interest expense}}{\text{avg earning assets}}$ | Core profitability of lending; rises when rates rise for asset-sensitive banks |
| Efficiency ratio | $\dfrac{\text{non-interest expense}}{\text{revenue}}$ | Lower is better; around 55–60% is typical |
| DuPont ROE | $\dfrac{NI}{Rev}\times\dfrac{Rev}{Assets}\times\dfrac{Assets}{Equity}$ | Shows how leverage drives bank returns |
| CET1 ratio | $\dfrac{\text{common equity tier 1}}{\text{risk-weighted assets}}$ | Capital buffer; minimum 4.5% plus buffers (roughly 7%+) |
| Leverage ratio | $\dfrac{\text{Tier 1 capital}}{\text{total exposure}}$ | Simple backstop to risk-weighted rules (minimum 3%) |
| LCR | $\dfrac{\text{high-quality liquid assets}}{\text{30-day net outflows}}\ge100\%$ | Can the bank survive a month of stress? |
| NSFR | $\dfrac{\text{available stable funding}}{\text{required stable funding}}\ge100\%$ | Is long-term lending funded by stable sources? |
| Funds transfer pricing | Internal rate charged for funding | Shows each product's true margin |

**DuPont example.** Net income/revenue $=25\%$, revenue/assets $=4\%$, assets/equity $=11$:

$$ROE=0.25\times0.04\times11=11\%$$

High leverage drives bank ROE, which is why regulators set capital floors.

**Interest-rate risk in the banking book (IRRBB).** Banks borrow short (deposits) and lend long, creating a duration gap. Approximately:

$$\Delta EVE\;\approx\;-\big(D_A-\tfrac{L}{A}D_L\big)\cdot A\cdot\Delta y$$

where $A$ and $L$ are assets and liabilities. If asset duration exceeds liability duration, rising rates cut the economic value of equity. Banks measure this with repricing gaps, duration gaps and net-interest-income simulations under $\pm100$bp shocks.

**Model risk.** Regulators (SR 11-7 in the US) expect every model, such as your PD scorecard, to be independently validated and monitored. The **three lines of defence** are the business, risk and compliance oversight, and internal audit.

# 12. Quick-fire Interview Answers

1. **Single most important idea in finance?** Value equals the present value of future cash flows, adjusted for risk.
2. **Rates rise: what happens to a bank?** Bond values fall, deposit costs rise, prepayments slow, credit risk increases. Net interest income rises if the bank is asset-sensitive.
3. **Explain your project simply.** "I built Python models that answer how much a loan costs, how risky a portfolio is, what a company is worth, and how much to set aside for loans that go bad."
4. **What would you change with real data?** Out-of-time validation, drift monitoring, macro-linked PDs, and documentation for model risk.
5. **Weakest part of your DCF?** Terminal value is about 73% of EV and very sensitive to WACC and $g$, hence the sensitivity grid and Monte Carlo.
6. **Why does correlation matter?** It sets how much diversification you get, and it spikes in a crisis, which is exactly when VaR can fail.

# Two-week Study Plan

- **Days 1–3:** sections 1–4. Re-derive each formula by hand once.
- **Days 4–6:** sections 5–7. Re-run the notebook modules with different parameters.
- **Days 7–9:** sections 8 and 11, your differentiator given your bank job.
- **Days 10–12:** sections 9–10. Practise a two-minute DCF walk-through aloud.
- **Days 13–14:** mock interviews from section 12, and explain each notebook module in 60 seconds.
