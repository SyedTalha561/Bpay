# PROJECT WORKFLOW & GITHUB SYNC RULES

## 1. Project-Specific Repositories
Every project in this workspace is organized into its own dedicated GitHub repository under account `SyedTalha561`:
- **Bpay** -> `git@github.com:SyedTalha561/Bpay.git` (Repository: https://github.com/SyedTalha561/Bpay)
- **Adelaide Metro** -> Dedicated Adelaide Metro repository under `SyedTalha561`
- Other projects -> Dedicated repository per project name

## 2. Mandatory Automatic GitHub Sync Rule
- Whenever any code, asset, documentation, or configuration change is made in a project, the updated code MUST be immediately staged, committed with a descriptive message, and pushed to its respective GitHub repository.
- No changes should remain unsynced or uncommitted.
- The sync script `./sync_github.sh` can be executed at any time to guarantee 100% sync integrity.
