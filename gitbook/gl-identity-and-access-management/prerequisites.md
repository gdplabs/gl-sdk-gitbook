---
icon: circle-exclamation
---

# Prerequisites

Before you begin building with GL IAM, ensure your environment is ready.

{% stepper %}
{% step %}
**Python 3.11+**

Make sure you have [Python](https://www.python.org/downloads/) v3.11 or v3.12 installed along with [pip](https://pip.pypa.io/en/stable/installation/).

```bash
python --version

# Python 3.11.x or Python 3.12.x
```
{% endstep %}

{% step %}
**Poetry**

Install [Poetry](https://python-poetry.org/docs/#installation) for dependency management.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```
{% endstep %}

{% step %}
**Access to GDP Labs' GL SDK Repository**

Access to the private repository is required. Submit a ticket to [ticket@gdplabs.id](mailto:ticket@gdplabs.id) or request via this [form](https://docs.google.com/forms/d/e/1FAIpQLScJxB-Xe9YjnohIzW6nic-_AeSJob6Il6spl1s85wc76tQkzQ/viewform).
{% endstep %}

{% step %}
**Choose Your Identity Provider**

{% tabs %}
{% tab title="PostgreSQL" %}
**Requirements:**

* [PostgreSQL](https://www.postgresql.org/) database (v13+)
* Database connection credentials
{% endtab %}

{% tab title="Stack Auth" %}
**Requirements:**

* [Stack Auth](https://stack-auth.com/) project
* Project ID, Publishable Client Key (`pck_...`), Secret Server Key (`sk_...`)

**Environment Variables:**

```bash
STACK_AUTH_BASE_URL=https://api.stack-auth.com
STACK_AUTH_PROJECT_ID=your-project-id
STACK_AUTH_PUBLISHABLE_CLIENT_KEY=pck_...
STACK_AUTH_SECRET_SERVER_KEY=sk_...
```
{% endtab %}

{% tab title="Keycloak" %}
**Requirements:**

* [Keycloak](https://www.keycloak.org/) server (v18.0+)
* Realm, Client ID, Client Secret

**Environment Variables:**

```bash
KEYCLOAK_SERVER_URL=https://keycloak.your-domain.com
KEYCLOAK_REALM=your-realm
KEYCLOAK_CLIENT_ID=your-client-id
KEYCLOAK_CLIENT_SECRET=your-client-secret
```
{% endtab %}
{% endtabs %}
{% endstep %}
{% endstepper %}

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fprerequisites).
{% endhint %}
