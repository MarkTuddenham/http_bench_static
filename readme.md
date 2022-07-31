<div align=center>
  <h1>http_bench_static</h1>
</div>

How do different web servers handle concurrent requests with the same static load.

## Task
Receive a JSON payload concurrently, wait for multiple different "workloads" to run, and return a JSON response.
e.g. a workload of 2s, 1s and 0.5s; since the workloads are parallel they should total the max time under clean conditions, however the added tasks will increase the overhead.

Optional timeout of e.g. 5s for the whole request

## Results
1 worker, 10 threads

Framework | lang | 20 conns (95%, req/s) | 100 conns (95%, req/s) | 250 conns (95%, req/s)
---|---|---|---|---
Flask & Gunicorn | python | 4657.61ms, 4.67 | 20780.28ms, 4.67 | ---
axum | rust | 2002.24ms, 9.33 | 2029.32ms, 46.67 | 2033.94ms, 116.66 
tide | rust | 2050.29ms, 9.33 | 2049.41ms, 46.66 | 2055.51ms, 116.67

To do:
- actix-web (rust)
- warp (rust)
- ? golang servers

## How to run
### Servers
For the rust servers you must `cd` in to `./rust`.

- flask: `./py/run_flask`
- axum: `cargo run --release --bin axum_server`
- tide: `ASYNC_STD_THREAD_COUNT=1 cargo run --release --bin tide_server`

### Benchmarks
- 20:  `CONNS=20 ./run_rewrk`
- 100: `CONNS=100 ./run_rewrk`
- 250: `CONNS=250 THREADS=20 ./run_rewrk`

Thanks to [rewrk](https://github.com/lnx-search/rewrk)

