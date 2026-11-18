use std::collections::VecDeque;
use std::io::{BufRead, BufReader, Result, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::thread;

const ADDR: &str = "127.0.0.1:7878";

#[allow(dead_code)]
fn single_thread_server() -> Result<()> {
    let listener = TcpListener::bind(ADDR)?;
    let mut queue: VecDeque<String> = VecDeque::new();

    for stream in listener.incoming() {
        let stream = stream?;
        let read_stream = stream.try_clone()?;

        let mut reader = BufReader::new(read_stream);
        let mut writer = stream;

        let mut line = String::new();

        loop {
            line.clear();
            let n = reader.read_line(&mut line)?;

            if n == 0 || !line.ends_with('\n') {
                break;
            }

            let cmd = line.trim_end_matches('\n').trim_end_matches('\r');

            if let Some(payload) = cmd.strip_prefix("PUBLISH ") {
                queue.push_back(payload.to_string());
                writer.write_all(b"OK\n")?;
            } else if cmd == "RETRIEVE" {
                match queue.pop_front() {
                    Some(s) => writeln!(writer, "{s}")?,
                    None => writer.write_all(b"EMPTY\n")?,
                }
            } else {
                writer.write_all(b"ERR unknown command\n")?;
            }
        }
    }

    Ok(())
}

fn handle_client(mut stream: TcpStream, queue: &Mutex<VecDeque<String>>) -> Result<()> {
    let read_stream = stream.try_clone()?;
    let mut reader = BufReader::new(read_stream);
    let mut line = String::new();

    loop {
        line.clear();
        let n = reader.read_line(&mut line)?;

        if n == 0 || !line.ends_with('\n') {
            break;
        }

        let cmd = line.trim_end_matches('\n').trim_end_matches('\r');

        if let Some(payload) = cmd.strip_prefix("PUBLISH ") {
            let mut q = queue.lock().unwrap();
            q.push_back(payload.to_string());

            drop(q);

            stream.write_all(b"OK\n")?;
        } else if cmd == "RETRIEVE" {
            let mut q = queue.lock().unwrap();
            let item = q.pop_front();
            drop(q);

            match item {
                Some(s) => writeln!(stream, "{s}")?,
                None => stream.write_all(b"EMPTY\n")?,
            }
        } else {
            stream.write(b"ERR unknown command")?;
        }
    }

    Ok(())
}

#[allow(dead_code)]
fn multi_threaded_server() -> Result<()> {
    let listener = TcpListener::bind(ADDR)?;
    let queue = Arc::new(Mutex::new(VecDeque::<String>::new()));

    for stream in listener.incoming() {
        let stream = stream?;
        let q = Arc::clone(&queue);

        thread::spawn(move || {
            let _ = handle_client(stream, &q);
        });
    }

    Ok(())
}

fn scoped_threaded_server() -> Result<()> {
    let listener = TcpListener::bind(ADDR)?;
    let queue = Mutex::new(VecDeque::<String>::new());

    thread::scope(|s| {
        for stream in listener.incoming() {
            let stream = match stream {
                Ok(s) => s,
                Err(_) => continue,
            };

            s.spawn({
                let q = &queue;
                move || {
                    let _ = handle_client(stream, q);
                }
            });
        }
    });

    Ok(())
}

fn main() -> Result<()> {
    //single_thread_server()
    //multi_threaded_server()
    scoped_threaded_server()
}

// Test it:
//
//     $ cargo run
//     # in another terminal:
//     $ printf 'PUBLISH hello\nRETRIEVE\n' | nc 127.0.0.1 7878
//     OK
//     hello
