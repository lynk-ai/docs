# Related assets

Data assets are tables and views in your data warehouse. It can be from any layer - from raw data to aggregated&#x20;

```yaml
// customer.yml

name: customer

description:

key_table: demo_dev.tpch_sf1.customer

aliases: []

features: []

related_assets:
  demo_dev.tpch_sf1.customer:
    relationship: one-to-one
    joins:
    - name: all_customers
      default: true
      type: fields
      fields:
      - entity_field: customer_id
        asset_field: customer_id
        operator: equal

  demo_dev.tpch_sf1.orders:
    relationship: one-to-one
    joins:
    - name: all_orders
      default: true
      type: sql
      sql:  {source}.customer_id = {destination}.customer_id

  lynk.core.payment:
    relationship: one-to-one
    joins:
    - name: all_payments
      default: true
      type: lookup
      lookup:
      - type: sql
        destination: lynk.core.order
        sql: {source}.cust_id = {destination}.customer_id
      - type: fields
        destination: lynk.core.payment
        fields:
        - source_field: order_id
          destination_field: order_id
          operator: equal
    - name: successful_payments
      default: false
      type: lookup
      lookup:
      - type: sql
        destination: lynk.core.order
        sql: {source}.cust_id = {destination}.customer_id and {destination}.order_status = 'O'
      - type: fields
        destination: lynk.core.payment
        fields:
        - source_field: order_id
          destination_field: order_id
          operator: equal
```

