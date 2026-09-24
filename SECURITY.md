# Security

**Report vulnerabilities privately** via GitHub security advisories on this repo. Do not open public issues for them.

## Model

- **No private keys in this repo, in env files, or on the robot.** The treasury is meant to be a multisig; automation proposes, humans approve. The live signing path is not implemented.
- **Dry-run by default.** Spending requires `cycle.dry_run: false` **and** `PEPEBOT_LIVE=true`, and even then every spend path throws `LiveExecutionDisabled` in this build.
- **Kill switch.** If the file at `guardrails.kill_switch_file` exists, the cycle halts before reading anything and the robot goes to HALT.
- **Caps.** `max_sol_per_cycle`, `max_slippage_bps`, `reserve_sol`.
- **Robot is output-only.** It authenticates to the backend with `BOT_TOKEN` and can only receive emote frames.
- **Ingest is authenticated** with `INGEST_TOKEN`. Change both default tokens before exposing the backend anywhere.
- `contracts/programs/*` is an unaudited draft. Do not deploy it.
