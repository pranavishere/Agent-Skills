# Hypothetical Inventory Data Guide

Default sample dataset path: `outputs/supply-chain-manager/data`.

Use the same five data sources and measures as the `inventory-sku-risk` skill. Join `inventory_monthly.csv` to `state_region.csv` before regional aggregation. Calculate coverage and safety-stock measures at SKU grain first, then roll up to region.
