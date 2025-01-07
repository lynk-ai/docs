# Git

## Code-first

Everything built on Lynk translates to code and is version controlled, even if built via the Studio.\
Apply coding best practices, CI/CD and tests to semantics definitions - while letting business users and analysts move fast.

## Connecting a Git repository

Connecting a Git repository is done on the onboarding process.&#x20;

<figure><img src="../../.gitbook/assets/image (1) (1).png" alt=""><figcaption><p>Connecting a Git repository on the onboarding process</p></figcaption></figure>

Once connected, Lynk will work with this repository to save the project files.&#x20;

***

## Working with Git

Adding and editing things like entities, features, measures and any other semantic definition to your Lynk project is done on a Git branch and needs to go through a Git PR (Pull Request) in order to be merged to the main brach (HEAD) of your repository.

### Working with YAML files as code

If you are working with YAML files to add and edit semantic definitions, make sure you're working with the right branch to commit your changes via your IDE (eg VScode) and once your changes are ready, It is recommended to create a PR for review with another data team member, and then merge those changes to the main branch (Production).

### Working with the Studio

If you are working with Lynk Studio to add and edit semantic definitions, you can choose the branch on the top bar when the Studio is on **edit mode**. When creating changes and additions using **edit mode**, Lynk Studio automatically commits those changes to the branch you are on. Once created a PR which is merged to your repository's main branch, you will be able to see those changes on the main branch as well.&#x20;

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption><p>On the top bar, you can switch to edit mode and choose a branch to work on</p></figcaption></figure>

In the above example we are on edit mode, using the branch `dev`.

***

## Freedom to create

Working with Git enables users like Analysts create business logic (e.g features) on the Studio, without being dependent on Data Engineers (or Analytics Engineers) - and then test it and consume it using the [branch](../consume-and-apis/sql-api.md#branch) option on the [`USE`](../consume-and-apis/sql-api.md#use) configuration block of the SQL API.

While this process enables freedom and working with fast iterations,  with less cross-team dependencies and less ad hoc requests to the DE team, Data Engineers still stay in focus on what's changing and/or added to the Source of truth - with Git version control capabilities.&#x20;

