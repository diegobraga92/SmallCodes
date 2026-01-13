use std::error::Error;
use std::io::Write;
use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};
use std::thread;
use std::fs::File;

#[derive(Debug, Deserialize, Serialize)]
struct Pokemon {
    name: String,
    id: i32,
    height: i32,
}

async fn get_pokemon(id: i32) -> Result<Pokemon, Box<dyn Error + Send + Sync>> {
    let url = format!("https://pokeapi.co/api/v2/pokemon/{}", id);
    let pokemon = reqwest::Client::new()
        .get(url)
        .send()
        .await?
        .json::<Pokemon>()
        .await?;
    Ok(pokemon)
}

async fn buscar_pokemons(ids: Vec<i32>) -> Vec<Pokemon> {
    let tasks: Vec<_> = ids.into_iter()
        .map(|id| tokio::spawn(async move { get_pokemon(id).await }))
        .collect();
    
    let mut res = vec![];
    for task in tasks {
        if let Ok(Ok(pokemon)) = task.await {
            res.push(pokemon);
        }
    }
    res
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        return Err("Missing output path argument.".into());
    }
    
    let chunks: Vec<Vec<i32>> = (1..=30)
        .collect::<Vec<_>>()
        .chunks(10)
        .map(|c| c.to_vec())
        .collect();
    
    let pokes = Arc::new(Mutex::new(Vec::new()));
    let handles: Vec<_> = chunks.into_iter()
        .map(|ids| {
            let pokes = Arc::clone(&pokes);
            thread::spawn(move || {
                let runtime = tokio::runtime::Runtime::new().unwrap();
                runtime.block_on(async {
                    let res = buscar_pokemons(ids).await;
                    pokes.lock().unwrap().extend(res);
                });
            })
        })
        .collect();
    
    for handle in handles {
        handle.join().unwrap();
    }
    
    let fin = Arc::try_unwrap(pokes).unwrap().into_inner().unwrap();
    let json = serde_json::to_string_pretty(&fin)?;
    File::create(&args[1])?.write_all(json.as_bytes())?;
    
    Ok(())
}