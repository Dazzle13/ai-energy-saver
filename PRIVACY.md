# Privacy & Data Contribution

**Local by default.**  
The library does not send data anywhere unless a user explicitly opts in.

## What may be collected (opt-in only)
- Aggregated, anonymised features (e.g., 30-minute bins, kWh mean/std, peak ratios, tariff buckets)
- Optional coarse region (e.g., GB-LND) chosen by the user
- Client version and schema version for reproducibility

**Never collected:**
- Names
- Emails
- Exact addresses
- Raw social handles
- Raw unbinned timestamps tied to identity

## Transport & Storage
- TLS for transfer  
- Encrypted at rest using managed keys  
- Schema validation and range checks on ingest  

## Retention
- Short retention for raw uploads (if any)  
- Aggregated features retained per data minimisation policy  

## Opt-out & Deletion
- Users can choose not to contribute  
- For deletion requests, contact `deep12650` or `justkarnaa` with an export key or anonymised token
