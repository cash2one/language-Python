package main

import (
	//"encoding/json"
	"github.com/gin-gonic/gin"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"strings"
)

func doPost(v string, url string) string {
	body := ioutil.NopCloser(strings.NewReader(v))
	req, _ := http.NewRequest("POST", url, body)
	// req.Header.Set("Content-Type", "application/x-www-form-urlencoded; param=value")
	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()
	data, _ := ioutil.ReadAll(resp.Body)
	return string(data)
}

func main() {
	gin.SetMode(gin.DebugMode)
	r := gin.New()

	r.GET("/:platform/*sourceurl", func(c *gin.Context) {
		platform := c.Params.ByName("platform")
		sourceurl := c.Params.ByName("sourceurl")[1:]

		v := url.Values{}
		var result string
		if platform == "sina" {
			v.Set("source", "")
			// v.Set("access_token", "")
			v.Set("url_long", sourceurl)
			log.Println(v.Encode())

			result = doPost(v.Encode(), "https://api.weibo.com/2/short_url/shorten.json")
		} else if platform == "baidu" {

		} else {
			result = platform + ": " + sourceurl
		}

		c.String(http.StatusOK, result)
	})

	r.Run(":8890")
}
