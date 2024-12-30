# First-Last



```yaml
# customer.yml
features: 
- asset: networx_prod.communications.phone_call_dim
  filters: null
  name: last_call_at
  type: first_last
  options:
    method: last
    sort_by: created_at
    field: created_at
```

