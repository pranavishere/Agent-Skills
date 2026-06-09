# Supply Chain Manager Codex Package

This workspace now contains a project-scoped Codex agent and three underlying skills for analyzing a hypothetical inventory database.

## Agent

Agent file:

`../../.codex/agents/supply-chain-manager.toml`

Agent name:

`supply-chain-manager`

Display concept:

`Supply Chain Manager`

Use it with prompts like:

```text
Spawn the supply-chain-manager agent to analyze the hypothetical inventory database and identify SKU-level stockout risk.
```

```text
Use the supply-chain-manager agent to recommend regional inventory transfers and replenishment quantities.
```

## Skills

Skill folders:

- `../../.agents/skills/inventory-sku-risk`
- `../../.agents/skills/regional-inventory-balance`
- `../../.agents/skills/supply-chain-optimization-insights`

Skill responsibilities:

- `inventory-sku-risk`: SKU, brand, state, warehouse, depletion forecast, stockout risk, and replenishment recommendations.
- `regional-inventory-balance`: East/West/North/South inventory trends, coverage, transfer opportunities, and region-level recommendations.
- `supply-chain-optimization-insights`: broader insights for lean inventory, safety stock tuning, working capital, forecast quality, and data quality.

## Hypothetical Data

Data folder:

`./data`

Files:

- `inventory_monthly.csv`: 325 rows across 25 months at state-warehouse-SKU grain.
- `sku_brand_pricing.csv`: 13 SKU/state/warehouse pricing and brand mapping rows.
- `depletion_forecast.csv`: 156 forward-looking forecast rows with planned receipts, coverage, risk, and replenishment measures.
- `state_region.csv`: state-to-region mapping.
- `date_dimension.csv`: month-end and fiscal calendar mapping.

## Validation

Local validation script:

`../../work/validate_supply_chain_manager.py`

Run from the workspace root:

```powershell
python .\work\validate_supply_chain_manager.py
```
