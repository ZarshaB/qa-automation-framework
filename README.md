# qa-automation-portfolio

![Tests](https://github.com/ZarshaB/qa-automation-framework/actions/workflows/run-tests.yml/badge.svg)

> Selenium (Python) automation framework built using Page Object Model pattern and pytest. Tests run automatically on every push via GitHub Actions CI/CD.

---

## 📁 Project Structure

```
qa-automation-portfolio/
├── pages/
│   ├── __init__.py
│   └── login_page.py       # Page Object for the Login page
├── tests/
│   ├── __init__.py
│   └── test_login.py       # Login test scenarios (4 tests + parametrized)
├── conftest.py             # Browser setup and teardown (pytest fixture)
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🧪 Test Scenarios Covered

| Test | Scenario | Expected Result |
|------|----------|----------------|
| test_successful_login | Valid credentials | Redirected to inventory page |
| test_login_with_wrong_password | Wrong password | Error message shown |
| test_locked_out_user | Locked account | Locked out error shown |
| test_login_with_empty_fields | No credentials entered | Validation error shown |
| test_login_validation_scenarios | 3 data-driven scenarios | Parametrized with pytest |

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **Automation:** Selenium WebDriver
- **Test Framework:** pytest
- **Pattern:** Page Object Model (POM)
- **CI/CD:** GitHub Actions
- **Browser:** Chrome (via webdriver-manager)

---

## ⚙️ How to Run

**1. Clone the repo**
```bash
git clone https://github.com/YOUR-USERNAME/qa-automation-portfolio.git
cd qa-automation-portfolio
```

**2. Install dependencies**
```bash
pip3 install -r requirements.txt
```

**3. Run all tests**
```bash
pytest tests/ -v
```

**4. Run a specific test**
```bash
pytest tests/test_login.py::test_successful_login -v
```

---

## 📦 Requirements

```
selenium
pytest
webdriver-manager
```
