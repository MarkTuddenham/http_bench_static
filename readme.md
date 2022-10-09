<div align=center>
  <h1>http_bench_static</h1>
</div>

How do different web servers handle concurrent requests with the same static load.

## Task
Receive a JSON payload concurrently, wait for multiple different "workloads" to run, and return a JSON response.
e.g. a workload of 2s, 1s and 0.5s; since the workloads are parallel they should total the max time under clean conditions, however the added tasks will increase the overhead.

Optional timeout of e.g. 5s for the whole request

## Results
Below are the results when attempting to limit cpu availability to reduce the affect of background processes on my pc.
Python is run with gunicorn at 1 worker and 10 threads since threads are the lowest level I/O blocking structures, the others are limited to 1 system thread.
This is not quite a fair test since, for example, `GOMAXPROCS` only limits the number of executing system threads, [so post](https://stackoverflow.com/questions/39245660/number-of-threads-used-by-go-runtime), and will allow many blocked threads to exist, which is not the same as python's limit of 10 threads in total.
It would be good to rent out a server to host the programs on so that we can test how well they can utilise a full system, i.e. un-cap the thread limits.

Framework | lang | 20 conns (95%, req/s) | 100 conns (95%, req/s) | 250 conns (95%, req/s)
---|---|---|---|---
Flask & Gunicorn | python | 4657.61ms, 4.67 | 20780.28ms, 4.67 | ---
axum | rust | 2002.24ms, 9.33 | 2029.32ms, 46.67 | 2033.94ms, 116.66
tide | rust | 2050.29ms, 9.33 | 2049.41ms, 46.66 | 2055.51ms, 116.67
net/http | go | 2001.94ms, 9.33 | 2019.90ms, 46.68 | 2058.82ms, 116.67

Other http servers:
- actix-web (rust)
- warp (rust)


## How to run
### Servers
For the rust servers you must `cd` in to `./rust`.

- flask: `./py/run_flask`
- axum: `cargo run --release --bin axum_server`
- tide: `ASYNC_STD_THREAD_COUNT=1 cargo run --release --bin tide_server`
- net/http: `GOMAXPROCS=1 go run go/main.go`

### Benchmarks
- 20:  `CONNS=20 ./run_rewrk`
- 100: `CONNS=100 ./run_rewrk`
- 250: `CONNS=250 THREADS=20 ./run_rewrk`

Thanks to [rewrk](https://github.com/lnx-search/rewrk)

