## Classifieds Ads API
### How to start
1. Create virtual ENV
``` shell
$ python3 -m venv venv
```
2. Activate virtual ENV
``` shell
$ source venv/bin/activate
```
3. Install requirements
``` shell
$ pip3 install -r requirements.txt
```
4. Start the service
``` shell
$ python3 app/main.py
```

### Request examples
- List all ads. Default sorting is done by ad id in ascending order
``` shell
$ curl http://127.0.0.1:5000/api/v1/classifieds_ads
```
- List all ads sorted by price/date of creation in descending/ascending order
``` shell
$ curl "http://127.0.0.1:5000/api/v1/classifieds_ads?sortby=price&sort=desc"
$ curl "http://127.0.0.1:5000/api/v1/classifieds_ads?sortby=created_at&sort=asc"
```
- Fetch an ad by id
``` shell
$ curl http://127.0.0.1:5000/api/v1/classifieds_ads/<ad_id>
```
- Insert an ad. Created object will be returned in the response
``` shell
$ curl -v http://127.0.0.1:5000/api/v1/classifieds_ads -H "content-type:application/json" -d '{"subject":"volvo v70","body":"super duper snygg bil","price":70000,"email":"fisk@apa.se"}'
```
- Delete an ad
``` shell
$ curl http://127.0.0.1:5000/api/v1/classifieds_ads/<ad_id> -x DELETE
```
