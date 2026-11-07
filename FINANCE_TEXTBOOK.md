---
title: "Financial Modeling for Banking and Analytics"
subtitle: "A Study Guide: Definitions, Mathematics, Classic Cases and Worked Examples"
---

# How to Use This Book

This guide is written like a textbook chapter set. Every chapter follows the same order, so you always know where to look:

1. **Learning objectives**: what you will be able to do.
2. **Key terms and full forms**: every abbreviation spelled out, with a plain-language definition.
3. **The idea**: why the concept exists and where it came from, with the classic book or paper that introduced it.
4. **The mathematics**: formulas, with short derivations where they help you remember them.
5. **Worked example**: step by step, with every number shown.
6. **A classic case**: the famous example from the literature or from history.
7. **In a bank**: where the concept is used in practice.
8. **Common mistakes.**
9. **Practice problems**: answers are in Appendix A.

**A note on sources.** The books and papers named here are real and are listed in Appendix B. I describe each source's *idea* in my own words and I do not reproduce their text. Where I say a well-known example "appears in" a textbook, check the edition you own, because books reorganise examples between editions. Numbers in the worked examples are my own calculations, matched to the companion notebook `Financial_Modeling_Toolkit.ipynb`.

## Notation and Full Forms

| Abbreviation | Full form | Meaning |
|---|---|---|
| PV, FV | Present Value, Future Value | Value of money now, or at a later date |
| APR | Annual Percentage Rate | Quoted yearly rate, before compounding is applied |
| APY, EAR | Annual Percentage Yield, Effective Annual Rate | True yearly rate after compounding |
| NPV | Net Present Value | Sum of discounted cash flows, including the cost |
| IRR | Internal Rate of Return | Discount rate at which NPV is zero |
| YTM | Yield To Maturity | Single discount rate that prices a bond |
| DV01 | Dollar Value of 01 (one basis point) | Dollar price change for a 0.01% change in yield |
| bp | Basis point | One hundredth of one percent (0.01%) |
| CAPM | Capital Asset Pricing Model | Required return as a function of beta |
| MRP | Market Risk Premium | Expected market return minus the risk-free rate |
| VaR | Value at Risk | Loss not exceeded at a given confidence level |
| ES | Expected Shortfall (also CVaR) | Average loss in the worst tail |
| FRTB | Fundamental Review of the Trading Book | Basel rules for market-risk capital |
| PD, LGD, EAD | Probability of Default, Loss Given Default, Exposure At Default | The three components of credit loss |
| CCF | Credit Conversion Factor | Share of an undrawn limit expected to be drawn by default |
| EL, UL | Expected Loss, Unexpected Loss | Average loss, and volatility of loss around it |
| ECL | Expected Credit Loss | Provision required under IFRS 9 / CECL |
| IFRS 9 | International Financial Reporting Standard 9 | Global accounting standard for loan impairment |
| CECL | Current Expected Credit Loss | US accounting standard for loan impairment |
| AUC, ROC | Area Under the Curve, Receiver Operating Characteristic | Measures of a scoring model's ranking power |
| KS | Kolmogorov–Smirnov statistic | Maximum separation between good and bad score distributions |
| PSI | Population Stability Index | Measure of drift between two populations |
| WACC | Weighted Average Cost of Capital | Blended cost of equity and debt |
| FCFF, FCFE | Free Cash Flow to the Firm, to Equity | Cash available to all investors, or to shareholders |
| EBIT, EBITDA | Earnings Before Interest and Taxes, (and) Depreciation and Amortization | Operating profit measures |
| D&A, CapEx, NWC | Depreciation and Amortization, Capital Expenditure, Net Working Capital | Items in the cash-flow build |
| TV, EV | Terminal Value, Enterprise Value | Value beyond forecast horizon; value of operations |
| DDM | Dividend Discount Model | Valuation by discounting dividends |
| MM | Modigliani–Miller | Capital structure theorems |
| GBM | Geometric Brownian Motion | Standard model of random price paths |
| NII, NIM | Net Interest Income, Net Interest Margin | Core bank earnings measures |
| ROA, ROE | Return On Assets, Return On Equity | Profitability ratios |
| RWA | Risk-Weighted Assets | Assets scaled by regulatory risk weights |
| CET1 | Common Equity Tier 1 | Highest-quality regulatory capital |
| LCR | Liquidity Coverage Ratio | Liquid assets versus 30-day stressed outflows |
| NSFR | Net Stable Funding Ratio | Stable funding versus long-term assets |
| HQLA | High-Quality Liquid Assets | Assets easily sold in a crisis |
| ALM | Asset–Liability Management | Managing balance-sheet interest and liquidity risk |
| IRRBB | Interest Rate Risk in the Banking Book | Rate risk on non-trading positions |
| EVE | Economic Value of Equity | PV of assets minus PV of liabilities |
| FTP | Funds Transfer Pricing | Internal charge for funding |
| RAROC | Risk-Adjusted Return On Capital | Profit after expected loss, divided by capital |
| FICO, DTI, LTV | Fair Isaac Corporation score, Debt-To-Income, Loan-To-Value | Common borrower risk features |

# Part I: Foundations of Value

# Chapter 1. The Time Value of Money

**Learning objectives.** Compute present and future values; value annuities and perpetuities; convert between quoted and effective rates; explain why discounting is the foundation of all valuation.

::: definition
**Key definitions**

- **Time value of money**: money available now is worth more than the same amount later, because it can be invested to earn a return and because of inflation and risk.
- **Interest rate** $r$: the price of using money for one period, as a fraction of the amount.
- **Compounding**: earning interest on previously earned interest.
- **Present value (PV)**: today's worth of a future cash flow.
- **Future value (FV)**: the worth, at a later date, of money invested today.
- **Discount rate**: the rate used to convert future values to present values; it reflects the opportunity cost and the risk of the cash flow.
- **Annuity**: equal payments at regular intervals for a fixed number of periods. **Perpetuity**: the same, forever.
- **APR (Annual Percentage Rate)**: the nominal yearly rate quoted by the lender. **EAR / APY**: the rate you really earn or pay once compounding is counted.
:::

## The idea and where it comes from

The modern treatment of interest as the link between present and future consumption comes from the American economist Irving Fisher in *The Theory of Interest* (1930). Fisher showed that a person or firm facing a financial market should evaluate any plan by its present value. Every corporate finance textbook opens with this idea: see Brealey, Myers and Allen, *Principles of Corporate Finance*, and Ross, Westerfield and Jaffe, *Corporate Finance*.

## The mathematics

**Compounding.** Invest $PV$ at rate $r$. After one period you hold $PV(1+r)$. Reinvesting that gives $PV(1+r)^2$, and after $n$ periods:

$$FV = PV\,(1+r)^{n} \qquad\Longleftrightarrow\qquad PV=\frac{FV}{(1+r)^{n}}$$

**Annuity.** Payments $C$ at the end of each of $n$ periods. Its present value is a geometric series:

$$PV=\frac{C}{1+r}+\frac{C}{(1+r)^2}+\dots+\frac{C}{(1+r)^n}=C\cdot\frac{1-(1+r)^{-n}}{r}$$

Its future value (value at the end of period $n$) is

$$FV_{annuity}=C\cdot\frac{(1+r)^{n}-1}{r}$$

**Perpetuity and growing perpetuity.** Let $n\to\infty$ in the annuity formula. If payments grow at rate $g$ with $r>g$:

$$PV=\frac{C}{r}\qquad\qquad PV=\frac{C_1}{r-g}$$

**Quoted versus effective rates.** If the APR is compounded $m$ times a year, and for continuous compounding:

$$EAR=\left(1+\frac{APR}{m}\right)^{m}-1 \qquad\qquad FV=PV\,e^{rn}$$

**Rule of 72.** Money doubles in about $72/r$ years when $r$ is in percent. Exact doubling time is $\ln 2/\ln(1+r)$.

## Worked example: saving for a house deposit

You deposit \$200 at the end of every month for 10 years in an account paying 6% APR, compounded monthly.

- Monthly rate $r=0.06/12=0.005$; number of periods $n=120$.
- $$FV=200\cdot\frac{(1.005)^{120}-1}{0.005}=200\cdot\frac{0.8194}{0.005}=\$32\text{,}775.87$$
- You contributed only \$24,000. The remaining \$8,775.87 is interest.

## Classic case: the \$24 purchase of Manhattan

A famous textbook illustration of compounding says Manhattan was bought in 1626 for \$24 worth of goods. If that \$24 had been invested at 6% a year for 400 years, it would be worth $24\times1.06^{400}\approx\$318$ billion. At 8% it would be about \$562 trillion. The lesson is not the history (which is disputed) but how enormously a small change in $r$ or $n$ changes the answer. This is why financial models are so sensitive to the discount rate.

## In a bank

- **Deposit and loan disclosure.** In the US, the Truth in Lending Act requires lenders to show APR, and the Truth in Savings Act requires banks to show APY, so customers can compare products honestly. A savings account at "6% compounded monthly" really yields 6.17%.
- **Pricing everything.** A bond is an annuity plus a lump sum. A pension liability is a stream of future payments discounted to today. A mortgage is the reverse of the annuity formula (Chapter 2).

## Common mistakes

- Using an annual rate with monthly periods (always match $r$ and $n$ to the same period).
- Using the growing-perpetuity formula when $r\le g$.
- Forgetting whether payments are at the start (annuity due) or end (ordinary annuity) of the period.

## Practice problems

1. What is the present value of \$5,000 received in 4 years at 8%?
2. A card charges 12% APR compounded monthly. What is the EAR?
3. How long does money take to double at 9%? Use the rule of 72 and compare with the exact value.
4. A perpetuity pays \$50 a year and the discount rate is 5%. What is its value?

# Chapter 2. Loans and Amortization

**Learning objectives.** Derive the level payment on a loan; split each payment into interest and principal; understand prepayment and payment shock.

::: definition
**Key definitions**

- **Principal**: the amount borrowed. **Balance**: principal still owed.
- **Amortization**: paying off a loan gradually through scheduled payments.
- **Amortization schedule**: the table showing interest, principal and balance each period.
- **Fixed-rate / adjustable-rate loan (ARM)**: the rate stays constant, or resets to a market-linked rate after a set period.
- **Prepayment**: paying more or earlier than scheduled. **CPR (Conditional Prepayment Rate)** is the annualised fraction of the pool prepaid.
:::

## The idea

A lender is buying an annuity: the loan amount equals the present value of the payments. Because the borrower pays interest only on the *remaining* balance, early payments are mostly interest. This structure is treated in every banking text, for example Saunders and Cornett, *Financial Institutions Management*, and in fixed-income texts such as Fabozzi, *Bond Markets, Analysis and Strategies*, where mortgage cash flows and prepayment are central.

## The mathematics

Set the PV of the payments equal to the loan $L$ and solve for the payment $P$ (monthly rate $r$, $n$ months):

$$L=P\cdot\frac{1-(1+r)^{-n}}{r}\quad\Longrightarrow\quad P=L\cdot\frac{r}{1-(1+r)^{-n}}$$

Each period:

$$I_t=r\,B_{t-1}\qquad \text{Principal}_t=P-I_t \qquad B_t=B_{t-1}-\text{Principal}_t$$

Closed-form balance after $k$ payments, and total interest paid:

$$B_k=L\cdot\frac{(1+r)^{n}-(1+r)^{k}}{(1+r)^{n}-1}\qquad\qquad \text{Total interest}=nP-L$$

## Worked example

A \$400,000 loan, 6.5% APR, 30 years: $r=0.065/12=0.005417$, $n=360$.

$$P=400\text{,}000\cdot\frac{0.005417}{1-(1.005417)^{-360}}=\$2\text{,}528.27$$

- Month 1 interest: $400\text{,}000\times0.005417=\$2\text{,}166.67$; principal is only **\$361.60** (14% of the payment).
- Total interest: $360\times2\text{,}528.27-400\text{,}000=\$510\text{,}178$, more than the amount borrowed.
- Paying an extra \$300 a month finishes the loan **7.6 years earlier** and saves about **\$149,581** of interest.

## Classic case: the 2/28 adjustable-rate mortgage and payment shock

Michael Lewis's *The Big Short* (2010) describes how, before the 2008 crisis, many subprime borrowers took "2/28" loans: a low fixed rate for 2 years, then a reset to a much higher rate. Take a \$300,000, 30-year loan at 7% for 2 years: the payment is **\$1,995.91** and the balance after 24 payments is **\$293,685**. When the rate resets to 11% for the remaining 28 years, the payment jumps to **\$2,823.72**, up 41% without any change in the borrower's income. Many could not pay, and defaults spread through mortgage-backed securities.

## In a bank

- **Loan systems** generate schedules using exactly this formula.
- **Prepayment risk.** When rates fall, borrowers refinance. The bank gets principal back early and must reinvest at lower rates, which is why mortgage bonds are priced on prepayment models rather than contractual maturity.
- **Stress testing** applies payment-shock scenarios to adjustable-rate books.

## Common mistakes

Dividing the annual rate by 12 but using years for $n$; forgetting the loan balance falls so interest falls; ignoring fees, which make the true cost (the APR) higher than the note rate.

## Practice problems

1. Monthly payment on a \$250,000, 7%, 15-year loan?
2. After the first payment of a \$100,000 loan at 6% (monthly payments), how much of the first payment is interest if the payment is \$599.55?
3. Why does the borrower pay so much more interest on a 30-year loan than a 15-year loan at the same rate?

# Chapter 3. Capital Budgeting: NPV, IRR and Payback

**Learning objectives.** Decide whether to accept a project using NPV and IRR; explain why NPV is the better rule; recognise when IRR fails.

::: definition
**Key definitions**

- **Capital budgeting**: choosing which long-lived investments to undertake.
- **Cash flow ($CF_t$)**: cash in or out at time $t$; the initial outlay is negative.
- **Net Present Value (NPV)**: PV of all cash flows, including the initial cost.
- **Internal Rate of Return (IRR)**: the discount rate that makes NPV exactly zero.
- **Hurdle rate**: minimum acceptable return, usually the cost of capital (WACC).
- **Payback period**: time to recover the initial cost; **discounted payback** uses PVs.
- **Profitability index**: PV of inflows divided by initial cost.
- **Mutually exclusive projects**: choosing one rules out the others.
:::

## The idea

Fisher (1930) showed that a firm maximises its owners' wealth by taking every project that earns more than the market rate of return, which is the same as taking every project with positive NPV. Brealey, Myers and Allen devote a chapter to why NPV beats other criteria. NPV also has the property of **value additivity**: the NPV of two projects together is the sum of their NPVs.

## The mathematics

$$NPV=\sum_{t=0}^{T}\frac{CF_t}{(1+r)^{t}}\qquad\qquad \text{IRR solves}\quad 0=\sum_{t=0}^{T}\frac{CF_t}{(1+IRR)^{t}}$$

$$PI=\frac{PV(\text{inflows})}{\text{initial cost}}\qquad\qquad \text{Decision: accept if } NPV>0 \;(\Leftrightarrow IRR>r\text{, for conventional cash flows})$$

The **modified IRR (MIRR)** fixes IRR's reinvestment assumption: compound all inflows to the end at the reinvestment rate $r_{reinv}$, discount all outflows at the finance rate $r_{fin}$:

$$MIRR=\left(\frac{FV(\text{inflows at }r_{reinv})}{PV(\text{outflows at }r_{fin})}\right)^{1/T}-1$$

## Worked example

A project costs \$5,000 and returns \$1,500, \$1,800, \$2,000 and \$2,200 over four years. Hurdle rate 8%.

| Year | Cash flow | Discount factor $1/1.08^t$ | PV |
|---|---|---|---|
| 0 | −5,000 | 1.0000 | −5,000.00 |
| 1 | 1,500 | 0.9259 | 1,388.89 |
| 2 | 1,800 | 0.8573 | 1,543.21 |
| 3 | 2,000 | 0.7938 | 1,587.66 |
| 4 | 2,200 | 0.7350 | 1,617.07 |
| | | **NPV** | **\$1,136.83** |

IRR solves the zero-NPV equation numerically: **IRR = 17.19%**, well above 8%. Accept. Profitability index $=6\text{,}136.83/5\text{,}000=1.23$.

## Classic case: the project with two IRRs

A standard textbook illustration (used, for example, in *Principles of Corporate Finance*) has cash flows $-4\text{,}000,\;+25\text{,}000,\;-25\text{,}000$. The sign changes twice, so the NPV equation has two roots:

$$NPV(r)=-4000+\frac{25000}{1+r}-\frac{25000}{(1+r)^2}$$

Check $r=25\%$: $-4000+20000-16000=0$. Check $r=400\%$: $-4000+5000-1000=0$. Both are IRRs, so "accept if IRR exceeds the hurdle" gives no clear answer. NPV at the actual cost of capital always gives a single, correct signal. This is the standard reason to prefer NPV.

## In a bank

- **Strategic investment.** A \$2.0M digital platform and a \$1.5M branch expansion are ranked by NPV at the bank's WACC. In the notebook the platform has NPV \$1.0M versus \$0.4M for the branch.
- **Corporate lending.** Credit officers run the borrower's project NPV and IRR to judge if cash flows can service the debt.
- **Capital rationing.** When capital is limited, banks rank by profitability index.

## Common mistakes

Ranking mutually exclusive projects by IRR; ignoring the scale of the project; comparing projects of different lives without annualising; using the wrong discount rate (the rate must match the project's risk, not the firm's average).

## Practice problems

1. Verify the NPV above by hand at 8%.
2. A project costs \$1,000 and returns \$400, \$400, \$400. Compute NPV at 10% and the payback period.
3. Why can IRR mis-rank two mutually exclusive projects of different size?

# Part II: Fixed Income

# Chapter 4. Bonds: Price, Yield, Duration and Convexity

**Learning objectives.** Price a bond; find its yield; compute duration and convexity; estimate price changes from rate changes; explain bank interest-rate risk.

::: definition
**Key definitions**

- **Bond**: a loan in security form. The issuer pays periodic **coupons** and returns the **face value (par)** at **maturity**.
- **Coupon rate**: coupon payment as a fraction of face value. **Zero-coupon bond**: pays no coupon, sells at a discount.
- **Yield to maturity (YTM)**: the single discount rate that makes the PV of all bond cash flows equal its price.
- **Duration**: a measure of a bond's sensitivity to interest rates and of the average time to receive its cash. **Macaulay duration** is in years; **modified duration** is the percentage price change per unit yield change.
- **Convexity**: the curvature of the price-yield relationship (second-order sensitivity).
- **DV01**: dollar value of one basis point.
- **Spot rate**: yield on a zero-coupon bond. **Forward rate**: the rate for a future period implied by today's spot rates.
:::

## The idea and where it comes from

**Frederick Macaulay** introduced duration in *Some Theoretical Problems Suggested by the Movements of Interest Rates, Bond Yields and Stock Prices in the United States since 1856* (NBER, 1938); **John Hicks** developed a similar idea independently in *Value and Capital* (1939). **F. M. Redington** (1952) used it to show how a financial institution could **immunise** its balance sheet: if assets and liabilities have the same present value and the same duration, small parallel rate moves do not change the value of equity. The standard modern references are Fabozzi, *Bond Markets, Analysis and Strategies*, and Saunders and Cornett for banks.

## The mathematics

**Price** with $m$ payments a year and $T$ years, coupon $C$, face value $F$, yield $y$:

$$P=\sum_{k=1}^{mT}\frac{C/m}{(1+y/m)^{k}}+\frac{F}{(1+y/m)^{mT}}$$

**Duration as a derivative.** Differentiate the annual-pay price with respect to $y$:

$$\frac{dP}{dy}=-\frac{1}{1+y}\sum_{t}t\cdot\frac{CF_t}{(1+y)^{t}}\quad\Longrightarrow\quad \frac{\Delta P}{P}\approx-D_{mod}\,\Delta y$$

$$D_{Mac}=\frac{1}{P}\sum_{t}t\cdot PV(CF_t)\qquad D_{mod}=\frac{D_{Mac}}{1+y/m}$$

The second derivative gives **convexity** and the improved estimate:

$$\text{Convexity}=\frac{1}{P\,(1+y)^{2}}\sum_{t}t(t+1)\,PV(CF_t)\qquad\qquad \frac{\Delta P}{P}\approx-D_{mod}\Delta y+\tfrac12\,\text{Convexity}\,(\Delta y)^2$$

$$DV01=P\cdot D_{mod}\cdot0.0001$$

**Forward rates** from spot rates:

$$(1+s_2)^2=(1+s_1)(1+f_{1,2})\quad\Longrightarrow\quad f_{1,2}=\frac{(1+s_2)^2}{1+s_1}-1$$

## Worked example

A 5-year bond, \$1,000 face, 6% annual coupon, yield 7%.

| Year $t$ | Cash flow | PV at 7% | $t\times PV$ | $t(t+1)\times PV$ |
|---|---|---|---|---|
| 1 | 60 | 56.07 | 56.07 | 112.15 |
| 2 | 60 | 52.40 | 104.80 | 314.40 |
| 3 | 60 | 48.98 | 146.93 | 587.72 |
| 4 | 60 | 45.77 | 183.08 | 915.40 |
| 5 | 1,060 | 755.77 | 3,778.83 | 22,673.00 |
| **Total** | | **958.99** | **4,269.71** | |

- Price $=\$958.99$ (below par because the coupon is below the yield).
- $D_{Mac}=4\text{,}269.71/958.99=4.452$ years; $D_{mod}=4.452/1.07=4.161$; Convexity $\approx22.4$; DV01 $\approx\$0.399$ per \$1,000 bond.
- For $\Delta y=+1\%$: $-4.161\%+\tfrac12(22.4)(0.01)^2=-4.05\%$. The exact repricing at 8% gives \$920.15, a fall of **4.05%**.
- For $\Delta y=-1\%$: estimate $+4.27\%$; the exact repricing at 6% gives \$1,000, a rise of **4.28%**.

**Forward rate.** If the 1-year spot rate is 4% and the 2-year spot rate is 5%: $f_{1,2}=1.05^2/1.04-1=6.01\%$.

## Classic case: the savings and loan crisis and Silicon Valley Bank

In the late 1970s and early 1980s, US savings and loan institutions funded long-term fixed-rate mortgages with short-term deposits, a large **duration gap**. When the Federal Reserve under Paul Volcker raised rates sharply, their deposit costs rose while their mortgage income stayed fixed, and the asset values collapsed. This case is a standard in bank-management texts such as Saunders and Cornett.

The same mistake reappeared in March 2023 at **Silicon Valley Bank**. It had invested a large share of its fast-growing deposits in long-dated securities. When rates rose, the securities lost value (reported unrealised losses were in the region of \$15 billion), depositors withdrew funds, and the bank failed. The mechanics are exactly the formula $\Delta P/P\approx-D_{mod}\Delta y$ applied to a large portfolio.

## In a bank

- **Treasury** measures the portfolio's DV01 and sets limits.
- **ALM** matches asset and liability durations or hedges the gap with interest-rate swaps.
- **Accounting**: bonds classified as held-to-maturity are not marked to market, which hides the loss until the bank is forced to sell.

## Common mistakes

Using Macaulay duration (years) when the price formula needs modified duration; applying duration to large rate moves without convexity; forgetting duration changes as yield and time change.

## Practice problems

1. Price a 5-year zero-coupon bond, \$1,000 face, yield 5%.
2. A bond has modified duration 7 and convexity 60. Estimate the price change if yields rise 50bp.
3. Spot rates are 3% (1-year) and 4% (2-year). Find the 1-year forward rate one year from now.

# Part III: Risk and Return

# Chapter 5. Risk, Return and the Capital Asset Pricing Model

**Learning objectives.** Measure return and risk; estimate beta; derive and apply CAPM; evaluate a fund with Sharpe, Treynor and Jensen's alpha.

::: definition
**Key definitions**

- **Return** $R=(P_1-P_0+D)/P_0$, including any dividend $D$.
- **Variance** $\sigma^2$ and **standard deviation (volatility)** $\sigma$: dispersion of returns.
- **Covariance** and **correlation** $\rho$: how two assets move together.
- **Systematic (market) risk**: risk that affects all assets and cannot be diversified. **Idiosyncratic risk**: risk specific to one asset, removed by diversification.
- **Beta** $\beta$: sensitivity of an asset's return to the market's return.
- **Risk-free rate** $r_f$ and **market risk premium (MRP)** $=E[R_m]-r_f$.
- **Alpha** $\alpha$: return beyond what CAPM predicts for the asset's beta.
:::

## The idea and where it comes from

CAPM was developed independently by **William Sharpe** ("Capital Asset Prices," *Journal of Finance*, 1964), **John Lintner** (1965) and **Jan Mossin** (1966), building on Markowitz's portfolio theory (Chapter 6). Sharpe shared the 1990 Nobel Prize in Economics. The key idea: the market rewards only risk that cannot be diversified away. **Fama and French** (1992–93) later showed that size and value also explain returns, giving multi-factor models. Textbook treatments: Bodie, Kane and Marcus, *Investments*; Brealey, Myers and Allen.

## The mathematics

**Beta** is a regression slope:

$$\beta_i=\frac{\mathrm{Cov}(R_i,R_m)}{\mathrm{Var}(R_m)}=\rho_{im}\frac{\sigma_i}{\sigma_m}\qquad R_{i,t}-r_f=\alpha+\beta_i(R_{m,t}-r_f)+\varepsilon_t$$

**Risk decomposition** (only the first term is rewarded):

$$\sigma_i^2=\underbrace{\beta_i^2\,\sigma_m^2}_{\text{systematic}}+\underbrace{\sigma_\varepsilon^2}_{\text{idiosyncratic}}$$

**Deriving the Security Market Line (sketch).** In equilibrium all investors hold the market portfolio. The risk an asset adds to that portfolio is measured by its covariance with it, i.e. by $\beta_i$. If reward per unit of risk differed across assets, investors would shift money until they were equal, so

$$\frac{E[R_i]-r_f}{\beta_i}=\frac{E[R_m]-r_f}{1}\quad\Longrightarrow\quad E[R_i]=r_f+\beta_i\big(E[R_m]-r_f\big)$$

**Performance measures:**

$$\text{Sharpe}=\frac{R_p-r_f}{\sigma_p}\qquad \text{Treynor}=\frac{R_p-r_f}{\beta_p}\qquad \alpha_{Jensen}=R_p-\big[r_f+\beta_p(R_m-r_f)\big]$$

## Worked example

**Beta.** $\mathrm{Cov}(R_i,R_m)=0.045$, $\mathrm{Var}(R_m)=0.03$: $\beta=0.045/0.03=1.5$.

**Required return.** $r_f=3\%$, MRP $=6\%$: $E[R]=3\%+1.5\times6\%=\mathbf{12\%}$.

**Fund evaluation.** A fund returned 14% with beta 1.2 and volatility 18%. Over the same period $r_f=3\%$, market return 10%, market volatility 15%.

- CAPM-implied return: $3+1.2\times7=11.4\%$, so **alpha $=14-11.4=+2.6\%$**.
- Fund Sharpe $=(14-3)/18=0.61$; market Sharpe $=(10-3)/15=0.47$. The fund beat the market on both measures.

## Classic case: the long-run equity premium

Jeremy Siegel's *Stocks for the Long Run* documents US stock returns over two centuries, and shows a long-run equity premium well above that of bonds. The size of the premium that investors should *expect* going forward is debated (many practitioners use 4–6%), which is why the MRP is the most argued-over input in any valuation.

## In a bank

- **Cost of equity** for the bank's hurdle rate and for valuing acquisition targets.
- **Performance attribution**: separating a portfolio's return into market exposure and genuine skill (alpha).
- **Bank stock betas** are typically above 1, because bank profits swing with the economy and credit cycle.

## Common mistakes

Using a raw historical beta without checking the regression fit ($R^2$); mixing monthly returns with an annual risk-free rate; assuming alpha is skill rather than luck or an omitted risk factor.

## Practice problems

1. A stock has $\mathrm{Cov}(R_i,R_m)=0.045$ and $\sigma_m=20\%$. Find beta.
2. With $r_f=3\%$ and MRP $6\%$, what return does CAPM require for beta 1.5?
3. Fund return 14%, beta 1.2, $r_f=3\%$, market return 10%: find Jensen's alpha.

# Chapter 6. Portfolio Theory

**Learning objectives.** Compute portfolio risk and return; explain diversification; find the minimum-variance portfolio; describe the efficient frontier.

::: definition
**Key definitions**

- **Portfolio**: a collection of assets with weights $w_i$ that sum to 1.
- **Diversification**: reducing risk by holding assets that do not move together perfectly.
- **Covariance matrix** $\Sigma$: all pairwise covariances.
- **Efficient frontier**: portfolios with the highest return for each level of risk.
- **Minimum-variance portfolio**: the lowest-risk point on the frontier.
- **Tangency portfolio**: the frontier portfolio with the best Sharpe ratio.
- **Capital Market Line (CML)**: combinations of the risk-free asset and the tangency portfolio.
:::

## The idea and where it comes from

**Harry Markowitz**, "Portfolio Selection," *Journal of Finance* (1952), and his book *Portfolio Selection: Efficient Diversification of Investments* (1959), made risk a quantity to be optimised, not just avoided. He shared the 1990 Nobel Prize. **James Tobin** (1958) added the risk-free asset and showed that investors split money between the risk-free asset and one common risky portfolio. In practice, **DeMiguel, Garlappi and Uppal** (2009) found that the naive equal-weight "1/N" portfolio is hard to beat out of sample because optimisers amplify estimation error. Markowitz himself has reportedly said he divided his own retirement savings equally between stocks and bonds.

## The mathematics

For two assets:

$$\mu_p=w_1\mu_1+w_2\mu_2\qquad \sigma_p^2=w_1^2\sigma_1^2+w_2^2\sigma_2^2+2w_1w_2\rho\sigma_1\sigma_2$$

The risk falls as $\rho$ falls. Setting the derivative of $\sigma_p^2$ to zero gives the minimum-variance weight:

$$w_1^{*}=\frac{\sigma_2^2-\rho\,\sigma_1\sigma_2}{\sigma_1^2+\sigma_2^2-2\rho\,\sigma_1\sigma_2}$$

For $N$ assets, with weight vector $w$, expected returns $\mu$, covariance matrix $\Sigma$:

$$\mu_p=w^{\top}\mu\qquad\sigma_p^2=w^{\top}\Sigma w$$

$$\text{Frontier: }\min_{w}\,w^{\top}\Sigma w\;\text{ s.t. }\;w^{\top}\mu=\mu_{target},\;\textstyle\sum w_i=1\qquad\text{Tangency: }\max_w\frac{w^{\top}\mu-r_f}{\sqrt{w^{\top}\Sigma w}}$$

## Worked example

Asset 1: $\sigma_1=15\%$; Asset 2: $\sigma_2=25\%$; $\rho=0.2$.

- 60/40 portfolio: $\sigma_p^2=0.36(0.0225)+0.16(0.0625)+2(0.6)(0.4)(0.2)(0.15)(0.25)=0.0081+0.01+0.0036=0.0217$, so $\sigma_p=14.73\%$. That is *below* the risk of Asset 1 alone (15%) even though 40% is in the riskier asset.
- Minimum variance: $w_1^*=\dfrac{0.0625-0.2(0.15)(0.25)}{0.0225+0.0625-2(0.2)(0.15)(0.25)}=0.786$, giving $\sigma_p=13.89\%$.

## Classic case: concentration in a loan book

Banks do not hold stocks, but the same mathematics governs a loan portfolio. A bank lending mostly to one industry has highly correlated defaults, so losses behave like a single large exposure. The Basel internal-ratings capital formula rests on **Vasicek's** single-factor model of correlated defaults (Chapter 8) for this reason. During the 1980s oil-price collapse, banks concentrated in Texas energy lending suffered losses far larger than the independent-default assumption would have suggested.

## In a bank

- **Wealth management and robo-advisors** place clients on a point of the efficient frontier that matches their risk tolerance.
- **Treasury** diversifies the investment securities portfolio across issuers, sectors and maturities.
- **Credit risk** sets concentration limits by industry, geography and borrower.

## Common mistakes

Believing correlations are stable (they rise in crises); trusting unconstrained optimisers with noisy expected returns; measuring risk only by standard deviation when returns are skewed.

## Practice problems

1. Verify the 60/40 variance above.
2. What happens to portfolio risk of a 50/50 mix if $\rho=1$? if $\rho=-1$ and $\sigma_1=\sigma_2$?
3. Why does an optimiser often put 100% in one asset?

# Chapter 7. Value at Risk and Expected Shortfall

**Learning objectives.** Define and compute VaR three ways; compute ES; explain why regulators moved from VaR to ES; backtest a VaR model.

::: definition
**Key definitions**

- **Value at Risk (VaR)**: the loss that will not be exceeded with probability $\alpha$ (the **confidence level**) over a stated **horizon**. "99% 1-day VaR of \$1M" means a loss above \$1M is expected on about 1 day in 100.
- **Expected Shortfall (ES)**, also **Conditional VaR (CVaR)**: the average loss on the days when the loss exceeds VaR.
- **Backtesting**: comparing realised losses with VaR to see how often VaR was exceeded (an **exception**).
- **Stress test**: measuring loss under a specified severe scenario.
- **Coherent risk measure**: one that is monotonic, sub-additive, positively homogeneous and translation invariant.
:::

## The idea and where it comes from

VaR became the industry standard after **J.P. Morgan** published its **RiskMetrics** methodology in 1994. It is widely reported that the firm's chairman, Dennis Weatherstone, wanted a single number summarising the bank's risk to be on his desk each afternoon (the "4:15 report"). The Basel Committee's 1996 market-risk amendment allowed banks to use VaR (99%, 10-day) for capital. Philippe Jorion's *Value at Risk: The New Benchmark for Managing Financial Risk* is the standard text. **Artzner, Delbaen, Eber and Heath** ("Coherent Measures of Risk," *Mathematical Finance*, 1999) showed VaR is not sub-additive, which motivated ES. The post-crisis **Fundamental Review of the Trading Book (FRTB)** replaces 99% VaR with ES at 97.5%.

## The mathematics

**Parametric (normal) VaR.** If returns are $N(\mu,\sigma^2)$ and $z_\alpha$ is the standard normal quantile ($z_{0.95}=1.645$, $z_{0.99}=2.326$):

$$VaR_\alpha=V\,(z_\alpha\sigma-\mu)$$

**Expected shortfall** (normal case, using the standard normal density $\varphi$, since $E[Z\mid Z>z_\alpha]=\varphi(z_\alpha)/(1-\alpha)$):

$$ES_\alpha=V\left(\sigma\,\frac{\varphi(z_\alpha)}{1-\alpha}-\mu\right)$$

**Time scaling.** If daily returns are independent with equal variance, the $T$-day variance is $T\sigma^2$, so

$$VaR_{T\text{ days}}=VaR_{1\text{ day}}\sqrt{T}$$

**Historical VaR.** Sort past profits and losses and take the $(1-\alpha)$ percentile. **Monte Carlo VaR** takes the same percentile from simulated outcomes.

**Backtesting.** Over 250 days at 99%, expect about 2.5 exceptions. The Basel "traffic light" test classes 0–4 exceptions as green, 5–9 yellow, and 10 or more red (higher capital multiplier).

## Worked example

Portfolio value \$5,000,000, daily volatility 2%, mean ignored.

- 95% 1-day VaR $=5\text{,}000\text{,}000\times1.645\times0.02=\mathbf{\$164\text{,}500}$.
- 10-day VaR $=164\text{,}500\times\sqrt{10}=\mathbf{\$520\text{,}195}$.
- ES at 95%: $\varphi(1.645)=0.1031$, so $ES=5\text{,}000\text{,}000\times0.02\times0.1031/0.05\approx\mathbf{\$206\text{,}200}$, about 25% above VaR.

## Classic case: Long-Term Capital Management (1998)

Roger Lowenstein's *When Genius Failed* (2000) tells the story of LTCM, a hedge fund run by finance professors and Nobel laureates. Its VaR models, based on calm historical periods, said losses of the 1998 magnitude were nearly impossible. After the Russian default, correlations among its positions jumped toward 1, losses were many times larger than VaR, and the Federal Reserve organised a private rescue. Nassim Taleb's *The Black Swan* (2007) builds a broader critique: models based on normal distributions understate rare, severe events. This is why practitioners add stress tests and use ES.

## In a bank

- **Daily limits**: each trading desk gets a VaR limit, reported every morning.
- **Regulatory capital**: market-risk capital is a multiple of recent VaR/ES, increased after backtesting failures.
- **Independent validation** compares the VaR model with alternative methods.

| Method | Strength | Weakness |
|---|---|---|
| Parametric | Fast, closed form | Normality understates fat tails |
| Historical | No distribution assumption | Depends on the window chosen |
| Monte Carlo | Handles options and non-linear risk | Model-dependent, slower |

## Common mistakes

Reporting VaR as "the maximum loss" (it is a threshold, not a maximum); scaling by $\sqrt{T}$ when returns are autocorrelated or positions illiquid; ignoring that VaR can rise when portfolios are combined.

## Practice problems

1. Compute the 99% 1-day VaR for \$5M with daily volatility 2%.
2. Why is ES always at least as large as VaR?
3. A bank's 99% VaR is exceeded on 8 of 250 days. What does the traffic-light test say?

# Part IV: Credit Risk

# Chapter 8. Credit Risk: PD, LGD, EAD and Expected Loss

**Learning objectives.** Compute expected loss; build and evaluate a PD model; apply the Altman Z-score and Merton model; explain IFRS 9 staging and Basel capital.

::: definition
**Key definitions**

- **Credit risk**: the risk a borrower fails to pay as promised.
- **Default**: commonly (Basel) 90 days past due on a material amount, or the bank judges the borrower unlikely to pay.
- **PD (Probability of Default)**: chance of default over a horizon, usually 12 months.
- **LGD (Loss Given Default)** $=1-$ recovery rate, expressed as a share of exposure.
- **EAD (Exposure At Default)** $=$ drawn balance $+\,CCF\times$ undrawn limit.
- **Expected Loss (EL)**: average loss. **Unexpected Loss (UL)**: the variability of loss around EL, covered by capital.
- **Scorecard**: a model that turns borrower characteristics into a score or PD.
- **Discrimination**: ability to rank risky above safe borrowers. **Calibration**: predicted PDs matching observed default rates.
:::

## The idea and where it comes from

Credit scoring began with **Edward Altman** ("Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy," *Journal of Finance*, 1968), who combined five accounting ratios into a single Z-score. **Robert Merton** ("On the Pricing of Corporate Debt," *Journal of Finance*, 1974) viewed a company's equity as a call option on its assets: default occurs if asset value falls below the debt at maturity. **Oldrich Vasicek**'s single-factor model of correlated defaults underlies the Basel internal-ratings capital formula. Standard texts: Saunders and Allen, *Credit Risk Measurement*, and Bessis, *Risk Management in Banking*.

## The mathematics

**Expected loss:**

$$EL=PD\times LGD\times EAD$$

**Multi-year PD.** If the annual PDs are $PD_1,PD_2,\dots$ and defaults are independent across years, cumulative PD is

$$PD_{cum}=1-\prod_{t}(1-PD_t)$$

**Logistic regression PD model.** Model the log-odds as linear in the features, then invert:

$$\ln\frac{p}{1-p}=\beta_0+\beta_1x_1+\dots+\beta_kx_k\qquad\Longleftrightarrow\qquad p=\frac{1}{1+e^{-(\beta_0+\beta^{\top}x)}}$$

The coefficients are fitted by maximum likelihood. A one-unit rise in $x_j$ multiplies the odds by $e^{\beta_j}$.

**Model quality:**

$$\text{Gini}=2\,AUC-1\qquad KS=\max_s\big|F_{bad}(s)-F_{good}(s)\big|\qquad PSI=\sum_i(a_i-e_i)\ln\frac{a_i}{e_i}$$

**Altman Z-score** (public manufacturing firms), with ratios as decimals:

$$Z=1.2X_1+1.4X_2+3.3X_3+0.6X_4+1.0X_5$$

$X_1=$ working capital / total assets; $X_2=$ retained earnings / total assets; $X_3=$ EBIT / total assets; $X_4=$ market value of equity / book value of liabilities; $X_5=$ sales / total assets. Conventional zones: $Z<1.81$ distress, $1.81$–$2.99$ grey, $Z>2.99$ safe.

**Merton model.** With asset value $V$, debt face value $D$, asset drift $\mu$, asset volatility $\sigma$, horizon $T$:

$$DD=\frac{\ln(V/D)+(\mu-\tfrac12\sigma^2)T}{\sigma\sqrt{T}}\qquad PD=N(-DD)$$

**Basel capital (simplified Vasicek).** Capital per unit of exposure at the 99.9% confidence level, with asset correlation $\rho$ and ignoring the maturity adjustment:

$$K=LGD\left[N\!\left(\frac{N^{-1}(PD)+\sqrt{\rho}\,N^{-1}(0.999)}{\sqrt{1-\rho}}\right)-PD\right]$$

**Pricing.** The minimum loan rate must cover funding, operating cost, expected loss and a profit margin:

$$r_{loan}=\text{funding}+\text{opex}+PD\times LGD+\text{margin}$$

## Worked examples

**Expected loss.** $PD=3\%$, $LGD=45\%$, $EAD=\$200\text{,}000$: $EL=0.03\times0.45\times200\text{,}000=\mathbf{\$2\text{,}700}$.

**Cumulative PD.** Annual PDs of 2%, 3%, 4%: $1-(0.98)(0.97)(0.96)=\mathbf{8.74\%}$ over three years.

**Altman Z.** $X_1=0.15$, $X_2=0.10$, $X_3=0.08$, $X_4=1.2$, $X_5=0.9$:
$Z=0.18+0.14+0.264+0.72+0.90=\mathbf{2.20}$, in the grey zone.

**Merton.** $V=120$, $D=100$, $\mu=8\%$, $\sigma=20\%$, $T=1$: $DD=\dfrac{\ln1.2+(0.08-0.02)}{0.20}=1.21$, so $PD=N(-1.21)=\mathbf{11.3\%}$.

**Basel capital.** $PD=2\%$, $LGD=45\%$, $\rho=0.15$: $K\approx\mathbf{7.0\%}$ of exposure (of which $PD\times LGD=0.9\%$ is expected loss covered by provisions and pricing).

**Pricing.** Funding 3.5%, opex 1.0%, margin 1.0%: a 2% PD loan with 40% LGD needs $3.5+1.0+0.8+1.0=\mathbf{6.3\%}$.

**Scorecard in the notebook.** A logistic model on 20,000 simulated loans reached **AUC 0.83 (Gini 0.66, KS 0.51)** on held-out data and was calibrated across risk deciles.

## Classic case: the 2008 crisis and the move to expected-loss accounting

Before 2008, accounting rules (the "incurred loss" model) recorded a provision only after a loss event had occurred. Michael Lewis's *The Big Short* describes how mortgage losses arrived suddenly, and the delayed recognition was widely described as "too little, too late." In response, the IASB issued **IFRS 9** (2014) and US regulators adopted **CECL** (2016), requiring provisions from day one based on expected losses. IFRS 9 stages:

| Stage | Condition | Provision |
|---|---|---|
| 1 | Performing, no significant increase in credit risk | 12-month ECL |
| 2 | Significant increase in credit risk | Lifetime ECL |
| 3 | Credit-impaired (default) | Lifetime ECL, interest on net balance |

In the 2020 COVID shock, forecast PDs rose sharply and banks added large provisions at the start of the pandemic, before many defaults had occurred. That is the model working as designed.

## In a bank

- **Retail lending**: automated approval and pricing from a scorecard (FICO, DTI, LTV, delinquency history).
- **Provisioning**: ECL by stage, using macroeconomic scenarios (base, upside, downside).
- **Capital**: Basel IRB capital computed from PD, LGD, EAD and correlation.
- **Model governance**: independent validation (discrimination, calibration, stability) and ongoing monitoring (PSI).

## Common mistakes

Judging a model by accuracy when only 7% of loans default (a model predicting "no default" is 93% accurate but useless); mixing through-the-cycle and point-in-time PDs; ignoring that LGD rises in recessions; training and testing on the same period (use out-of-time validation).

## Practice problems

1. Compute EL for $PD=3\%$, $LGD=45\%$, $EAD=\$200\text{,}000$.
2. Compute cumulative 3-year PD for annual PDs of 2%, 3%, 4%.
3. Compute the Altman Z-score above and state its zone.
4. In a Merton model, what happens to PD when asset volatility rises? Why?

# Part V: Valuation

# Chapter 9. Cost of Capital and Discounted Cash Flow Valuation

**Learning objectives.** Compute WACC; build free cash flow; value a firm using DCF; explain terminal value; value a dividend-paying stock and a bank.

::: definition
**Key definitions**

- **Cost of equity** $r_e$: return shareholders require (often from CAPM). **Cost of debt** $r_d$: interest rate on borrowing; **after-tax** because interest is deductible.
- **WACC (Weighted Average Cost of Capital)**: the blended cost of financing.
- **FCFF (Free Cash Flow to the Firm)** $=EBIT(1-t)+D\&A-CapEx-\Delta NWC$: cash available to all capital providers.
- **Terminal value (TV)**: value of the firm beyond the explicit forecast.
- **Enterprise value (EV)**: value of operations. **Equity value** $=EV-\text{debt}+\text{cash}$.
- **Intrinsic value**: the value implied by the business's fundamentals, as opposed to its market price.
- **Margin of safety**: buying only when price is well below intrinsic value.
:::

## The idea and where it comes from

**John Burr Williams**, in *The Theory of Investment Value* (1938), argued that a stock's value is the present value of its future dividends. **Myron Gordon** later popularised the constant-growth version. **Franco Modigliani and Merton Miller** (1958) showed that, without taxes or distress costs, capital structure does not change firm value, and with taxes debt adds value through the interest tax shield; both won Nobel Prizes. For practice, see Koller, Goldhaber and Wessels (McKinsey), *Valuation: Measuring and Managing the Value of Companies*, and Aswath Damodaran, *Investment Valuation*. **Benjamin Graham and David Dodd**, *Security Analysis* (1934), and Graham's *The Intelligent Investor* (1949) introduced the discipline of intrinsic value and the **margin of safety**, which Warren Buffett has long cited.

## The mathematics

**Cost of capital.**

$$WACC=\frac{E}{V}\,r_e+\frac{D}{V}\,r_d\,(1-t)\qquad r_e=r_f+\beta\cdot MRP\qquad V=E+D$$

**Free cash flow and enterprise value.**

$$FCFF_t=EBIT_t(1-t)+D\&A_t-CapEx_t-\Delta NWC_t$$

$$EV=\sum_{t=1}^{N}\frac{FCFF_t}{(1+WACC)^{t}}+\frac{TV}{(1+WACC)^{N}}\qquad TV=\frac{FCFF_N(1+g)}{WACC-g}$$

$$\text{Equity value}=EV-\text{Debt}+\text{Cash}\qquad \text{Value per share}=\frac{\text{Equity value}}{\text{Shares outstanding}}$$

**Gordon growth derivation.** If dividends grow at $g$ forever, $D_t=D_0(1+g)^t$ and the price is a geometric series that sums to

$$P_0=\sum_{t=1}^{\infty}\frac{D_0(1+g)^t}{(1+r)^t}=\frac{D_1}{r-g}\qquad(r>g)$$

**Levering and unlevering beta** (to compare firms with different debt):

$$\beta_U=\frac{\beta_L}{1+(1-t)\,D/E}$$

**Banks.** For banks, debt is raw material rather than financing, so value equity directly. With a constant return on equity, the justified price-to-book ratio is

$$\frac{P}{B}=\frac{ROE-g}{r_e-g}$$

## Worked examples

**WACC.** $r_e=10.6\%$, $E=3\text{,}600$, $D=600$, $r_d=6\%$, $t=25\%$: $WACC=0.857(10.6\%)+0.143(6\%)(0.75)=\mathbf{9.73\%}$.

**DCF (company in the notebook).** Year-5 FCFF is \$356.1M, $g=2.5\%$:
$TV=356.1\times1.025/(0.0973-0.025)=\$5\text{,}048$M; $PV(TV)=5\text{,}048/1.0973^5=\$3\text{,}173$M, which is **73% of EV (\$4,338M)**. Equity $=4\text{,}338-600+150=\$3\text{,}888$M, or **\$38.88 per share** against a \$36 market price.

**Sensitivity.** Lowering WACC by 1 percentage point lifts value per share from \$38.9 to \$46.0 (+18%), which is why valuations are presented as ranges.

**Small DCF to do by hand.** FCFF: 100, 110, 120 for years 1–3; $g=3\%$; WACC $8.38\%$. PV of forecast flows $=\$280.18$; $TV=120\times1.03/(0.0838-0.03)=\$2\text{,}297.40$; $PV(TV)=\$1\text{,}804.63$; $EV=\mathbf{\$2\text{,}084.81}$.

**Gordon growth.** Last dividend \$2.00, growth 4%, required return 10%: $P_0=2.00\times1.04/(0.10-0.04)=\mathbf{\$34.67}$.

**Bank P/B.** ROE 12%, $g=3\%$, $r_e=10\%$: $P/B=(0.12-0.03)/(0.10-0.03)=\mathbf{1.29}$. A bank earning exactly its cost of equity ($ROE=r_e$) is worth exactly book value.

**Unlevering.** Observed $\beta_L=1.4$, $D/E=0.5$, $t=25\%$: $\beta_U=1.4/(1+0.75\times0.5)=1.02$.

## Classic case: valuing Uber

In June 2014, Aswath Damodaran published a widely read valuation of the ride-hailing company Uber, building a DCF from explicit assumptions about the taxi market size, Uber's market share and margins. He arrived at roughly \$6 billion, while a recent funding round had implied about \$17 billion. The exercise is a standard teaching example of a "story-to-numbers" valuation: each assumption about the business maps to an input (market size, share, margin, reinvestment, risk), and disagreement about value becomes disagreement about explicit inputs. It also illustrates that DCF is a framework for discussion, not a source of exact answers.

## In a bank

- **Mergers and acquisitions**: the acquirer values the target and compares with the offer price; M&A teams present a WACC versus growth sensitivity grid.
- **Equity research**: price targets come from DCF or from the P/B and ROE relationship.
- **Credit analysis**: lenders forecast FCFF to test debt service and use EV as the cushion beneath the loan.
- **Hurdle rates**: the cost of equity is the minimum return a business line must earn.

## Common mistakes

Terminal growth above the economy's long-run growth rate; WACC not exceeding $g$; discounting FCFF at the cost of equity (use WACC) or FCFE at WACC (use $r_e$); double counting debt; using a DCF for a bank's operating cash flows.

## Practice problems

1. With $r_f=3\%$, $\beta=1.1$, MRP $6\%$: find $r_e$. Then with $E=1\text{,}600$, $D=400$, $r_d=5\%$, $t=30\%$: find WACC.
2. Using WACC $8.38\%$, FCFF 100, 110, 120 and $g=3\%$, find EV. If debt is 400 and cash 100, find equity value.
3. A stock pays \$2 next year, growth 4%, required return 10%. What is it worth?
4. Why does terminal value dominate DCF value?

# Chapter 10. Monte Carlo Simulation

**Learning objectives.** Explain how random simulation estimates expected values and risk; simulate a price path; attach a probability to a valuation; compute simulation error.

::: definition
**Key definitions**

- **Monte Carlo simulation**: estimating a quantity by averaging results from many random draws.
- **Random variable and distribution**: a quantity with uncertain value, and the probabilities of its outcomes.
- **Geometric Brownian Motion (GBM)**: a model in which price changes are proportional to price, with a drift $\mu$ and random shocks of size $\sigma$.
- **Standard error (SE)**: the uncertainty of the simulated estimate itself.
- **Scenario analysis / stress test**: evaluating specific, deliberately chosen outcomes.
:::

## The idea and where it comes from

The method was developed at Los Alamos in the 1940s by **Stanislaw Ulam**, **John von Neumann** and **Nicholas Metropolis** for nuclear-physics calculations; Ulam's colleague named it after the Monte Carlo casino. The first paper in the field is Metropolis and Ulam, "The Monte Carlo Method," *Journal of the American Statistical Association* (1949). **Phelim Boyle** applied it to option pricing in 1977. Standard references: John Hull, *Options, Futures, and Other Derivatives*, and Paul Glasserman, *Monte Carlo Methods in Financial Engineering*.

## The mathematics

**Law of large numbers.** The average of $N$ independent draws converges to the true expected value, and the error shrinks with $\sqrt{N}$:

$$\hat\theta=\frac1N\sum_{i=1}^{N}X_i\qquad SE=\frac{s}{\sqrt{N}}$$

To halve the error you need four times as many simulations.

**Geometric Brownian Motion.** The price follows $dS=\mu S\,dt+\sigma S\,dW$, which has the exact solution used to simulate each step with $Z\sim N(0,1)$:

$$S_{t+\Delta t}=S_t\exp\!\Big[\big(\mu-\tfrac12\sigma^{2}\big)\Delta t+\sigma\sqrt{\Delta t}\,Z\Big]$$

The expected price is $E[S_T]=S_0e^{\mu T}$ and the median is $S_0e^{(\mu-\sigma^2/2)T}$.

**Valuation under uncertainty.** Draw the uncertain inputs (growth, margin, beta, terminal growth) from distributions, run the DCF each time, and read the percentiles of the resulting values.

## Worked examples

**Estimating $\pi$ (the classic teaching example).** Throw $N$ random points into the unit square. The fraction landing inside the quarter circle $x^2+y^2<1$ estimates $\pi/4$, so $\hat\pi=4\times\text{fraction}$. With $N=10\text{,}000$ the standard error is $4\sqrt{p(1-p)/N}\approx0.016$, so the estimate is typically within about $\pm0.03$ of 3.1416.

**GBM.** $S_0=100$, $\mu=8\%$, $\sigma=20\%$, $T=1$ year: expected price $=100e^{0.08}=\mathbf{108.33}$; median price $=100e^{0.06}=\mathbf{106.18}$. The average is above the median because prices cannot go below zero but can rise without limit (log-normal skew).

**Monte Carlo DCF (notebook).** 10,000 simulations: median **\$38.8** per share, 5th to 95th percentile **\$26 to \$56**, and a **62.9% probability** that value exceeds the \$36 market price.

## Classic case: stress testing banks

After the 2008 crisis, regulators introduced annual stress tests (in the US, **CCAR** and **DFAST**). Banks must project losses, revenue and capital over several years under severely adverse scenarios for unemployment, house prices and interest rates. Monte Carlo methods are used to propagate randomness through these models and to estimate a distribution of capital outcomes, so that capital planning is based on probabilities and not on a single forecast.

## In a bank

- **Stress testing and capital planning** (above).
- **Pricing derivatives** that have no closed-form formula.
- **Portfolio credit risk**: simulating correlated defaults to find the loss distribution and economic capital.
- **Valuation ranges** for investment committees.

## Common mistakes

Sampling correlated inputs as if independent; choosing distributions without evidence; reporting results with more precision than the inputs justify; forgetting a fixed random seed makes results reproducible while a different seed gives slightly different numbers.

## Practice problems

1. A simulation's standard deviation is \$8 and $N=10\text{,}000$. What is the standard error of the mean?
2. By how much must $N$ increase to cut the standard error in half?
3. For a GBM with $S_0=50$, $\mu=10\%$, $\sigma=30\%$, $T=1$, what are the expected and median prices?

# Part VI: Banking

# Chapter 11. Bank Financial Analysis and Balance-Sheet Risk

**Learning objectives.** Read a bank's profitability and capital ratios; measure interest-rate risk using gap and duration; apply liquidity ratios; compute risk-adjusted profitability.

::: definition
**Key definitions**

- **Net Interest Income (NII)** $=$ interest income $-$ interest expense. **Net Interest Margin (NIM)** $=$ NII / average earning assets.
- **ROA** (Return On Assets) $=$ net income / assets. **ROE** (Return On Equity) $=$ net income / equity.
- **Efficiency ratio** $=$ non-interest expense / revenue.
- **Risk-Weighted Assets (RWA)**: assets multiplied by regulatory risk weights.
- **CET1 (Common Equity Tier 1)**: the highest-quality capital (common shares and retained earnings).
- **HQLA (High-Quality Liquid Assets)**: cash, central-bank reserves and government bonds that can be sold quickly.
- **LCR (Liquidity Coverage Ratio)** $=$ HQLA / net cash outflows over 30 days of stress, required $\ge100\%$.
- **NSFR (Net Stable Funding Ratio)** $=$ available stable funding / required stable funding, required $\ge100\%$.
- **ALM (Asset–Liability Management)**, **IRRBB**, **EVE**, **FTP**, **RAROC**: see the glossary.
:::

## The idea and where it comes from

A bank borrows short (deposits) and lends long, so it earns a spread but carries interest-rate and liquidity risk. The standard textbooks are Saunders and Cornett, *Financial Institutions Management: A Risk Management Approach*; Koch and MacDonald, *Bank Management*; and Hull, *Risk Management and Financial Institutions*. The **Basel Committee on Banking Supervision** sets global standards: Basel I (1988) introduced a minimum capital ratio of 8% of risk-weighted assets, Basel II added internal models for credit risk, and Basel III (after 2008) raised capital quality and introduced the liquidity ratios LCR and NSFR. The **DuPont analysis** of ROE originates with the DuPont company's finance department in the early 1900s, credited to Donaldson Brown.

## The mathematics

**Profitability and DuPont decomposition:**

$$NIM=\frac{\text{Interest income}-\text{Interest expense}}{\text{Average earning assets}}\qquad ROE=\underbrace{\frac{NI}{Revenue}}_{\text{margin}}\times\underbrace{\frac{Revenue}{Assets}}_{\text{turnover}}\times\underbrace{\frac{Assets}{Equity}}_{\text{leverage}}$$

**Repricing gap.** For rate-sensitive assets (RSA) and liabilities (RSL) over a horizon:

$$GAP=RSA-RSL\qquad\Delta NII\approx GAP\times\Delta r$$

**Duration gap.** With assets $A$, liabilities $L$, $k=L/A$, durations $D_A,D_L$:

$$\Delta EVE\approx-\big(D_A-k\,D_L\big)\cdot A\cdot\frac{\Delta y}{1+y}$$

**Capital and liquidity ratios:**

$$CET1\text{ ratio}=\frac{CET1\text{ capital}}{RWA}\qquad LCR=\frac{HQLA}{\text{Net 30-day outflows}}\ge100\%$$

**RAROC.** Risk-adjusted return on capital compares profit after expected loss with the capital held against unexpected loss:

$$RAROC=\frac{\text{Revenue}-\text{Costs}-\text{Expected loss}}{\text{Economic capital}}$$

A business line creates value when $RAROC$ exceeds the cost of equity.

## Worked examples

**NIM.** Interest income 50, interest expense 20, average earning assets 600: $NIM=30/600=\mathbf{5.0\%}$.

**DuPont.** Net income / revenue $=20\%$, revenue / assets $=5\%$, assets / equity $=10$: $ROE=0.20\times0.05\times10=\mathbf{10\%}$. A bank's high ROE comes mostly from leverage, which is why regulators impose capital floors.

**Repricing gap.** RSA $=400$, RSL $=500$ over 1 year: $GAP=-100$. If rates rise 1%: $\Delta NII\approx-100\times0.01=\mathbf{-1}$ (million). This bank is liability-sensitive and loses when rates rise.

**Duration gap.** $A=1\text{,}000$, $L=900$, $D_A=4$, $D_L=2$, $y=5\%$, $\Delta y=+1\%$: $k=0.9$ and $D_A-kD_L=4-1.8=2.2$, so

$$\Delta EVE\approx-2.2\times1\text{,}000\times\frac{0.01}{1.05}=\mathbf{-\$20.95}$$

On equity of \$100 this is a **21% loss from a 1% rise in rates**, a vivid illustration of leverage plus duration mismatch.

**Capital and liquidity.** CET1 capital 12 and RWA 100: ratio $=12\%$. HQLA 150 and net outflows 120: $LCR=125\%$.

**RAROC.** Per \$100 loan: interest income 7.5, funding 3.5, operating cost 1.0, expected loss 0.8 gives profit 2.2. With \$10 of economic capital: $RAROC=2.2/10=\mathbf{22\%}$, above a 10% cost of equity, so the loan creates value.

## Classic case: the savings and loan crisis and Silicon Valley Bank

Both episodes (see Chapter 4) are textbook examples of the duration gap formula above: assets with long duration funded by short, rate-sensitive liabilities. The lesson that regulators and risk managers took from both is to measure EVE and NII sensitivity to rate shocks routinely (IRRBB) and to hold sufficient liquid assets (LCR) so that deposit outflows do not force the sale of bonds at a loss.

## In a bank

- **Treasury / ALM** runs gap, duration and NII simulations, and uses swaps to adjust sensitivity.
- **Finance** uses **funds transfer pricing (FTP)** so each product is charged for the funding it uses, which reveals true profitability by product.
- **Risk** sets capital and liquidity limits, and produces CET1, LCR and NSFR reports.
- **Model risk management** (US guidance SR 11-7) requires every model, including credit scorecards and VaR, to be validated independently. The **three lines of defence** are the business, risk and compliance oversight, and internal audit.

## Common mistakes

Reading NIM alone (it can rise while credit quality deteriorates); ignoring deposit behaviour (deposits may not reprice when rates move, or may leave); treating held-to-maturity securities as if they had no market risk; using RAROC without a consistent capital allocation.

## Practice problems

1. Interest income 80, interest expense 35, average earning assets 900. Find NIM.
2. RSA 600, RSL 450. Find the gap and the change in NII for a 2% rate rise.
3. Net income / revenue 18%, revenue / assets 6%, assets / equity 12. Find ROE.
4. Assets 2,000, liabilities 1,800, $D_A=5$, $D_L=1.5$, $y=4\%$, rates up 1%. Find $\Delta EVE$ and compare with equity.

# Appendix A: Answers to Practice Problems

**Chapter 1.** (1) $5\text{,}000/1.08^4=\$3\text{,}675.15$. (2) $(1.01)^{12}-1=12.68\%$. (3) Rule of 72: $72/9=8$ years; exact $\ln2/\ln1.09=8.04$ years. (4) $50/0.05=\$1\text{,}000$.

**Chapter 2.** (1) $250\text{,}000\times\dfrac{0.07/12}{1-(1+0.07/12)^{-180}}=\$2\text{,}247.07$. (2) First-month interest $=100\text{,}000\times0.005=\$500$ (so \$99.55 is principal). (3) The balance stays high for longer, so interest accrues on a larger amount for twice as many months.

**Chapter 3.** (1) See the table: \$1,136.83. (2) $NPV=400\times\frac{1-1.1^{-3}}{0.1}-1000=994.74-1000=-\$5.26$ (slightly negative; reject). Payback $=2.5$ years. (3) IRR is a percentage and ignores the scale of cash flows: a small project with a high IRR can create less total value than a large project with a lower IRR.

**Chapter 4.** (1) $1\text{,}000/1.05^5=\$783.53$. (2) $-7\times0.005+\tfrac12\times60\times0.005^2=-3.5\%+0.075\%=-3.43\%$. (3) $f=1.04^2/1.03-1=5.01\%$.

**Chapter 5.** (1) $\sigma_m^2=0.04$, so $\beta=0.045/0.04=1.125$. (2) $3\%+1.5\times6\%=12\%$. (3) $\alpha=14-[3+1.2(10-3)]=+2.6\%$.

**Chapter 6.** (1) $0.0081+0.0100+0.0036=0.0217$. (2) If $\rho=1$, $\sigma_p$ is the weighted average of volatilities (no diversification benefit). If $\rho=-1$ and $\sigma_1=\sigma_2$ with equal weights, risk is zero. (3) Expected-return estimates differ slightly across assets, and the optimiser exploits those differences; this is estimation error, which is why constraints are used.

**Chapter 7.** (1) $5\text{,}000\text{,}000\times2.326\times0.02=\$232\text{,}600$. (2) ES is the average of the losses beyond VaR, all of which are at least as large as VaR. (3) 8 exceptions is in the **yellow** zone (5 to 9), which can trigger a capital multiplier increase and a model review.

**Chapter 8.** (1) \$2,700. (2) 8.74%. (3) $Z=2.20$, grey zone. (4) PD rises: higher volatility makes it more likely that asset value falls below debt (the distance to default $DD$ falls). Equity holders benefit from the extra volatility, as with an option; lenders do not.

**Chapter 9.** (1) $r_e=3+1.1\times6=9.6\%$; $WACC=0.8(9.6\%)+0.2(5\%)(0.7)=7.68\%+0.70\%=8.38\%$. (2) $EV=\$2\text{,}084.81$; equity $=2\text{,}084.81-400+100=\$1\text{,}784.81$. (3) $2/(0.10-0.04)=\$33.33$ when \$2 is next year's dividend $D_1$. (4) The terminal value captures all cash flows after the forecast window, which usually extends for decades, and it is discounted only by the forecast length; it is also highly sensitive to $WACC-g$.

**Chapter 10.** (1) $8/\sqrt{10\text{,}000}=\$0.08$. (2) Four times as many simulations. (3) Expected price $50e^{0.10}=\$55.26$; median $50e^{0.10-0.045}=\$52.83$.

**Chapter 11.** (1) $45/900=5.0\%$. (2) $GAP=+150$; $\Delta NII=150\times0.02=+3$. (3) $0.18\times0.06\times12=12.96\%$. (4) $k=0.9$, $D_A-kD_L=5-1.35=3.65$; $\Delta EVE=-3.65\times2\text{,}000\times0.01/1.04=-\$70.19$. Equity is $200$, so the loss is about 35% of equity.

# Appendix B: Reading List

**Core textbooks**

- Brealey, R., Myers, S., Allen, F. *Principles of Corporate Finance*. McGraw-Hill. (NPV, CAPM, WACC, capital structure.)
- Ross, S., Westerfield, R., Jaffe, J. *Corporate Finance*. McGraw-Hill.
- Bodie, Z., Kane, A., Marcus, A. *Investments*. McGraw-Hill. (CAPM, portfolio theory.)
- Fabozzi, F. *Bond Markets, Analysis and Strategies*. Pearson. (Bonds, duration, mortgages.)
- Hull, J. *Options, Futures, and Other Derivatives*; and *Risk Management and Financial Institutions*. Wiley/Pearson.
- Saunders, A., Cornett, M. *Financial Institutions Management: A Risk Management Approach*. McGraw-Hill. (ALM, duration gap, bank capital.)
- Saunders, A., Allen, L. *Credit Risk Measurement*. Wiley.
- Bessis, J. *Risk Management in Banking*. Wiley.
- Koch, T., MacDonald, S. *Bank Management*. Cengage.
- Jorion, P. *Value at Risk: The New Benchmark for Managing Financial Risk*. McGraw-Hill.
- Koller, T., Goldhaber, M., Wessels, D. *Valuation: Measuring and Managing the Value of Companies* (McKinsey). Wiley.
- Damodaran, A. *Investment Valuation*. Wiley.
- Glasserman, P. *Monte Carlo Methods in Financial Engineering*. Springer.

**Foundational papers and books**

- Fisher, I. (1930). *The Theory of Interest*.
- Williams, J. B. (1938). *The Theory of Investment Value*.
- Macaulay, F. (1938). *Some Theoretical Problems Suggested by the Movements of Interest Rates, Bond Yields and Stock Prices in the United States since 1856*. NBER.
- Markowitz, H. (1952). "Portfolio Selection." *Journal of Finance*.
- Redington, F. M. (1952). "Review of the Principles of Life-Office Valuations." *Journal of the Institute of Actuaries*.
- Modigliani, F., Miller, M. (1958). "The Cost of Capital, Corporation Finance and the Theory of Investment." *American Economic Review*.
- Sharpe, W. (1964). "Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk." *Journal of Finance*.
- Altman, E. (1968). "Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy." *Journal of Finance*.
- Merton, R. (1974). "On the Pricing of Corporate Debt: The Risk Structure of Interest Rates." *Journal of Finance*.
- Artzner, P., Delbaen, F., Eber, J.-M., Heath, D. (1999). "Coherent Measures of Risk." *Mathematical Finance*.
- DeMiguel, V., Garlappi, L., Uppal, R. (2009). "Optimal Versus Naive Diversification: How Inefficient Is the 1/N Portfolio Strategy?" *Review of Financial Studies*.

**Case-study and narrative books**

- Lewis, M. *The Big Short* (2010). (Subprime mortgages and the 2008 crisis.)
- Lowenstein, R. *When Genius Failed* (2000). (LTCM and the limits of risk models.)
- Taleb, N. *The Black Swan* (2007). (Rare events and model risk.)
- Graham, B., Dodd, D. *Security Analysis* (1934); Graham, B. *The Intelligent Investor* (1949). (Intrinsic value and margin of safety.)
- Siegel, J. *Stocks for the Long Run*. (Long-run asset returns.)
