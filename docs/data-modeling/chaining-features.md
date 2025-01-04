# Chaining features

Features are reusable. You can use existing features to create new features on related entities.

{% hint style="info" %}
Each entity in Lynk has a virtual data asset
{% endhint %}



\[A diagram of chaining features]







In this case, the `asset` property should be the entity name. The rest of the feature properties remain the same as in creating field features from regular data assets.

{% hint style="info" %}
This is a powerful feature that allows creating robust ETLs with Lynk's well structured data modeling framework. See [chaining features](chaining-features.md) for in depth information about this.
{% endhint %}





### Creating features from related entities

Lynk supports creating features based on related entities.&#x20;

This means you can create features on one entity and then create features on another entity based on those previously created features.

For example, let's assume we have an entity called `user` and another entity called `team`, and their relation is many-to-one. You can create a feature called `is_active_user` on the `user` level and consume it for creating a metric feature `active_users_count` on the `team` entity level.&#x20;

{% hint style="info" %}
This allows building consistent, accessible and governed business logic - which is also very flexible in terms of [time aggregations](../consume-and-apis/time-aggregation.md).
{% endhint %}

See [chaining features](chaining-features.md) for in depth information about this.





See the below example:

```yaml
# customer.yml
features: 

- type: field
  name: team_name
  asset: team
  field: name
  filters: null
```

{% hint style="info" %}
The entity we refer to as `asset` has to be related to our entity (see [related entities](entities/related-entities.md)).
{% endhint %}

## Create metric features from related entities

In case of a creating a metric from a related entity, the entity name should be specified as the `asset`. The rest of the parameters remain the same as in creating metric features from regular data assets.

See the below example:

```yaml
# customer.yml
features: 

- type: metric
  name: total_
  asset: team
  field: name
  filters: null
```

{% hint style="info" %}
The entity we refer to as `asset` has to be related to our entity (see [related entities](entities/related-entities.md)).
{% endhint %}

***
