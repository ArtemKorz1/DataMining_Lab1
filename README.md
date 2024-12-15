## Lab 1-3
Run main.py in root directory

## Lab 4
### Spider for "пермь-светофор-магазин.рф"
Terminal:
1. cd Lab4\spiders
2. scrapy runspider tl_spider.py

Run main.py to save json

### Spider for protected "www.regard.ru"
Terminal:
1. cd Lab4\spiders
2. scrapy runspider Experimental.py

Required to parse: <b>USER_AGENT</b>\
Run main.py to save json

## Lab 5
<b>Spider is located in Lab4/spiders</b>
1. docker run -p 8050:8050 scrapinghub/splash
2. cd Lab4\spiders
3. scrapy runspider quotes_spider.py

Run main.py to save json

## Lab 6
Run main.py in root directory

## Lab 7
Run: Terminal:
1. Create application (e.g. React app): <b>npx create-react-app cypress-test</b>
2. Goto: <b>cd E:\VS\cypress-test</b>
3. Add cypress to project: <b>npm install cypress --save-dev</b>
4. Run Editor: <b>npx cypress open</b>