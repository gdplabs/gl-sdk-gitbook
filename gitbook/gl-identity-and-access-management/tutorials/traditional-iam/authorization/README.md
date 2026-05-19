---
icon: shield-check
---

# Authorization

Tutorials for controlling what authenticated users can access.

{% hint style="info" %}
Learn the concepts first? See [Introduction to GL IAM.](../../../introduction-to-gl-iam.md)
{% endhint %}

## Roles vs Permissions

<figure><img src="../../../../.gitbook/assets/GL IAM - Roles vs Permission.png" alt=""><figcaption></figcaption></figure>

## When to Use

| Question                         | Check                      | Example                         |
| -------------------------------- | -------------------------- | ------------------------------- |
| "Can user access admin panel?"   | **Role**                   | `has_standard_role(ORG_ADMIN)`  |
| "Can user delete this document?" | **Permission**             | `has_permission("docs:delete")` |
| "Can user view billing?"         | **Role** or **Permission** | Depends on granularity          |

## Role Hierarchy

Higher roles automatically include lower role permissions.

## Tutorials

| Topic       | Tutorial                            | What You'll Learn                        |
| ----------- | ----------------------------------- | ---------------------------------------- |
| Roles       | [Standard Roles](standard-roles.md) | `has_standard_role()` with hierarchy     |
| Permissions | [Permissions](permissions.md)       | `has_permission()`, `has_all`, `has_any` |

***

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url\&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Fauthorization).
{% endhint %}
