
<a name="readme-top"></a>


<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="sauce_logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Sauce Lab Test Demo</h3>

</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#tests">Tests</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is built using Python, PyTest, and Selenium frameworks to test a simple e-commercial demo page

Test cases:
* Login with valid and invalid credentials, also with locked out user
* Putting items into cart, removing them
* Checking out order
* Finalizing order, finish checkout




<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Python 3.9.0 or above
* Google Chrome
* install requirements.txt
  ```sh
  pip install requirements.txt pip install
  ```
* In case the ChromeDriver is not detected automatically, you can configure it using this page:
  https://www.browserstack.com/guide/run-selenium-tests-using-selenium-chromedriver



<!-- USAGE EXAMPLES -->
## Usage
Navigate into root folder: ../sacuce_demo_test
* To run all test cases (with a txt file as log, names "output_final.txt"): 
```sh
   pytest -v -s > output_final.txt --durations=0 
  ```
  Running all the tests takes about 13 minutes! A real log result can be found in the repository. (output_final_result.txt)

* To run only login page test cases (with a txt file as log, names "output_final.txt"): 
```sh
   pytest -k TestLoginPage -v -s  > output_final.txt
  ```
* To run only inventory page test cases (with a txt file as log, names "output_final.txt"): 
```sh
   pytest -k TestInventoryPage -v -s  > output_final.txt
  ```
* To run only cart page test cases (with a txt file as log, names "output_final.txt"): 
```sh
   pytest -k TestCartPage -v -s  > output_final.txt
  ```
* To run only checkout page test cases (with a txt file as log, names "output_final.txt"): 
```sh
   pytest -k TestCheckoutPage -v -s  > output_final.txt
  ```
* To run only checkout step two page test cases (with a txt file as log, names "output_final.txt"): 
```sh
   pytest -k TestCheckoutStepTwoPage -v -s  > output_final.txt
  ```

If pytest is not recognized, you can try running the tests with:
```sh
   python -m pytest 
  ```


## Tests
To run specific testcase, use -k flag with the name of the test. For example:
```sh
  pytest -v -s -k test_login_valid > output_final.txt --durations=0 
  ```
  This one above runs only the "test_login_valid" testcase


```sh
Login page  tests
```
#### Test fixture
  * Accessing login page
#### Connected tests
* test_login_valid: 
  * Testing if the login is successful if correct credentials are provided.
* test_login_invalid: 
  * Testing if login is declined if wrong credentials are provided.
* test_login_locked_out_user: 
  * Testing if locked out user is declined with correct error message.

```sh
Inventory page  tests
```
#### Test fixture
  * Accessing login page
  * Login with different users, then visit inventory page
#### Connected tests
* test_check_alignments_inventory_page: 
  * Testing if alignements are correct.
* test_add_to_cart_everything: 
  * Testing if all items are added to the cart.
* test_add_to_cart_some_element: 
  * Testing if selected items are added to the cart, and selected items are removed sucessfully.
* test_sort: 
  * Testing sort functionality.
* test_logout: 
  * Testing if loging out is successful.
* test_remove_item_from_item_page: 
  * Testing if selected item is removed from the cart.
* test_add_item_from_item_page: 
  * Testing if item is added to the cart (clicking add button from the item page).
* test_reset_state: 
  * Testing if cart is empty after resetting the state.
  


```sh
Cart page  tests
```
#### Test fixture
  * Accessing login page
  * Login with different users, then visit inventory page
  * Adding every item to cart
#### Connected tests
* test_continue_shopping: 
  * Testing if "Continue shopping" button navigates back to inventory page.
* test_remove_item_from_cart: 
  * Testing if item can be removed from cart.
* test_from_item_page_remove_item_from_cart: 
  * Testing if selected item can removed from cart (clicking remove button from the item page).
* test_checkout_cart: 
  * Testing id "Checkout" button navigates to checkout page.
* test_checkout2_cart_with_zero_elements: 
  * Testing if "Checkout" button is disabled in case cart is empty.
* test_check_alignments_cart_page: 
  * Testing if alignements are correct.


```sh
Checkout page  tests
```
#### Test fixture
  * Accessing login page
  * Login with different users, then visit inventory page
  * Adding every item to cart
  * Clicking "Checkout" button
* test_checkout_final: 
  * Testing if checkout is successful after providing correct data.

```sh
Checkout Step Two page  tests
```
#### Test fixture
  * Accessing login page
  * Login with different users, then visit inventory page
  * Adding every item to cart
  * Clicking "Checkout" button
  * Clicking "Continue" button to navigate to second checkout page
* test_check_total_price: 
  * Testing if sum of checkout items's prices are equal to final price .
* test_complete_order: 
  * Testing if checkout is finished successful after providing correct data.
* test_cancel_order:
  * Testing if clicking "Cancel" button navigates back to intentory page.





