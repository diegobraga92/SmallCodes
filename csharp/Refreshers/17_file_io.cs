/*
    C# FILE I/O (INPUT/OUTPUT)
    File: 17_file_io.cs
    
    Comprehensive guide to file and directory operations in C#.
    Covers file system operations, streams, text/binary I/O,
    async file operations, compression, file monitoring, and best practices.
*/

using System;
using System.IO;
using System.IO.Compression;
using System.Text;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace CSharpRefresher.FileIO
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# File I/O Operations ===\n");
            
            DemonstrateFileSystemOperations();
            DemonstrateFileReadingWriting();
            DemonstrateStreamOperations();
            DemonstrateAsyncFileOperations();
            DemonstrateSpecializedOperations();
            DemonstrateBestPractices();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateFileSystemOperations()
        {
            Console.WriteLine("=== 1. File System Operations ===\n");
            
            // Working directory
            Console.WriteLine($"Current Directory: {Environment.CurrentDirectory}");
            Console.WriteLine($"System Directory: {Environment.SystemDirectory}");
            Console.WriteLine($"Temp Path: {Path.GetTempPath()}");
            
            // Path operations
            Console.WriteLine("\n1. Path Operations:");
            string filePath = @"C:\Users\Test\Documents\file.txt";
            Console.WriteLine($"Directory: {Path.GetDirectoryName(filePath)}");
            Console.WriteLine($"Filename: {Path.GetFileName(filePath)}");
            Console.WriteLine($"Filename without extension: {Path.GetFileNameWithoutExtension(filePath)}");
            Console.WriteLine($"Extension: {Path.GetExtension(filePath)}");
            Console.WriteLine($"Full path: {Path.GetFullPath(filePath)}");
            Console.WriteLine($"Root: {Path.GetPathRoot(filePath)}");
            Console.WriteLine($"Random filename: {Path.GetRandomFileName()}");
            Console.WriteLine($"Temp filename: {Path.GetTempFileName()}");
            
            // Combine paths safely
            string combined = Path.Combine("folder1", "folder2", "file.txt");
            Console.WriteLine($"Combined path: {combined}");
            
            // Directory operations
            Console.WriteLine("\n2. Directory Operations:");
            string testDir = Path.Combine(Path.GetTempPath(), "TestDirectory");
            
            // Create directory
            if (!Directory.Exists(testDir))
            {
                Directory.CreateDirectory(testDir);
                Console.WriteLine($"Created directory: {testDir}");
            }
            
            // Get directory information
            var dirInfo = new DirectoryInfo(testDir);
            Console.WriteLine($"Directory exists: {dirInfo.Exists}");
            Console.WriteLine($"Directory name: {dirInfo.Name}");
            Console.WriteLine($"Full name: {dirInfo.FullName}");
            Console.WriteLine($"Parent: {dirInfo.Parent?.Name}");
            Console.WriteLine($"Root: {dirInfo.Root.Name}");
            Console.WriteLine($"Created: {dirInfo.CreationTime}");
            Console.WriteLine($"Last accessed: {dirInfo.LastAccessTime}");
            Console.WriteLine($"Last written: {dirInfo.LastWriteTime}");
            
            // List files and directories
            Console.WriteLine("\n3. Enumerating Files and Directories:");
            
            // Create some test files
            for (int i = 1; i <= 3; i++)
            {
                string testFile = Path.Combine(testDir, $"test{i}.txt");
                File.WriteAllText(testFile, $"Content {i}");
            }
            
            // Create subdirectory
            string subDir = Path.Combine(testDir, "Subfolder");
            Directory.CreateDirectory(subDir);
            
            // Enumerate files
            Console.WriteLine("Files in directory:");
            var files = Directory.EnumerateFiles(testDir);
            foreach (var file in files)
            {
                Console.WriteLine($"  {Path.GetFileName(file)}");
            }
            
            // Enumerate directories
            Console.WriteLine("Directories in directory:");
            var dirs = Directory.EnumerateDirectories(testDir);
            foreach (var dir in dirs)
            {
                Console.WriteLine($"  {Path.GetFileName(dir)}");
            }
            
            // Recursive enumeration
            Console.WriteLine("All files (recursive):");
            var allFiles = Directory.EnumerateFiles(testDir, "*", SearchOption.AllDirectories);
            foreach (var file in allFiles)
            {
                Console.WriteLine($"  {file}");
            }
            
            // File operations
            Console.WriteLine("\n4. File Operations:");
            string sourceFile = Path.Combine(testDir, "test1.txt");
            string destFile = Path.Combine(testDir, "test1_copy.txt");
            string moveFile = Path.Combine(testDir, "test1_moved.txt");
            
            // Copy file
            File.Copy(sourceFile, destFile, overwrite: true);
            Console.WriteLine($"Copied: {sourceFile} -> {destFile}");
            
            // Move/rename file
            File.Move(destFile, moveFile);
            Console.WriteLine($"Moved: {destFile} -> {moveFile}");
            
            // Delete file
            File.Delete(moveFile);
            Console.WriteLine($"Deleted: {moveFile}");
            
            // File attributes
            Console.WriteLine("\n5. File Attributes:");
            var fileInfo = new FileInfo(sourceFile);
            Console.WriteLine($"File exists: {fileInfo.Exists}");
            Console.WriteLine($"File size: {fileInfo.Length} bytes");
            Console.WriteLine($"Is read-only: {fileInfo.IsReadOnly}");
            Console.WriteLine($"Attributes: {fileInfo.Attributes}");
            
            // Set file attributes
            fileInfo.Attributes |= FileAttributes.ReadOnly;
            Console.WriteLine($"Set read-only attribute");
            
            // Remove read-only attribute
            fileInfo.Attributes &= ~FileAttributes.ReadOnly;
            Console.WriteLine($"Removed read-only attribute");
            
            // Drive information
            Console.WriteLine("\n6. Drive Information:");
            DriveInfo[] drives = DriveInfo.GetDrives();
            foreach (DriveInfo drive in drives)
            {
                if (drive.IsReady)
                {
                    Console.WriteLine($"Drive: {drive.Name}");
                    Console.WriteLine($"  Type: {drive.DriveType}");
                    Console.WriteLine($"  Format: {drive.DriveFormat}");
                    Console.WriteLine($"  Total size: {drive.TotalSize:N0} bytes");
                    Console.WriteLine($"  Free space: {drive.TotalFreeSpace:N0} bytes");
                    Console.WriteLine($"  Available: {drive.AvailableFreeSpace:N0} bytes");
                }
            }
            
            // Cleanup
            Directory.Delete(testDir, recursive: true);
            Console.WriteLine($"\nCleaned up test directory: {testDir}");
        }
        
        static void DemonstrateFileReadingWriting()
        {
            Console.WriteLine("\n=== 2. File Reading and Writing ===\n");
            
            string tempFile = Path.GetTempFileName();
            
            // 1. Simple text file operations
            Console.WriteLine("1. Simple Text File Operations:");
            
            // WriteAllText
            File.WriteAllText(tempFile, "Hello, World!\nThis is a test file.");
            Console.WriteLine($"Written to file: {tempFile}");
            
            // ReadAllText
            string content = File.ReadAllText(tempFile);
            Console.WriteLine($"File content:\n{content}");
            
            // AppendAllText
            File.AppendAllText(tempFile, "\nAppended line.");
            content = File.ReadAllText(tempFile);
            Console.WriteLine($"After append:\n{content}");
            
            // WriteAllLines / ReadAllLines
            Console.WriteLine("\n2. Line-based Operations:");
            string[] lines = { "Line 1", "Line 2", "Line 3" };
            File.WriteAllLines(tempFile, lines);
            
            string[] readLines = File.ReadAllLines(tempFile);
            Console.WriteLine($"Lines read ({readLines.Length}):");
            foreach (var line in readLines)
            {
                Console.WriteLine($"  {line}");
            }
            
            // 3. Binary file operations
            Console.WriteLine("\n3. Binary File Operations:");
            
            byte[] binaryData = { 0x48, 0x65, 0x6C, 0x6C, 0x6F }; // "Hello"
            File.WriteAllBytes(tempFile, binaryData);
            
            byte[] readBytes = File.ReadAllBytes(tempFile);
            Console.WriteLine($"Bytes read ({readBytes.Length}): {BitConverter.ToString(readBytes)}");
            
            // 4. Character encoding
            Console.WriteLine("\n4. Character Encoding:");
            
            // Write with specific encoding
            File.WriteAllText(tempFile, "Café", Encoding.UTF8);
            byte[] utf8Bytes = File.ReadAllBytes(tempFile);
            Console.WriteLine($"UTF-8 bytes: {BitConverter.ToString(utf8Bytes)}");
            
            File.WriteAllText(tempFile, "Café", Encoding.Unicode);
            byte[] unicodeBytes = File.ReadAllBytes(tempFile);
            Console.WriteLine($"Unicode bytes: {BitConverter.ToString(unicodeBytes)}");
            
            // Detect encoding
            using (var reader = new StreamReader(tempFile, detectEncodingFromByteOrderMarks: true))
            {
                Console.WriteLine($"Detected encoding: {reader.CurrentEncoding.EncodingName}");
                Console.WriteLine($"Content: {reader.ReadToEnd()}");
            }
            
            // 5. File streaming with using statement
            Console.WriteLine("\n5. FileStream Operations:");
            
            using (FileStream fs = new FileStream(tempFile, FileMode.Create, FileAccess.Write))
            {
                string text = "Streaming text content";
                byte[] buffer = Encoding.UTF8.GetBytes(text);
                fs.Write(buffer, 0, buffer.Length);
                Console.WriteLine($"Written {buffer.Length} bytes via FileStream");
            }
            
            using (FileStream fs = new FileStream(tempFile, FileMode.Open, FileAccess.Read))
            {
                byte[] buffer = new byte[fs.Length];
                int bytesRead = fs.Read(buffer, 0, buffer.Length);
                string text = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                Console.WriteLine($"Read {bytesRead} bytes: {text}");
            }
            
            // Cleanup
            File.Delete(tempFile);
        }
        
        static void DemonstrateStreamOperations()
        {
            Console.WriteLine("\n=== 3. Stream Operations ===\n");
            
            string tempFile = Path.GetTempFileName();
            
            // 1. StreamWriter and StreamReader
            Console.WriteLine("1. StreamWriter and StreamReader:");
            
            using (StreamWriter writer = new StreamWriter(tempFile))
            {
                writer.WriteLine("First line");
                writer.WriteLine("Second line");
                writer.Write("Third line");
                writer.Flush(); // Explicit flush
                Console.WriteLine("Written with StreamWriter");
            }
            
            using (StreamReader reader = new StreamReader(tempFile))
            {
                string line;
                while ((line = reader.ReadLine()) != null)
                {
                    Console.WriteLine($"Read line: {line}");
                }
                Console.WriteLine($"End of stream: {reader.EndOfStream}");
            }
            
            // 2. BinaryWriter and BinaryReader
            Console.WriteLine("\n2. BinaryWriter and BinaryReader:");
            
            using (FileStream fs = new FileStream(tempFile, FileMode.Create))
            using (BinaryWriter writer = new BinaryWriter(fs))
            {
                writer.Write(42); // int
                writer.Write(3.14159); // double
                writer.Write(true); // bool
                writer.Write("Hello"); // string
                Console.WriteLine("Written binary data");
            }
            
            using (FileStream fs = new FileStream(tempFile, FileMode.Open))
            using (BinaryReader reader = new BinaryReader(fs))
            {
                int intValue = reader.ReadInt32();
                double doubleValue = reader.ReadDouble();
                bool boolValue = reader.ReadBoolean();
                string stringValue = reader.ReadString();
                
                Console.WriteLine($"Read values: {intValue}, {doubleValue}, {boolValue}, \"{stringValue}\"");
            }
            
            // 3. MemoryStream
            Console.WriteLine("\n3. MemoryStream:");
            
            using (MemoryStream ms = new MemoryStream())
            {
                byte[] data = Encoding.UTF8.GetBytes("Memory stream content");
                ms.Write(data, 0, data.Length);
                
                ms.Position = 0; // Reset position for reading
                byte[] buffer = new byte[ms.Length];
                ms.Read(buffer, 0, buffer.Length);
                Console.WriteLine($"MemoryStream content: {Encoding.UTF8.GetString(buffer)}");
            }
            
            // 4. BufferedStream
            Console.WriteLine("\n4. BufferedStream:");
            
            using (FileStream fs = new FileStream(tempFile, FileMode.Create))
            using (BufferedStream bs = new BufferedStream(fs, 4096)) // 4KB buffer
            using (StreamWriter writer = new StreamWriter(bs))
            {
                for (int i = 0; i < 1000; i++)
                {
                    writer.WriteLine($"Line {i}");
                }
                Console.WriteLine("Written with buffering for performance");
            }
            
            // 5. Seeking in streams
            Console.WriteLine("\n5. Stream Seeking:");
            
            using (FileStream fs = new FileStream(tempFile, FileMode.Open))
            {
                Console.WriteLine($"Length: {fs.Length}");
                Console.WriteLine($"Position: {fs.Position}");
                
                // Seek to middle
                fs.Seek(fs.Length / 2, SeekOrigin.Begin);
                Console.WriteLine($"Position after seek to middle: {fs.Position}");
                
                // Seek from current position
                fs.Seek(-10, SeekOrigin.Current);
                Console.WriteLine($"Position after seeking back 10 bytes: {fs.Position}");
                
                // Seek from end
                fs.Seek(-20, SeekOrigin.End);
                Console.WriteLine($"Position after seeking 20 bytes from end: {fs.Position}");
            }
            
            // 6. Stream copying
            Console.WriteLine("\n6. Stream Copying:");
            
            string sourceFile = tempFile;
            string destFile = Path.Combine(Path.GetTempPath(), "copied_file.txt");
            
            using (FileStream source = new FileStream(sourceFile, FileMode.Open))
            using (FileStream dest = new FileStream(destFile, FileMode.Create))
            {
                source.CopyTo(dest);
                Console.WriteLine($"Copied {source.Length} bytes from {sourceFile} to {destFile}");
            }
            
            // Cleanup
            File.Delete(tempFile);
            File.Delete(destFile);
        }
        
        static void DemonstrateAsyncFileOperations()
        {
            Console.WriteLine("\n=== 4. Async File Operations ===\n");
            
            string tempFile = Path.GetTempFileName();
            
            // 1. Async text operations
            Console.WriteLine("1. Async Text Operations:");
            
            async Task AsyncTextExample()
            {
                await File.WriteAllTextAsync(tempFile, "Async file content");
                Console.WriteLine("Async write completed");
                
                string content = await File.ReadAllTextAsync(tempFile);
                Console.WriteLine($"Async read completed: {content}");
                
                await File.AppendAllTextAsync(tempFile, "\nAppended async");
                Console.WriteLine("Async append completed");
            }
            
            AsyncTextExample().Wait();
            
            // 2. Async line operations
            Console.WriteLine("\n2. Async Line Operations:");
            
            async Task AsyncLinesExample()
            {
                string[] lines = { "Async line 1", "Async line 2", "Async line 3" };
                await File.WriteAllLinesAsync(tempFile, lines);
                
                var readLines = await File.ReadAllLinesAsync(tempFile);
                Console.WriteLine($"Read {readLines.Length} lines asynchronously");
            }
            
            AsyncLinesExample().Wait();
            
            // 3. Async stream operations
            Console.WriteLine("\n3. Async Stream Operations:");
            
            async Task AsyncStreamExample()
            {
                using (FileStream fs = new FileStream(tempFile, FileMode.Create, FileAccess.Write, 
                       FileShare.None, bufferSize: 4096, useAsync: true))
                {
                    string text = "Async stream content";
                    byte[] buffer = Encoding.UTF8.GetBytes(text);
                    await fs.WriteAsync(buffer, 0, buffer.Length);
                    Console.WriteLine("Async stream write completed");
                }
                
                using (FileStream fs = new FileStream(tempFile, FileMode.Open, FileAccess.Read, 
                       FileShare.None, bufferSize: 4096, useAsync: true))
                {
                    byte[] buffer = new byte[fs.Length];
                    int bytesRead = await fs.ReadAsync(buffer, 0, buffer.Length);
                    string text = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    Console.WriteLine($"Async stream read: {text}");
                }
            }
            
            AsyncStreamExample().Wait();
            
            // 4. Async StreamReader/StreamWriter
            Console.WriteLine("\n4. Async StreamReader/StreamWriter:");
            
            async Task AsyncReaderWriterExample()
            {
                using (StreamWriter writer = new StreamWriter(tempFile))
                {
                    await writer.WriteLineAsync("Async line 1");
                    await writer.WriteLineAsync("Async line 2");
                    await writer.FlushAsync();
                }
                
                using (StreamReader reader = new StreamReader(tempFile))
                {
                    string line;
                    while ((line = await reader.ReadLineAsync()) != null)
                    {
                        Console.WriteLine($"Async read line: {line}");
                    }
                }
            }
            
            AsyncReaderWriterExample().Wait();
            
            // 5. Cancellation support
            Console.WriteLine("\n5. Async with Cancellation:");
            
            async Task AsyncWithCancellation()
            {
                var cts = new System.Threading.CancellationTokenSource();
                cts.CancelAfter(100); // Cancel after 100ms
                
                try
                {
                    using (FileStream fs = new FileStream(tempFile, FileMode.Create, FileAccess.Write,
                           FileShare.None, bufferSize: 4096, useAsync: true))
                    {
                        byte[] buffer = new byte[1000000]; // Large buffer
                        await fs.WriteAsync(buffer, 0, buffer.Length, cts.Token);
                    }
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("Async operation cancelled");
                }
            }
            
            AsyncWithCancellation().Wait();
            
            // Cleanup
            File.Delete(tempFile);
        }
        
        static void DemonstrateSpecializedOperations()
        {
            Console.WriteLine("\n=== 5. Specialized File Operations ===\n");
            
            // 1. File compression (GZip)
            Console.WriteLine("1. File Compression (GZip):");
            
            string sourceFile = Path.GetTempFileName();
            string compressedFile = sourceFile + ".gz";
            string decompressedFile = sourceFile + ".decompressed";
            
            // Write test data
            string testData = new string('X', 10000); // 10KB of data
            File.WriteAllText(sourceFile, testData);
            
            // Compress
            using (FileStream sourceStream = new FileStream(sourceFile, FileMode.Open))
            using (FileStream compressedStream = File.Create(compressedFile))
            using (GZipStream compressionStream = new GZipStream(compressedStream, CompressionMode.Compress))
            {
                sourceStream.CopyTo(compressionStream);
            }
            
            Console.WriteLine($"Original size: {new FileInfo(sourceFile).Length} bytes");
            Console.WriteLine($"Compressed size: {new FileInfo(compressedFile).Length} bytes");
            Console.WriteLine($"Compression ratio: {(double)new FileInfo(compressedFile).Length / new FileInfo(sourceFile).Length:P}");
            
            // Decompress
            using (FileStream compressedStream = new FileStream(compressedFile, FileMode.Open))
            using (FileStream decompressedStream = File.Create(decompressedFile))
            using (GZipStream decompressionStream = new GZipStream(compressedStream, CompressionMode.Decompress))
            {
                decompressionStream.CopyTo(decompressedStream);
            }
            
            string decompressedData = File.ReadAllText(decompressedFile);
            Console.WriteLine($"Decompressed successfully: {decompressedData.Length == testData.Length}");
            
            // 2. ZIP archives
            Console.WriteLine("\n2. ZIP Archive Operations:");
            
            string zipFile = Path.GetTempFileName() + ".zip";
            string extractDir = Path.Combine(Path.GetTempPath(), "Extracted");
            
            // Create ZIP archive
            using (ZipArchive archive = ZipFile.Open(zipFile, ZipArchiveMode.Create))
            {
                archive.CreateEntryFromFile(sourceFile, "file1.txt");
                archive.CreateEntryFromFile(sourceFile, "folder/file2.txt");
                Console.WriteLine($"Created ZIP archive with {archive.Entries.Count} entries");
            }
            
            // Extract ZIP archive
            ZipFile.ExtractToDirectory(zipFile, extractDir);
            Console.WriteLine($"Extracted to: {extractDir}");
            
            // Read ZIP archive
            using (ZipArchive archive = ZipFile.OpenRead(zipFile))
            {
                foreach (ZipArchiveEntry entry in archive.Entries)
                {
                    Console.WriteLine($"  Entry: {entry.FullName}, Size: {entry.Length}, Compressed: {entry.CompressedLength}");
                }
            }
            
            // 3. File system watcher
            Console.WriteLine("\n3. File System Watcher:");
            
            string watchDir = Path.GetTempPath();
            using (FileSystemWatcher watcher = new FileSystemWatcher(watchDir))
            {
                watcher.NotifyFilter = NotifyFilters.LastWrite | NotifyFilters.FileName | NotifyFilters.DirectoryName;
                watcher.Filter = "*.txt";
                
                watcher.Changed += (sender, e) => Console.WriteLine($"Changed: {e.FullPath}");
                watcher.Created += (sender, e) => Console.WriteLine($"Created: {e.FullPath}");
                watcher.Deleted += (sender, e) => Console.WriteLine($"Deleted: {e.FullPath}");
                watcher.Renamed += (sender, e) => Console.WriteLine($"Renamed: {e.OldFullPath} -> {e.FullPath}");
                
                watcher.EnableRaisingEvents = true;
                watcher.IncludeSubdirectories = true;
                
                Console.WriteLine($"Watching directory: {watchDir} (press any key to stop)");
                System.Threading.Thread.Sleep(2000); // Give time to see events
            }
            
            // 4. Memory-mapped files (advanced)
            Console.WriteLine("\n4. Memory-Mapped Files (Concept):");
            Console.WriteLine("""
                Memory-mapped files allow file access via memory pointers.
                Useful for:
                • Large file processing
                • Inter-process communication
                • Random access to large files
                
                Classes: MemoryMappedFile, MemoryMappedViewAccessor
                Namespace: System.IO.MemoryMappedFiles
                """);
            
            // 5. Isolated storage (legacy, for sandboxed apps)
            Console.WriteLine("\n5. Isolated Storage (Concept):");
            Console.WriteLine("""
                Isolated storage provides safe file access for:
                • Partial-trust applications
                • ClickOnce deployments
                • Silverlight applications
                
                Note: Less used in modern .NET, consider AppData instead.
                """);
            
            // Cleanup
            File.Delete(sourceFile);
            File.Delete(compressedFile);
            File.Delete(decompressedFile);
            File.Delete(zipFile);
            Directory.Delete(extractDir, recursive: true);
        }
        
        static void DemonstrateBestPractices()
        {
            Console.WriteLine("\n=== 6. File I/O Best Practices ===\n");
            
            Console.WriteLine("1. Always Use Using Statements:");
            Console.WriteLine("""
                Good:
                using (var stream = new FileStream(...))
                {
                    // work with stream
                }
                
                Bad:
                var stream = new FileStream(...);
                // work with stream
                stream.Dispose(); // Might not be called on exception
                """);
            
            Console.WriteLine("\n2. Handle Exceptions Properly:");
            Console.WriteLine("""
                Common file exceptions:
                • FileNotFoundException
                • DirectoryNotFoundException
                • IOException (disk full, sharing violation)
                • UnauthorizedAccessException
                • PathTooLongException
                • ArgumentException (invalid characters)
                """);
            
            Console.WriteLine("\n3. Use Async I/O for Responsive Applications:");
            Console.WriteLine("""
                Synchronous (blocks thread):
                File.ReadAllText(path);
                
                Asynchronous (doesn't block):
                await File.ReadAllTextAsync(path);
                """);
            
            Console.WriteLine("\n4. Validate File Paths:");
            Console.WriteLine("""
                Before using paths:
                • Check for invalid characters: Path.GetInvalidPathChars()
                • Validate length: path.Length < 260 (Windows limit)
                • Use Path.Combine() instead of string concatenation
                • Consider cross-platform path separators
                """);
            
            Console.WriteLine("\n5. Consider Security:");
            Console.WriteLine("""
                Security considerations:
                • Validate user input for file paths
                • Use appropriate file permissions
                • Consider encryption for sensitive data
                • Sanitize file names to prevent path traversal
                • Use secure temp file creation
                """);
            
            Console.WriteLine("\n6. Performance Tips:");
            Console.WriteLine("""
                • Use buffering (BufferedStream, default buffer sizes)
                • Consider memory-mapped files for large files
                • Use appropriate FileOptions (e.g., FileOptions.SequentialScan)
                • Avoid many small I/O operations (batch when possible)
                • Use async I/O for concurrent operations
                """);
            
            Console.WriteLine("\n7. Cross-Platform Considerations:");
            Console.WriteLine("""
                • Use Path.Combine() for path building
                • Be aware of case sensitivity on Linux/macOS
                • Use Environment.NewLine for line endings
                • Consider different path length limits
                • Test on target platforms
                """);
            
            Console.WriteLine("\n8. File Locking and Sharing:");
            Console.WriteLine("""
                • Use appropriate FileShare modes
                • Consider FileStream.Lock() for region locking
                • Implement retry logic for sharing violations
                • Use Mutex or other synchronization for cross-process
                """);
            
            Console.WriteLine("\n9. Monitoring and Logging:");
            Console.WriteLine("""
                • Log file operations for debugging
                • Monitor disk space before large operations
                • Implement progress reporting for long operations
                • Consider using FileSystemWatcher for reactive applications
                """);
            
            Console.WriteLine("\n10. Testing Considerations:");
            Console.WriteLine("""
                • Use mock file systems for unit tests
                • Test edge cases (empty files, large files, special characters)
                • Test error conditions (disk full, permissions)
                • Consider using temporary files for testing
                • Clean up test files after tests
                """);
            
            Console.WriteLine("\n=== Common Patterns ===");
            Console.WriteLine("""
                1. Read/Process/Write Pattern:
                   - Read file into memory
                   - Process data
                   - Write results to new file
                
                2. Streaming Pattern:
                   - Process file in chunks
                   - Low memory usage for large files
                   - Use StreamReader/StreamWriter or BinaryReader/BinaryWriter
                
                3. Producer/Consumer with Files:
                   - Producer reads/writes files
                   - Consumer processes data
                   - Use BlockingCollection or Channels
                
                4. File Import/Export:
                   - Validate file format
                   - Parse with appropriate reader
                   - Handle format errors gracefully
                   - Provide progress feedback
                
                5. Log File Rotation:
                   - Create new log file periodically
                   - Compress old logs
                   - Delete very old logs
                   - Use rolling file appenders (log4net, NLog)
                """);
        }
    }
}