# Related Entities

Entities can relate to to other entities.\
Lynk manages all entity relationships centrally in one file `entities_relationships.yml` , to ensure consistency and simplicity. You can add entity relations via code, directly to this YAML file, or via the Studio UI.

{% hint style="info" %}
Related entities will allow us to enrich an entity with features from other entities (see [chaining features](../chaining-features.md)), or to join entities via [SQL API](../../consume-and-apis/sql-api.md) and REST SQL API calls
{% endhint %}

***

### Simple entity-to-entity relation

In this example, the entity `nation` relates to the entity `customer` in a one-to-many relationship (a nation has many customers)

```yaml
# entities_relationships.yml

relationships:
  
  nation-customer:
    relationship: one_to_many
    joins:
    - name: nation_id
      default: true
      type: fields
      fields:
      - source: nation_id
        destination: nation_id
        operator: equal
```

### `Relationships`

This is where we define all of our entity-to-entity relationships in the `entities_relationships.yml` file

{% hint style="info" %}
A relationship should be defined once regardless of the direction (e.g `nation-customer` is the same relationship as `customer-nation`). Lynk will automatically reverse the direction when needed.
{% endhint %}

Define a relationship by adding an object `entity1-entity2`.\
In our example `nation-customer`, the direction is nation -> to -> customer.

Note that the direction applies to the `Relationship` parameter as well as to the `source` and `destination` parameters (see below)

### `Relationship`

Sets the `Relationship` type between the two entities, according to the direction. In the above example, the entity `nation` has a one-to-many relationship with the `customer` entity (A nation can have many customers, and a customer can have only one nation).

The options for the Relationship property are:

* `one_to_one`
* `one_to_many`
* `many_to_many`
* `many_to_one`

{% hint style="info" %}
Lynk will use the relationship property to suggest the correct entities when creating features. For example, when creating metrics, Lynk will only suggest related data assets and entities with a one\_to\_many relationship (as metrics are essentially aggregations)
{% endhint %}

### `Joins`

Define how the entities should be joined, by connecting features of the first (source) entity to features of the second (destination) entity.

### **`name` \[optional]**

Give the join path a name.

If you choose not to name a join path, lynk will automatically name as the join path as "default" followed by a number. For example, the first unnamed join path will be named by Lynk to `default_1`, the second to `default_2` etc..

Note that Join path `name` has to be unique on a related entity level.

{% hint style="info" %}
The `name` property will be used when creating features or when joining two entities via SQL/REST API. In case there is more than one join path between two entities, you will be able to tell Lynk how connect the two entities by using the join path `name`.
{% endhint %}

### **`default` \[optional]**

The `default` property takes boolean values (`true` / `false`).\
There can be only one default join path between two entities. Lynk will use the default join path, unless a name of another join path will be stated.

In case there is more than one join path between an entity and a data asset, setting the `default` property becomes mandatory.

### `type`

The `type` property tells Lynk which method to use for defining the join path.\
The options for `type` are:

* `sql`
* `fields`
* `lookup`

### `sql` (type)

Use sql code to define how the two entities are related.\
When setting `type: sql`, you will need to add the `sql` property with the SQL definition of the relation.

See the following example:

```yaml
# entities_relationships.yml

relationships:
  
  nation-customer:
    relationship: one_to_many
    joins:
    - name: nation_id
      default: true
      type: sql
      sql: "{source}.{nation_id} = {destination}.{nation_id}"
```

Using the `sql` type;

`{source}` refers to the first entity

`{destination}` refers to the second entity

In the above example, the relationship direction is nation-customer. So the `source` is nation and the `destination` is customer.

### `fields` (type)

A simple YAML-style to define how two entities are related.\
When setting `type: fields`, you will need to add the `fields` property with the fields and the operator that define the relation.

See the following example:

```yaml
# entities_relationships.yml

relationships:
  
  nation-customer:
    relationship: one_to_many
    joins:
    - name: nation_id
      default: true
      type: fields
      fields: 
      - source: nation_id
      - destination: nation_id
      - operator: equal
```

Using the `fields` type;

`{source}` refers to the first entity

`{destination}` refers to the second entity

`operator` defines the operator of the relation between the two fields.\
The options for the operator property are:

* equal
* gt
* gte
* lt
* lte

In the above example, the relationship direction is nation-customer. So the `source` is nation and the `destination` is customer.\
The entity nation has a feature `nation_id` which connects to the feature `nation_id` of the entity customer, using the operator `equal.`\
This translates to `nation.nation_id = customer.nation_id`

{% hint style="info" %}
Lynk supports multiple related fields from the source to the destination, enabling joins on more than one field when needed.
{% endhint %}

### `lookup` (type)

Sometimes the relation between two entities is not direct. Meaning, in order to connect two entities we have to join them via one or more lookup tables ("hops"). Lynk supports this scenario using the `lookup` join type.

See the below example:

```yaml
# entities_relationships.yml

relationships:

  customer-organization:
    relationship: many_to_one
    joins:
    - name: lookup_via_team
      default: true
      type: lookup
      lookup:
      - destination: db_prod.core.team
        type: sql
        sql: "{source}.{team_id} = {destination}.{team_id}"
      - destination: organization
        type: sql
        sql: "{source}.{organization_id} = {destination}.{id}"
```

In the above example, we connect the entity customer to the entity organization.\
Note that there is no direct connection between the two, and we have to join customer to db\_prod.core.team first and then join db\_prod.core.team to organization.

{% hint style="info" %}
When joining two entities via lookups there is no limit to the amount of lookups ("hops")
{% endhint %}

Using the `lookup` type;

As seen on the above code, lookups are an ordered list of steps;

* On the first step, `source` is always the first entity
* On the last step, `destination` is always the second entity
* The middle lookup assets should be data assets (not entities)

Inside each lookup step, we can define the connection between the source and destination, and choose how - using the `type` parameter as usual - `SQL` or `fields`
