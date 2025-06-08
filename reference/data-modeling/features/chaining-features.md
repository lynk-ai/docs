# Chaining features

Features are reusable.\
It is possible to create features on an entity, based on features of another (related) entity. This makes it possible to create robust data pipelines within Lynk - from raw data to final KPIs.

{% hint style="info" %}
Chaining features is a critical component in Lynk's design.

Within Lynk everything is Semantically important, from raw data to final KPIs, making the whole data pipeline well defined centrally, structured, governed and highly accessible for AI not only to ask questions but also to build new features and semantic definitions on the fly.
{% endhint %}

## Virtual data assets

[Virtual data assets](../data-assets/#virtual-data-assets) are data assets that live "virtually" within Lynk. Meaning, there is no materialized asset on the underlying data source. **A virtual data assets is created for each entity within Lynk**, where the entity is the "asset" and it's features are the "fields".

## Creating features from related entities

For example, let's assume we have an entity called `user` and another entity called `team`, and their relation is many-to-one. You can create a feature called `is_active_user` on the `user` level and consume it for creating a metric feature `active_users_count` on the `team` entity level.

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
Note that the `asset` in this case is the related entity name (see [related entities](../relationships/related-entities.md)).
{% endhint %}

***
