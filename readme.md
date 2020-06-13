# Website test with Selenium
This app is an attempt to learn some basics of the Selenium web driver. As a test site, I use the website-info app. Find more information about the test website on [the demo page](https://website-info.herokuapp.com/ "the demo page") and [GitHub](https://github.com/deermeapart/website-info "GitHub").

To test the website-info app I emulate user behavior with Selenium. The application performs the following actions:
1. goes to the page,
2. enters a query,
3. clicks on the button,
4. waits for the result,
5. and creates a screenshot of the page.

As a list of requests, I use [Alexa top 1 million sites](http://s3.amazonaws.com/alexa-static/top-1m.csv.zip' "Alexa top 1 million sites"). Please note that ranks in the archive might be outdated. Meanwhile, ranks are out of the scope.

The application will not test all websites from the list. It will create a small sample by utilizing the Pandas library. You can change the size of the sample in the `website_queries` variable.

The application uses the Firefox browser, so the user must first [install the Firefox](https://www.mozilla.org/en-US/firefox/new/ "install the Firefox") and [download geckodriver](https://github.com/mozilla/geckodriver/releases "download geckodriver") of the corresponding version. Unzip the archive with geckodriver to the directory with the Selenium app.

All requests are written to an app.log file to analyze the behavior of the application later. Screenshots are saved in `./screenshots/pass/` and `screenshots/fail/` folders.
