# 🧪 GithubOrgClient - Unit & Integration Tests

This project contains Python unit and integration tests for a GitHub API client.

---

## 📁 Files

- `client.py`: Main class `GithubOrgClient` that calls GitHub API
- `utils.py`: Utility functions
- `fixtures.py`: Sample test data for integration tests
- `test_client.py`: Unit and integration tests for `client.py`
- `test_utils.py`: Unit tests for `utils.py`

---

## ✅ What We Tested

### `utils.py`

- `access_nested_map`: Get values from nested dicts
- `get_json`: Fetch JSON from a URL (mocked)
- `memoize`: Caches method results

### `client.py`

- `org`: Fetch org info
- `_public_repos_url`: Get repos URL from org info
- `repos_payload`: Fetch list of repos
- `public_repos`: Get names of public repos (with optional license filter)
- `has_license`: Check if repo has a certain license

---

## 🔁 Integration Tests

- Mocked only external HTTP calls (`requests.get`)
- Used data from `fixtures.py`
- Tested:
  - `public_repos()`
  - `public_repos(license="apache-2.0")`

---

## ▶️ Run Tests

```bash
python -m unittest test_utils.py
python -m unittest test_client.py
