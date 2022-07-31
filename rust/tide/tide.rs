use tide::{self, Request};

use async_std::task::{sleep, spawn};
use core::time::Duration;

use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
struct APIArgs {
    text: String,
    count: u32,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct APIResponse {
    texts: Vec<String>,
}

#[async_std::main]
async fn main() -> tide::Result<()> {
    let mut app = tide::new();
    app.at("/").post(task).get(task);
    app.listen("127.0.0.1:1729").await?;
    Ok(())
}

async fn task(mut req: Request<()>) -> tide::Result {
    let APIArgs { text, count } = req.body_json().await?;
    let mut resp = APIResponse { texts: vec![] };

    let mut tasks = vec![];
    for _ in 0..count {
        for t in [500, 1000, 2000].iter() {
            let ret_text = text.clone();
            tasks.push(spawn(async move {
                sleep(Duration::from_millis(*t)).await;
                ret_text
            }));
        }
    }

    for t in tasks {
        resp.texts.push(t.await);
    }
    Ok(serde_json::to_string(&resp).unwrap().into())
}
