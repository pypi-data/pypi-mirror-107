# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['youtube_channel_scraper']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141.0,<4.0.0']

entry_points = \
{'console_scripts': ['youtube-channel-scraper = '
                     'youtube_channel_scraper.__main__:run']}

setup_kwargs = {
    'name': 'youtube-channel-scraper',
    'version': '0.1.1',
    'description': 'Scrape videos from YouTube channels.',
    'long_description': '# YouTube Channel Scraper\n\nScrapes videos from a YouTube channel using Python.\n\nIt takes a YouTube channel URL as an input and produces a list of videos as an output.\n\nVideo attributes:\n* `url`\n* `title`\n* `description`\n* `author`\n* `published_at`\n* `thumbnail`\n\n## Requirements\n\n* Install chromedriver at `/chromedriver`. For more details refer to [scripts/install_chromedriver.sh](scripts/install_chromedriver.sh)\n\n## Install\n\n```bash\npip install youtube-channel-scraper\n```\n\n## Usage\n\n```python\nfrom youtube_channel_scraper.scraper import YoutubeScraper\n\nscraper = YoutubeScraper(channel_url)\ncrawled_videos = scraper.scrape()\n```\n\n### Optional parameters\n\n* *stop_id:* stop scraping when this video ID is encountered. Older videos are always scraped first.\n* *max_videos:* maximum amount of videos to scrape\n* *proxy_ip:* proxy IP with port \n\n\n## CLI usage\n\n```bash\nyoutube-channel-scraper "https://www.youtube.com/channel/CHANNEL_ID"\n```\n\n### Available arguments\n\n```bash\npositional arguments:\n  channel_url           Youtube channel URL\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --filename FILENAME   Output file\n  --stop_video_id STOP_VIDEO_ID\n                        Youtube video ID that indicates to stop crawling\n  --max_videos MAX_VIDEOS\n                        Max videos to crawl\n  --proxy PROXY         Proxy IP\n  --screenshot_filename SCREENSHOT_FILENAME\n                        Path to exceptions screenshot\n```\n\n## Usage with Docker\n\n### Why?\n\nWhen running `youtube-channel-scraper` in a Docker container there is no need to manually install chrome driver in your environment.\n\n### How?\n\n```bash\ngit clone https://github.com/hajkr/youtube-channel-scraper.git\ncd youtube_channel_scraper\n\n# Builds the container when running for the first time\nmake run\n\n# Enter the container\nmake to_container\n\npython youtube_channel_scraper "https://www.youtube.com/channel/CHANNEL_ID"\n```\n',
    'author': 'Tadej Hribar',
    'author_email': 'tadej.996@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hajkr/youtube-channel-scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
