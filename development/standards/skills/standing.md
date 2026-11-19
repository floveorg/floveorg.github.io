# Standing rules — every flove skill

Read once; applies everywhere. A skill restates one only when it **deviates**.

1. **No browser, ever.** The owner opens the page. Verify with tooling and by
   reasoning through every interactive path you touched.
2. **No commit, push or deploy** unless the request or the active workflow says
   so. Skills edit the working tree; state what is left dirty.
3. **Inline surveys only.** Risky findings go to the agent's own question
   mechanism, batched into one coherent set. Never render an HTML form for a
   survey unless the owner invokes `/questy-html`.
4. **Headless** (subagent, batch, CI): never block. Write the survey as text,
   apply the navigation-preserving recommendation, and label those edits
   *"applied on recommendation — pending user confirmation"*.
5. **Overrides come from `https://flove.org/development/standards/skills/CONFIG.md`** (routes and
   keys). Each skill's defaults apply when no key is set.
6. **Secrets by location, never by value.** Name the file that holds the token
   (`~/agents/token-*.md`) and never print it.
7. **Coverage honesty.** A partial pass stated plainly beats a green claim that
   isn't true.
