#include <curl/curl.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>


struct url_data {
    size_t size;
    char* data;
};

void request(char *url){
    CURL *curl = curl_easy_init();

    struct url_data data;
    data.size = 0;
    data.data = malloc(4096); /* reasonable size initial buffer */
    if(NULL == data.data) {
        fprintf(stderr, "Failed to allocate memory.\n");
    }

    data.data[0] = '\0';


    if(!curl)return;
    curl_easy_setopt(curl, CURLOPT_URL, url);
    // curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION,)
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &data);
    CURLcode res = curl_easy_perform(curl);
	/* Check for errors */
	if(res != CURLE_OK)
		fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
	/* always cleanup */
	curl_easy_cleanup(curl);
    free(url);


    printf("data: %s\n", data.data);
}

int main(){
    request("https://google.com/");
    return 0;
}