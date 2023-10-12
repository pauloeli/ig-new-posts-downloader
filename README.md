# Instagram New Post Downloader

This Python script allows you to download Instagram posts from specific user profiles and generate HTML pages for easy
viewing. **Please note that the developer is not responsible for any misuse of this script**, and it should be used in
compliance with Instagram's terms of service.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Developer Disclaimer](#developer-disclaimer)
- [Piece of Advice](#piece-of-advice)

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/instagram-post-downloader.git
   cd instagram-post-downloader
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project directory and add the following environment variables:

   ```
   username=your_instagram_username
   password=your_instagram_password
   user_posts=number_of_posts_to_download_if_user_has_history
   new_user_posts=number_of_posts_to_download_if_user_has_not_history
   save_method=new|profile
   profiles=profile1,profile2,profile3
   ```

   Replace `your_instagram_username` and `your_instagram_password` with your Instagram credentials, specify the number
   of posts to download in `number_of_posts_to_download_if_user_has_history` if user has history and
   in `number_of_posts_to_download_if_user_has_not_history` if is the first time of profile and the history folder
   doesn't exist, and list the profiles you want to download posts from
   in `profile1,profile2,profile3`.

   On `save_method` specify if you want save the posts inside the profile folder (`profile` value) or news posts must be
   save in the `new` folder.

## Usage

1. Run the script:

   ```bash
   python instagram_post_downloader.py
   ```

   The script will log in to your Instagram account, download the specified number of posts from the specified profiles,
   and generate HTML pages for each post.

2. The downloaded posts and HTML pages can be found in the `profiles` directory in the project folder.

## Piece of Advice

It's highly recommended not to use your primary Instagram account to log in when running this
script. Create a separate Instagram account for this purpose to protect your primary account's credentials and privacy.

Additionally, please pay attention to any potential security issues related to the `instagrapi` library, and ensure that
you are using the latest version to minimize security risks.

To prevent your account from being blocked due to suspicious activity, follow these steps after running the application:

1. Visit the [Login Activity](https://accountscenter.instagram.com/password_and_security/login_activity/) page on
   Instagram.
2. Mark the application's login as safe.

Failing to do so may result in your account being temporarily blocked if there are multiple login attempts within a
short period.

## Developer Disclaimer

The developer of this script is not responsible for any misuse of this tool. This script is intended for educational and
personal use only. Please respect Instagram's terms of service and the privacy of other users when using this script.
Use it responsibly and at your own risk.