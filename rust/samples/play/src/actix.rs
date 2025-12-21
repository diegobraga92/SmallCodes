// Dependências necessárias no Cargo.toml:
// [dependencies]
// actix-web = "4"
// serde = { version = "1.0", features = ["derive"] }
// serde_json = "1.0"
// reqwest = { version = "0.11", features = ["json"] }
// tokio = { version = "1", features = ["full"] }

use actix_web::{web, App, HttpResponse, HttpServer, Result};
use serde::{Deserialize, Serialize};

// ============================================
// ESTRUTURAS DE DADOS
// ============================================

// Estrutura para receber dados no POST
#[derive(Deserialize, Serialize)]
struct Usuario {
    nome: String,
    email: String,
}

// Estrutura para a resposta da API externa (JSONPlaceholder)
#[derive(Deserialize, Serialize)]
struct Post {
    #[serde(rename = "userId")]
    user_id: i32,
    id: i32,
    title: String,
    body: String,
}

// Estrutura para processar e retornar dados da API externa
#[derive(Serialize)]
struct PostProcessado {
    id: i32,
    titulo: String,
    resumo: String,
    tamanho_original: usize,
}

// ============================================
// HANDLERS (Funções que tratam as requisições)
// ============================================

// GET simples - Retorna uma mensagem de boas-vindas
async fn index() -> Result<HttpResponse> {
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "mensagem": "Bem-vindo ao servidor Actix-web!",
        "status": "online"
    })))
}

// GET com parâmetro na URL - Ex: /usuarios/123
async fn get_usuario(path: web::Path<i32>) -> Result<HttpResponse> {
    let user_id = path.into_inner();
    
    // Simula busca de usuário (em produção, buscaria no banco de dados)
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "id": user_id,
        "nome": format!("Usuário {}", user_id),
        "ativo": true
    })))
}

// POST - Recebe dados JSON no body
async fn criar_usuario(usuario: web::Json<Usuario>) -> Result<HttpResponse> {
    // Acessa os dados recebidos
    println!("Recebido: {} - {}", usuario.nome, usuario.email);
    
    // Retorna confirmação com os dados processados
    Ok(HttpResponse::Created().json(serde_json::json!({
        "mensagem": "Usuário criado com sucesso!",
        "usuario": {
            "nome": usuario.nome,
            "email": usuario.email,
            "id": 42 // Em produção, seria o ID gerado no banco
        }
    })))
}

// PUT - Atualiza um recurso existente
async fn atualizar_usuario(
    path: web::Path<i32>,
    usuario: web::Json<Usuario>
) -> Result<HttpResponse> {
    let user_id = path.into_inner();
    
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "mensagem": "Usuário atualizado!",
        "id": user_id,
        "novos_dados": {
            "nome": usuario.nome,
            "email": usuario.email
        }
    })))
}

// DELETE - Remove um recurso
async fn deletar_usuario(path: web::Path<i32>) -> Result<HttpResponse> {
    let user_id = path.into_inner();
    
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "mensagem": format!("Usuário {} deletado com sucesso!", user_id),
        "id": user_id
    })))
}

// PATCH - Atualização parcial
async fn atualizar_parcial(
    path: web::Path<i32>,
    dados: web::Json<serde_json::Value>
) -> Result<HttpResponse> {
    let user_id = path.into_inner();
    
    Ok(HttpResponse::Ok().json(serde_json::json!({
        "mensagem": "Atualização parcial realizada!",
        "id": user_id,
        "campos_atualizados": dados.into_inner()
    })))
}

// GET que chama API externa - Busca posts e processa os dados
async fn buscar_posts_externos() -> Result<HttpResponse> {
    // Cria um cliente HTTP
    let cliente = reqwest::Client::new();
    
    // Faz requisição GET para a API JSONPlaceholder (API pública de testes)
    let resposta = cliente
        .get("https://jsonplaceholder.typicode.com/posts")
        .send()
        .await;
    
    // Trata possíveis erros na requisição
    match resposta {
        Ok(resp) => {
            // Converte a resposta para JSON
            match resp.json::<Vec<Post>>().await {
                Ok(posts) => {
                    // Processa os dados: pega apenas os 5 primeiros posts
                    // e cria um resumo de cada um
                    let posts_processados: Vec<PostProcessado> = posts
                        .into_iter()
                        .take(5) // Limita a 5 posts
                        .map(|post| {
                            // Cria um resumo com os primeiros 50 caracteres
                            let resumo = if post.body.len() > 50 {
                                format!("{}...", &post.body[..50])
                            } else {
                                post.body.clone()
                            };
                            
                            // Retorna estrutura processada
                            PostProcessado {
                                id: post.id,
                                titulo: post.title,
                                resumo,
                                tamanho_original: post.body.len(),
                            }
                        })
                        .collect();
                    
                    // Retorna os dados processados
                    Ok(HttpResponse::Ok().json(serde_json::json!({
                        "total_processado": posts_processados.len(),
                        "posts": posts_processados
                    })))
                }
                Err(e) => {
                    // Erro ao fazer parse do JSON
                    Ok(HttpResponse::InternalServerError().json(serde_json::json!({
                        "erro": "Falha ao processar resposta da API",
                        "detalhes": e.to_string()
                    })))
                }
            }
        }
        Err(e) => {
            // Erro na requisição HTTP
            Ok(HttpResponse::BadGateway().json(serde_json::json!({
                "erro": "Falha ao conectar com API externa",
                "detalhes": e.to_string()
            })))
        }
    }
}

// ============================================
// FUNÇÃO MAIN - Configura e inicia o servidor
// ============================================

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    println!("🚀 Servidor iniciando em http://127.0.0.1:8080");
    
    // Cria e configura o servidor HTTP
    HttpServer::new(|| {
        App::new()
            // Rotas GET
            .route("/", web::get().to(index))
            .route("/usuarios/{id}", web::get().to(get_usuario))
            .route("/posts-externos", web::get().to(buscar_posts_externos))
            
            // Rota POST
            .route("/usuarios", web::post().to(criar_usuario))
            
            // Rota PUT
            .route("/usuarios/{id}", web::put().to(atualizar_usuario))
            
            // Rota DELETE
            .route("/usuarios/{id}", web::delete().to(deletar_usuario))
            
            // Rota PATCH
            .route("/usuarios/{id}", web::patch().to(atualizar_parcial))
    })
    .bind(("127.0.0.1", 8080))? // Define endereço e porta
    .run() // Inicia o servidor
    .await
}

// ============================================
// COMO TESTAR (usando curl ou Postman):
// ============================================
// 
// GET simples:
// curl http://localhost:8080/
//
// GET com parâmetro:
// curl http://localhost:8080/usuarios/123
//
// GET que chama API externa:
// curl http://localhost:8080/posts-externos
//
// POST:
// curl -X POST http://localhost:8080/usuarios \
//   -H "Content-Type: application/json" \
//   -d '{"nome":"João","email":"joao@email.com"}'
//
// PUT:
// curl -X PUT http://localhost:8080/usuarios/123 \
//   -H "Content-Type: application/json" \
//   -d '{"nome":"Maria","email":"maria@email.com"}'
//
// DELETE:
// curl -X DELETE http://localhost:8080/usuarios/123
//
// PATCH:
// curl -X PATCH http://localhost:8080/usuarios/123 \
//   -H "Content-Type: application/json" \
//   -d '{"email":"novoemail@email.com"}'