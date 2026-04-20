/*
    C# DATABASE ADO.NET
    File: 20_database_ado.cs
    
    Comprehensive guide to ADO.NET database access in C#.
    Covers connection management, command execution, data readers,
    transactions, stored procedures, parameterized queries, and best practices.
*/

using System;
using System.Data;
using System.Data.Common;
using System.Data.SqlClient;
using System.Data.SqlTypes;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;

namespace CSharpRefresher.DatabaseAdo
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# ADO.NET Database Access ===\n");
            
            DemonstrateConnectionManagement();
            DemonstrateCommandExecution();
            DemonstrateDataReaders();
            DemonstrateTransactions();
            DemonstrateStoredProcedures();
            DemonstrateBestPractices();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateConnectionManagement()
        {
            Console.WriteLine("=== 1. Connection Management ===\n");
            
            // 1. Connection strings
            Console.WriteLine("1. Connection Strings:");
            
            // SQL Server connection string examples
            string connectionString = "Server=localhost;Database=TestDB;Integrated Security=True;";
            string connectionStringWithCreds = "Server=localhost;Database=TestDB;User Id=sa;Password=password;";
            string connectionStringWithOptions = """
                Server=localhost;Database=TestDB;Integrated Security=True;
                Connect Timeout=30;Encrypt=True;TrustServerCertificate=False;
                Application Name=MyApp;MultipleActiveResultSets=True;
                Pooling=True;Min Pool Size=5;Max Pool Size=100;
                """;
            
            Console.WriteLine("""
                Common connection string parameters:
                • Server/Data Source: Database server
                • Database/Initial Catalog: Database name
                • Integrated Security/Trusted_Connection: Windows auth
                • User Id/Password: SQL auth credentials
                • Connect Timeout: Connection timeout in seconds
                • Encrypt: Enable TLS encryption
                • TrustServerCertificate: Bypass certificate validation
                • Application Name: Identifying application name
                • MultipleActiveResultSets (MARS): Multiple queries on same connection
                • Pooling: Connection pooling enabled
                • Min/Max Pool Size: Connection pool limits
                """);
            
            // 2. Creating and opening connections
            Console.WriteLine("\n2. Creating and Opening Connections:");
            
            // Using statement ensures proper disposal
            using (var connection = new SqlConnection(connectionString))
            {
                try
                {
                    connection.Open();
                    Console.WriteLine($"Connection opened: State={connection.State}, Database={connection.Database}");
                    
                    // Connection properties
                    Console.WriteLine($"Server version: {connection.ServerVersion}");
                    Console.WriteLine($"Connection timeout: {connection.ConnectionTimeout}");
                    Console.WriteLine($"Workstation ID: {connection.WorkstationId}");
                    Console.WriteLine($"Packet size: {connection.PacketSize}");
                }
                catch (SqlException ex)
                {
                    Console.WriteLine($"SQL error: {ex.Message}");
                    Console.WriteLine($"Error number: {ex.Number}");
                    foreach (SqlError error in ex.Errors)
                    {
                        Console.WriteLine($"  Error: {error.Message}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"General error: {ex.Message}");
                }
            } // Connection automatically closed and disposed
            
            // 3. Connection pooling
            Console.WriteLine("\n3. Connection Pooling:");
            Console.WriteLine("""
                Connection pooling benefits:
                • Reuses connections instead of creating new ones
                • Improves performance
                • Manages connection lifetime
                
                How it works:
                1. Application requests connection
                2. Pool checks for available connection with matching connection string
                3. If found, returns existing connection
                4. If not, creates new connection (if under Max Pool Size)
                5. Connection returned to pool when closed/disposed
                
                Monitoring:
                • Use SQL Server Profiler or Extended Events
                • Monitor sys.dm_exec_connections
                • Check performance counters
                """);
            
            // 4. Async connection opening
            Console.WriteLine("\n4. Async Connection Opening:");
            
            async Task AsyncConnectionExample()
            {
                using (var connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();
                    Console.WriteLine($"Async connection opened: {connection.State}");
                    
                    // Use async operations within connection
                    await Task.Delay(100);
                }
            }
            AsyncConnectionExample().Wait();
            
            // 5. Connection events
            Console.WriteLine("\n5. Connection Events:");
            
            using (var connection = new SqlConnection(connectionString))
            {
                connection.InfoMessage += (sender, e) =>
                {
                    Console.WriteLine($"Info message: {e.Message}");
                    foreach (SqlError error in e.Errors)
                    {
                        Console.WriteLine($"  Source: {error.Source}, Procedure: {error.Procedure}");
                    }
                };
                
                connection.StateChange += (sender, e) =>
                {
                    Console.WriteLine($"State changed: {e.OriginalState} -> {e.CurrentState}");
                };
                
                // Open and close to trigger events
                try { connection.Open(); } catch { }
                connection.Close();
            }
            
            // 6. Connection string builders
            Console.WriteLine("\n6. Connection String Builders:");
            
            var builder = new SqlConnectionStringBuilder
            {
                DataSource = "localhost",
                InitialCatalog = "TestDB",
                IntegratedSecurity = true,
                ConnectTimeout = 30,
                Encrypt = true,
                TrustServerCertificate = false,
                ApplicationName = "MyApp",
                MultipleActiveResultSets = true,
                Pooling = true,
                MinPoolSize = 5,
                MaxPoolSize = 100
            };
            
            Console.WriteLine($"Built connection string: {builder.ConnectionString}");
            Console.WriteLine($"Individual properties - DataSource: {builder.DataSource}, Timeout: {builder.ConnectTimeout}");
            
            // Modify existing connection string
            builder["Connect Timeout"] = 60;
            builder["Application Name"] = "UpdatedApp";
            
            // 7. Different database providers
            Console.WriteLine("\n7. Database Providers:");
            Console.WriteLine("""
                Common ADO.NET providers:
                • SQL Server: System.Data.SqlClient (Microsoft)
                • SQL Server (new): Microsoft.Data.SqlClient
                • MySQL: MySql.Data.MySqlClient
                • PostgreSQL: Npgsql
                • Oracle: Oracle.ManagedDataAccess.Client
                • SQLite: Microsoft.Data.Sqlite
                
                Using DbProviderFactories for provider-agnostic code:
                DbProviderFactory factory = DbProviderFactories.GetFactory("System.Data.SqlClient");
                using (DbConnection connection = factory.CreateConnection())
                {
                    connection.ConnectionString = connectionString;
                    connection.Open();
                }
                """);
        }
        
        static void DemonstrateCommandExecution()
        {
            Console.WriteLine("\n=== 2. Command Execution ===\n");
            
            string connectionString = "Server=localhost;Database=TestDB;Integrated Security=True;";
            
            // 1. Basic command execution
            Console.WriteLine("1. Basic Command Execution:");
            
            using (var connection = new SqlConnection(connectionString))
            {
                // Note: In real code, you would open the connection
                // For demonstration, we'll show command creation without opening
                
                // Create command
                using (var command = connection.CreateCommand())
                {
                    command.CommandText = "SELECT COUNT(*) FROM Users";
                    command.CommandType = CommandType.Text;
                    command.CommandTimeout = 30; // 30 second timeout
                    
                    Console.WriteLine($"Command text: {command.CommandText}");
                    Console.WriteLine($"Command type: {command.CommandType}");
                    Console.WriteLine($"Command timeout: {command.CommandTimeout}");
                }
            }
            
            // 2. Parameterized queries (CRITICAL for security)
            Console.WriteLine("\n2. Parameterized Queries (Prevent SQL Injection):");
            
            using (var connection = new SqlConnection(connectionString))
            using (var command = new SqlCommand())
            {
                command.Connection = connection;
                command.CommandText = """
                    SELECT * FROM Users 
                    WHERE Username = @username AND IsActive = @isActive
                    ORDER BY CreatedDate DESC
                    """;
                
                // Add parameters
                command.Parameters.AddWithValue("@username", "john.doe");
                command.Parameters.AddWithValue("@isActive", true);
                
                // Alternative: Strongly-typed parameter creation
                var param = new SqlParameter("@username", SqlDbType.NVarChar, 50)
                {
                    Value = "john.doe",
                    Direction = ParameterDirection.Input
                };
                command.Parameters.Add(param);
                
                Console.WriteLine($"Parameterized query with {command.Parameters.Count} parameters");
                Console.WriteLine("""
                    ALWAYS use parameters to:
                    • Prevent SQL injection attacks
                    • Improve performance (query plan caching)
                    • Handle data type conversion
                    • Avoid SQL syntax errors
                    """);
            }
            
            // 3. ExecuteScalar for single value
            Console.WriteLine("\n3. ExecuteScalar (Single Value):");
            
            async Task ExecuteScalarExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand("SELECT COUNT(*) FROM Users", connection))
                {
                    await connection.OpenAsync();
                    object result = await command.ExecuteScalarAsync();
                    int count = result != null ? Convert.ToInt32(result) : 0;
                    Console.WriteLine($"User count: {count}");
                }
            }
            // ExecuteScalarExample().Wait(); // Commented for demo
            
            // 4. ExecuteNonQuery for INSERT/UPDATE/DELETE
            Console.WriteLine("\n4. ExecuteNonQuery (DML Operations):");
            
            async Task ExecuteNonQueryExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand())
                {
                    command.Connection = connection;
                    command.CommandText = """
                        INSERT INTO Users (Username, Email, CreatedDate)
                        VALUES (@username, @email, @createdDate)
                        """;
                    
                    command.Parameters.AddWithValue("@username", "new.user");
                    command.Parameters.AddWithValue("@email", "user@example.com");
                    command.Parameters.AddWithValue("@createdDate", DateTime.UtcNow);
                    
                    await connection.OpenAsync();
                    int rowsAffected = await command.ExecuteNonQueryAsync();
                    Console.WriteLine($"Rows affected: {rowsAffected}");
                    
                    // Get identity value
                    command.CommandText = "SELECT SCOPE_IDENTITY()";
                    object newId = await command.ExecuteScalarAsync();
                    Console.WriteLine($"New ID: {newId}");
                }
            }
            // ExecuteNonQueryExample().Wait(); // Commented for demo
            
            // 5. Command types
            Console.WriteLine("\n5. Command Types:");
            Console.WriteLine("""
                CommandType enumeration:
                • Text (default): SQL text command
                • StoredProcedure: Stored procedure name
                • TableDirect: Table name (returns all rows)
                
                Example using stored procedure:
                command.CommandType = CommandType.StoredProcedure;
                command.CommandText = "sp_GetUsers";
                command.Parameters.AddWithValue("@activeOnly", true);
                """);
            
            // 6. Command timeout
            Console.WriteLine("\n6. Command Timeout:");
            Console.WriteLine("""
                Setting appropriate timeouts:
                • Default: 30 seconds
                • Short queries: 5-10 seconds
                • Reports/long-running: 300+ seconds
                • Consider using CommandTimeout = 0 for no timeout (use with caution)
                
                Timeout behavior:
                • SqlException with Number = -2 (timeout)
                • Connection remains open
                • Transaction may need cleanup
                """);
            
            // 7. Batch commands
            Console.WriteLine("\n7. Batch Commands:");
            
            using (var connection = new SqlConnection(connectionString))
            using (var command = new SqlCommand())
            {
                command.Connection = connection;
                command.CommandText = """
                    UPDATE Users SET LastLogin = GETDATE() WHERE Id = 1;
                    UPDATE Users SET FailedAttempts = 0 WHERE Id = 2;
                    DELETE FROM UserSessions WHERE Expires < GETDATE();
                    """;
                
                Console.WriteLine("Batch command with multiple statements");
                Console.WriteLine("""
                    Batch considerations:
                    • All statements execute in single round-trip
                    • Use GO separator in SSMS, not in ADO.NET
                    • Errors may stop execution (depends on XACT_ABORT)
                    • Use transactions for atomicity
                    """);
            }
        }
        
        static void DemonstrateDataReaders()
        {
            Console.WriteLine("\n=== 3. Data Readers ===\n");
            
            string connectionString = "Server=localhost;Database=TestDB;Integrated Security=True;";
            
            // 1. Basic DataReader usage
            Console.WriteLine("1. Basic DataReader Usage:");
            
            async Task DataReaderExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand("SELECT Id, Username, Email FROM Users", connection))
                {
                    await connection.OpenAsync();
                    
                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        Console.WriteLine("Reading data with DataReader:");
                        
                        // Get schema information
                        var schemaTable = reader.GetSchemaTable();
                        Console.WriteLine($"Schema columns: {schemaTable?.Rows.Count ?? 0}");
                        
                        // Read data
                        while (await reader.ReadAsync())
                        {
                            int id = reader.GetInt32(0); // By ordinal
                            string username = reader.GetString(1);
                            string email = reader.GetString(reader.GetOrdinal("Email")); // By name
                            
                            Console.WriteLine($"  User: {id}, {username}, {email}");
                        }
                        
                        Console.WriteLine($"Total records: {reader.RecordsAffected}");
                    }
                }
            }
            // DataReaderExample().Wait(); // Commented for demo
            
            // 2. DataReader with null handling
            Console.WriteLine("\n2. DataReader with Null Handling:");
            
            async Task DataReaderNullExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand("SELECT Id, Username, LastLogin FROM Users", connection))
                {
                    await connection.OpenAsync();
                    
                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            int id = reader.GetInt32(0);
                            string username = reader.GetString(1);
                            
                            // Safe way to read nullable columns
                            DateTime? lastLogin = reader.IsDBNull(2) ? null : reader.GetDateTime(2);
                            
                            // Alternative using GetValue
                            object lastLoginObj = reader.GetValue(2);
                            DateTime? lastLogin2 = lastLoginObj == DBNull.Value ? null : (DateTime?)lastLoginObj;
                            
                            Console.WriteLine($"  User: {id}, {username}, LastLogin: {lastLogin?.ToString() ?? "Never"}");
                        }
                    }
                }
            }
            // DataReaderNullExample().Wait(); // Commented for demo
            
            // 3. Multiple result sets
            Console.WriteLine("\n3. Multiple Result Sets:");
            
            async Task MultipleResultSetsExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand())
                {
                    command.Connection = connection;
                    command.CommandText = """
                        SELECT * FROM Users WHERE IsActive = 1;
                        SELECT * FROM Orders WHERE Status = 'Pending';
                        SELECT COUNT(*) AS ActiveUsers FROM Users WHERE IsActive = 1;
                        """;
                    
                    await connection.OpenAsync();
                    
                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        int resultSet = 0;
                        
                        do
                        {
                            Console.WriteLine($"Result set {++resultSet}:");
                            
                            while (await reader.ReadAsync())
                            {
                                // Process each row
                                if (resultSet == 1)
                                {
                                    // Process users
                                }
                                else if (resultSet == 2)
                                {
                                    // Process orders
                                }
                            }
                        } while (await reader.NextResultAsync());
                        
                        Console.WriteLine($"Total result sets: {resultSet}");
                    }
                }
            }
            // MultipleResultSetsExample().Wait(); // Commented for demo
            
            // 4. DataReader performance tips
            Console.WriteLine("\n4. DataReader Performance Tips:");
            Console.WriteLine("""
                • Use GetOrdinal once and cache for repeated access
                • Prefer typed getters (GetInt32, GetString) over GetValue
                • Use async methods for scalability
                • Consider CommandBehavior for optimization
                
                CommandBehavior options:
                • Default: Multiple result sets allowed
                • SingleResult: Only first result set
                • SchemaOnly: Returns only column information
                • KeyInfo: Returns primary key information
                • SingleRow: Optimized for single row
                • SequentialAccess: For BLOB/CLOB streaming
                • CloseConnection: Close connection when reader closed
                """);
            
            // 5. Typed accessors
            Console.WriteLine("\n5. Typed Accessors:");
            
            async Task TypedAccessorsExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand("SELECT * FROM Users", connection))
                {
                    await connection.OpenAsync();
                    
                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        // Get column ordinals (do once)
                        int idOrdinal = reader.GetOrdinal("Id");
                        int usernameOrdinal = reader.GetOrdinal("Username");
                        int emailOrdinal = reader.GetOrdinal("Email");
                        int createdOrdinal = reader.GetOrdinal("CreatedDate");
                        
                        while (await reader.ReadAsync())
                        {
                            // Fast typed access using cached ordinals
                            int id = reader.GetInt32(idOrdinal);
                            string username = reader.GetString(usernameOrdinal);
                            string email = reader.GetString(emailOrdinal);
                            DateTime created = reader.GetDateTime(createdOrdinal);
                            
                            // Process data
                        }
                    }
                }
            }
            // TypedAccessorsExample().Wait(); // Commented for demo
            
            // 6. DataReader vs DataAdapter
            Console.WriteLine("\n6. DataReader vs DataAdapter:");
            Console.WriteLine("""
                DataReader:
                • Forward-only, read-only access
                • Low memory footprint
                • High performance
                • Connection must remain open
                • Manual data processing
                
                DataAdapter/DataSet:
                • Disconnected data access
                • Bidirectional navigation
                • Data modification capabilities
                • Higher memory usage
                • Automatic connection management
                • Built-in change tracking
                
                Choose DataReader for:
                • Read-only operations
                • Large data sets
                • High-performance scenarios
                • Simple data processing
                
                Choose DataAdapter for:
                • Disconnected scenarios
                • Data binding in Windows Forms
                • Complex data manipulation
                • Offline data access
                """);
        }
        
        static void DemonstrateTransactions()
        {
            Console.WriteLine("\n=== 4. Transactions ===\n");
            
            string connectionString = "Server=localhost;Database=TestDB;Integrated Security=True;";
            
            // 1. Local transactions
            Console.WriteLine("1. Local Transactions:");
            
            async Task LocalTransactionExample()
            {
                using (var connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();
                    
                    // Begin transaction
                    using (var transaction = connection.BeginTransaction(IsolationLevel.ReadCommitted))
                    {
                        try
                        {
                            using (var command = connection.CreateCommand())
                            {
                                command.Transaction = transaction;
                                command.CommandText = "UPDATE Accounts SET Balance = Balance - 100 WHERE Id = 1";
                                await command.ExecuteNonQueryAsync();
                                
                                command.CommandText = "UPDATE Accounts SET Balance = Balance + 100 WHERE Id = 2";
                                await command.ExecuteNonQueryAsync();
                                
                                // Simulate error condition
                                bool shouldCommit = true; // Change to false to test rollback
                                
                                if (shouldCommit)
                                {
                                    transaction.Commit();
                                    Console.WriteLine("Transaction committed successfully");
                                }
                                else
                                {
                                    transaction.Rollback();
                                    Console.WriteLine("Transaction rolled back");
                                }
                            }
                        }
                        catch (Exception ex)
                        {
                            Console.WriteLine($"Error in transaction: {ex.Message}");
                            transaction.Rollback();
                            Console.WriteLine("Transaction rolled back due to error");
                            throw;
                        }
                    }
                }
            }
            // LocalTransactionExample().Wait(); // Commented for demo
            
            // 2. Transaction isolation levels
            Console.WriteLine("\n2. Transaction Isolation Levels:");
            Console.WriteLine("""
                Isolation levels (from least to most restrictive):
                
                1. Read Uncommitted (dirty reads allowed):
                   • Can read uncommitted changes from other transactions
                   • No locks on read data
                   • Fastest but least safe
                
                2. Read Committed (default):
                   • Only read committed data
                   • Prevents dirty reads
                   • Can have non-repeatable reads
                
                3. Repeatable Read:
                   • Locks read data
                   • Prevents non-repeatable reads
                   • Can have phantom reads
                
                4. Serializable:
                   • Highest isolation
                   • Locks range of data
                   • Prevents phantom reads
                   • Slowest, can cause deadlocks
                
                5. Snapshot:
                   • Uses row versioning
                   • No blocking of readers
                   • Requires tempdb space
                   • Good for read-heavy workloads
                """);
            
            // 3. Distributed transactions (System.Transactions)
            Console.WriteLine("\n3. Distributed Transactions:");
            
            async Task DistributedTransactionExample()
            {
                // Requires reference to System.Transactions
                // using (var scope = new TransactionScope(
                //     TransactionScopeOption.Required,
                //     new TransactionOptions
                //     {
                //         IsolationLevel = System.Transactions.IsolationLevel.ReadCommitted,
                //         Timeout = TimeSpan.FromMinutes(5)
                //     },
                //     TransactionScopeAsyncFlowOption.Enabled))
                // {
                //     // Multiple database operations across different connections
                //     using (var conn1 = new SqlConnection(connectionString1))
                //     using (var conn2 = new SqlConnection(connectionString2))
                //     {
                //         await conn1.OpenAsync();
                //         await conn2.OpenAsync();
                //         
                //         // Operations automatically enlisted in transaction
                //         // ...
                //     }
                //     
                //     scope.Complete(); // Commit transaction
                // }
                
                Console.WriteLine("""
                    Distributed transactions:
                    • Coordinate across multiple resources (databases, queues, etc.)
                    • Use MSDTC (Microsoft Distributed Transaction Coordinator)
                    • Complex setup and management
                    • Consider microservices patterns instead for modern apps
                    """);
            }
            DistributedTransactionExample().Wait();
            
            // 4. Savepoints
            Console.WriteLine("\n4. Transaction Savepoints:");
            
            async Task SavepointExample()
            {
                using (var connection = new SqlConnection(connectionString))
                {
                    await connection.OpenAsync();
                    
                    using (var transaction = connection.BeginTransaction())
                    {
                        try
                        {
                            using (var command = connection.CreateCommand())
                            {
                                command.Transaction = transaction;
                                
                                // First operation
                                command.CommandText = "INSERT INTO Log (Message) VALUES ('Operation 1')";
                                await command.ExecuteNonQueryAsync();
                                
                                // Create savepoint
                                transaction.Save("Savepoint1");
                                
                                // Second operation (might fail)
                                command.CommandText = "INSERT INTO Log (Message) VALUES ('Operation 2')";
                                await command.ExecuteNonQueryAsync();
                                
                                // Rollback to savepoint if needed
                                // transaction.Rollback("Savepoint1");
                                
                                transaction.Commit();
                            }
                        }
                        catch
                        {
                            transaction.Rollback();
                            throw;
                        }
                    }
                }
            }
            // SavepointExample().Wait(); // Commented for demo
            
            // 5. Transaction best practices
            Console.WriteLine("\n5. Transaction Best Practices:");
            Console.WriteLine("""
                1. Keep transactions short:
                   • Acquire locks late, release early
                   • Do minimal work within transaction
                   • Move non-essential work outside transaction
                
                2. Choose appropriate isolation level:
                   • Default to ReadCommitted
                   • Use Snapshot for read-heavy workloads
                   • Avoid Serializable unless absolutely necessary
                
                3. Handle errors properly:
                   • Always use try-catch
                   • Rollback on error
                   • Don't swallow exceptions
                
                4. Avoid distributed transactions:
                   • Complex and problematic
                   • Consider eventual consistency
                   • Use saga pattern in microservices
                
                5. Monitor transaction performance:
                   • Watch for blocking/deadlocks
                   • Monitor transaction log growth
                   • Set appropriate timeouts
                """);
            
            // 6. Deadlock handling
            Console.WriteLine("\n6. Deadlock Handling:");
            Console.WriteLine("""
                Deadlock prevention:
                • Access resources in same order
                • Keep transactions short
                • Use lower isolation levels
                • Implement retry logic
                
                Deadlock retry pattern:
                int retries = 3;
                for (int i = 0; i < retries; i++)
                {
                    try
                    {
                        // Execute transaction
                        break;
                    }
                    catch (SqlException ex) when (ex.Number == 1205) // Deadlock
                    {
                        if (i == retries - 1) throw;
                        Thread.Sleep(100 * (i + 1)); // Exponential backoff
                    }
                }
                """);
        }
        
        static void DemonstrateStoredProcedures()
        {
            Console.WriteLine("\n=== 5. Stored Procedures ===\n");
            
            string connectionString = "Server=localhost;Database=TestDB;Integrated Security=True;";
            
            // 1. Calling stored procedures
            Console.WriteLine("1. Calling Stored Procedures:");
            
            async Task StoredProcedureExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand("sp_GetUserByEmail", connection))
                {
                    command.CommandType = CommandType.StoredProcedure;
                    
                    // Input parameters
                    command.Parameters.AddWithValue("@email", "user@example.com");
                    
                    // Output parameter
                    var outputParam = new SqlParameter("@userCount", SqlDbType.Int)
                    {
                        Direction = ParameterDirection.Output
                    };
                    command.Parameters.Add(outputParam);
                    
                    // Return value parameter
                    var returnParam = new SqlParameter()
                    {
                        ParameterName = "@ReturnValue",
                        Direction = ParameterDirection.ReturnValue
                    };
                    command.Parameters.Add(returnParam);
                    
                    await connection.OpenAsync();
                    
                    using (var reader = await command.ExecuteReaderAsync())
                    {
                        while (await reader.ReadAsync())
                        {
                            // Process results
                        }
                    }
                    
                    // Access output parameter after reader is closed
                    int userCount = (int)outputParam.Value;
                    int returnValue = (int)returnParam.Value;
                    
                    Console.WriteLine($"User count: {userCount}, Return value: {returnValue}");
                }
            }
            // StoredProcedureExample().Wait(); // Commented for demo
            
            // 2. Table-valued parameters
            Console.WriteLine("\n2. Table-Valued Parameters:");
            
            async Task TableValuedParameterExample()
            {
                using (var connection = new SqlConnection(connectionString))
                using (var command = new SqlCommand("sp_InsertUsersBatch", connection))
                {
                    command.CommandType = CommandType.StoredProcedure;
                    
                    // Create DataTable for TVP
                    var userTable = new DataTable();
                    userTable.Columns.Add("Username", typeof(string));
                    userTable.Columns.Add("Email", typeof(string));
                    userTable.Columns.Add("IsActive", typeof(bool));
                    
                    // Add rows
                    userTable.Rows.Add("user1", "user1@example.com", true);
                    userTable.Rows.Add("user2", "user2@example.com", true);
                    
                    // Create TVP parameter
                    var tvpParam = new SqlParameter("@users", SqlDbType.Structured)
                    {
                        TypeName = "dbo.UserTableType", // User-defined table type
                        Value = userTable
                    };
                    command.Parameters.Add(tvpParam);
                    
                    await connection.OpenAsync();
                    await command.ExecuteNonQueryAsync();
                }
            }
            // TableValuedParameterExample().Wait(); // Commented for demo
            
            // 3. Dynamic SQL vs Stored Procedures
            Console.WriteLine("\n3. Dynamic SQL vs Stored Procedures:");
            Console.WriteLine("""
                Stored Procedures advantages:
                • Security: Execute permissions only
                • Performance: Pre-compiled, plan caching
                • Maintainability: Business logic in database
                • Reduced network traffic: Batch operations
                
                Dynamic SQL advantages:
                • Flexibility: Dynamic queries
                • Simplicity: No need to deploy procedures
                • ORM compatibility: Works better with some ORMs
                
                Security note:
                • Always use parameters, even in dynamic SQL
                • Consider sp_executesql for parameterized dynamic SQL
                """);
            
            // 4. Parameter direction
            Console.WriteLine("\n4. Parameter Direction:");
            Console.WriteLine("""
                ParameterDirection enumeration:
                • Input (default): Parameter is input only
                • InputOutput: Parameter is both input and output
                • Output: Parameter is output only
                • ReturnValue: Parameter represents return value
                
                Example with Output parameter:
                var param = new SqlParameter("@totalUsers", SqlDbType.Int)
                {
                    Direction = ParameterDirection.Output
                };
                command.Parameters.Add(param);
                
                // Execute command
                // int total = (int)param.Value; // Access after execution
                """);
        }
        
        static void DemonstrateBestPractices()
        {
            Console.WriteLine("\n=== 6. ADO.NET Best Practices ===\n");
            
            Console.WriteLine("1. Security:");
            Console.WriteLine("""
                • ALWAYS use parameterized queries
                • Never concatenate user input into SQL
                • Use least-privilege database accounts
                • Encrypt connection strings in config files
                • Validate all input before using in queries
                • Consider using stored procedures for additional security
                """);
            
            Console.WriteLine("\n2. Performance:");
            Console.WriteLine("""
                • Use connection pooling (enabled by default)
                • Open connections late, close early
                • Use async methods for scalability
                • Consider MARS (MultipleActiveResultSets) for multiple operations
                • Use appropriate CommandBehavior
                • Cache frequently used data
                • Implement pagination for large result sets
                """);
            
            Console.WriteLine("\n3. Resource Management:");
            Console.WriteLine("""
                • ALWAYS use using statements for disposable objects
                • Close DataReaders before using connection for other operations
                • Set appropriate timeouts
                • Monitor connection leaks with performance counters
                • Consider using dependency injection for connection management
                """);
            
            Console.WriteLine("\n4. Error Handling:");
            Console.WriteLine("""
                • Catch specific exceptions (SqlException, DbException)
                • Log detailed error information
                • Implement retry logic for transient errors
                • Use structured exception handling
                • Consider circuit breaker pattern for external dependencies
                """);
            
            Console.WriteLine("\n5. Connection String Management:");
            Console.WriteLine("""
                • Store connection strings in configuration files
                • Use encrypted sections for sensitive data
                • Consider using Azure Key Vault or similar for production
                • Use connection string builders for dynamic construction
                • Validate connection strings at application startup
                """);
            
            Console.WriteLine("\n6. Testing:");
            Console.WriteLine("""
                • Mock database dependencies for unit tests
                • Use in-memory databases for integration tests
                • Test with different isolation levels
                • Test error scenarios (timeouts, deadlocks)
                • Use test data factories
                """);
            
            Console.WriteLine("\n7. Migration to Entity Framework:");
            Console.WriteLine("""
                When to consider EF Core:
                • New projects with complex data models
                • Need for LINQ queries
                • Automatic change tracking
                • Cross-platform requirements
                • Microservices architecture
                
                When to stick with ADO.NET:
                • High-performance bulk operations
                • Complex stored procedure usage
                • Legacy system integration
                • Simple data access needs
                • Full control over SQL generation
                
                Hybrid approach:
                • Use EF Core for most operations
                • Use Dapper for performance-critical queries
                • Use raw ADO.NET for specialized scenarios
                """);
            
            Console.WriteLine("\n=== Common Patterns ===");
            Console.WriteLine("""
                1. Repository Pattern:
                   • Abstract data access logic
                   • Centralize SQL/Stored Procedure calls
                   • Easier testing and maintenance
                
                2. Unit of Work Pattern:
                   • Group multiple operations in single transaction
                   • Ensure data consistency
                   • Track changes across multiple repositories
                
                3. Connection Factory Pattern:
                   • Centralize connection creation
                   • Implement connection pooling strategies
                   • Easier configuration management
                
                4. Retry Pattern:
                   • Handle transient database errors
                   • Implement exponential backoff
                   • Use Polly library for complex scenarios
                
                5. Bulk Operations Pattern:
                   • Use SqlBulkCopy for large data inserts
                   • Consider table-valued parameters
                   • Batch operations to reduce round-trips
                """);
            
            Console.WriteLine("\n=== Tools and Libraries ===");
            Console.WriteLine("""
                • Dapper: Micro-ORM, high performance
                • Entity Framework Core: Full ORM
                • Polly: Resilience and transient fault handling
                • SqlBulkCopy: High-performance bulk inserts
                • MiniProfiler: Database performance profiling
                • DbUp: Database migration tool
                
                Choose based on:
                • Performance requirements
                • Development team expertise
                • Application complexity
                • Maintenance considerations
                """);
        }
    }
}