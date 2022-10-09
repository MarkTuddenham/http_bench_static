package main

import (
	"encoding/json"
	"net/http"
	"sync"
	"time"
)

type APIArgs struct {
	Text  string `json:"text"`
	Count int    `json:"count"`
}

type APIResponse struct {
	Texts []string `json:"texts"`
}

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {

		decoder := json.NewDecoder(r.Body)
		var args APIArgs
		err := decoder.Decode(&args)
		if err != nil {
			panic(err)
		}

		var resp APIResponse

		sleep_times := []int{500, 1000, 2000}

		ch := make(chan string)
		var wg sync.WaitGroup
		wg.Add(args.Count * len(sleep_times))

		go func() {
			wg.Wait()
			close(ch)
		}()

		for c := 0; c < args.Count; c++ {
			for _, sleep_time := range sleep_times {
				go do_task(sleep_time, args.Text, ch, &wg)
			}
		}

		for t := range ch {
			resp.Texts = append(resp.Texts, t)
		}

		writer := json.NewEncoder(w)
		writer.Encode(&resp)

	})

	http.ListenAndServe(":1729", nil)
}

func do_task(taskDuration int, text string, ch chan string, wg *sync.WaitGroup) {
	defer wg.Done()
	time.Sleep(time.Duration(taskDuration) * time.Millisecond)
	ch <- text
}
