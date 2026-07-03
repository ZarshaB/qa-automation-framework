// ============================================================
// FILE: saucedemo.cy.js
// PURPOSE: Test Login + Add to Cart on https://www.saucedemo.com
// AUTHOR: You! (A QA engineer learning Cypress 🎉)
// HOW TO RUN: npx cypress open  →  click this file
// ============================================================


// ---------------------------------------------------------------
// 💡 CYPRESS CONCEPT: describe()
//    Think of describe() as a "folder" or "group" for your tests.
//    It helps organise related tests together.
//    First argument = the name of the group (just a label for you).
//    Second argument = a function containing your tests.
// ---------------------------------------------------------------
describe('Saucedemo - Login & Add to Cart', () => {


  // -------------------------------------------------------------
  // 💡 CYPRESS CONCEPT: beforeEach()
  //    This block runs BEFORE every single test (it/test block).
  //    Perfect for setup steps that every test needs — like
  //    visiting the page. This way you don't repeat yourself.
  // -------------------------------------------------------------
  beforeEach(() => {
    // cy.visit() → opens the URL in the Cypress browser
    cy.visit('https://www.saucedemo.com')
  })


  // =============================================================
  // TEST 1: Successful Login
  // =============================================================
  // 💡 CYPRESS CONCEPT: it()
  //    Each it() block is ONE test case.
  //    The string describes what the test is checking.
  //    Think of it like writing a sentence: "It should..."
  // =============================================================
  it('should log in successfully with valid credentials', () => {

    // ----------------------------------------------------------
    // STEP 1: Find the username input and type into it
    //
    // cy.get() uses CSS selectors — the same ones you use in CSS!
    //   '#user-name'  →  finds element with id="user-name"
    //   '.btn_action' →  finds element with class="btn_action"
    //
    // .type() → simulates a user typing into that field
    // ----------------------------------------------------------
    cy.get('#user-name').type('standard_user')

    // STEP 2: Find the password input and type the password
    cy.get('#password').type('secret_sauce')

    // ----------------------------------------------------------
    // STEP 3: Click the Login button
    //
    // .click() → simulates a mouse click on the element
    // ----------------------------------------------------------
    cy.get('#login-button').click()

    // ----------------------------------------------------------
    // STEP 4: Assert we landed on the right page
    //
    // 💡 CYPRESS CONCEPT: cy.url() + .should()
    //    cy.url() grabs the current browser URL.
    //    .should('include', '...') checks that the URL contains
    //    the text '/inventory.html' — proving login worked.
    //
    //    should() is your ASSERTION tool. You'll use it constantly.
    //    Common assertions:
    //      .should('exist')          → element is on the page
    //      .should('be.visible')     → element is visible
    //      .should('include', 'text')→ string contains something
    //      .should('have.text', 'x') → element text equals 'x'
    // ----------------------------------------------------------
    cy.url().should('include', '/inventory.html')

    // STEP 5: Double-check the page header is visible
    // This confirms we're truly on the Products page
    cy.get('.title').should('have.text', 'Products')

  })


  // =============================================================
  // TEST 2: Login with wrong password (Negative Test)
  //
  // 💡 QA TIP: Always test the "sad path" too!
  //    A good QA engineer doesn't just test what SHOULD work —
  //    they test what should FAIL and make sure it fails properly.
  // =============================================================
  it('should show an error message with invalid credentials', () => {

    cy.get('#user-name').type('standard_user')
    cy.get('#password').type('wrong_password')
    cy.get('#login-button').click()

    // Assert the error message container appears
    // cy.get() with a class selector: finds element with that class
    cy.get('[data-test="error"]')
      .should('be.visible')
      .and('contain', 'Username and password do not match')
    //
    // 💡 NOTE: .and() is just another .should() chained on.
    //    You can chain as many assertions as you want!

  })


  // =============================================================
  // TEST 3: Add a product to the cart
  //
  // This test:
  //   1. Logs in first (because you can't shop without logging in)
  //   2. Clicks "Add to cart" on the first product
  //   3. Checks the cart badge shows "1"
  // =============================================================
  it('should add a product to the cart', () => {

    // --- LOGIN FIRST ---
    // We need to log in before we can reach the products page
    cy.get('#user-name').type('standard_user')
    cy.get('#password').type('secret_sauce')
    cy.get('#login-button').click()

    // Wait until we're on the inventory page before continuing
    cy.url().should('include', '/inventory.html')

    // ----------------------------------------------------------
    // STEP: Click the "Add to cart" button for the first product
    //
    // 💡 CYPRESS CONCEPT: .first()
    //    If multiple elements match your selector (e.g. there are
    //    6 "Add to cart" buttons), .first() grabs just the first one.
    //
    //    Other useful ones:
    //      .last()      → last matching element
    //      .eq(2)       → element at index 2 (zero-based)
    //      .contains()  → find by visible text (see below)
    // ----------------------------------------------------------
    cy.get('.btn_inventory').first().click()

    // ----------------------------------------------------------
    // STEP: Assert the cart badge now shows "1"
    //
    // The little red number circle on the cart icon is the "badge".
    // After adding 1 item, it should display the number 1.
    // ----------------------------------------------------------
    cy.get('.shopping_cart_badge')
      .should('be.visible')
      .and('have.text', '1')

  })


  // =============================================================
  // TEST 4: Add a SPECIFIC product by name
  //
  // 💡 CYPRESS CONCEPT: cy.contains()
  //    Instead of using a CSS selector, you can find elements
  //    by the TEXT they contain. Super useful when selectors
  //    are complex or unreliable.
  //
  //    cy.contains('Add to cart') → finds the element with that text
  // =============================================================
  it('should add "Sauce Labs Backpack" to the cart by product name', () => {

    // Login
    cy.get('#user-name').type('standard_user')
    cy.get('#password').type('secret_sauce')
    cy.get('#login-button').click()
    cy.url().should('include', '/inventory.html')

    // ----------------------------------------------------------
    // Find the product card for "Sauce Labs Backpack"
    // then find the Add to Cart button WITHIN that card only.
    //
    // 💡 CYPRESS CONCEPT: .parents() / scoping with .within()
    //    cy.contains('.inventory_item', 'Sauce Labs Backpack')
    //    → finds the inventory_item div that contains that text
    //
    //    .find() → search for a child element within a parent
    // ----------------------------------------------------------
    cy.contains('.inventory_item', 'Sauce Labs Backpack')
      .find('button')
      .click()

    // Assert cart badge shows 1
    cy.get('.shopping_cart_badge').should('have.text', '1')

    // ----------------------------------------------------------
    // BONUS: Navigate to the cart and verify the item is there
    // ----------------------------------------------------------
    cy.get('.shopping_cart_link').click()

    cy.url().should('include', '/cart.html')

    // Check the product name appears in the cart
    cy.get('.cart_item').should('contain', 'Sauce Labs Backpack')

  })


  // =============================================================
  // TEST 5: Add multiple items and verify cart count
  //
  // 💡 This shows how Cypress tests read almost like plain English
  // =============================================================
  it('should add two products and show count of 2 in cart', () => {

    // Login
    cy.get('#user-name').type('standard_user')
    cy.get('#password').type('secret_sauce')
    cy.get('#login-button').click()
    cy.url().should('include', '/inventory.html')

    // Add first product
    cy.get('.btn_inventory').eq(0).click()  // eq(0) = first item (index 0)

    // Add second product
    cy.get('.btn_inventory').eq(1).click()  // eq(1) = second item (index 1)

    // Cart badge should now show 2
    cy.get('.shopping_cart_badge')
      .should('be.visible')
      .and('have.text', '2')

  })

})


// ============================================================
// 🎓 WHAT YOU LEARNED IN THIS FILE:
//
//   describe()     → Groups related tests together
//   it()           → One individual test case
//   beforeEach()   → Runs setup before every test
//   cy.visit()     → Opens a URL
//   cy.get()       → Finds elements by CSS selector
//   cy.contains()  → Finds elements by visible text
//   .type()        → Types into an input field
//   .click()       → Clicks an element
//   .should()      → Makes an assertion (the CHECK)
//   .and()         → Chains a second assertion
//   .first()       → Grabs first matching element
//   .eq(n)         → Grabs element at index n
//   .find()        → Finds a child within a parent element
//   cy.url()       → Gets the current page URL
//
// NEXT STEPS TO EXPLORE:
//   - cy.intercept()  → Mock/stub API calls
//   - cy.fixture()    → Load test data from JSON files
//   - cy.wrap()       → Wrap values for Cypress chaining
//   - Custom commands → Reuse login as cy.login()
// ============================================================
