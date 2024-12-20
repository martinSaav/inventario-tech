[![Python application](https://github.com/martinSaav/inventory-management/actions/workflows/python-app.yml/badge.svg)](https://github.com/martinSaav/inventory-management/actions/workflows/python-app.yml)

# Inventory management

This [repository](https://github.com/martinSaav/inventory-management) contains a Python-based inventory management system.

## Table of Contents
- [Introduction](#introduction)
- [Contributors](#contributors)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Introduction

This project aims to provide a simple and efficient way to manage inventories. It includes basic functionality to add, update, and remove items from the inventory.

## Contributors
- [Martín Alejandro Estrada Saavedra](https://github.com/martinSaav)

## Features

- Add items to the inventory
- Update items in the inventory
- Remove items from the inventory
- List all items in the inventory
- Search for items in the inventory
- List all items whose quantity is below a certain threshold

## Installation

### Prerequisites
- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

To install the inventory manager, you can clone this repository and run the following command:

1. Clone the repository:
   ```bash
   git clone https://github.com/martinSaav/inventory-management.git
   ```
2. Navigate to the project directory:
   ```bash
   cd inventory-management
    ```
3. Create a virtual environment:
    ```bash
    virtualenv .venv
    ```
4. Activate the virtual environment:
    ```bash
    source .\.venv\Scripts\activate 
    ```
5. if it doesn't work then try this command

    ```bash
    source ./.venv/bin/activate 
    ```
   
5. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. To run the inventory manager, use the following command:
    ```bash
    python app.py
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.