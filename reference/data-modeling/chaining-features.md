# Chaining features

Features are reusable. This means it is possible to create robust data pipelines within Lynk - by adding  features to an entity, based on features of other (related) entities.

{% hint style="info" %}
Common challenges in data modeling are questions like "how should I model this?" and "was this done before, somewhere else?"

Lynk takes care of such challenges by providing a structured way to model data (defining features on entities via YAML files), governing it with the [Governance](../governance.md) layer and making it all accessible via the Studio interface.
{% endhint %}

## Virtual data assets

[Virtual data assets](data-assets/#virtual-data-assets) are data assets that live "virtually" within Lynk. Meaning, there is no materialized asset on the underlying data source. **A virtual data assets is created for each entity within Lynk**, where the entity is the "asset" and it's features are the "fields".&#x20;

## Creating features from related entities

For example, let's assume we have an entity called `user` and another entity called `team`, and their relation is many-to-one. You can create a feature called `is_active_user` on the `user` level and consume it for creating a metric feature `active_users_count` on the `team` entity level.&#x20;

```yaml
# user.yml (virtual data asset)

asset: user
...

measures:
- name: active_users_count
  description: count of active users
  sql: SUM(IFF({is_active_user} = true, 1, 0))
```

```yaml
# team.yml (team entity)
...
features: 

- type: metric
  name: active_users_count
  asset: user
  field: active_users_count
  filters: null
```

{% hint style="info" %}
Note that the `asset` in this case is the related entity name (see [related entities](entities/related-entities.md)).
{% endhint %}

***

