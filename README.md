# EAF Raw Material Value-in-Use (VIU) Model

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2.3-black.svg)](https://nextjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-red.svg)](https://flask.palletsprojects.com/)

## Table of Contents

- [Introduction](#introduction)
  - [Project Goals](#project-goals)
  - [What is Value-in-Use (VIU)?](#what-is-value-in-use-viu)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Step-by-Step Guide](#step-by-step-guide)
  - [Example Workflow](#example-workflow)
- [Technical Details](#technical-details)
  - [Thermodynamics and Process Modeling](#thermodynamics-and-process-modeling)
  - [Key Assumptions and Limitations](#key-assumptions-and-limitations)
- [For Future Software Development](#for-future-software-development)
  - [Code Structure and Extensibility](#code-structure-and-extensibility)
  - [Potential Enhancements](#potential-enhancements)
- [Financial Analysis Improvements](#financial-analysis-improvements)
  - [Current Financial Capabilities](#current-financial-capabilities)
  - [Advanced Financial Extensions](#advanced-financial-extensions)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments and References](#acknowledgments-and-references)
- [Contact](#contact)

## Introduction

The **EAF Raw Material Value-in-Use (VIU) Model** is an open-source tool designed to assist steelmakers, procurement specialists, and process engineers in optimizing raw material selection for Electric Arc Furnace (EAF) steelmaking. Built with a Next.js frontend and a Python (Flask) backend, the model computes the holistic economic value of raw materials (e.g., scrap, DRI, pig iron, hot metal) by accounting for their downstream impacts on EAF operations. This goes beyond simple purchase prices to include process credits (e.g., energy from oxidation) and penalties (e.g., flux needs, yield losses, residual dilution).

The tool enables side-by-side comparisons of two materials, with an optional blended summary, generating a tabular output similar to the provided example image. It is grounded in thermodynamic principles, mass and energy balances, and empirical data from steelmaking literature, making it a strategic asset for cost minimization while adhering to quality and operational constraints.

### Project Goals

The primary objectives of this tool are:

1. **Optimize Charge Mixes:** Provide a data-driven framework to minimize the total cost per net ton (NT) of liquid steel by evaluating raw material blends.
2. **Facilitate Material Comparisons:** Allow users to compare low-cost, high-residual scraps against premium alternatives (e.g., prime DRI), quantifying trade-offs in energy, yield, and residuals.
3. **Support Decision-Making:** Aid procurement in negotiating based on true value, engineers in process tweaks, and analysts in forecasting costs.
4. **Promote Sustainability and Efficiency:** Highlight energy credits from chemical reactions and penalties from inefficiencies, encouraging low-carbon feeds like DRI or hot metal.
5. **Enable Extensibility:** Serve as a foundation for future enhancements, such as integration with real-time plant data or advanced financial modeling.

Secondary goals include educational value (explaining EAF thermodynamics) and reproducibility (open-source code for community contributions).

### What is Value-in-Use (VIU)?

Value-in-Use (VIU) is a comprehensive economic evaluation methodology that quantifies the total impact of a raw material on a production process, extending beyond its market price. In EAF steelmaking, VIU adjusts the purchase cost by incorporating:

- **Process Credits:** Positive contributions, such as chemical energy from oxidizing elements (e.g., Si, C, Al) that reduce electrical energy demand.
- **Process Penalties:** Negative impacts, like increased flux consumption for gangue neutralization, yield losses to slag, dilution costs for residuals (e.g., Cu, Sn), or productivity delays from refining impurities (e.g., P, S).

The VIU formula is typically:

\[ \text{VIU Cost/NT} = \frac{\text{Purchase Cost} + \text{Process Penalties} - \text{Process Credits}}{\text{Yield Factor}} \]

Where:
- **Yield Factor** normalizes to cost per net ton of usable liquid steel.
- Examples: A high-Si scrap might offer energy credits but incur flux penalties; high-Cu scrap requires expensive dilution with clean DRI.

VIU transforms procurement from cost-minimization to value-maximization, enabling smarter decisions in volatile markets. For instance, a $450/ton DRI might have a lower VIU than $350/ton scrap due to better yield and lower residuals.

## Features

- **User-Friendly Web Interface:** A Next.js-based interface for adding materials, setting parameters, and visualizing comparisons.
- **Material Database:** Dynamically add and store raw materials with detailed compositions (e.g., %Fe, %C, gangue oxides, residuals).
- **Blended Summaries:** Compare two materials side-by-side with a weighted blend, auto-diluting for residuals using a prime feed (e.g., DRI).
- **VIU Calculations:** Physics-based modeling of energy credits, flux/slag penalties, yield losses, oxygen costs, and residual dilutions, all handled by a Python backend.
- **Output Table:** Color-coded credits (green) and penalties (red), plus metrics like yield %, slag volume, and residual %.
- **Customization:** Adjustable operational costs, targets (e.g., basicity, MgO saturation), and assumptions (e.g., preheating credits).
- **Export and Visualization:** Potential for downloading results as CSV and adding charts for cost breakdowns.
- **Validation:** Incorporates empirical models for cross-checking predictions.

## Installation

This tool requires Node.js and Python 3.8+.

1. **Clone the Repository:**
   ```
    https://github.com/your-repo/eaf-viu-model.git
   cd eaf-viu-model
   ```

2. **Install Frontend Dependencies:**
   Create a virtual environment (recommended):
   ```
   npm install

   ```
   Install packages:
   ```
   pip install streamlit pandas numpy
   ```

3. **Install Backend Dependencies:**
   Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   Install packages:

   ```
   pip install -r requirements.txt
   ```

4. **Run the App:**
   In one terminal, start the Next.js frontend:

   ```
   npm run dev
   ```

  In another terminal, start the Flask backend:
   ```
   flask --app api/app run
   ```



Open http://localhost:3000 in your browser.

**System Requirements:**
- OS: Windows, macOS, Linux.
- RAM: 4GB+ for large datasets.

## Usage

### Running the Application

After installation, launch the frontend and backend in separate terminals as described above. The app will be available at http://localhost:3000.

### Step-by-Step Guide

1. **Set Operational Parameters:**
- Input costs (e.g., electricity $0.07/kWh), targets (e.g., max 0.10% Cu), and options (e.g., enable preheating).
- Define a prime diluent for residuals (e.g., DRI at $450/ton).

2. **Add Raw Materials:**
- Use the form to input material details (name, price, % compositions, gangue, etc.).
- Add at least two (e.g., "Low-Cost Scrap" with high Cu, "Prime DRI" with low residuals).

3. **Compare Materials:**
- Select two materials and a blend ratio (e.g., 50% each).
- Click "Compute VIU Summary" to generate the table.

4. **Interpret Results:**
- The table shows columns for each material and the blend.
- Green: Credits (e.g., Energy Credit from oxidation).
- Red: Penalties (e.g., Copper Dilution if exceeding target).
- Blue highlight: VIU Cost/NT (key metric).

### Example Workflow

- **Scenario:** Compare $350/ton scrap (0.4% Cu, 0.025% P) vs. $450/ton DRI (0.01% Cu, 0.008% P) at 50% blend.
- **Inputs:** Set targets (0.10% Cu max), add materials.
- **Output:** The table will show the scrap's high dilution penalty versus the DRI's, along with the blended VIU and yield.
- **Insight:** Despite its higher base price, the DRI's VIU may be lower due to the absence of a dilution penalty and better yield.

## Technical Details

### Thermodynamics and Process Modeling

The model is rooted in EAF thermodynamics, using mass/energy balances to simulate melting/refining. Key aspects:

- **Mass Balance:** Tracks inputs (charge, fluxes, O2) to outputs (steel, slag, off-gas). Oxidation reactions form slag components (e.g., Si + O2 → SiO2, ΔH = -910.9 kJ/mol). Empirical FeO% (10-30%) estimates yield losses: Yield = 100 - (FeO% × slag mass / charge).

- **Energy Balance:** Total input ~500-800 kWh/ton. Credits from exothermic reactions (e.g., C to CO/CO2 at -110.5/-393.5 kJ/mol, efficiency 80%). Penalties for slag heating (0.6 kWh/kg) and gangue reduction. Post-combustion recovers 30% of CO energy. Hot feeds (e.g., 1400°C metal) add ~0.4 kWh/°C/ton credit.

- **Residual Handling:** Auto-dilutes Cu/Sn with prime feed: Dilution ratio = (actual - target) / (actual - prime level). Penalty = ratio × prime price.

- **Productivity:** Tap-to-tap time = base + charging (density-based) + refining (excess C/P/S, limited to 0.1% C/min to avoid splashing).

- **Equations:**
- Energy Credit: \( E = \frac{-\Delta H \times m / M_w \times \eta}{3600} \) kWh.
- Slag Flux: Required CaO = basicity × SiO2 - gangue CaO.
- VIU Normalization: Cost/NT = Total Cost / (Yield / 100).

The model assumes steady-state equilibrium, calibrated from papers (e.g., Pfeifer/Kirschen balances, Jones VIU).

### Key Assumptions and Limitations

- **Steady-State:** No kinetics; assumes instant equilibrium at tap.
- **Efficiencies:** Chemical 80%, post-combustion 30%, useful energy 65% (adjustable by scrap type).
- **Fixed Ratios:** Dolo-lime 60% CaO/40% MgO; 70% CO/30% CO2 in C oxidation.
- **Yield/FeO:** Empirical (20% base, adjusted by slag vol/C); Fe-dominant (ignores minor alloys).
- **Residuals:** Only Cu/Sn diluted; P/S as flat penalties (customizable).
- **Limitations:** No real-time integration; no CO2 emissions; assumes 100-ton furnace (scalable).

## For Future Software Development

### Code Structure and Extensibility

- **Modular Design:** Core functions (e.g., `compute_viu`) are separate from the API; easy to add reactions by extending constants/calculations.
- **Data Flow:** The frontend manages the UI state, while the backend handles calculations and data storage (in-memory).
- **Extensibility Points:**
- Add elements: Extend the material form and the mass balance calculations.
- Dynamic Modeling: Integrate ODEs for time-varying reactions.
- API Integration: Fetch market prices via web APIs.
- ML Enhancements: Use machine learning for predictive yield from historical data.
- **Deployment:** The application is designed to be deployed on Vercel.

### Potential Enhancements

- **UI/UX:** Add charts for cost breakdowns; allow for multi-material blends; save/load configurations.
- **Advanced Physics:** Incorporate kinetic rates and full off-gas modeling.
- **Sustainability:** Calculate the carbon footprint of different material mixes.
- **Scalability:** Use a more robust database for storing materials and results.

## Financial Analysis Improvements

### Current Financial Capabilities

- **Core VIU:** Adjusts costs for operational impacts, outputting $/NT with breakdowns.
- **Sensitivity Analysis:** Tweak inputs to see the effects on the VIU; adjust blend ratios for optimization.

### Advanced Financial Extensions

- **NPV/ROI for Investments:** Add modules to evaluate the return on investment for capital expenditures.
- **Monte Carlo Simulations:** Model price volatility to understand risk.
- **Scenario Forecasting:** Integrate market data APIs for real-time price information.
- **Break-Even Analysis:** Determine the price thresholds at which different materials become economically viable.

## Contributing

Contributions are welcome! Fork the repository, create a feature branch, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments and References

- Inspired by the work of A. Abraham, S. Chen, H. Pfeifer, M. Kirschen, and J. Jones.
- Libraries: Next.js, React, Flask, pandas, numpy.
- Data Sources: Thermodynamic constants from NIST and engineering handbooks.

## Contact

For questions or feedback, please open an issue on GitHub.
