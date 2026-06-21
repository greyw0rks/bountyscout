# ... (truncated) ...

    # ── GitHub Issue (zero-config, uses built-in GITHUB_TOKEN) ───────────────
    if github_token and repo_fullname:
        issue_title = f"🎯 Bounty Alert: {count} New Opportunities — {now_str}"
        issue_body  = f"### Bounty Scan Results\n\n**Scan Time:** {now_str}\n\n"
        for i, b in enumerate(new_bounties, 1):
            issue_body += (
                f"#### {i}. [{b['title']}]({b['url']})\n"
                f"- **Repo:** [{b['repo']}](https://github.com/{b['repo']})\n"
                f"- **Comments:** {b['comments']}\n"
                f"- **Last Updated:** {b['updated_at']}\n\n"
            )
        create_github_issue(repo_fullname, github_token, issue_title, issue_body)

    save_seen_bounties(seen_urls)
    print("💾 State saved.")


if __name__ == "__main__":
    main()
