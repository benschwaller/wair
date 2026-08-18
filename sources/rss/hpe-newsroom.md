# HPE Newsroom

URL: https://www.hpe.com/us/en/newsroom/press-hub/_jcr_content/polaris-body-zone/aem.model.json?type=press-release&restype=press-release&topic=&offset=0
Type: json

Description: 0–3 day lead on HPE announcements (updated 2026-08-17: HPE publishes no RSS feed — the newsroom is a JS app. Discovered the backing AEM JSON API at /us/en/newsroom/press-hub/_jcr_content/polaris-body-zone/aem.model.json which returns structured press releases with title, link, and date. Marked type:json so fetch_new_rss.py parses the items array. The basic health check will report this as inactive because it expects HTML; that is expected and the fetch path works.)
