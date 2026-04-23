# ============================================
# RUBY GEMS - CREATION, DEVELOPMENT, AND PUBLISHING
# ============================================

puts "=" * 60
puts "RUBY GEMS - COMPREHENSIVE GUIDE"
puts "=" * 60

# ============================================
# 1. WHAT ARE GEMS?
# ============================================

puts "\n" + "=" * 40
puts "1. WHAT ARE GEMS?"
puts "=" * 40

puts <<~GEMS_INTRO

  RUBY GEMS:
  • Packages of Ruby code and resources
  • Distributed via RubyGems.org
  • Managed by the 'gem' command-line tool
  • Similar to npm (Node), pip (Python), cargo (Rust)
  
  STRUCTURE:
  my_gem/
    ├── lib/              # Ruby source code
    │   └── my_gem.rb     # Main entry point
    ├── bin/              # Executable scripts
    ├── test/             # Tests
    ├── spec/             # RSpec tests
    ├── README.md         # Documentation
    ├── LICENSE.txt       # License
    ├── CHANGELOG.md      # Version history
    ├── Gemfile           # Development dependencies
    └── my_gem.gemspec    # Gem specification

GEMS_INTRO

# ============================================
# 2. CREATING A NEW GEM
# ============================================

puts "\n" + "=" * 40
puts "2. CREATING A NEW GEM"
puts "=" * 40

puts <<~CREATE_GEM

  METHOD 1: Using Bundler (recommended)
  $ bundle gem my_awesome_gem
  
  Options:
  --test=rspec          # Use RSpec for testing
  --test=minitest       # Use Minitest (default)
  --ci=github           # Setup GitHub Actions
  --linter=rubocop      # Include RuboCop
  --mit                 # Use MIT license
  
  Example:
  $ bundle gem my_awesome_gem --test=rspec --ci=github --linter=rubocop --mit
  
  METHOD 2: Manual creation
  $ mkdir my_gem
  $ cd my_gem
  $ touch my_gem.gemspec
  $ mkdir lib

CREATE_GEM

# ============================================
# 3. GEMSPEC FILE
# ============================================

puts "\n" + "=" * 40
puts "3. GEMSPEC FILE STRUCTURE"
puts "=" * 40

# Example gemspec file
gemspec_example = <<~GEMSPEC
  # my_awesome_gem.gemspec
  
  Gem::Specification.new do |spec|
    spec.name          = "my_awesome_gem"
    spec.version       = "0.1.0"
    spec.authors       = ["Your Name"]
    spec.email         = ["your.email@example.com"]
    
    spec.summary       = "A brief summary of what your gem does"
    spec.description   = "A longer description explaining the gem's purpose"
    spec.homepage      = "https://github.com/username/my_awesome_gem"
    spec.license       = "MIT"
    
    # Minimum Ruby version required
    spec.required_ruby_version = ">= 2.7.0"
    
    # Metadata
    spec.metadata["homepage_uri"] = spec.homepage
    spec.metadata["source_code_uri"] = "https://github.com/username/my_awesome_gem"
    spec.metadata["changelog_uri"] = "https://github.com/username/my_awesome_gem/blob/main/CHANGELOG.md"
    
    # Files to include in the gem
    spec.files = Dir[
      "lib/**/*.rb",
      "bin/*",
      "README.md",
      "LICENSE.txt",
      "CHANGELOG.md"
    ]
    
    spec.bindir        = "bin"
    spec.executables   = spec.files.grep(%r{^bin/}) { |f| File.basename(f) }
    spec.require_paths = ["lib"]
    
    # Runtime dependencies (required for gem to work)
    spec.add_dependency "httparty", "~> 0.21"
    spec.add_dependency "json", ">= 2.0"
    
    # Development dependencies (only for development/testing)
    spec.add_development_dependency "rspec", "~> 3.0"
    spec.add_development_dependency "rubocop", "~> 1.0"
  end
GEMSPEC

puts gemspec_example

# ============================================
# 4. GEM STRUCTURE AND CODE ORGANIZATION
# ============================================

puts "\n" + "=" * 40
puts "4. GEM CODE ORGANIZATION"
puts "=" * 40

# lib/my_awesome_gem.rb - Main entry point
main_file_example = <<~MAIN_FILE
  # lib/my_awesome_gem.rb
  
  require_relative "my_awesome_gem/version"
  require_relative "my_awesome_gem/configuration"
  require_relative "my_awesome_gem/client"
  require_relative "my_awesome_gem/error"
  
  module MyAwesomeGem
    class Error < StandardError; end
    
    class << self
      attr_accessor :configuration
    end
    
    def self.configuration
      @configuration ||= Configuration.new
    end
    
    def self.configure
      yield(configuration)
    end
    
    def self.reset_configuration
      @configuration = Configuration.new
    end
  end
MAIN_FILE

puts main_file_example

# lib/my_awesome_gem/version.rb
version_file_example = <<~VERSION_FILE
  # lib/my_awesome_gem/version.rb
  
  module MyAwesomeGem
    VERSION = "0.1.0"
  end
VERSION_FILE

puts version_file_example

# lib/my_awesome_gem/configuration.rb
config_file_example = <<~CONFIG_FILE
  # lib/my_awesome_gem/configuration.rb
  
  module MyAwesomeGem
    class Configuration
      attr_accessor :api_key, :timeout, :base_url
      
      def initialize
        @api_key = nil
        @timeout = 30
        @base_url = "https://api.example.com"
      end
    end
  end
CONFIG_FILE

puts config_file_example

# lib/my_awesome_gem/client.rb
client_file_example = <<~CLIENT_FILE
  # lib/my_awesome_gem/client.rb
  
  require 'httparty'
  
  module MyAwesomeGem
    class Client
      include HTTParty
      
      def initialize(api_key: nil)
        @api_key = api_key || MyAwesomeGem.configuration.api_key
        @base_url = MyAwesomeGem.configuration.base_url
        @timeout = MyAwesomeGem.configuration.timeout
        
        raise Error, "API key required" unless @api_key
        
        self.class.base_uri @base_url
        self.class.default_timeout @timeout
      end
      
      def get_data(id)
        response = self.class.get(
          "/data/\#{id}",
          headers: { "Authorization" => "Bearer \#{@api_key}" }
        )
        
        handle_response(response)
      end
      
      private
      
      def handle_response(response)
        case response.code
        when 200
          response.parsed_response
        when 404
          raise Error, "Resource not found"
        else
          raise Error, "Request failed: \#{response.code}"
        end
      end
    end
  end
CLIENT_FILE

puts client_file_example

# ============================================
# 5. USING THE GEM
# ============================================

puts "\n" + "=" * 40
puts "5. USING THE GEM"
puts "=" * 40

usage_example = <<~USAGE
  # Configure the gem
  MyAwesomeGem.configure do |config|
    config.api_key = "your_api_key_here"
    config.timeout = 60
    config.base_url = "https://custom.api.com"
  end
  
  # Use the gem
  client = MyAwesomeGem::Client.new
  data = client.get_data(123)
  
  # Or pass configuration inline
  client = MyAwesomeGem::Client.new(api_key: "inline_key")
USAGE

puts usage_example

# ============================================
# 6. TESTING YOUR GEM
# ============================================

puts "\n" + "=" * 40
puts "6. TESTING YOUR GEM"
puts "=" * 40

# spec/spec_helper.rb
spec_helper_example = <<~SPEC_HELPER
  # spec/spec_helper.rb
  
  require "my_awesome_gem"
  require "webmock/rspec"
  
  RSpec.configure do |config|
    config.expect_with :rspec do |expectations|
      expectations.include_chain_clauses_in_custom_matcher_descriptions = true
    end
    
    config.mock_with :rspec do |mocks|
      mocks.verify_partial_doubles = true
    end
    
    config.shared_context_metadata_behavior = :apply_to_host_groups
    
    # Reset configuration before each test
    config.before(:each) do
      MyAwesomeGem.reset_configuration
    end
  end
SPEC_HELPER

puts spec_helper_example

# spec/my_awesome_gem_spec.rb
gem_spec_example = <<~GEM_SPEC
  # spec/my_awesome_gem_spec.rb
  
  RSpec.describe MyAwesomeGem do
    it "has a version number" do
      expect(MyAwesomeGem::VERSION).not_to be nil
    end
    
    describe ".configure" do
      it "allows configuration" do
        MyAwesomeGem.configure do |config|
          config.api_key = "test_key"
        end
        
        expect(MyAwesomeGem.configuration.api_key).to eq("test_key")
      end
    end
  end
GEM_SPEC

puts gem_spec_example

# spec/my_awesome_gem/client_spec.rb
client_spec_example = <<~CLIENT_SPEC
  # spec/my_awesome_gem/client_spec.rb
  
  RSpec.describe MyAwesomeGem::Client do
    before do
      MyAwesomeGem.configure do |config|
        config.api_key = "test_key"
        config.base_url = "https://api.example.com"
      end
    end
    
    describe "#get_data" do
      it "fetches data successfully" do
        stub_request(:get, "https://api.example.com/data/123")
          .with(headers: { "Authorization" => "Bearer test_key" })
          .to_return(status: 200, body: '{"id": 123, "name": "Test"}')
        
        client = MyAwesomeGem::Client.new
        data = client.get_data(123)
        
        expect(data["id"]).to eq(123)
        expect(data["name"]).to eq("Test")
      end
      
      it "raises error when resource not found" do
        stub_request(:get, "https://api.example.com/data/999")
          .to_return(status: 404)
        
        client = MyAwesomeGem::Client.new
        
        expect {
          client.get_data(999)
        }.to raise_error(MyAwesomeGem::Error, "Resource not found")
      end
    end
  end
CLIENT_SPEC

puts client_spec_example

# ============================================
# 7. BUILDING AND INSTALLING LOCALLY
# ============================================

puts "\n" + "=" * 40
puts "7. BUILDING AND TESTING LOCALLY"
puts "=" * 40

puts <<~LOCAL_TESTING

  BUILD THE GEM:
  $ gem build my_awesome_gem.gemspec
  # Creates: my_awesome_gem-0.1.0.gem
  
  INSTALL LOCALLY:
  $ gem install ./my_awesome_gem-0.1.0.gem
  
  TEST IN IRB:
  $ irb
  > require 'my_awesome_gem'
  > MyAwesomeGem.configure { |c| c.api_key = "test" }
  > client = MyAwesomeGem::Client.new
  
  UNINSTALL:
  $ gem uninstall my_awesome_gem

LOCAL_TESTING

# ============================================
# 8. PUBLISHING TO RUBYGEMS.ORG
# ============================================

puts "\n" + "=" * 40
puts "8. PUBLISHING TO RUBYGEMS.ORG"
puts "=" * 40

puts <<~PUBLISHING

  PREREQUISITES:
  1. Create account at rubygems.org
  2. Configure credentials:
     $ gem signin
  
  PUBLISH:
  $ gem build my_awesome_gem.gemspec
  $ gem push my_awesome_gem-0.1.0.gem
  
  YANKING (UNPUBLISH):
  $ gem yank my_awesome_gem -v 0.1.0
  
  BEST PRACTICES BEFORE PUBLISHING:
  ✓ Run all tests
  ✓ Update CHANGELOG.md
  ✓ Update version in version.rb
  ✓ Commit all changes
  ✓ Tag the release: git tag v0.1.0
  ✓ Push tags: git push --tags

PUBLISHING

# ============================================
# 9. VERSIONING AND RELEASES
# ============================================

puts "\n" + "=" * 40
puts "9. SEMANTIC VERSIONING"
puts "=" * 40

puts <<~VERSIONING

  SEMANTIC VERSIONING (SemVer):
  MAJOR.MINOR.PATCH (e.g., 2.3.1)
  
  MAJOR (2.x.x):
  • Breaking changes
  • Incompatible API changes
  • Remove deprecated features
  
  MINOR (x.3.x):
  • New features
  • Backward compatible
  • Deprecate features
  
  PATCH (x.x.1):
  • Bug fixes
  • Security patches
  • Backward compatible
  
  DEPENDENCY SPECIFIERS:
  gem 'my_gem', '~> 1.0'      # >= 1.0, < 2.0
  gem 'my_gem', '~> 1.2.3'    # >= 1.2.3, < 1.3.0
  gem 'my_gem', '>= 1.0'      # Any version >= 1.0
  gem 'my_gem', '1.2.3'       # Exact version
  
  VERSION RELEASE PROCESS:
  1. Update version.rb
  2. Update CHANGELOG.md
  3. Commit: git commit -am "Release v1.2.3"
  4. Tag: git tag v1.2.3
  5. Push: git push && git push --tags
  6. Build: gem build my_gem.gemspec
  7. Publish: gem push my_gem-1.2.3.gem

VERSIONING

# ============================================
# 10. EXECUTABLE GEMS (COMMAND-LINE TOOLS)
# ============================================

puts "\n" + "=" * 40
puts "10. CREATING CLI TOOLS"
puts "=" * 40

# bin/my_awesome_gem
cli_executable_example = <<~CLI_EXECUTABLE
  #!/usr/bin/env ruby
  
  require 'my_awesome_gem'
  require 'optparse'
  
  options = {}
  
  OptionParser.new do |opts|
    opts.banner = "Usage: my_awesome_gem [options]"
    
    opts.on("-k", "--api-key KEY", "API key") do |key|
      options[:api_key] = key
    end
    
    opts.on("-i", "--id ID", Integer, "Resource ID") do |id|
      options[:id] = id
    end
    
    opts.on("-h", "--help", "Show help") do
      puts opts
      exit
    end
    
    opts.on("-v", "--version", "Show version") do
      puts MyAwesomeGem::VERSION
      exit
    end
  end.parse!
  
  # Validate required options
  unless options[:api_key] && options[:id]
    puts "Error: --api-key and --id are required"
    exit 1
  end
  
  # Use the gem
  begin
    MyAwesomeGem.configure do |config|
      config.api_key = options[:api_key]
    end
    
    client = MyAwesomeGem::Client.new
    data = client.get_data(options[:id])
    
    puts "Data: \#{data}"
  rescue MyAwesomeGem::Error => e
    puts "Error: \#{e.message}"
    exit 1
  end
CLI_EXECUTABLE

puts cli_executable_example

puts <<~CLI_SETUP

  MAKE EXECUTABLE:
  $ chmod +x bin/my_awesome_gem
  
  TEST LOCALLY:
  $ ruby -Ilib bin/my_awesome_gem --help
  
  AFTER INSTALLING GEM:
  $ my_awesome_gem --api-key abc123 --id 42

CLI_SETUP

# ============================================
# 11. ADVANCED GEM FEATURES
# ============================================

puts "\n" + "=" * 40
puts "11. ADVANCED GEM FEATURES"
puts "=" * 40

# Extensions (C code)
extensions_example = <<~EXTENSIONS

  C EXTENSIONS:
  For performance-critical code, write C extensions
  
  In gemspec:
  spec.extensions = ["ext/my_gem/extconf.rb"]
  
  ext/my_gem/extconf.rb:
  require 'mkmf'
  create_makefile('my_gem/my_gem')
  
  ext/my_gem/my_gem.c:
  #include "ruby.h"
  
  VALUE method_fast_calculation(VALUE self, VALUE num) {
      int n = NUM2INT(num);
      return INT2NUM(n * 2);
  }
  
  void Init_my_gem() {
      VALUE MyGem = rb_define_module("MyGem");
      rb_define_module_function(MyGem, "fast_calculation", method_fast_calculation, 1);
  }

EXTENSIONS

puts extensions_example

# ============================================
# 12. BEST PRACTICES
# ============================================

puts "\n" + "=" * 40
puts "12. GEM DEVELOPMENT BEST PRACTICES"
puts "=" * 40

puts <<~BEST_PRACTICES

  CODE ORGANIZATION:
  ✓ One gem = one responsibility
  ✓ Use modules to namespace your code
  ✓ Keep public API small and stable
  ✓ Document all public methods
  
  DEPENDENCIES:
  ✓ Minimize runtime dependencies
  ✓ Specify version constraints
  ✓ Use pessimistic versioning (~>)
  ✓ Keep dependencies up to date
  
  TESTING:
  ✓ Achieve high test coverage (>90%)
  ✓ Test both success and failure cases
  ✓ Use CI/CD (GitHub Actions, Travis, etc.)
  ✓ Test against multiple Ruby versions
  
  DOCUMENTATION:
  ✓ Write clear README with examples
  ✓ Document all public APIs with YARD
  ✓ Include CHANGELOG.md
  ✓ Provide usage examples
  
  MAINTENANCE:
  ✓ Follow semantic versioning
  ✓ Respond to issues promptly
  ✓ Keep dependencies updated
  ✓ Deprecate before breaking changes
  
  SECURITY:
  ✓ Never commit secrets
  ✓ Validate user input
  ✓ Handle errors gracefully
  ✓ Regular security audits

BEST_PRACTICES

puts "\n=== Complete ==="

# ============================================
# SUMMARY: FULL GEM WORKFLOW
# ============================================

puts <<~WORKFLOW

  COMPLETE GEM DEVELOPMENT WORKFLOW:
  
  1. CREATE:
     $ bundle gem my_gem --test=rspec
  
  2. DEVELOP:
     • Write code in lib/
     • Write tests in spec/
     • Document in README.md
  
  3. TEST:
     $ bundle exec rspec
     $ bundle exec rubocop
  
  4. VERSION:
     • Update lib/my_gem/version.rb
     • Update CHANGELOG.md
  
  5. BUILD:
     $ gem build my_gem.gemspec
  
  6. TEST LOCALLY:
     $ gem install ./my_gem-0.1.0.gem
  
  7. PUBLISH:
     $ gem push my_gem-0.1.0.gem
  
  8. TAG RELEASE:
     $ git tag v0.1.0
     $ git push --tags

WORKFLOW
