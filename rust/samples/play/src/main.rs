use tokio::{task, time::{sleep, Duration}};

#[tokio::main]
async fn main() {
    // Spawn concurrent tasks
    let task1 = task::spawn(async {
        sleep(Duration::from_secs(1)).await; // Await is a Yield Point. Can suspend and resume on another Thread
        println!("Task 1 completed");
    });
    
    let task2 = task::spawn(async {
        sleep(Duration::from_secs(2)).await;
        println!("Task 2 completed");
    });
    
    // Join handles to wait for completion
    let _ = tokio::join!(task1, task2);
    
    // Select for the first completed
    tokio::select! {
        _ = sleep(Duration::from_secs(1)) => {
            println!("1 second passed first");
        }
        _ = sleep(Duration::from_secs(2)) => {
            println!("2 seconds passed first");
        }
    }
}