Feature: Login
  As a user of SauceDemo
  I want to log in with my credentials
  So that I can access the inventory page

  Background:
    Given I am on the SauceDemo login page

  Scenario: Successful login with valid credentials
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be redirected to the inventory page

  Scenario Outline: Login attempts with invalid or edge-case credentials
    When I log in with username "<username>" and password "<password>"
    Then I should see the error message "<expected_error>"

    Examples: Invalid credentials
      | username        | password        | expected_error                                                          |
      | invalid_user    | secret_sauce    | Epic sadface: Username and password do not match any user in this service |
      | standard_user   | wrong_password  | Epic sadface: Username and password do not match any user in this service |
      | locked_out_user | secret_sauce    | Epic sadface: Sorry, this user has been locked out.                      |

  Scenario Outline: Login attempts with missing fields
    When I log in with username "<username>" and password "<password>"
    Then I should see the error message "<expected_error>"

    Examples: Empty fields
      | username      | password     | expected_error                          |
      |               | secret_sauce | Epic sadface: Username is required      |
      | standard_user |              | Epic sadface: Password is required      |
