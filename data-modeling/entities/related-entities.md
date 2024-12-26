# Related Entities

Entities can relate to other entities. \
For example, `customers` can relate to `orders`, where each customer may have many orders.&#x20;

Lynk stores all entity relationships in one place - `entities_relationships.yml` file, to ensure DRY  pattern and consistency.

```
// .lynk/default/entities_relationships.yml

relationships:
  
  customer-nation:
    relationship: many-to-one
    joins:
    - name: direct_on_nation_id
      default: true
      type: fields
      fields:
      - source: nation_id
        destination: nation_id
        operator: equal

  customer-device:
    relationship: one-to-one
    joins:
    - name: direct_on_customer_id
      default: true
      type: sql
      sql: '{source}.customer_id = {destination}.customerid'
    - name: lookup_via_team
      default: false
      type: lookup
      lookup:
      - type: fields
        destination: db.schema.team
        fields:
        - source: nation_id
          destination: nation_id
          operator: equal
      - type: sql
        destination: device
        sql: sql: '{source}.device_id = {destination}.device_id'       
```



### Relation (customer-order)

### Relationship

### joins









## bi-directional relationships

## Types of joins

### Direct join

### Lookup join

Sometimes entities relate to each other not directly, but via a loopup table. \
For example:&#x20;

customer.nation\_id = nation.nation\_id

Examples of entity relations usage:

* Creating fratures:



and \
nation.region\_id = region.region\_id





