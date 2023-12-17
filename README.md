
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
  pip install requirements.txt
  ```



<!-- USAGE EXAMPLES -->
## Usage
Navigate into root folder: ../sacuce_demo_test
* To run all test cases (with a txt file as log, names "output_final.txt"): 
```sh
   pytest -v -s > output_final.txt
  ```
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


<p align="right">(<a href="#readme-top">back to top</a>)</p>



