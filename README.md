# SCN API security lab files

Files for the API Security and Secrets Management lab in UFCFLC-30-2 Secure Computer Networks
at UWE Bristol. Follow the lab worksheet on Blackboard.

On the UWEcyber VM, clone this repository into your home folder, then clone the API repository
inside it as `vulnerable-api`:

```bash
cd ~
git clone https://github.com/plumpmonkey/scn-api-lab.git
cd scn-api-lab
git clone https://github.com/plumpmonkey/scn-notes-api.git vulnerable-api
```

| Folder or file | What it is |
|----------------|------------|
| `vulnerable-api/` | The notes service, cloned from [scn-notes-api](https://github.com/plumpmonkey/scn-notes-api). Its git history is part of the exercise. |
| `checkpoints/` | Copies of `app.py` as it should look at three points in Tasks 2–4, for when you get stuck. |
| `trufflehog-extension/` | A sample file for Extension 1. |
| `SETUP.md` | Setup and troubleshooting. |

**The secrets in both repositories are fake.** They were put there on purpose for the lab and do
not work anywhere.
