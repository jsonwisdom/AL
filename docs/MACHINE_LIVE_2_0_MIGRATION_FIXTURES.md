# Machine LIVE 2.0 Fixture Migration

Status: OPERATOR_COMMAND_READY
Repo: jsonwisdom/AL
Branch: master

Jay rule:

```text
Schema is National
Fixtures State
Secrets Personal
```

## Correct action

Move **state fixtures only** from the scaffold repo into the AL repo.

Do not move secrets.
Do not move wallet material.
Do not move personal/private records.

## Command

Run from Cloud Shell:

```bash
cd ~

# Get source scaffold if it does not already exist
if [ ! -d layered-proofing-state-level-alms ]; then
  git clone https://github.com/jsonwisdom/layered-proofing-state-level-alms.git
fi

# Get AL if it does not already exist
if [ ! -d AL ]; then
  git clone https://github.com/jsonwisdom/AL.git
fi

cd ~/AL
git checkout master
git pull --ff-only

# Copy state fixtures only
mkdir -p fixtures
cp -R ~/layered-proofing-state-level-alms/fixtures/* fixtures/

# Safety check: show what is moving
git status --short

# Commit
git add fixtures
git commit -m "migrate: state fixtures into AL for Machine LIVE 2.0"
git push
```

## Expected result

After push, GitHub Actions should run in:

```text
https://github.com/jsonwisdom/AL/actions
```

Expected generated outputs:

```text
alms/national/national_root_ci_latest.json
alms/anchors/runtime/github_direct_anchor_state.json
```

## Boundary

This migration is the body/data move.

National schema stays national.
State fixtures stay state.
Personal secrets stay off GitHub.
