# 08 · “Else” and the two Browsy chips

> Two labels in the public diagram are ambiguous. This note explains them and
> proposes wording; it does not change the model.

## “Else”

In the decentral diagram, **Else** is a dashed chip below Authy. It was added
to represent **everything outside the flove loop**: other websites, native
apps, or services that still sign through Authy.

Today it has:

- no data model,
- no owner,
- no class,
- no index page.

So it reads like a product but is a catch-all. Two honest options:

| Option | What it means | Consequence |
|---|---|---|
| **Define it** | **Else = non-flove web/apps that use Authy for signing and keep their records L** | Add a short definition and a link; keep the chip |
| **Retire it** | Remove the chip; “Else” was only a diagram device | Simpler model; the diagram loses the “outside flove” branch |

**Decided 2026-11-18:** retire the “Else” chip (O24=B). The decentral diagram
now removes the chip and its Authy→Else arrow.

## Two Browsy chips

The diagram shows **Browsy twice**:

1. **Browsy below Authy** — the **entry**: the extension popup/content bridge
   the user opens, which hands identity to Authy and exposes the page bridge.
2. **Browsy bottom-right** — the **host**: the vault, Local records, Wizy and
   the peer-facing side. Peers pull from this side.

They are the same product, not two apps. The duplicate label is what confuses.

### Decided 2026-11-18

Label them by role in the decentral index chips too:

- **Browsy entry** — popup, bridge, “open Authy”.
- **Browsy host** — vault, records, groups, Wizy, peer pulls.

The two chips are the same extension; the labels make the roles explicit.

### Why it matters

- A reader may think there are two extensions.
- The vocabulary audit already flagged “Browsy product vs Browsy index vs
  Browsy extension”.
- The spec uses **Browsy** for the product and **Browsy extension** for the
  MV3 artifact; the diagram should not invent a third meaning.

## Proposed wording

- **Browsy** — the product.
- **Browsy extension** — the installed MV3/Firefox artifact.
- **Browsy entry** — the popup/bridge role.
- **Browsy host** — the vault/records/Wizy role.
- **Browsy index** — the static info page.

## Open

- None for the diagram; the chips now read **Browsy entry** / **Browsy host**
  and the Else chip is removed.
- If a non-flove branch is needed later, define it then; it is retired now.
