# Governance

Lynk makes sure your data model stays trusted, clean and efficient by applying governance rules on top of it's structure [data modeling framework](data-modeling/).

## Governance Rules&#x20;

Below you can find the list of governance rules

| Rule                                   | Applied to | More details                          |
| -------------------------------------- | ---------- | ------------------------------------- |
| Contexts have unique names             | Contexts   |                                       |
| Entities have unique names             | Entities   |                                       |
| Entities have unique Key data asset    | Entities   |                                       |
| Entity key asset validation            | Entities   | no duplications, no missing instances |
| Entities do not share the same aliases | Entities   |                                       |
| Features have unique names             | Features   | On context level                      |
| Features have unique definitions       | Features   | On context level                      |
| Unique measure definitions             | Measures   | On data asset level                   |

