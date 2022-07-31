<div align=center>
  <h1>http_bench_static</h1>
</div>

---
How do different web servers handle concurrent requests with the same static load.

## Task
Receive a JSON payload concurrently, wait for multiple different "workloads" to run, and return a JSON response.
e.g. a workload of 2s, 1s and 0.5s; since the workloads are parrellel they should total the max time under clean conditions, however the added tasks will increase load.

Optional timeout of e.g. 5s for the whole request

## Tools
[hyperfine](https://github.com/sharkdp/hyperfine)
```
hyperfine ./send_curl
```

[rewrk](https://github.com/lnx-search/rewrk)
```
./send_rewrk
```

## results
1 worker, 10 threads

hyperfine format is avg ± std, min … max
rewrk format is  95th %, req/s

Framework | lang | hyperfine  | rewrk
---|---|---|---
Flask & Gunicorn | python | 2.019s ± 0.010s, 2.009s …  2.037s | 4657.61ms, 4.67
axum | rust | 2.021s ± 0.008s, 2.011s …  2.034s | 2012.50ms, 9.


To do:
- Tide (rust)
- warp (rust)
- actix-web (rust)

