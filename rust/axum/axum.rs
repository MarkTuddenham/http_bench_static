use axum::{
    extract::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use tokio::{
    task::spawn,
    time::{sleep, Duration},
};

#[derive(Serialize, Deserialize, Debug, Clone)]
struct APIArgs {
    text: String,
    count: u32,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct APIResponse {
    texts: Vec<String>,
}

#[tokio::main(flavor = "multi_thread", worker_threads = 1)]
async fn main() {
    let app = Router::new().route("/", get(task)).route("/", post(task));

    axum::Server::bind(&"0.0.0.0:1729".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn task(Json(args): Json<APIArgs>) -> String {
    let mut resp = APIResponse { texts: vec![] };
    let mut tasks = vec![];
    for _ in 0..args.count {
        for t in [500, 1000, 2000].iter() {
            let text = args.text.clone();
            tasks.push(spawn(async move {
                sleep(Duration::from_millis(*t)).await;
                text
            }));
        }
    }

    for t in tasks{
        resp.texts.push(t.await.unwrap());
    }
    serde_json::to_string(&resp).unwrap()
}
