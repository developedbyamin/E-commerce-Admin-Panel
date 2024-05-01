# E-commerce Admin Panel RESTful API

## Overview

This project aims to develop a RESTful API for the administrative panel of an e-commerce platform. The API manages various functionalities, including approving companies, adding other admin users, and handling authentication for companies and users.

## Objectives

1. **Company Approval**: Endpoints to allow admins to approve or reject companies that register on the platform.
2. **Admin Management**: Functionality to add and manage admin users.
3. **User and Company Authentication**: Registration and login endpoints for both companies and users.
4. **User Problem Posting**: Endpoints for users to post issues or problems regarding services or products.
5. **Problem Reviews**: Endpoints for admins to review, respond to, and manage user-submitted problems.

## Requirements

1. **Company Approval**
    - Endpoint to list all companies awaiting approval.
    - Endpoint to approve or reject a company.

2. **Admin Management**
    - Endpoint to create a new admin user.
    - Endpoint to list all admin users.

3. **User and Company Authentication**
    - Endpoints for user and company registration.
    - Endpoints for user and company login.

4. **User Problem Posting**
    - Endpoint for users to submit problems.
    - Endpoint to list all problems submitted by users.

5. **Problem Reviews**
    - Endpoint for admins to view all submitted problems.
    - Endpoints for admins to respond to or resolve problems.

## Setup

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask application:

    ```bash
    python app.py
    ```

## Usage

The API provides various endpoints to interact with the e-commerce administrative functionalities:

- `/companies/awaiting_approval`: GET endpoint to list all companies awaiting approval.
- `/companies/approve`: POST endpoint to approve a company.
- `/companies/reject`: POST endpoint to reject a company.
- `/admin/create`: POST endpoint to create a new admin user.
- `/admin`: GET endpoint to list all admin users.
- `/user/register`: POST endpoint to register a new user.
- `/user/login`: POST endpoint for user login.
- `/company/register`: POST endpoint to register a new company.
- `/company/login`: POST endpoint for company login.
- `/problems/submit`: POST endpoint for users to submit problems.
- `/problems`: GET endpoint to list all problems submitted by users.
- `/admin/problems`: GET endpoint to view all submitted problems.
- `/admin/review`: POST endpoint for admins to review problems.

## Contributors

   - Ilqar
   - Urfan
   - Amin
   - Novruz