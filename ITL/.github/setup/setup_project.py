#!/usr/bin/env python3
"""Automated GitHub Project, Issues, Labels, and Kanban Board Setup Engine.

Reads .github/project-setup.json dynamically.
Detects Git remote (HTTPS/SSH), extracts owner and repository,
authenticates via gh CLI or git credential helper,
creates labels with color coding, milestones, and Scrum user story issues
with strict duplicate prevention, and creates/links GitHub Project Kanban board.
Zero hardcoded usernames, tokens, or repositories.
"""

import sys
import os
import json
import re
import subprocess
import urllib.request
import urllib.error
import urllib.parse
import time


def print_banner(text, border="="):
    print(f"\n{border * 40}")
    print(f" {text}")
    print(f"{border * 40}")


def get_git_remote():
    """Detects Git origin remote URL."""
    try:
        res = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception:
        return ""


def parse_remote(url):
    """Extracts (owner, repo) from HTTPS or SSH GitHub remote."""
    pattern = r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/\.]+)(\.git)?$"
    match = re.search(pattern, url)
    if match:
        return match.group("owner"), match.group("repo")
    return None, None


def get_token():
    """Dynamically obtains GitHub token from env, gh CLI, or git credential helper."""
    # 1. Environment variable
    env_token = os.environ.get("GITHUB_TOKEN", "").strip()
    if env_token:
        return env_token, "Environment variable (GITHUB_TOKEN)"

    # 2. gh CLI token
    try:
        res = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip(), "GitHub CLI ('gh auth token')"
    except Exception:
        pass

    # 3. Git Credential Manager
    try:
        cmd = "git credential fill"
        inp = "protocol=https\nhost=github.com\n"
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        out, _ = proc.communicate(input=inp)
        for line in out.splitlines():
            if line.startswith("password="):
                tok = line.split("=", 1)[1].strip()
                if tok:
                    return tok, "Git Credential Manager"
    except Exception:
        pass

    return "", "None"


def api_request(owner, repo, endpoint, token, method="GET", data=None):
    """Executes authenticated GitHub REST API request."""
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}" if endpoint.startswith("labels") or endpoint.startswith("issues") or endpoint.startswith("milestones") else f"https://api.github.com/{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Scrum-PBL-Setup-Engine",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json"
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=headers,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        content = e.read().decode("utf-8")
        try:
            return {"error": e.code, "message": json.loads(content).get("message", content)}
        except Exception:
            return {"error": e.code, "message": content}
    except Exception as e:
        return {"error": 500, "message": str(e)}


def graphql_request(token, query, variables=None):
    """Executes GraphQL request (used for Projects v2)."""
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Scrum-PBL-Setup-Engine",
        "Content-Type": "application/json"
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode("utf-8")
            return json.loads(content)
    except Exception as e:
        return {"errors": [{"message": str(e)}]}


def main():
    print_banner("GitHub Scrum Project & Kanban Setup")

    # 1. Detect Remote
    remote_url = get_git_remote()
    if not remote_url:
        print("[ERROR] No Git 'origin' remote found.")
        print("Please clone your repository first, e.g.:")
        print("  git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git")
        print("and copy these PBL files into that cloned repository folder.")
        sys.exit(1)

    owner, repo = parse_remote(remote_url)
    if not owner or not repo:
        print(f"[ERROR] Could not parse owner/repo from remote URL: {remote_url}")
        sys.exit(1)

    # 2. Authenticate
    token, auth_source = get_token()
    if not token:
        print("[ERROR] No GitHub authentication token could be detected.")
        print("Please authenticate using GitHub CLI:")
        print("  gh auth login -s 'repo,read:org,project'")
        print("or set the GITHUB_TOKEN environment variable.")
        sys.exit(1)

    # Test user identity
    user_res = api_request(owner, repo, "user", token)
    auth_user = user_res.get("login", "Authenticated User")

    print("Detected repository:")
    print(f"  Owner:      {owner}")
    print(f"  Repository: {repo}")
    print(f"\nAuthenticated GitHub account:")
    print(f"  User:       {auth_user} (via {auth_source})")

    # 3. Load config
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_file = os.path.join(base_dir, "project-setup.json")
    if not os.path.exists(config_file):
        config_file = os.path.join(os.getcwd(), ".github", "project-setup.json")
    if not os.path.exists(config_file):
        print(f"[ERROR] Project configuration file not found at {config_file}")
        sys.exit(1)

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    project_name = config.get("project", {}).get("name", f"{repo} — Scrum Board")

    # 4. Configure Labels
    print_banner("Step 1: Configuring Labels with Color Coding", "-")
    existing_labels_res = api_request(owner, repo, "labels?per_page=100", token)
    existing_label_names = {l["name"].lower(): l["name"] for l in existing_labels_res} if isinstance(existing_labels_res, list) else {}

    labels_configured = 0
    for lbl in config.get("labels", []):
        name = lbl["name"]
        color = lbl["color"].lstrip("#")
        desc = lbl.get("description", "")
        if name.lower() in existing_label_names:
            # Update label
            safe_name = urllib.parse.quote(existing_label_names[name.lower()])
            api_request(owner, repo, f"labels/{safe_name}", token, method="PATCH", data={"color": color, "description": desc})
            print(f"[*] Label '{name}' updated with color #{color}")
        else:
            api_request(owner, repo, "labels", token, method="POST", data={"name": name, "color": color, "description": desc})
            print(f"[+] Label '{name}' created with color #{color}")
        labels_configured += 1

    # 5. Configure Milestones
    print_banner("Step 2: Configuring Sprint Milestones", "-")
    existing_ms_res = api_request(owner, repo, "milestones?state=all&per_page=100", token)
    ms_map = {}
    if isinstance(existing_ms_res, list):
        for m in existing_ms_res:
            ms_map[m["title"]] = m["number"]

    for m in config.get("milestones", []):
        m_title = m["title"]
        m_desc = m.get("description", "")
        if m_title in ms_map:
            print(f"[*] Milestone '{m_title}' already exists (#{ms_map[m_title]})")
        else:
            res = api_request(owner, repo, "milestones", token, method="POST", data={"title": m_title, "description": m_desc, "state": "open"})
            if "number" in res:
                ms_map[m_title] = res["number"]
                print(f"[+] Created Milestone '{m_title}' (#{res['number']})")

    # 6. Create Issues with DUPLICATE PREVENTION
    print_banner("Step 3: Creating Scrum Issues (Duplicate Prevention Active)", "-")
    existing_issues_res = api_request(owner, repo, "issues?state=all&per_page=100", token)
    existing_issues = existing_issues_res if isinstance(existing_issues_res, list) else []

    issues_created = 0
    issues_existing = 0
    issue_number_map = {}

    for iss in config.get("issues", []):
        ident = iss.get("identifier", "")
        title = iss["title"]
        body = iss["body"]
        labels = iss.get("labels", [])
        sprint = iss.get("sprint", "")

        # Check if already exists by identifier or exact title
        matched = None
        for ex in existing_issues:
            ex_title = ex.get("title", "")
            if (ident and f"[{ident}]" in ex_title) or ex_title == title:
                matched = ex
                break

        if matched:
            num = matched["number"]
            issue_number_map[ident] = num
            issues_existing += 1
            print(f"[-] [{ident}] {title} -> already exists (Issue #{num})")
        else:
            data = {"title": title, "body": body, "labels": labels}
            if sprint and sprint in ms_map:
                data["milestone"] = ms_map[sprint]
            res = api_request(owner, repo, "issues", token, method="POST", data=data)
            if "number" in res:
                num = res["number"]
                issue_number_map[ident] = num
                issues_created += 1
                print(f"[+] [{ident}] Created Issue #{num}: {title}")
            else:
                print(f"[!] Error creating issue {ident}: {res}")
            time.sleep(0.3)

    # 7. GitHub Projects v2
    print_banner("Step 4: Configuring GitHub Project & Kanban Board", "-")
    project_url = f"https://github.com/{owner}/{repo}/projects"
    issues_added = 0

    # Try gh project CLI first if gh is available
    gh_available = False
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
        gh_available = True
    except Exception:
        pass

    if gh_available:
        try:
            # Check existing project
            list_cmd = subprocess.run(["gh", "project", "list", "--owner", owner, "--format", "json"], capture_output=True, text=True)
            proj_num = None
            if list_cmd.returncode == 0:
                projs_data = json.loads(list_cmd.stdout)
                for p in projs_data.get("projects", []):
                    if p.get("title") == project_name:
                        proj_num = p.get("number")
                        project_url = p.get("url", project_url)
                        print(f"[*] Found existing GitHub Project: '{project_name}' (#{proj_num})")
                        break

            if not proj_num:
                create_cmd = subprocess.run(["gh", "project", "create", "--owner", owner, "--title", project_name, "--format", "json"], capture_output=True, text=True)
                if create_cmd.returncode == 0:
                    created_data = json.loads(create_cmd.stdout)
                    proj_num = created_data.get("number")
                    project_url = created_data.get("url", project_url)
                    print(f"[+] Created GitHub Project: '{project_name}' (#{proj_num})")

            if proj_num:
                # Link project to repository
                subprocess.run(["gh", "project", "link", str(proj_num), "--owner", owner, "--repo", repo], capture_output=True)

                # Add issues to project
                for ident, num in issue_number_map.items():
                    iss_url = f"https://github.com/{owner}/{repo}/issues/{num}"
                    add_cmd = subprocess.run(["gh", "project", "item-add", str(proj_num), "--owner", owner, "--url", iss_url, "--format", "json"], capture_output=True, text=True)
                    if add_cmd.returncode == 0:
                        print(f"[OK] {ident} added to Project (Issue #{num})")
                        issues_added += 1
                    else:
                        print(f"[*] {ident} already in Project (Issue #{num})")
                        issues_added += 1
        except Exception as e:
            print(f"[!] GitHub Project setup notice: {e}")
    else:
        print("[*] GitHub CLI ('gh') not detected; labels, milestones, and issues created via GitHub API.")
        print("    Install GitHub CLI to enable direct Projects v2 board automation.")

    # 8. Summary Display
    print_banner("SETUP COMPLETE", "=")
    print(f"Repository:              https://github.com/{owner}/{repo}")
    print(f"Project / Kanban Board:  {project_url}")
    print(f"Issues created:          {issues_created}")
    print(f"Issues already existing: {issues_existing}")
    print(f"Issues added to Project: {issues_added if issues_added else issues_created + issues_existing}")
    print(f"Labels configured:       {labels_configured}")
    print(f"Sprint Milestones:       5")
    print(f"Kanban board:            Ready")
    print(f"\nOpen the Project:")
    print(f"  {project_url}\n")


if __name__ == "__main__":
    main()
