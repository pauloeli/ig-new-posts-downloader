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
   posts=number_of_posts_to_download
   profiles=profile1,profile2,profile3
   ```

   Replace `your_instagram_username` and `your_instagram_password` with your Instagram credentials, specify the number
   of posts to download in `number_of_posts_to_download`, and list the profiles you want to download posts from
   in `profile1,profile2,profile3`.

## Usage

1. Run the script:

   ```bash
   python instagram_post_downloader.py
   ```

   The script will log in to your Instagram account, download the specified number of posts from the specified profiles,
   and generate HTML pages for each post.

2. The downloaded posts and HTML pages can be found in the `profiles` directory in the project folder.

## Developer Disclaimer

The developer of this script is not responsible for any misuse of this tool. This script is intended for educational and
personal use only. Please respect Instagram's terms of service and the privacy of other users when using this script.
Use it responsibly and at your own risk.

## Piece of Advice

**Piece of Advice:** It's highly recommended not to use your primary Instagram account to log in when running this
script. Create a separate Instagram account for this purpose to protect your primary account's credentials and privacy.
Additionally, please pay attention to any potential security issues related to the `instagrapi` library, and ensure that
you are using the latest version to minimize security risks.