/*
    C# DEPLOYMENT
    File: 29_deployment.cs
    
    Comprehensive guide to deployment in C# and .NET applications.
    Covers build systems, packaging, deployment targets, CI/CD pipelines,
    containerization, cloud deployment, configuration management, monitoring,
    and real-world deployment strategies.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;
using System.Reflection;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace CSharpRefresher.Deployment
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Deployment ===\n");
            
            DemonstrateDeploymentFundamentals();
            DemonstrateBuildSystems();
            DemonstratePackaging();
            DemonstrateDeploymentTargets();
            DemonstrateCICD();
            DemonstrateContainerization();
            DemonstrateCloudDeployment();
            DemonstrateConfigurationManagement();
            DemonstrateMonitoringAndObservability();
            DemonstrateRealWorldDeploymentStrategies();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateDeploymentFundamentals()
        {
            Console.WriteLine("=== 1. Deployment Fundamentals ===\n");
            
            // 1. Deployment concepts
            Console.WriteLine("1. Deployment Concepts:");
            Console.WriteLine("""
                Key deployment concepts:
                • Build: Compiling source code into executable artifacts
                • Package: Bundling artifacts with dependencies
                • Deploy: Installing/updating software on target environments
                • Release: Making software available to users
                • Rollback: Reverting to previous version
                • Blue-green deployment: Running two identical environments
                • Canary deployment: Gradual rollout to subset of users
                • Feature flags: Conditional feature activation
                
                Deployment environments:
                • Development: Local developer machines
                • Testing/QA: Dedicated testing environment
                • Staging: Production-like environment for final testing
                • Production: Live environment serving users
                • Disaster Recovery (DR): Backup environment for failures
                
                Deployment models:
                • On-premises: Self-hosted infrastructure
                • Cloud: Hosted on cloud providers (Azure, AWS, GCP)
                • Hybrid: Mix of on-premises and cloud
                • Serverless: Function-as-a-Service (FaaS)
                • Containerized: Docker, Kubernetes
                """);
            
            // 2. .NET deployment options
            Console.WriteLine("\n2. .NET Deployment Options:");
            Console.WriteLine("""
                Framework-dependent deployment (FDD):
                • Requires .NET runtime on target machine
                • Smaller deployment package
                • Uses shared framework
                • Easier updates (just update runtime)
                
                Self-contained deployment (SCD):
                • Includes .NET runtime in package
                • Larger deployment package
                • No runtime dependency on target
                • Can target specific OS/architecture
                
                Single-file deployment:
                • All dependencies in single executable
                • No extraction at runtime (ready-to-run)
                • Improved startup performance
                • Smaller footprint with trimming
                
                ReadyToRun (R2R) compilation:
                • Ahead-of-time (AOT) compilation
                • Faster startup, less JIT compilation
                • Larger binaries
                • Platform-specific
                
                Native AOT (NativeAOT):
                • Fully native compilation
                • Smallest footprint, fastest startup
                • No JIT, no runtime
                • Limited reflection capabilities
                """);
            
            // 3. Deployment checklist
            Console.WriteLine("\n3. Deployment Checklist:");
            Console.WriteLine("""
                Pre-deployment:
                • Code review completed
                • All tests passing (unit, integration, E2E)
                • Security scan completed
                • Performance testing completed
                • Documentation updated
                • Rollback plan defined
                
                Deployment:
                • Backup current version
                • Deploy to staging first
                • Smoke tests on staging
                • Deploy to production
                • Monitor during deployment
                • Run health checks
                
                Post-deployment:
                • Verify functionality
                • Monitor metrics and logs
                • Gather user feedback
                • Update deployment documentation
                • Schedule cleanup (if needed)
                
                Rollback criteria:
                • Critical bugs affecting core functionality
                • Performance degradation beyond threshold
                • Security vulnerabilities discovered
                • Data corruption or loss
                • Service unavailability
                """);
        }
        
        static void DemonstrateBuildSystems()
        {
            Console.WriteLine("\n=== 2. Build Systems ===\n");
            
            // 1. MSBuild
            Console.WriteLine("1. MSBuild:");
            Console.WriteLine("""
                MSBuild project file (csproj):
                <Project Sdk="Microsoft.NET.Sdk">
                  <PropertyGroup>
                    <TargetFramework>net8.0</TargetFramework>
                    <OutputType>Exe</OutputType>
                    <Nullable>enable</Nullable>
                    <ImplicitUsings>enable</ImplicitUsings>
                    <AssemblyName>MyApplication</AssemblyName>
                    <RootNamespace>MyCompany.MyApplication</RootNamespace>
                    
                    <!-- Build configuration -->
                    <Configuration>Release</Configuration>
                    <Platform>AnyCPU</Platform>
                    
                    <!-- Optimization -->
                    <Optimize>true</Optimize>
                    <DebugType>embedded</DebugType>
                    <DebugSymbols>true</DebugSymbols>
                    
                    <!-- Deployment settings -->
                    <SelfContained>true</SelfContained>
                    <RuntimeIdentifier>win-x64</RuntimeIdentifier>
                    <PublishSingleFile>true</PublishSingleFile>
                    <PublishTrimmed>true</PublishTrimmed>
                    <PublishReadyToRun>true</PublishReadyToRun>
                    
                    <!-- Versioning -->
                    <Version>1.2.3.4</Version>
                    <AssemblyVersion>1.2.3.4</AssemblyVersion>
                    <FileVersion>1.2.3.4</FileVersion>
                    <InformationalVersion>1.2.3-beta</InformationalVersion>
                  </PropertyGroup>
                  
                  <PropertyGroup Condition="'$(Configuration)' == 'Release'">
                    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
                    <WarningsAsErrors>NU1605</WarningsAsErrors>
                  </PropertyGroup>
                  
                  <ItemGroup>
                    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
                    <PackageReference Include="Microsoft.Extensions.Logging" Version="8.0.0" />
                  </ItemGroup>
                </Project>
                
                MSBuild commands:
                // Restore dependencies
                dotnet restore
                
                // Build project
                dotnet build --configuration Release
                
                // Clean build artifacts
                dotnet clean
                
                // Publish for deployment
                dotnet publish --configuration Release --runtime win-x64 --self-contained true
                
                // Build with specific properties
                dotnet build -p:Version=2.0.0 -p:AssemblyVersion=2.0.0.0
                
                Custom MSBuild targets:
                <Target Name="CustomDeployment" AfterTargets="Publish">
                  <Message Importance="high" Text="Custom deployment step..." />
                  <Copy SourceFiles="$(PublishDir)\*.*" 
                        DestinationFolder="C:\Deployments\$(AssemblyName)" />
                  <Exec Command="powershell -File deploy.ps1 -Path 'C:\Deployments\$(AssemblyName)'" />
                </Target>
                """);
            
            // 2. Build configurations
            Console.WriteLine("\n2. Build Configurations:");
            Console.WriteLine("""
                Debug vs Release:
                • Debug: Debug symbols, no optimization, defines DEBUG constant
                • Release: Optimized, smaller, faster, defines RELEASE constant
                
                Custom configurations:
                // In Directory.Build.props or csproj
                <Project>
                  <PropertyGroup>
                    <Configurations>Debug;Release;Staging;Production</Configurations>
                  </PropertyGroup>
                  
                  <PropertyGroup Condition="'$(Configuration)' == 'Staging'">
                    <DefineConstants>STAGING</DefineConstants>
                    <EnvironmentName>Staging</EnvironmentName>
                    <DebugType>embedded</DebugType>
                  </PropertyGroup>
                  
                  <PropertyGroup Condition="'$(Configuration)' == 'Production'">
                    <DefineConstants>PRODUCTION</DefineConstants>
                    <EnvironmentName>Production</EnvironmentName>
                    <Optimize>true</Optimize>
                    <DebugType>none</DebugType>
                  </PropertyGroup>
                </Project>
                
                Conditional compilation:
                #if DEBUG
                    // Debug-only code
                    services.AddSingleton<IDebugService, DebugService>();
                #endif
                
                #if STAGING
                    // Staging-specific configuration
                    services.Configure<ApiOptions>(options => 
                        options.BaseUrl = "https://staging-api.example.com");
                #endif
                
                #if PRODUCTION
                    // Production-specific configuration  
                    services.Configure<ApiOptions>(options =>
                        options.BaseUrl = "https://api.example.com");
                #endif
                
                Build optimization:
                • Incremental builds: Only rebuild changed files
                • Parallel builds: Build multiple projects simultaneously
                • Build caching: Reuse previous build outputs
                • Deterministic builds: Same input produces same output
                """);
            
            // 3. Build automation
            Console.WriteLine("\n3. Build Automation:");
            Console.WriteLine("""
                Directory.Build.props and Directory.Build.targets:
                // Directory.Build.props (common properties)
                <Project>
                  <PropertyGroup>
                    <Authors>My Company</Authors>
                    <Company>My Company Inc.</Company>
                    <Copyright>Copyright © $(Company) $([System.DateTime]::Now.Year)</Copyright>
                    <NeutralLanguage>en</NeutralLanguage>
                    <PackageLicenseExpression>MIT</PackageLicenseExpression>
                    <PackageProjectUrl>https://github.com/mycompany/myapp</PackageProjectUrl>
                    <RepositoryUrl>https://github.com/mycompany/myapp.git</RepositoryUrl>
                    <RepositoryType>git</RepositoryType>
                  </PropertyGroup>
                </Project>
                
                // Directory.Build.targets (common targets)
                <Project>
                  <Target Name="GenerateBuildInfo" BeforeTargets="CoreCompile">
                    <WriteLinesToFile 
                      File="$(IntermediateOutputPath)BuildInfo.g.cs"
                      Lines="
                        namespace $(RootNamespace).Build 
                        {
                          public static class BuildInfo 
                          {
                            public const string Version = "$(Version)";
                            public const string Configuration = "$(Configuration)";
                            public const string TargetFramework = "$(TargetFramework)";
                            public static readonly DateTime BuildDate = 
                              DateTime.Parse("$([System.DateTime]::Now.ToString("o"))");
                          }
                        }"
                      Overwrite="true" />
                    
                    <ItemGroup>
                      <Compile Include="$(IntermediateOutputPath)BuildInfo.g.cs" />
                    </ItemGroup>
                  </Target>
                </Project>
                
                Custom build scripts:
                // build.ps1 (PowerShell)
                param(
                    [string]$Configuration = "Release",
                    [string]$Runtime = "win-x64",
                    [switch]$Clean,
                    [switch]$Test,
                    [switch]$Publish
                )
                
                if ($Clean) {
                    Write-Host "Cleaning..." -ForegroundColor Yellow
                    dotnet clean -c $Configuration
                }
                
                Write-Host "Restoring dependencies..." -ForegroundColor Yellow
                dotnet restore
                
                Write-Host "Building..." -ForegroundColor Yellow
                dotnet build -c $Configuration --no-restore
                
                if ($Test) {
                    Write-Host "Testing..." -ForegroundColor Yellow
                    dotnet test -c $Configuration --no-build
                }
                
                if ($Publish) {
                    Write-Host "Publishing..." -ForegroundColor Yellow
                    dotnet publish -c $Configuration -r $Runtime --self-contained true
                }
                
                // build.sh (Bash)
                #!/bin/bash
                CONFIGURATION=${1:-Release}
                RUNTIME=${2:-linux-x64}
                
                echo "Building with configuration: $CONFIGURATION, runtime: $RUNTIME"
                
                dotnet restore
                dotnet build -c $CONFIGURATION --no-restore
                dotnet test -c $CONFIGURATION --no-build
                dotnet publish -c $CONFIGURATION -r $RUNTIME --self-contained true
                """);
        }
        
        static void DemonstratePackaging()
        {
            Console.WriteLine("\n=== 3. Packaging ===\n");
            
            // 1. NuGet packages
            Console.WriteLine("1. NuGet Packages:");
            Console.WriteLine("""
                Creating NuGet packages:
                <Project Sdk="Microsoft.NET.Sdk">
                  <PropertyGroup>
                    <TargetFramework>net8.0</TargetFramework>
                    <PackageId>MyCompany.MyLibrary</PackageId>
                    <Version>1.0.0</Version>
                    <Authors>My Company</Authors>
                    <Description>An awesome .NET library</Description>
                    <PackageLicenseExpression>MIT</PackageLicenseExpression>
                    <PackageProjectUrl>https://github.com/mycompany/mylibrary</PackageProjectUrl>
                    <RepositoryUrl>https://github.com/mycompany/mylibrary.git</RepositoryUrl>
                    <RepositoryType>git</RepositoryType>
                    <GeneratePackageOnBuild>true</GeneratePackageOnBuild>
                    <IncludeSymbols>true</IncludeSymbols>
                    <SymbolPackageFormat>snupkg</SymbolPackageFormat>
                  </PropertyGroup>
                </Project>
                
                Pack command:
                dotnet pack --configuration Release --output ./nupkg
                
                Package sources:
                // Add package source
                dotnet nuget add source https://api.nuget.org/v3/index.json -n nuget.org
                
                // List sources
                dotnet nuget list source
                
                // Push package
                dotnet nuget push .\nupkg\*.nupkg -k $API_KEY -s https://api.nuget.org/v3/index.json
                
                Local package feeds:
                // Create local feed directory
                mkdir C:\LocalNuGetFeed
                
                // Add as source
                dotnet nuget add source C:\LocalNuGetFeed -n LocalFeed
                
                // Push to local feed
                dotnet nuget push .\nupkg\*.nupkg -s LocalFeed
                
                Package versioning (SemVer):
                • Major: Breaking changes (2.0.0)
                • Minor: New features, backward compatible (1.1.0)
                • Patch: Bug fixes (1.0.1)
                • Prerelease: Alpha/beta/rc (1.0.0-beta.1)
                • Build metadata: Additional info (1.0.0+20240101)
                """);
            
            // 2. Deployment packages
            Console.WriteLine("\n2. Deployment Packages:");
            Console.WriteLine("""
                ZIP packages:
                public class ZipPackager
                {
                    public void CreateDeploymentPackage(string sourceDir, string outputPath)
                    {
                        using (var zip = System.IO.Compression.ZipFile.Open(outputPath, 
                            System.IO.Compression.ZipArchiveMode.Create))
                        {
                            foreach (var file in Directory.GetFiles(sourceDir, "*", 
                                SearchOption.AllDirectories))
                            {
                                var relativePath = Path.GetRelativePath(sourceDir, file);
                                zip.CreateEntryFromFile(file, relativePath);
                            }
                        }
                    }
                    
                    public void ExtractDeploymentPackage(string zipPath, string extractDir)
                    {
                        System.IO.Compression.ZipFile.ExtractToDirectory(zipPath, extractDir, 
                            overwriteFiles: true);
                    }
                }
                
                WebDeploy (MSDeploy):
                // Create publish profile
                <Project>
                  <PropertyGroup>
                    <PublishProtocol>FileSystem</PublishProtocol>
                    <PublishUrl>bin\Release\net8.0\publish</PublishUrl>
                    <DeleteExistingFiles>true</DeleteExistingFiles>
                  </PropertyGroup>
                </Project>
                
                // Command line
                msbuild MyProject.csproj /p:DeployOnBuild=true /p:PublishProfile=FolderProfile
                
                // WebDeploy to IIS
                msbuild MyProject.csproj /p:DeployOnBuild=true /p:PublishProfile=AzureProfile
                
                ClickOnce deployment:
                // In csproj
                <PropertyGroup>
                  <TargetFramework>net8.0-windows</TargetFramework>
                  <OutputType>WinExe</OutputType>
                  <UseWPF>true</UseWPF>
                  <IsWebBootstrapper>false</IsWebBootstrapper>
                  <BootstrapperEnabled>true</BootstrapperEnabled>
                  <GenerateManifests>true</GenerateManifests>
                  <SignManifests>true</SignManifests>
                  <ManifestCertificateThumbprint>...</ManifestCertificateThumbprint>
                  <ManifestKeyFile>MyKey.pfx</ManifestKeyFile>
                  <ApplicationRevision>1</ApplicationRevision>
                  <ApplicationVersion>1.0.0.%2a</ApplicationVersion>
                  <Install>true</Install>
                  <InstallFrom>Web</InstallFrom>
                  <UpdateEnabled>true</UpdateEnabled>
                  <UpdateMode>Foreground</UpdateMode>
                  <UpdateInterval>7</UpdateInterval>
                  <UpdateIntervalUnits>Days</UpdateIntervalUnits>
                  <UpdatePeriodically>true</UpdatePeriodically>
                  <UpdateRequired>false</UpdateRequired>
                  <MapFileExtensions>true</MapFileExtensions>
                  <InstallUrl>http://mycompany.com/myapp/</InstallUrl>
                  <SupportUrl>http://mycompany.com/support/</SupportUrl>
                  <ProductName>My Application</ProductName>
                  <PublisherName>My Company</PublisherName>
                </PropertyGroup>
                """);
            
            // 3. Docker images
            Console.WriteLine("\n3. Docker Images:");
            Console.WriteLine("""
                Dockerfile for .NET applications:
                # Build stage
                FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
                WORKDIR /src
                
                # Copy csproj and restore
                COPY ["MyApp/MyApp.csproj", "MyApp/"]
                RUN dotnet restore "MyApp/MyApp.csproj"
                
                # Copy everything else and build
                COPY . .
                WORKDIR "/src/MyApp"
                RUN dotnet build "MyApp.csproj" -c Release -o /app/build
                
                # Publish
                RUN dotnet publish "MyApp.csproj" -c Release -o /app/publish \
                    --no-restore \
                    -p:PublishReadyToRun=true \
                    -p:PublishTrimmed=true \
                    -p:PublishSingleFile=true
                
                # Runtime stage  
                FROM mcr.microsoft.com/dotnet/runtime:8.0 AS runtime
                WORKDIR /app
                
                # Install runtime dependencies
                RUN apt-get update && apt-get install -y \
                    curl \
                    && rm -rf /var/lib/apt/lists/*
                
                # Copy published app
                COPY --from=build /app/publish .
                
                # Create non-root user
                RUN groupadd -r appgroup && useradd -r -g appgroup appuser
                USER appuser
                
                # Configure entrypoint
                ENTRYPOINT ["./MyApp"]
                
                # Health check
                HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
                    CMD curl -f http://localhost:8080/health || exit 1
                
                Multi-stage builds:
                # First stage: Build
                FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
                # ... build steps
                
                # Second stage: Test
                FROM build AS test
                RUN dotnet test --no-build
                
                # Third stage: Publish
                FROM build AS publish
                RUN dotnet publish -c Release -o /app/publish
                
                # Final stage: Runtime
                FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
                COPY --from=publish /app/publish .
                ENTRYPOINT ["dotnet", "MyApp.dll"]
                
                Building and tagging:
                # Build image
                docker build -t myapp:1.0.0 -t myapp:latest .
                
                # Tag for registry
                docker tag myapp:1.0.0 myregistry.azurecr.io/myapp:1.0.0
                
                # Push to registry
                docker push myregistry.azurecr.io/myapp:1.0.0
                
                # Run container
                docker run -d -p 8080:80 --name myapp myapp:1.0.0
                """);
        }
        
        static void DemonstrateDeploymentTargets()
        {
            Console.WriteLine("\n=== 4. Deployment Targets ===\n");
            
            // 1. IIS deployment
            Console.WriteLine("1. IIS Deployment:");
            Console.WriteLine("""
                IIS requirements:
                • .NET Runtime/Hosting Bundle installed
                • Application pool with correct .NET CLR version
                • Appropriate permissions (IIS_IUSRS, IUSR)
                • Windows Authentication (if needed)
                
                Web.config for IIS:
                <?xml version="1.0" encoding="utf-8"?>
                <configuration>
                  <location path="." inheritInChildApplications="false">
                    <system.webServer>
                      <handlers>
                        <add name="aspNetCore" 
                             path="*" 
                             verb="*" 
                             modules="AspNetCoreModuleV2" 
                             resourceType="Unspecified" />
                      </handlers>
                      <aspNetCore processPath="dotnet" 
                                  arguments=".\MyApp.dll" 
                                  stdoutLogEnabled="true"
                                  stdoutLogFile=".\logs\stdout"
                                  hostingModel="inprocess">
                        <environmentVariables>
                          <environmentVariable name="ASPNETCORE_ENVIRONMENT" value="Production" />
                          <environmentVariable name="DOTNET_PRINT_TELEMETRY_MESSAGE" value="false" />
                        </environmentVariables>
                      </aspNetCore>
                      <security>
                        <requestFiltering>
                          <requestLimits maxAllowedContentLength="52428800" />
                        </requestFiltering>
                      </security>
                    </system.webServer>
                  </location>
                  
                  <system.web>
                    <httpRuntime targetFramework="4.7.2" 
                                maxRequestLength="51200" 
                                executionTimeout="300" />
                  </system.web>
                  
                  <runtime>
                    <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
                      <dependentAssembly>
                        <assemblyIdentity name="System.Runtime.CompilerServices.Unsafe" 
                                          publicKeyToken="b03f5f7f11d50a3a" 
                                          culture="neutral" />
                        <bindingRedirect oldVersion="0.0.0.0-6.0.0.0" newVersion="6.0.0.0" />
                      </dependentAssembly>
                    </assemblyBinding>
                  </runtime>
                </configuration>
                
                IIS deployment methods:
                • WebDeploy (MSDeploy): Automated deployment from Visual Studio/CLI
                • File copy: Manual copy to IIS directory
                • PowerShell DSC: Desired State Configuration
                • Ansible/Chef/Puppet: Configuration management tools
                
                Application pool configuration:
                // PowerShell
                Import-Module WebAdministration
                
                # Create application pool
                New-WebAppPool -Name "MyAppPool" -Force
                Set-ItemProperty "IIS:\AppPools\MyAppPool" -Name managedRuntimeVersion -Value ""
                Set-ItemProperty "IIS:\AppPools\MyAppPool" -Name managedPipelineMode -Value "Integrated"
                Set-ItemProperty "IIS:\AppPools\MyAppPool" -Name startMode -Value "AlwaysRunning"
                Set-ItemProperty "IIS:\AppPools\MyAppPool" -Name recycling.periodicRestart.time -Value "00:00:00"
                Set-ItemProperty "IIS:\AppPools\MyAppPool" -Name processModel.idleTimeout -Value "00:00:00"
                
                # Create website
                New-Website -Name "MyApp" -Port 80 -IPAddress "*" -HostHeader "" -PhysicalPath "C:\inetpub\MyApp" -ApplicationPool "MyAppPool" -Force
                """);
            
            // 2. Linux deployment
            Console.WriteLine("\n2. Linux Deployment:");
            Console.WriteLine("""
                Kestrel as reverse proxy:
                // Program.cs
                var builder = WebApplication.CreateBuilder(args);
                
                builder.WebHost.ConfigureKestrel(serverOptions =>
                {
                    serverOptions.Listen(IPAddress.Any, 5000); // Kestrel
                    serverOptions.Listen(IPAddress.Any, 5001, listenOptions =>
                    {
                        listenOptions.UseHttps("certificate.pfx", "password");
                    });
                });
                
                // Configure for behind proxy
                builder.Services.Configure<ForwardedHeadersOptions>(options =>
                {
                    options.ForwardedHeaders = ForwardedHeaders.XForwardedFor | 
                                              ForwardedHeaders.XForwardedProto;
                    options.KnownNetworks.Clear();
                    options.KnownProxies.Clear();
                });
                
                var app = builder.Build();
                app.UseForwardedHeaders();
                
                Nginx configuration:
                # /etc/nginx/sites-available/myapp
                server {
                    listen 80;
                    server_name myapp.example.com;
                    
                    location / {
                        proxy_pass http://localhost:5000;
                        proxy_http_version 1.1;
                        proxy_set_header Upgrade $http_upgrade;
                        proxy_set_header Connection keep-alive;
                        proxy_set_header Host $host;
                        proxy_set_header X-Real-IP $remote_addr;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto $scheme;
                        proxy_cache_bypass $http_upgrade;
                        
                        # Timeouts
                        proxy_connect_timeout 60s;
                        proxy_send_timeout 60s;
                        proxy_read_timeout 60s;
                    }
                    
                    # Static files
                    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
                        expires 1y;
                        add_header Cache-Control "public, immutable";
                        proxy_pass http://localhost:5000;
                    }
                    
                    # Health check
                    location /health {
                        proxy_pass http://localhost:5000/health;
                        access_log off;
                    }
                }
                
                Systemd service:
                # /etc/systemd/system/myapp.service
                [Unit]
                Description=My .NET Application
                After=network.target
                
                [Service]
                Type=notify
                WorkingDirectory=/var/www/myapp
                ExecStart=/usr/bin/dotnet /var/www/myapp/MyApp.dll
                Restart=always
                RestartSec=10
                KillSignal=SIGINT
                Environment=ASPNETCORE_ENVIRONMENT=Production
                Environment=DOTNET_PRINT_TELEMETRY_MESSAGE=false
                Environment=ASPNETCORE_URLS=http://localhost:5000
                SyslogIdentifier=myapp
                User=www-data
                Group=www-data
                
                # Security
                NoNewPrivileges=true
                PrivateTmp=true
                ProtectSystem=full
                ProtectHome=true
                ReadWritePaths=/var/log/myapp
                
                [Install]
                WantedBy=multi-user.target
                
                # Commands
                sudo systemctl daemon-reload
                sudo systemctl enable myapp
                sudo systemctl start myapp
                sudo systemctl status myapp
                sudo journalctl -fu myapp
                
                Deployment script:
                #!/bin/bash
                APP_NAME="myapp"
                APP_PATH="/var/www/$APP_NAME"
                SERVICE_NAME="$APP_NAME.service"
                
                # Stop service
                sudo systemctl stop $SERVICE_NAME
                
                # Backup current version
                TIMESTAMP=$(date +%Y%m%d_%H%M%S)
                sudo cp -r $APP_PATH $APP_PATH.backup_$TIMESTAMP
                
                # Deploy new version
                sudo rm -rf $APP_PATH/*
                sudo cp -r ./publish/* $APP_PATH/
                sudo chown -R www-data:www-data $APP_PATH
                sudo chmod -R 755 $APP_PATH
                
                # Update environment file
                echo "ASPNETCORE_ENVIRONMENT=Production" | sudo tee $APP_PATH/.env
                
                # Start service
                sudo systemctl start $SERVICE_NAME
                sudo systemctl status $SERVICE_NAME
                """);
            
            // 3. Windows Service deployment
            Console.WriteLine("\n3. Windows Service Deployment:");
            Console.WriteLine("""
                BackgroundService as Windows Service:
                // Install-Package Microsoft.Extensions.Hosting.WindowsServices
                
                var builder = Host.CreateApplicationBuilder(args);
                builder.Services.AddWindowsService(options =>
                {
                    options.ServiceName = "My .NET Application";
                });
                
                builder.Services.AddHostedService<Worker>();
                
                var host = builder.Build();
                host.Run();
                
                // Worker.cs
                public class Worker : BackgroundService
                {
                    private readonly ILogger<Worker> _logger;
                    
                    public Worker(ILogger<Worker> logger)
                    {
                        _logger = logger;
                    }
                    
                    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
                    {
                        while (!stoppingToken.IsCancellationRequested)
                        {
                            _logger.LogInformation("Worker running at: {time}", DateTimeOffset.Now);
                            await Task.Delay(1000, stoppingToken);
                        }
                    }
                }
                
                SC commands for service management:
                # Create service
                sc create "MyService" binPath="C:\MyApp\MyApp.exe" start=auto
                
                # Configure service
                sc description "MyService" "My .NET Application Service"
                sc config "MyService" start=delayed-auto
                sc failure "MyService" reset=86400 actions=restart/5000/restart/30000/restart/60000
                
                # Service commands
                sc start "MyService"
                sc stop "MyService"
                sc query "MyService"
                sc delete "MyService"
                
                PowerShell deployment:
                # Deploy-WindowsService.ps1
                param(
                    [string]$ServiceName = "MyService",
                    [string]$ServiceDisplayName = "My .NET Application",
                    [string]$ServiceDescription = "Runs my .NET application as a Windows service",
                    [string]$InstallPath = "C:\Applications\MyApp",
                    [string]$ExecutablePath = "MyApp.exe"
                )
                
                # Stop and remove existing service
                if (Get-Service $ServiceName -ErrorAction SilentlyContinue) {
                    Stop-Service $ServiceName -Force
                    sc.exe delete $ServiceName
                    Start-Sleep -Seconds 2
                }
                
                # Create installation directory
                if (!(Test-Path $InstallPath)) {
                    New-Item -ItemType Directory -Path $InstallPath -Force
                }
                
                # Copy files (assumes files are in current directory)
                Copy-Item -Path ".\*" -Destination $InstallPath -Recurse -Force
                
                # Create service
                $binPath = "`"$InstallPath\$ExecutablePath`""
                New-Service -Name $ServiceName `
                            -DisplayName $ServiceDisplayName `
                            -Description $ServiceDescription `
                            -BinaryPathName $binPath `
                            -StartupType Automatic `
                            -ErrorAction Stop
                
                # Configure service recovery
                sc.exe failure $ServiceName reset=86400 actions=restart/5000/restart/30000/restart/60000
                
                # Set service description
                Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\$ServiceName" `
                                 -Name Description -Value $ServiceDescription
                
                # Start service
                Start-Service $ServiceName
                Get-Service $ServiceName
                """);
        }
        
        static void DemonstrateCICD()
        {
            Console.WriteLine("\n=== 5. CI/CD ===\n");
            
            // 1. GitHub Actions
            Console.WriteLine("1. GitHub Actions:");
            Console.WriteLine("""
                GitHub Actions workflow for .NET:
                # .github/workflows/dotnet.yml
                name: .NET
                
                on:
                  push:
                    branches: [ main, develop ]
                  pull_request:
                    branches: [ main ]
                
                jobs:
                  build:
                    runs-on: ubuntu-latest
                    
                    steps:
                    - uses: actions/checkout@v4
                    
                    - name: Setup .NET
                      uses: actions/setup-dotnet@v4
                      with:
                        dotnet-version: '8.0.x'
                    
                    - name: Restore dependencies
                      run: dotnet restore
                    
                    - name: Build
                      run: dotnet build --configuration Release --no-restore
                    
                    - name: Test
                      run: dotnet test --configuration Release --no-build --verbosity normal
                    
                    - name: Publish
                      run: dotnet publish --configuration Release -o ./publish
                    
                    - name: Upload artifacts
                      uses: actions/upload-artifact@v4
                      with:
                        name: myapp
                        path: ./publish
                
                  deploy:
                    needs: build
                    runs-on: ubuntu-latest
                    if: github.ref == 'refs/heads/main'
                    
                    steps:
                    - uses: actions/download-artifact@v4
                      with:
                        name: myapp
                        
                    - name: Deploy to Azure Web App
                      uses: azure/webapps-deploy@v3
                      with:
                        app-name: 'myapp'
                        slot-name: 'production'
                        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
                        package: .
                
                Workflow with matrix strategy:
                jobs:
                  build-and-test:
                    runs-on: ${{ matrix.os }}
                    strategy:
                      matrix:
                        os: [ubuntu-latest, windows-latest, macos-latest]
                        dotnet-version: ['6.0.x', '7.0.x', '8.0.x']
                    
                    steps:
                    - uses: actions/checkout@v4
                    
                    - name: Setup .NET ${{ matrix.dotnet-version }}
                      uses: actions/setup-dotnet@v4
                      with:
                        dotnet-version: ${{ matrix.dotnet-version }}
                    
                    - name: Build and Test
                      run: |
                        dotnet restore
                        dotnet build --configuration Release
                        dotnet test --configuration Release --no-build
                
                Secrets management:
                # In repository settings -> Secrets and variables -> Actions
                # Add secrets: AZURE_CREDENTIALS, DEPLOY_KEY, etc.
                
                # Use in workflow
                - name: Login to Azure
                  uses: azure/login@v1
                  with:
                    creds: ${{ secrets.AZURE_CREDENTIALS }}
                """);
            
            // 2. Azure DevOps
            Console.WriteLine("\n2. Azure DevOps:");
            Console.WriteLine("""
                Azure Pipeline YAML:
                # azure-pipelines.yml
                trigger:
                  branches:
                    include:
                    - main
                    - develop
                  paths:
                    exclude:
                    - README.md
                    - 'docs/*'
                
                pool:
                  vmImage: 'ubuntu-latest'
                
                variables:
                  buildConfiguration: 'Release'
                  solution: '**/*.sln'
                  
                stages:
                - stage: Build
                  jobs:
                  - job: Build
                    steps:
                    - task: UseDotNet@2
                      inputs:
                        packageType: 'sdk'
                        version: '8.0.x'
                    
                    - task: DotNetCoreCLI@2
                      displayName: 'Restore'
                      inputs:
                        command: 'restore'
                        projects: '$(solution)'
                    
                    - task: DotNetCoreCLI@2
                      displayName: 'Build'
                      inputs:
                        command: 'build'
                        projects: '$(solution)'
                        arguments: '--configuration $(buildConfiguration) --no-restore'
                    
                    - task: DotNetCoreCLI@2
                      displayName: 'Test'
                      inputs:
                        command: 'test'
                        projects: '**/*Tests.csproj'
                        arguments: '--configuration $(buildConfiguration) --no-build'
                    
                    - task: DotNetCoreCLI@2
                      displayName: 'Publish'
                      inputs:
                        command: 'publish'
                        projects: '**/*.csproj'
                        publishWebProjects: false
                        arguments: '--configuration $(buildConfiguration) --output $(Build.ArtifactStagingDirectory)'
                        zipAfterPublish: true
                    
                    - task: PublishBuildArtifacts@1
                      inputs:
                        PathtoPublish: '$(Build.ArtifactStagingDirectory)'
                        ArtifactName: 'drop'
                
                - stage: Deploy
                  dependsOn: Build
                  condition: succeeded()
                  jobs:
                  - deployment: DeployToAzure
                    environment: 'production'
                    strategy:
                      runOnce:
                        deploy:
                          steps:
                          - download: current
                            artifact: drop
                          
                          - task: AzureWebApp@1
                            inputs:
                              azureSubscription: 'Azure Connection'
                              appName: 'myapp'
                              package: '$(Pipeline.Workspace)/drop/*.zip'
                
                Release pipeline:
                • Multi-stage deployments (Dev -> Test -> Staging -> Production)
                • Approval gates between stages
                • Deployment strategies (blue-green, canary)
                • Rollback capabilities
                • Environment-specific configurations
                
                Pipeline variables and variable groups:
                # Variable groups (linked to Azure Key Vault)
                # Pipeline variables (secrets, non-secrets)
                # Library secure files
                """);
            
            // 3. Jenkins
            Console.WriteLine("\n3. Jenkins:");
            Console.WriteLine("""
                Jenkinsfile for .NET:
                pipeline {
                    agent any
                    
                    environment {
                        DOTNET_VERSION = '8.0'
                        BUILD_CONFIGURATION = 'Release'
                    }
                    
                    stages {
                        stage('Checkout') {
                            steps {
                                checkout scm
                            }
                        }
                        
                        stage('Setup') {
                            steps {
                                bat """
                                    choco install dotnet-${env.DOTNET_VERSION}-sdk -y
                                    dotnet --version
                                """
                            }
                        }
                        
                        stage('Restore') {
                            steps {
                                bat 'dotnet restore'
                            }
                        }
                        
                        stage('Build') {
                            steps {
                                bat "dotnet build --configuration ${env.BUILD_CONFIGURATION} --no-restore"
                            }
                        }
                        
                        stage('Test') {
                            steps {
                                bat "dotnet test --configuration ${env.BUILD_CONFIGURATION} --no-build --logger trx"
                                junit '**/*.trx'
                            }
                        }
                        
                        stage('Publish') {
                            steps {
                                bat "dotnet publish --configuration ${env.BUILD_CONFIGURATION} -o ./publish"
                                archiveArtifacts artifacts: 'publish/**', fingerprint: true
                            }
                        }
                        
                        stage('Deploy') {
                            when {
                                branch 'main'
                            }
                            steps {
                                withCredentials([azureServicePrincipal(credentialsId: 'azure-credentials', 
                                                          subscriptionIdVariable: 'SUBSCRIPTION_ID', 
                                                          clientIdVariable: 'CLIENT_ID', 
                                                          clientSecretVariable: 'CLIENT_SECRET', 
                                                          tenantIdVariable: 'TENANT_ID')]) {
                                    bat """
                                        az login --service-principal -u %CLIENT_ID% -p %CLIENT_SECRET% --tenant %TENANT_ID%
                                        az webapp deployment source config-zip --resource-group my-rg --name myapp --src ./publish.zip
                                    """
                                }
                            }
                        }
                    }
                    
                    post {
                        always {
                            cleanWs()
                        }
                        success {
                            emailext (
                                subject: "Build Successful: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                                body: "The build ${env.BUILD_URL} completed successfully.",
                                to: 'team@example.com'
                            )
                        }
                        failure {
                            emailext (
                                subject: "Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                                body: "The build ${env.BUILD_URL} failed. Please check the logs.",
                                to: 'team@example.com'
                            )
                        }
                    }
                }
                
                Jenkins pipeline libraries:
                // Shared libraries for reusable code
                // Custom steps, utilities, configurations
                // Version controlled separately
                
                Jenkins configuration as code (JCasC):
                # Manage Jenkins configuration via YAML files
                # Version control for Jenkins configuration
                # Reproducible Jenkins setups
                """);
        }
        
        static void DemonstrateContainerization()
        {
            Console.WriteLine("\n=== 6. Containerization ===\n");
            
            // 1. Docker Compose
            Console.WriteLine("1. Docker Compose:");
            Console.WriteLine("""
                docker-compose.yml for .NET applications:
                version: '3.8'
                
                services:
                  webapp:
                    build:
                      context: .
                      dockerfile: Dockerfile
                      args:
                        - BUILD_CONFIGURATION=Release
                    ports:
                      - "8080:80"
                      - "8081:443"
                    environment:
                      - ASPNETCORE_ENVIRONMENT=Production
                      - ConnectionStrings__DefaultConnection=Host=db;Database=myapp;Username=postgres;Password=password
                    depends_on:
                      - db
                      - redis
                    networks:
                      - app-network
                    volumes:
                      - app-data:/app/data
                    restart: unless-stopped
                    healthcheck:
                      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
                      interval: 30s
                      timeout: 10s
                      retries: 3
                      start_period: 40s
                
                  db:
                    image: postgres:15-alpine
                    environment:
                      - POSTGRES_DB=myapp
                      - POSTGRES_USER=postgres
                      - POSTGRES_PASSWORD=password
                    volumes:
                      - postgres-data:/var/lib/postgresql/data
                    networks:
                      - app-network
                    restart: unless-stopped
                    healthcheck:
                      test: ["CMD-SHELL", "pg_isready -U postgres"]
                      interval: 10s
                      timeout: 5s
                      retries: 5
                
                  redis:
                    image: redis:7-alpine
                    command: redis-server --appendonly yes
                    volumes:
                      - redis-data:/data
                    networks:
                      - app-network
                    restart: unless-stopped
                
                  nginx:
                    image: nginx:alpine
                    ports:
                      - "80:80"
                      - "443:443"
                    volumes:
                      - ./nginx.conf:/etc/nginx/nginx.conf:ro
                      - ./ssl:/etc/ssl:ro
                    depends_on:
                      - webapp
                    networks:
                      - app-network
                    restart: unless-stopped
                
                networks:
                  app-network:
                    driver: bridge
                
                volumes:
                  app-data:
                  postgres-data:
                  redis-data:
                
                Compose commands:
                # Build and start
                docker-compose up -d --build
                
                # View logs
                docker-compose logs -f webapp
                
                # Scale services
                docker-compose up -d --scale webapp=3
                
                # Stop services
                docker-compose down
                
                # Stop and remove volumes
                docker-compose down -v
                
                # Run commands in container
                docker-compose exec webapp dotnet ef database update
                """);
            
            // 2. Kubernetes
            Console.WriteLine("\n2. Kubernetes:");
            Console.WriteLine("""
                Kubernetes manifests for .NET:
                # deployment.yaml
                apiVersion: apps/v1
                kind: Deployment
                metadata:
                  name: myapp-deployment
                  labels:
                    app: myapp
                spec:
                  replicas: 3
                  selector:
                    matchLabels:
                      app: myapp
                  strategy:
                    type: RollingUpdate
                    rollingUpdate:
                      maxSurge: 1
                      maxUnavailable: 0
                  template:
                    metadata:
                      labels:
                        app: myapp
                    spec:
                      containers:
                      - name: myapp
                        image: myregistry.azurecr.io/myapp:1.0.0
                        ports:
                        - containerPort: 80
                        env:
                        - name: ASPNETCORE_ENVIRONMENT
                          value: "Production"
                        - name: ConnectionStrings__DefaultConnection
                          valueFrom:
                            secretKeyRef:
                              name: myapp-secrets
                              key: connection-string
                        resources:
                          requests:
                            memory: "256Mi"
                            cpu: "250m"
                          limits:
                            memory: "512Mi"
                            cpu: "500m"
                        livenessProbe:
                          httpGet:
                            path: /health
                            port: 80
                          initialDelaySeconds: 30
                          periodSeconds: 10
                          timeoutSeconds: 5
                          failureThreshold: 3
                        readinessProbe:
                          httpGet:
                            path: /health/ready
                            port: 80
                          initialDelaySeconds: 5
                          periodSeconds: 10
                          timeoutSeconds: 5
                          failureThreshold: 3
                        volumeMounts:
                        - name: app-data
                          mountPath: /app/data
                      volumes:
                      - name: app-data
                        persistentVolumeClaim:
                          claimName: myapp-pvc
                      imagePullSecrets:
                      - name: regcred
                
                # service.yaml
                apiVersion: v1
                kind: Service
                metadata:
                  name: myapp-service
                spec:
                  selector:
                    app: myapp
                  ports:
                  - port: 80
                    targetPort: 80
                  type: LoadBalancer
                
                # ingress.yaml
                apiVersion: networking.k8s.io/v1
                kind: Ingress
                metadata:
                  name: myapp-ingress
                  annotations:
                    nginx.ingress.kubernetes.io/rewrite-target: /
                    nginx.ingress.kubernetes.io/ssl-redirect: "true"
                    cert-manager.io/cluster-issuer: "letsencrypt-prod"
                spec:
                  ingressClassName: nginx
                  tls:
                  - hosts:
                    - myapp.example.com
                    secretName: myapp-tls
                  rules:
                  - host: myapp.example.com
                    http:
                      paths:
                      - path: /
                        pathType: Prefix
                        backend:
                          service:
                            name: myapp-service
                            port:
                              number: 80
                
                # horizontalpodautoscaler.yaml
                apiVersion: autoscaling/v2
                kind: HorizontalPodAutoscaler
                metadata:
                  name: myapp-hpa
                spec:
                  scaleTargetRef:
                    apiVersion: apps/v1
                    kind: Deployment
                    name: myapp-deployment
                  minReplicas: 2
                  maxReplicas: 10
                  metrics:
                  - type: Resource
                    resource:
                      name: cpu
                      target:
                        type: Utilization
                        averageUtilization: 70
                  - type: Resource
                    resource:
                      name: memory
                      target:
                        type: Utilization
                        averageUtilization: 80
                
                Helm charts:
                # Chart.yaml
                apiVersion: v2
                name: myapp
                description: A .NET application
                version: 1.0.0
                appVersion: "1.0.0"
                
                # values.yaml
                replicaCount: 3
                image:
                  repository: myregistry.azurecr.io/myapp
                  tag: 1.0.0
                  pullPolicy: IfNotPresent
                service:
                  type: LoadBalancer
                  port: 80
                ingress:
                  enabled: true
                  host: myapp.example.com
                resources:
                  requests:
                    memory: "256Mi"
                    cpu: "250m"
                  limits:
                    memory: "512Mi"
                    cpu: "500m"
                
                # templates/deployment.yaml
                apiVersion: apps/v1
                kind: Deployment
                metadata:
                  name: {{ .Chart.Name }}
                spec:
                  replicas: {{ .Values.replicaCount }}
                  # ... template continues
                """);
            
            // 3. Container orchestration platforms
            Console.WriteLine("\n3. Container Orchestration Platforms:");
            Console.WriteLine("""
                Azure Kubernetes Service (AKS):
                # Create AKS cluster
                az group create --name myResourceGroup --location eastus
                az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-managed-identity
                
                # Deploy to AKS
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                
                # Update deployment
                kubectl set image deployment/myapp-deployment myapp=myregistry.azurecr.io/myapp:2.0.0
                kubectl rollout status deployment/myapp-deployment
                
                # Rollback
                kubectl rollout undo deployment/myapp-deployment
                
                Amazon EKS:
                # Create EKS cluster
                eksctl create cluster --name my-cluster --region us-east-1 --nodegroup-name standard-workers --node-type t3.medium --nodes 3
                
                # Deploy to EKS
                kubectl apply -f deployment.yaml
                
                # Configure load balancer
                # EKS automatically creates Elastic Load Balancer for LoadBalancer services
                
                Google GKE:
                # Create GKE cluster
                gcloud container clusters create my-cluster --num-nodes=3 --zone=us-central1-a
                
                # Deploy to GKE
                kubectl apply -f deployment.yaml
                
                Container registry integration:
                • Azure Container Registry (ACR)
                • Amazon Elastic Container Registry (ECR)
                • Google Container Registry (GCR)
                • Docker Hub
                
                CI/CD with containers:
                # Build and push
                docker build -t myregistry.azurecr.io/myapp:$GITHUB_SHA .
                docker push myregistry.azurecr.io/myapp:$GITHUB_SHA
                
                # Update deployment
                kubectl set image deployment/myapp-deployment myapp=myregistry.azurecr.io/myapp:$GITHUB_SHA
                kubectl rollout status deployment/myapp-deployment
                """);
        }
        
        static void DemonstrateCloudDeployment()
        {
            Console.WriteLine("\n=== 7. Cloud Deployment ===\n");
            
            // 1. Azure App Service
            Console.WriteLine("1. Azure App Service:");
            Console.WriteLine("""
                Azure App Service deployment:
                # Create App Service
                az group create --name myResourceGroup --location eastus
                az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
                az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myapp --runtime "DOTNETCORE:8.0"
                
                # Configure App Service
                az webapp config set --resource-group myResourceGroup --name myapp --always-on true
                az webapp config appsettings set --resource-group myResourceGroup --name myapp --settings ASPNETCORE_ENVIRONMENT=Production
                
                # Deploy from local
                az webapp deployment source config-local-git --resource-group myResourceGroup --name myapp
                git remote add azure https://myapp.scm.azurewebsites.net:443/myapp.git
                git push azure main
                
                # Deploy from ZIP
                dotnet publish -c Release -o ./publish
                cd ./publish
                zip -r ../site.zip *
                az webapp deployment source config-zip --resource-group myResourceGroup --name myapp --src ../site.zip
                
                # Configure staging slots
                az webapp deployment slot create --resource-group myResourceGroup --name myapp --slot staging
                az webapp config appsettings set --resource-group myResourceGroup --name myapp --slot staging --settings ASPNETCORE_ENVIRONMENT=Staging
                az webapp deployment slot swap --resource-group myResourceGroup --name myapp --slot staging
                
                App Service configuration:
                // appsettings.json for App Service
                {
                  "Logging": {
                    "LogLevel": {
                      "Default": "Information",
                      "Microsoft.AspNetCore": "Warning"
                    },
                    "ApplicationInsights": {
                      "LogLevel": {
                        "Default": "Information"
                      }
                    }
                  },
                  "ApplicationInsights": {
                    "ConnectionString": "InstrumentationKey=..."
                  },
                  "AllowedHosts": "*",
                  "WEBSITE_TIME_ZONE": "Eastern Standard Time",
                  "WEBSITE_LOAD_CERTIFICATES": "*"
                }
                
                // Configure in Startup.cs
                public void ConfigureServices(IServiceCollection services)
                {
                    // Azure App Service logging
                    services.AddApplicationInsightsTelemetry();
                    
                    // Azure App Service authentication
                    services.AddAuthentication(AzureADDefaults.AuthenticationScheme)
                        .AddAzureAD(options => Configuration.Bind("AzureAd", options));
                    
                    // Health checks for App Service
                    services.AddHealthChecks()
                        .AddCheck<SampleHealthCheck>("sample")
                        .AddAzureServiceBusQueue(...)
                        .AddAzureKeyVault(...);
                }
                
                App Service scaling:
                # Scale up (change pricing tier)
                az appservice plan update --name myAppServicePlan --resource-group myResourceGroup --sku P1V2
                
                # Scale out (add instances)
                az monitor autoscale create --resource-group myResourceGroup --resource myAppServicePlan --resource-type Microsoft.Web/serverfarms --name autoscale --min-count 1 --max-count 10 --count 2
                az monitor autoscale rule create --resource-group myResourceGroup --autoscale-name autoscale --condition "CpuPercentage > 70 avg 5m" --scale out 1
                az monitor autoscale rule create --resource-group myResourceGroup --autoscale-name autoscale --condition "CpuPercentage < 30 avg 5m" --scale in 1
                """);
            
            // 2. AWS Elastic Beanstalk
            Console.WriteLine("\n2. AWS Elastic Beanstalk:");
            Console.WriteLine("""
                Elastic Beanstalk deployment:
                # Create Elastic Beanstalk application
                aws elasticbeanstalk create-application --application-name myapp
                
                # Create environment
                aws elasticbeanstalk create-environment --application-name myapp \
                  --environment-name myapp-prod \
                  --solution-stack-name "64bit Amazon Linux 2023 v4.0.1 running .NET 8" \
                  --option-settings file://options.json
                
                # Deploy application
                dotnet publish -c Release -o ./publish
                cd ./publish
                zip -r ../myapp.zip *
                aws elasticbeanstalk create-application-version --application-name myapp \
                  --version-label v1.0.0 \
                  --source-bundle S3Bucket=my-bucket,S3Key=myapp.zip
                aws elasticbeanstalk update-environment --environment-name myapp-prod \
                  --version-label v1.0.0
                
                // options.json
                [
                  {
                    "Namespace": "aws:elasticbeanstalk:application:environment",
                    "OptionName": "ASPNETCORE_ENVIRONMENT",
                    "Value": "Production"
                  },
                  {
                    "Namespace": "aws:elasticbeanstalk:application:environment",
                    "OptionName": "DOTNET_PRINT_TELEMETRY_MESSAGE",
                    "Value": "false"
                  },
                  {
                    "Namespace": "aws:elasticbeanstalk:cloudwatch:logs",
                    "OptionName": "StreamLogs",
                    "Value": "true"
                  },
                  {
                    "Namespace": "aws:elasticbeanstalk:cloudwatch:logs",
                    "OptionName": "RetentionInDays",
                    "Value": "7"
                  }
                ]
                
                Elastic Beanstalk configuration files:
                # .ebextensions/01-nginx.config
                files:
                  "/etc/nginx/conf.d/proxy.conf":
                    mode: "000644"
                    owner: root
                    group: root
                    content: |
                      client_max_body_size 50M;
                
                  "/opt/elasticbeanstalk/hooks/appdeploy/pre/01_setup_env.sh":
                    mode: "000755"
                    owner: root
                    group: root
                    content: |
                      #!/bin/bash
                      set -xe
                      EB_APP_USER=$(/opt/elasticbeanstalk/bin/get-config container -k app_user)
                      EB_SUPPORT_DIR=$(/opt/elasticbeanstalk/bin/get-config container -k support_dir)
                      EB_APP_DEPLOY_DIR=$(/opt/elasticbeanstalk/bin/get-config container -k app_deploy_dir)
                      EB_APP_STAGING_DIR=$(/opt/elasticbeanstalk/bin/get-config container -k app_staging_dir)
                
                # .ebextensions/02-dotnet.config
                container_commands:
                  01-install-dotnet:
                    command: "sudo yum install -y dotnet-8"
                    ignoreErrors: false
                
                  02-migrate-database:
                    command: "dotnet ef database update"
                    leader_only: true
                
                Elastic Beanstalk CLI (EB CLI):
                # Initialize EB CLI
                eb init -p .NET Core -r us-east-1
                
                # Create environment
                eb create myapp-env --single -i t3a.small
                
                # Deploy
                eb deploy
                
                # View logs
                eb logs
                
                # SSH into instance
                eb ssh
                
                # Terminate environment
                eb terminate
                """);
            
            // 3. Google Cloud Run
            Console.WriteLine("\n3. Google Cloud Run:");
            Console.WriteLine("""
                Cloud Run deployment:
                # Build and push container
                gcloud auth configure-docker
                docker build -t gcr.io/my-project/myapp:latest .
                docker push gcr.io/my-project/myapp:latest
                
                # Deploy to Cloud Run
                gcloud run deploy myapp \
                  --image gcr.io/my-project/myapp:latest \
                  --platform managed \
                  --region us-central1 \
                  --allow-unauthenticated \
                  --memory 512Mi \
                  --cpu 1 \
                  --max-instances 10 \
                  --timeout 300s \
                  --concurrency 80 \
                  --set-env-vars ASPNETCORE_ENVIRONMENT=Production
                
                # Update service
                gcloud run deploy myapp --image gcr.io/my-project/myapp:new-version
                
                # Traffic splitting (canary)
                gcloud run services update-traffic myapp \
                  --to-tags v1=90,v2=10
                
                Cloud Run configuration:
                // appsettings.json for Cloud Run
                {
                  "Logging": {
                    "LogLevel": {
                      "Default": "Information",
                      "Microsoft": "Warning",
                      "Microsoft.Hosting.Lifetime": "Information"
                    },
                    "GoogleCloud": {
                      "ProjectId": "my-project",
                      "ServiceName": "myapp",
                      "Version": "1.0.0"
                    }
                  },
                  "CloudRun": {
                    "Service": {
                      "Name": "myapp",
                      "Region": "us-central1"
                    }
                  }
                }
                
                // Program.cs for Cloud Run
                var builder = WebApplication.CreateBuilder(args);
                
                // Google Cloud Logging
                builder.Logging.AddGoogle(new GoogleLoggerOptions
                {
                    ProjectId = builder.Configuration["GoogleCloud:ProjectId"],
                    ServiceName = builder.Configuration["GoogleCloud:ServiceName"],
                    Version = builder.Configuration["GoogleCloud:Version"]
                });
                
                // Health checks for Cloud Run
                builder.Services.AddHealthChecks()
                    .AddCheck("self", () => HealthCheckResult.Healthy());
                
                var app = builder.Build();
                
                // Health check endpoint
                app.MapHealthChecks("/health");
                
                // Readiness check
                app.MapGet("/health/ready", () => "Ready");
                
                app.Run();
                
                Cloud Run with Cloud SQL:
                # Create Cloud SQL instance
                gcloud sql instances create myapp-db \
                  --database-version POSTGRES_15 \
                  --tier db-f1-micro \
                  --region us-central1
                
                # Create database
                gcloud sql databases create myapp \
                  --instance myapp-db
                
                # Configure Cloud Run to use Cloud SQL
                gcloud run deploy myapp \
                  --image gcr.io/my-project/myapp:latest \
                  --add-cloudsql-instances my-project:us-central1:myapp-db \
                  --set-env-vars ConnectionStrings__DefaultConnection="Server=/cloudsql/my-project:us-central1:myapp-db;Database=myapp;Uid=postgres;Pwd=[PASSWORD]"
                
                Cloud Run CI/CD:
                # cloudbuild.yaml
                steps:
                # Build container
                - name: 'gcr.io/cloud-builders/docker'
                  args: ['build', '-t', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA', '.']
                
                # Push container
                - name: 'gcr.io/cloud-builders/docker'
                  args: ['push', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA']
                
                # Deploy to Cloud Run
                - name: 'gcr.io/cloud-builders/gcloud'
                  args: ['run', 'deploy', 'myapp',
                         '--image', 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA',
                         '--region', 'us-central1',
                         '--platform', 'managed',
                         '--allow-unauthenticated']
                
                images:
                - 'gcr.io/$PROJECT_ID/myapp:$COMMIT_SHA'
                """);
        }
        
        static void DemonstrateConfigurationManagement()
        {
            Console.WriteLine("\n=== 8. Configuration Management ===\n");
            
            // 1. Configuration sources
            Console.WriteLine("1. Configuration Sources:");
            Console.WriteLine("""
                Hierarchical configuration in .NET:
                var builder = WebApplication.CreateBuilder(args);
                
                // Add configuration sources (order matters - later sources override earlier)
                builder.Configuration
                    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                    .AddJsonFile($"appsettings.{builder.Environment.EnvironmentName}.json", optional: true)
                    .AddEnvironmentVariables()
                    .AddCommandLine(args)
                    .AddUserSecrets<Program>(optional: true)
                    .AddAzureKeyVault("https://myvault.vault.azure.net/")
                    .AddAzureAppConfiguration("ConnectionString");
                
                // Access configuration
                var apiSettings = builder.Configuration.GetSection("ApiSettings");
                var apiUrl = apiSettings["BaseUrl"];
                var timeout = apiSettings.GetValue<int>("Timeout", 30);
                
                // Bind to class
                var options = new ApiOptions();
                builder.Configuration.GetSection("ApiSettings").Bind(options);
                
                // Or use IOptions pattern
                builder.Services.Configure<ApiOptions>(
                    builder.Configuration.GetSection("ApiSettings"));
                
                Environment-specific configuration:
                // appsettings.Development.json
                {
                  "Logging": {
                    "LogLevel": {
                      "Default": "Debug",
                      "Microsoft": "Warning"
                    }
                  },
                  "ApiSettings": {
                    "BaseUrl": "https://dev-api.example.com",
                    "Timeout": 60
                  }
                }
                
                // appsettings.Production.json  
                {
                  "Logging": {
                    "LogLevel": {
                      "Default": "Warning",
                      "Microsoft": "Error"
                    }
                  },
                  "ApiSettings": {
                    "BaseUrl": "https://api.example.com",
                    "Timeout": 30
                  }
                }
                
                Configuration providers:
                • JSON files (appsettings.json)
                • Environment variables (prefixed with DOTNET_ or ASPNETCORE_)
                • Command-line arguments
                • User secrets (development only)
                • Azure Key Vault
                • Azure App Configuration
                • HashiCorp Vault
                • Database
                • Etcd/Consul
                """);
            
            // 2. Secrets management
            Console.WriteLine("\n2. Secrets Management:");
            Console.WriteLine("""
                User secrets (development):
                # Initialize user secrets
                dotnet user-secrets init
                
                # Set secret
                dotnet user-secrets set "ConnectionStrings:DefaultConnection" "Server=localhost;Database=MyDb;Trusted_Connection=True;"
                dotnet user-secrets set "ApiKey" "my-secret-api-key"
                
                # List secrets
                dotnet user-secrets list
                
                # Remove secret
                dotnet user-secrets remove "ApiKey"
                
                # Clear all secrets
                dotnet user-secrets clear
                
                // Access in code
                var connectionString = builder.Configuration["ConnectionStrings:DefaultConnection"];
                var apiKey = builder.Configuration["ApiKey"];
                
                Azure Key Vault:
                // Install-Package Azure.Identity
                // Install-Package Azure.Extensions.AspNetCore.Configuration.Secrets
                
                var builder = WebApplication.CreateBuilder(args);
                
                // Using Managed Identity
                var keyVaultEndpoint = new Uri("https://myvault.vault.azure.net/");
                builder.Configuration.AddAzureKeyVault(keyVaultEndpoint, new DefaultAzureCredential());
                
                // Using service principal
                var credential = new ClientSecretCredential(
                    tenantId: "tenant-id",
                    clientId: "client-id", 
                    clientSecret: "client-secret");
                builder.Configuration.AddAzureKeyVault(keyVaultEndpoint, credential);
                
                // Access secrets
                var secretValue = builder.Configuration["MySecret"];
                
                Key rotation:
                public class KeyVaultSecretManager : IKeyVaultSecretManager
                {
                    public bool Load(SecretProperties secret)
                    {
                        // Only load secrets with specific prefix
                        return secret.Name.StartsWith("MyApp-");
                    }
                    
                    public string GetKey(KeyVaultSecret secret)
                    {
                        // Remove prefix and replace -- with : for hierarchical config
                        return secret.Name["MyApp-".Length..].Replace("--", ":");
                    }
                }
                
                // Use custom secret manager
                builder.Configuration.AddAzureKeyVault(
                    keyVaultEndpoint,
                    new DefaultAzureCredential(),
                    new KeyVaultSecretManager());
                
                Environment variables in production:
                # Linux/macOS
                export ConnectionStrings__DefaultConnection="Server=localhost;Database=MyDb"
                export ApiSettings__BaseUrl="https://api.example.com"
                
                # Windows
                set ConnectionStrings__DefaultConnection=Server=localhost;Database=MyDb
                set ApiSettings__BaseUrl=https://api.example.com
                
                # Docker
                docker run -e ConnectionStrings__DefaultConnection="Server=db;Database=MyDb" myapp
                
                # Kubernetes
                env:
                - name: ConnectionStrings__DefaultConnection
                  valueFrom:
                    secretKeyRef:
                      name: myapp-secrets
                      key: connection-string
                """);
            
            // 3. Feature flags
            Console.WriteLine("\n3. Feature Flags:");
            Console.WriteLine("""
                Microsoft.FeatureManagement:
                // Install-Package Microsoft.FeatureManagement.AspNetCore
                
                // appsettings.json
                {
                  "FeatureManagement": {
                    "NewCheckout": true,
                    "AdvancedSearch": false,
                    "BetaFeatures": {
                      "EnabledFor": [
                        {
                          "Name": "Percentage",
                          "Parameters": {
                            "Value": 30
                          }
                        }
                      ]
                    }
                  }
                }
                
                // Program.cs
                var builder = WebApplication.CreateBuilder(args);
                builder.Services.AddFeatureManagement();
                
                var app = builder.Build();
                
                // Use in controllers
                public class HomeController : Controller
                {
                    private readonly IFeatureManager _featureManager;
                    
                    public HomeController(IFeatureManager featureManager)
                    {
                        _featureManager = featureManager;
                    }
                    
                    public async Task<IActionResult> Index()
                    {
                        if (await _featureManager.IsEnabledAsync("NewCheckout"))
                        {
                            return View("NewCheckout");
                        }
                        
                        return View("OldCheckout");
                    }
                }
                
                // Use in views
                @inject Microsoft.FeatureManagement.IFeatureManager FeatureManager
                @if (await FeatureManager.IsEnabledAsync("NewCheckout"))
                {
                    <partial name="_NewCheckout" />
                }
                else
                {
                    <partial name="_OldCheckout" />
                }
                
                Feature filters:
                // Percentage filter
                [FilterAlias("Percentage")]
                public class PercentageFilter : IFeatureFilter
                {
                    public Task<bool> EvaluateAsync(FeatureFilterEvaluationContext context)
                    {
                        var settings = context.Parameters.Get<PercentageFilterSettings>();
                        var random = new Random().Next(0, 100);
                        return Task.FromResult(random < settings.Value);
                    }
                }
                
                public class PercentageFilterSettings
                {
                    public int Value { get; set; }
                }
                
                // Time window filter
                [FilterAlias("TimeWindow")]
                public class TimeWindowFilter : IFeatureFilter
                {
                    public Task<bool> EvaluateAsync(FeatureFilterEvaluationContext context)
                    {
                        var settings = context.Parameters.Get<TimeWindowFilterSettings>();
                        var now = DateTimeOffset.Now;
                        return Task.FromResult(now >= settings.Start && now <= settings.End);
                    }
                }
                
                Dynamic feature flags:
                // Azure App Configuration
                builder.Configuration.AddAzureAppConfiguration(options =>
                {
                    options.Connect("ConnectionString")
                           .UseFeatureFlags();
                });
                
                builder.Services.AddAzureAppConfiguration()
                               .AddFeatureManagement();
                
                // Refresh configuration
                app.UseAzureAppConfiguration();
                
                // Feature flag UI
                // Install-Package Microsoft.FeatureManagement.AspNetCore
                app.MapControllers();
                app.UseAzureAppConfiguration();
                """);
        }
        
        static void DemonstrateMonitoringAndObservability()
        {
            Console.WriteLine("\n=== 9. Monitoring and Observability ===\n");
            
            // 1. Application Insights
            Console.WriteLine("1. Application Insights:");
            Console.WriteLine("""
                Application Insights setup:
                // Install-Package Microsoft.ApplicationInsights.AspNetCore
                
                var builder = WebApplication.CreateBuilder(args);
                
                // Add Application Insights
                builder.Services.AddApplicationInsightsTelemetry(options =>
                {
                    options.ConnectionString = builder.Configuration["APPLICATIONINSIGHTS_CONNECTION_STRING"];
                    options.EnableAdaptiveSampling = false;
                    options.EnablePerformanceCounterCollectionModule = true;
                    options.EnableAzureInstanceMetadataTelemetryModule = true;
                });
                
                // Add logging to Application Insights
                builder.Logging.AddApplicationInsights();
                
                var app = builder.Build();
                
                // Custom telemetry
                public class OrderController : Controller
                {
                    private readonly TelemetryClient _telemetryClient;
                    
                    public OrderController(TelemetryClient telemetryClient)
                    {
                        _telemetryClient = telemetryClient;
                    }
                    
                    public async Task<IActionResult> Create(Order order)
                    {
                        // Track custom event
                        _telemetryClient.TrackEvent("OrderCreated", new Dictionary<string, string>
                        {
                            ["OrderId"] = order.Id.ToString(),
                            ["CustomerId"] = order.CustomerId.ToString(),
                            ["Total"] = order.Total.ToString("C")
                        });
                        
                        // Track metric
                        _telemetryClient.GetMetric("OrdersProcessed").TrackValue(1);
                        
                        // Track dependency
                        using (_telemetryClient.StartOperation<DependencyTelemetry>("ProcessPayment"))
                        {
                            await _paymentService.ProcessAsync(order);
                        }
                        
                        // Track exception
                        try
                        {
                            // Operation that might fail
                        }
                        catch (Exception ex)
                        {
                            _telemetryClient.TrackException(ex, new Dictionary<string, string>
                            {
                                ["Operation"] = "ProcessOrder",
                                ["OrderId"] = order.Id.ToString()
                            });
                            throw;
                        }
                        
                        return Ok();
                    }
                }
                
                Application Insights configuration:
                // appsettings.json
                {
                  "ApplicationInsights": {
                    "ConnectionString": "InstrumentationKey=...",
                    "EnableAdaptiveSampling": false,
                    "EnablePerformanceCounterCollectionModule": true,
                    "EnableAzureInstanceMetadataTelemetryModule": true,
                    "RequestCollectionOptions": {
                      "TrackExceptions": true
                    }
                  },
                  "Logging": {
                    "LogLevel": {
                      "Default": "Information",
                      "Microsoft": "Warning"
                    },
                    "ApplicationInsights": {
                      "LogLevel": {
                        "Default": "Information",
                        "Microsoft": "Error"
                      }
                    }
                  }
                }
                
                Distributed tracing:
                // Install-Package Microsoft.ApplicationInsights.DependencyCollector
                
                builder.Services.AddApplicationInsightsTelemetryWorkerService();
                builder.Services.AddApplicationInsightsKubernetesEnricher();
                
                // Propagate correlation IDs
                app.Use(async (context, next) =>
                {
                    var requestId = context.Request.Headers["Request-Id"];
                    if (!string.IsNullOrEmpty(requestId))
                    {
                        Activity.Current?.SetParentId(requestId);
                    }
                    
                    await next();
                });
                """);
            
            // 2. Health checks
            Console.WriteLine("\n2. Health Checks:");
            Console.WriteLine("""
                Health checks in ASP.NET Core:
                var builder = WebApplication.CreateBuilder(args);
                
                // Add health checks
                builder.Services.AddHealthChecks()
                    .AddCheck<SampleHealthCheck>("sample_health_check")
                    .AddCheck<DatabaseHealthCheck>("database", tags: new[] { "database", "sql" })
                    .AddCheck<ExternalApiHealthCheck>("external_api", tags: new[] { "api", "external" })
                    .AddRedis("localhost:6379", tags: new[] { "redis", "cache" })
                    .AddSqlServer(builder.Configuration.GetConnectionString("DefaultConnection"))
                    .AddAzureServiceBusQueue("ConnectionString", "queue-name")
                    .AddAzureKeyVault(new Uri("https://myvault.vault.azure.net/"), new DefaultAzureCredential())
                    .AddApplicationInsightsPublisher();
                
                var app = builder.Build();
                
                // Map health check endpoints
                app.MapHealthChecks("/health");
                app.MapHealthChecks("/health/ready", new HealthCheckOptions
                {
                    Predicate = check => check.Tags.Contains("ready")
                });
                app.MapHealthChecks("/health/live", new HealthCheckOptions
                {
                    Predicate = _ => false // No checks for liveness
                });
                
                // Custom health check
                public class DatabaseHealthCheck : IHealthCheck
                {
                    private readonly string _connectionString;
                    
                    public DatabaseHealthCheck(IConfiguration configuration)
                    {
                        _connectionString = configuration.GetConnectionString("DefaultConnection");
                    }
                    
                    public async Task<HealthCheckResult> CheckHealthAsync(
                        HealthCheckContext context, 
                        CancellationToken cancellationToken = default)
                    {
                        try
                        {
                            using var connection = new SqlConnection(_connectionString);
                            await connection.OpenAsync(cancellationToken);
                            
                            using var command = connection.CreateCommand();
                            command.CommandText = "SELECT 1";
                            var result = await command.ExecuteScalarAsync(cancellationToken);
                            
                            if (result?.ToString() == "1")
                            {
                                return HealthCheckResult.Healthy("Database is working");
                            }
                            
                            return HealthCheckResult.Unhealthy("Database query failed");
                        }
                        catch (Exception ex)
                        {
                            return HealthCheckResult.Unhealthy("Database connection failed", ex);
                        }
                    }
                }
                
                Health check UI:
                // Install-Package AspNetCore.HealthChecks.UI
                // Install-Package AspNetCore.HealthChecks.UI.InMemory.Storage
                
                builder.Services.AddHealthChecksUI(options =>
                {
                    options.SetEvaluationTimeInSeconds(60); // Time in seconds between check
                    options.MaximumHistoryEntriesPerEndpoint(50); // Maximum history entries
                    options.SetApiMaxActiveRequests(1); // Maximum concurrent requests
                    
                    options.AddHealthCheckEndpoint("API", "/health");
                    options.AddHealthCheckEndpoint("Database", "/health/ready");
                })
                .AddInMemoryStorage();
                
                app.MapHealthChecksUI(options =>
                {
                    options.UIPath = "/health-ui";
                    options.ApiPath = "/health-ui-api";
                    options.WebhookPath = "/health-ui-webhook";
                });
                
                // Navigate to /health-ui to see dashboard
                
                Kubernetes health checks:
                # deployment.yaml
                livenessProbe:
                  httpGet:
                    path: /health/live
                    port: 80
                  initialDelaySeconds: 30
                  periodSeconds: 10
                  timeoutSeconds: 5
                  failureThreshold: 3
                
                readinessProbe:
                  httpGet:
                    path: /health/ready
                    port: 80
                  initialDelaySeconds: 5
                  periodSeconds: 10
                  timeoutSeconds: 5
                  failureThreshold: 3
                
                startupProbe:
                  httpGet:
                    path: /health/startup
                    port: 80
                  initialDelaySeconds: 0
                  periodSeconds: 10
                  timeoutSeconds: 5
                  failureThreshold: 30
                """);
            
            // 3. Logging and diagnostics
            Console.WriteLine("\n3. Logging and Diagnostics:");
            Console.WriteLine("""
                Structured logging with Serilog:
                // Install-Package Serilog.AspNetCore
                // Install-Package Serilog.Sinks.File
                // Install-Package Serilog.Sinks.Console
                // Install-Package Serilog.Sinks.Seq
                
                var builder = WebApplication.CreateBuilder(args);
                
                // Configure Serilog
                Log.Logger = new LoggerConfiguration()
                    .ReadFrom.Configuration(builder.Configuration)
                    .Enrich.FromLogContext()
                    .Enrich.WithProperty("Application", "MyApp")
                    .Enrich.WithProperty("Environment", builder.Environment.EnvironmentName)
                    .WriteTo.Console(outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}")
                    .WriteTo.File("logs/myapp-.log", 
                        rollingInterval: RollingInterval.Day,
                        outputTemplate: "{Timestamp:yyyy-MM-dd HH:mm:ss.fff zzz} [{Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}")
                    .WriteTo.Seq("http://localhost:5341")
                    .CreateLogger();
                
                builder.Host.UseSerilog();
                
                // Use in code
                public class OrderService
                {
                    private readonly ILogger<OrderService> _logger;
                    
                    public OrderService(ILogger<OrderService> logger)
                    {
                        _logger = logger;
                    }
                    
                    public async Task ProcessOrderAsync(Order order)
                    {
                        // Structured logging
                        _logger.LogInformation("Processing order {OrderId} for customer {CustomerId}", 
                            order.Id, order.CustomerId);
                        
                        try
                        {
                            // Process order
                            _logger.LogDebug("Order details: {@Order}", order);
                        }
                        catch (Exception ex)
                        {
                            _logger.LogError(ex, "Failed to process order {OrderId}", order.Id);
                            throw;
                        }
                        
                        _logger.LogInformation("Order {OrderId} processed successfully", order.Id);
                    }
                }
                
                Diagnostic tools:
                // DotNetCounters
                dotnet-counters monitor --process-id 1234
                dotnet-counters monitor --process-id 1234 System.Runtime
                
                // DotNetTrace
                dotnet-trace collect --process-id 1234
                dotnet-trace collect --process-id 1234 --profile cpu-sampling
                
                // DotNetDump
                dotnet-dump collect --process-id 1234
                dotnet-dump analyze core_20240101.dmp
                
                // PerfView
                // Windows performance analysis tool
                
                Custom diagnostics middleware:
                public class DiagnosticsMiddleware
                {
                    private readonly RequestDelegate _next;
                    private readonly ILogger<DiagnosticsMiddleware> _logger;
                    
                    public DiagnosticsMiddleware(RequestDelegate next, ILogger<DiagnosticsMiddleware> logger)
                    {
                        _next = next;
                        _logger = logger;
                    }
                    
                    public async Task InvokeAsync(HttpContext context)
                    {
                        var stopwatch = Stopwatch.StartNew();
                        
                        try
                        {
                            await _next(context);
                            stopwatch.Stop();
                            
                            _logger.LogInformation(
                                "Request {Method} {Path} completed with {StatusCode} in {ElapsedMilliseconds}ms",
                                context.Request.Method,
                                context.Request.Path,
                                context.Response.StatusCode,
                                stopwatch.ElapsedMilliseconds);
                        }
                        catch (Exception ex)
                        {
                            stopwatch.Stop();
                            
                            _logger.LogError(ex,
                                "Request {Method} {Path} failed with error in {ElapsedMilliseconds}ms",
                                context.Request.Method,
                                context.Request.Path,
                                stopwatch.ElapsedMilliseconds);
                            
                            throw;
                        }
                    }
                }
                
                // Register middleware
                app.UseMiddleware<DiagnosticsMiddleware>();
                """);
        }
        
        static void DemonstrateRealWorldDeploymentStrategies()
        {
            Console.WriteLine("\n=== 10. Real-World Deployment Strategies ===\n");
            
            // 1. Blue-green deployment
            Console.WriteLine("1. Blue-Green Deployment:");
            Console.WriteLine("""
                Blue-green deployment concept:
                • Two identical production environments: Blue (current) and Green (new)
                • Route traffic from Blue to Green after testing
                • Instant rollback by routing back to Blue
                • Zero downtime during deployment
                
                Implementation with load balancer:
                # Initial state: 100% traffic to Blue
                az network traffic-manager endpoint update \
                  --name blue-endpoint \
                  --profile-name myapp-profile \
                  --resource-group my-rg \
                  --weight 100
                
                az network traffic-manager endpoint update \
                  --name green-endpoint \
                  --profile-name myapp-profile \
                  --resource-group my-rg \
                  --weight 0
                
                # Deploy new version to Green
                az webapp deployment source config-zip \
                  --resource-group my-rg \
                  --name myapp-green \
                  --src ./publish.zip
                
                # Test Green environment
                curl https://green.myapp.example.com/health
                
                # Switch traffic (gradual or all at once)
                az network traffic-manager endpoint update \
                  --name blue-endpoint \
                  --profile-name myapp-profile \
                  --resource-group my-rg \
                  --weight 0
                
                az network traffic-manager endpoint update \
                  --name green-endpoint \
                  --profile-name myapp-profile \
                  --resource-group my-rg \
                  --weight 100
                
                # Rollback if needed
                az network traffic-manager endpoint update \
                  --name blue-endpoint \
                  --profile-name myapp-profile \
                  --resource-group my-rg \
                  --weight 100
                
                az network traffic-manager endpoint update \
                  --name green-endpoint \
                  --profile-name myapp-profile \
                  --resource-group my-rg \
                  --weight 0
                
                Blue-green with Kubernetes:
                # Blue deployment
                kubectl apply -f deployment-blue.yaml
                
                # Green deployment
                kubectl apply -f deployment-green.yaml
                
                # Switch service selector
                kubectl patch service myapp-service -p '{"spec":{"selector":{"version":"green"}}}'
                
                # Or use Istio for traffic shifting
                apiVersion: networking.istio.io/v1beta1
                kind: VirtualService
                metadata:
                  name: myapp
                spec:
                  hosts:
                  - myapp.example.com
                  http:
                  - route:
                    - destination:
                        host: myapp
                        subset: blue
                      weight: 0
                    - destination:
                        host: myapp
                        subset: green
                      weight: 100
                """);
            
            // 2. Canary deployment
            Console.WriteLine("\n2. Canary Deployment:");
            Console.WriteLine("""
                Canary deployment concept:
                • Deploy new version to small subset of users
                • Monitor metrics and errors
                • Gradually increase traffic to new version
                • Roll back if issues detected
                
                Implementation with feature flags:
                // Use feature flags to control canary rollout
                public class CanaryFeatureFilter : IFeatureFilter
                {
                    private readonly IHttpContextAccessor _httpContextAccessor;
                    
                    public CanaryFeatureFilter(IHttpContextAccessor httpContextAccessor)
                    {
                        _httpContextAccessor = httpContextAccessor;
                    }
                    
                    public Task<bool> EvaluateAsync(FeatureFilterEvaluationContext context)
                    {
                        var settings = context.Parameters.Get<CanarySettings>();
                        var httpContext = _httpContextAccessor.HttpContext;
                        
                        // Check user ID
                        var userId = httpContext.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
                        if (!string.IsNullOrEmpty(userId))
                        {
                            // Deterministic hash based on user ID
                            var hash = Math.Abs(userId.GetHashCode()) % 100;
                            return Task.FromResult(hash < settings.Percentage);
                        }
                        
                        // Check IP address
                        var ipAddress = httpContext.Connection.RemoteIpAddress?.ToString();
                        if (!string.IsNullOrEmpty(ipAddress))
                        {
                            var hash = Math.Abs(ipAddress.GetHashCode()) % 100;
                            return Task.FromResult(hash < settings.Percentage);
                        }
                        
                        return Task.FromResult(false);
                    }
                }
                
                Canary with Kubernetes and Istio:
                apiVersion: networking.istio.io/v1beta1
                kind: VirtualService
                metadata:
                  name: myapp
                spec:
                  hosts:
                  - myapp.example.com
                  http:
                  - route:
                    - destination:
                        host: myapp
                        subset: stable
                      weight: 90
                    - destination:
                        host: myapp
                        subset: canary
                      weight: 10
                
                # Monitor canary
                kubectl get pods -l version=canary
                kubectl logs deployment/myapp-canary
                
                # Increase canary traffic
                kubectl patch virtualservice myapp -p '
                spec:
                  http:
                  - route:
                    - destination:
                        host: myapp
                        subset: stable
                      weight: 50
                    - destination:
                        host: myapp
                        subset: canary
                      weight: 50
                '
                
                Canary analysis and metrics:
                // Monitor key metrics
                • Error rate (should be similar or lower)
                • Response time (should be similar or faster)
                • Throughput (should be similar or higher)
                • Business metrics (conversion rate, revenue)
                
                // Automated canary analysis
                if (canaryErrorRate > stableErrorRate * 1.5)
                {
                    // Roll back canary
                    RollbackCanary();
                }
                
                if (canaryResponseTime > stableResponseTime * 2)
                {
                    // Roll back canary
                    RollbackCanary();
                }
                """);
            
            // 3. Disaster recovery
            Console.WriteLine("\n3. Disaster Recovery:");
            Console.WriteLine("""
                Disaster recovery planning:
                • RTO (Recovery Time Objective): Maximum acceptable downtime
                • RPO (Recovery Point Objective): Maximum data loss acceptable
                • Backup strategy: Frequency, retention, testing
                • Failover strategy: Automatic vs manual, DNS vs traffic manager
                
                Multi-region deployment:
                # Deploy to multiple regions
                az group create --name myapp-eastus --location eastus
                az group create --name myapp-westus --location westus
                
                # Create Traffic Manager profile
                az network traffic-manager profile create \
                  --name myapp-profile \
                  --resource-group my-rg \
                  --routing-method Performance \
                  --unique-dns-name myapp-global
                
                # Add endpoints
                az network traffic-manager endpoint create \
                  --name eastus \
                  --resource-group my-rg \
                  --profile-name myapp-profile \
                  --type azureEndpoints \
                  --target-resource-id /subscriptions/.../resourceGroups/myapp-eastus/... \
                  --endpoint-status Enabled
                
                az network traffic-manager endpoint create \
                  --name westus \
                  --resource-group my-rg \
                  --profile-name myapp-profile \
                  --type azureEndpoints \
                  --target-resource-id /subscriptions/.../resourceGroups/myapp-westus/... \
                  --endpoint-status Enabled
                
                Database disaster recovery:
                # Azure SQL Geo-Replication
                az sql db replica create \
                  --name MyDatabase \
                  --partner-server westus-server \
                  --resource-group my-rg \
                  --server eastus-server \
                  --partner-resource-group my-rg-westus
                
                # Failover to secondary
                az sql db replica set-primary \
                  --name MyDatabase \
                  --resource-group my-rg-westus \
                  --server westus-server
                
                # Cosmos DB multi-region
                az cosmosdb update \
                  --name my-cosmosdb \
                  --resource-group my-rg \
                  --locations regionName=eastus failoverPriority=0 isZoneRedundant=false \
                  --locations regionName=westus failoverPriority=1 isZoneRedundant=false \
                  --enable-multiple-write-locations true
                
                Backup and restore:
                # Database backup
                az sql db export \
                  --name MyDatabase \
                  --resource-group my-rg \
                  --server eastus-server \
                  --storage-uri https://mystorage.blob.core.windows.net/backups/MyDatabase.bacpac \
                  --admin-user $USER \
                  --admin-password $PASSWORD
                
                # Restore database
                az sql db import \
                  --name MyDatabase-Restored \
                  --resource-group my-rg \
                  --server eastus-server \
                  --storage-uri https://mystorage.blob.core.windows.net/backups/MyDatabase.bacpac \
                  --admin-user $USER \
                  --admin-password $PASSWORD
                
                Disaster recovery testing:
                // Regular DR drills
                // Simulate region failure
                // Test failover procedures
                // Measure RTO and RPO
                // Update documentation based on findings
                """);
            
            // 4. Zero-downtime deployment
            Console.WriteLine("\n4. Zero-Downtime Deployment:");
            Console.WriteLine("""
                Database migration strategies:
                // 1. Expand/contract pattern
                // Add new column, migrate data, update code, remove old column
                
                // 2. Parallel change
                // Write to both old and new structures
                // Read from new structure with fallback to old
                // Migrate old data to new structure
                // Remove old structure
                
                // 3. Feature flags for database changes
                if (await _featureManager.IsEnabledAsync("NewDatabaseSchema"))
                {
                    // Use new schema
                    await _newRepository.SaveAsync(entity);
                }
                else
                {
                    // Use old schema
                    await _oldRepository.SaveAsync(entity);
                }
                
                Application lifecycle management:
                // Graceful shutdown
                public class GracefulShutdownMiddleware
                {
                    private readonly RequestDelegate _next;
                    private readonly IHostApplicationLifetime _appLifetime;
                    private readonly ILogger<GracefulShutdownMiddleware> _logger;
                    
                    public GracefulShutdownMiddleware(
                        RequestDelegate next,
                        IHostApplicationLifetime appLifetime,
                        ILogger<GracefulShutdownMiddleware> logger)
                    {
                        _next = next;
                        _appLifetime = appLifetime;
                        _logger = logger;
                    }
                    
                    public async Task InvokeAsync(HttpContext context)
                    {
                        if (_appLifetime.ApplicationStopping.IsCancellationRequested)
                        {
                            context.Response.StatusCode = 503;
                            await context.Response.WriteAsync("Service is shutting down");
                            return;
                        }
                        
                        await _next(context);
                    }
                }
                
                // Register in Program.cs
                app.UseMiddleware<GracefulShutdownMiddleware>();
                
                // Configure shutdown timeout
                builder.Services.Configure<HostOptions>(options =>
                {
                    options.ShutdownTimeout = TimeSpan.FromSeconds(30);
                });
                
                Load balancer coordination:
                // Connection draining
                # Remove instance from load balancer
                az network lb address-pool address remove \
                  --resource-group my-rg \
                  --lb-name my-lb \
                  --pool-name backend-pool \
                  --name vm-instance
                
                # Wait for connections to drain
                Start-Sleep -Seconds 30
                
                # Deploy new version
                # Add instance back to load balancer
                az network lb address-pool address add \
                  --resource-group my-rg \
                  --lb-name my-lb \
                  --pool-name backend-pool \
                  --name vm-instance \
                  --vnet /subscriptions/.../resourceGroups/my-rg/... \
                  --ip-address 10.0.0.5
                
                Health checks for zero-downtime:
                // Readiness check for dependencies
                public class ReadinessHealthCheck : IHealthCheck
                {
                    private readonly IServiceProvider _serviceProvider;
                    
                    public async Task<HealthCheckResult> CheckHealthAsync(
                        HealthCheckContext context, 
                        CancellationToken cancellationToken)
                    {
                        // Check all dependencies
                        var tasks = new List<Task<bool>>
                        {
                            CheckDatabaseAsync(),
                            CheckCacheAsync(),
                            CheckExternalApiAsync()
                        };
                        
                        var results = await Task.WhenAll(tasks);
                        
                        if (results.All(r => r))
                        {
                            return HealthCheckResult.Healthy("All dependencies are ready");
                        }
                        
                        return HealthCheckResult.Unhealthy("Some dependencies are not ready");
                    }
                }
                
                Deployment automation:
                // Infrastructure as Code (IaC)
                // Automated testing
                // Automated rollback
                // Canary analysis
                // Feature flag management
                // Monitoring and alerting
                """);
        }
    }
    
    // Supporting classes for examples
    
    public class ApiOptions
    {
        public string BaseUrl { get; set; }
        public int Timeout { get; set; }
    }
    
    public class Order
    {
        public int Id { get; set; }
        public int CustomerId { get; set; }
        public decimal Total { get; set; }
    }
    
    public class SampleHealthCheck : IHealthCheck
    {
        public Task<HealthCheckResult> CheckHealthAsync(
            HealthCheckContext context, CancellationToken cancellationToken = default)
        {
            return Task.FromResult(HealthCheckResult.Healthy());
        }
    }
    
    public class DatabaseHealthCheck : IHealthCheck
    {
        public Task<HealthCheckResult> CheckHealthAsync(
            HealthCheckContext context, CancellationToken cancellationToken = default)
        {
            return Task.FromResult(HealthCheckResult.Healthy());
        }
    }
    
    public class ExternalApiHealthCheck : IHealthCheck
    {
        public Task<HealthCheckResult> CheckHealthAsync(
            HealthCheckContext context, CancellationToken cancellationToken = default)
        {
            return Task.FromResult(HealthCheckResult.Healthy());
        }
    }
    
    public class CanarySettings
    {
        public int Percentage { get; set; }
    }
    
    public class TimeWindowFilterSettings
    {
        public DateTimeOffset Start { get; set; }
        public DateTimeOffset End { get; set; }
    }
    
    public class OrderService
    {
        private readonly ILogger<OrderService> _logger;
        
        public OrderService(ILogger<OrderService> logger)
        {
            _logger = logger;
        }
        
        public Task ProcessOrderAsync(Order order)
        {
            return Task.CompletedTask;
        }
    }
    
    public class PaymentService
    {
        public Task ProcessAsync(Order order)
        {
            return Task.CompletedTask;
        }
    }
    
    // Mock services for examples
    public interface IDebugService { }
    public class DebugService : IDebugService { }
}