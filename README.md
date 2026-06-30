# 🎯 BountyScout

Automated GitHub bounty scanner — runs **hourly** via GitHub Actions, surfaces new paid bounty issues, and pings you once per bounty via GitHub Issues, Telegram, or Discord.

Forked from [dev-kp-eloper/BountyScout](https://github.com/dev-kp-eloper/BountyScout) and tuned for Web3 / hackathon ecosystems (Hedera, Celo, Stacks, Base, Mantle, LangChain).

---

## How It Works

1. **Scheduled trigger** — GitHub Actions cron fires at `0 * * * *` (top of every hour).
2. **Scouts GitHub** — Runs ~13 search queries across generic bounty keywords and Web3-specific terms.
3. **Triages candidates** — Skips PRs, already-assigned issues, overcrowded threads (>25 comments), and spam keywords.
4. **Deduplicates** — Compares against `seen_bounties.json`; only surfaces truly new entries.
5. **Notifies** — Dispatches via your configured channel(s).
6. **Persists state** — Commits updated `seen_bounties.json` back to the repo so you never get duplicates.

---

## Setup

### 1. Fork / create this repo

Push all three files to a new GitHub repo:

```
BountyScout/
├── .github/
│   └── workflows/
│       └── bounty-scout.yml
├── scout_bounties.py
├── seen_bounties.json
└── README.md
```

### 2. Choose your notification channel

#### Option A — GitHub Issues (zero config, recommended)
The built-in `GITHUB_TOKEN` handles everything. Watch your repo and you'll get a native GitHub push notification per scan.

#### Option B — Telegram
1. Message `@BotFather` → `/newbot` → copy the **API Token**
2. Send a message to your bot, then open `https://api.telegram.org/botTOKEN/getUpdates` and copy the numeric `chat.id`
3. Add repo secrets:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

#### Option C — Discord
1. Channel Settings → Integrations → Webhooks → Create Webhook → copy URL
2. Add repo secret: `DISCORD_WEBHOOK_URL`

### 3. Trigger manually to test

Actions tab → **Scout Active Bounties Hourly** → **Run workflow**

---

## Search Keywords

The scanner runs these query groups by default:

| Category | Queries |
|---|---|
| Generic | `bounty`, `reward bounty`, `paid PR bounty`, `Opire bounty` |
| Web3 | `HBAR bounty`, `Hedera bounty`, `Celo bounty`, `Stacks bounty`, `Base bounty`, `Mantle bounty` |
| Dev tooling | `hackathon prize TypeScript`, `LangChain/LangGraph bounty`, `grant open source good first issue` |

Edit `SEARCH_QUERIES` in `scout_bounties.py` to add or remove terms.

---

## Spam Filters

Issues are dropped if they contain any of: `airdrop`, `referral`, `casino`, `gambling`, `trading bot`, `blog post`, `article writing`, `tutorial proposal`, `content creator`, `phishing`, `spam`, `scam`, or match known farming patterns (honeypot tasks, star-gating bots).

Additional filters:

| Filter | What it blocks |
|---|---|
| **Title blocklist** | Meta scan digests (`Bounty Alert`, `New Opportunit…`), support tickets (`account recovery`) |
| **Label blocklist** | `bounty-alert`, `honeypot-task` |
| **Repo blocklist** | Known farming repos, `pypi/support`, other `*/bountyscout` forks |

Edit `BLOCKLIST`, `TITLE_BLOCKLIST`, `LABEL_BLOCKLIST`, and `REPO_BLOCKLIST` in `scout_bounties.py` to tune.

### Disable GitHub Issue alerts

If hourly issue creation is too noisy (see #100), keep Telegram/Discord and set:

```yaml
env:
  BOUNTYSCOUT_GITHUB_ISSUES: "0"
```

in `.github/workflows/bounty-scout.yml`.
