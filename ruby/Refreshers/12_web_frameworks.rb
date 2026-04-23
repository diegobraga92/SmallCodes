# ============================================
# RUBY WEB FRAMEWORKS - SINATRA AND RAILS
# ============================================

# This comprehensive guide covers Ruby web frameworks from junior to senior level
# Topics: Sinatra basics, Rails patterns, MVC, routing, middleware, testing

puts "=" * 60
puts "RUBY WEB FRAMEWORKS - SINATRA AND RAILS"
puts "=" * 60

# ============================================
# 1. SINATRA - LIGHTWEIGHT WEB FRAMEWORK
# ============================================

puts "\n" + "=" * 40
puts "1. SINATRA BASICS"
puts "=" * 40

puts <<~SINATRA_INTRO

  SINATRA OVERVIEW:
  • Lightweight DSL for creating web applications
  • Minimal setup, perfect for APIs and small apps
  • Just define routes and handlers
  • No MVC structure by default (you add it if needed)
  
  Install: gem install sinatra
  
  Basic app structure:
SINATRA_INTRO

=begin
# Basic Sinatra application
require 'sinatra'

# Root route
get '/' do
  'Hello, Sinatra!'
end

# Route with parameters
get '/hello/:name' do
  "Hello, #{params[:name]}!"
end

# JSON response
get '/api/users/:id' do
  content_type :json
  { id: params[:id], name: 'Alice' }.to_json
end

# POST route
post '/users' do
  # params contains form data
  "Created user: #{params[:name]}"
end

# Query parameters
get '/search' do
  # Access ?q=ruby with params[:q]
  "Searching for: #{params[:q]}"
end

# Run: ruby app.rb
# Visit: http://localhost:4567
=end

# ============================================
# 2. SINATRA - ROUTE PATTERNS
# ============================================

puts "\n" + "=" * 40
puts "2. SINATRA ROUTE PATTERNS"
puts "=" * 40

=begin
require 'sinatra'

# Named parameters
get '/posts/:id' do
  "Post ID: #{params[:id]}"
end

# Splat parameters (captures everything)
get '/download/*.*' do
  # /download/path/to/file.png
  # params['splat'] => ['path/to/file', 'png']
  path = params['splat'][0]
  extension = params['splat'][1]
  "Download: #{path}.#{extension}"
end

# Regular expression routes
get /\/posts\/(\d+)/ do
  "Post ID: #{params['captures'].first}"
end

# Optional parameters
get '/users/:id/?' do
  # Matches both /users/123 and /users/123/
  "User: #{params[:id]}"
end

# Multiple routes for same handler
get '/hello', '/hi', '/greetings' do
  'Hello!'
end

# Pass to next matching route
get '/guess/:who' do
  pass unless params[:who] == 'admin'
  'You guessed right!'
end

get '/guess/*' do
  'Wrong guess!'
end
=end

# ============================================
# 3. SINATRA - REQUEST AND RESPONSE
# ============================================

puts "\n" + "=" * 40
puts "3. SINATRA REQUEST/RESPONSE"
puts "=" * 40

=begin
require 'sinatra'

get '/request-info' do
  <<~INFO
    Method: #{request.request_method}
    Path: #{request.path_info}
    Query: #{request.query_string}
    User Agent: #{request.user_agent}
    IP: #{request.ip}
  INFO
end

# Setting response status
get '/not-found' do
  status 404
  'Page not found'
end

# Setting headers
get '/api/data' do
  headers 'X-Custom-Header' => 'Value'
  content_type :json
  { data: 'example' }.to_json
end

# Redirect
get '/old-path' do
  redirect '/new-path'
end

# Cookies
get '/set-cookie' do
  response.set_cookie('user_id', value: '123', path: '/')
  'Cookie set'
end

get '/get-cookie' do
  "Cookie: #{request.cookies['user_id']}"
end

# Sessions
enable :sessions

get '/login' do
  session[:user_id] = params[:id]
  'Logged in'
end

get '/profile' do
  halt 401, 'Not authenticated' unless session[:user_id]
  "Profile for user: #{session[:user_id]}"
end
=end

# ============================================
# 4. SINATRA - TEMPLATES AND VIEWS
# ============================================

puts "\n" + "=" * 40
puts "4. SINATRA TEMPLATES"
puts "=" * 40

=begin
require 'sinatra'

# ERB template
get '/welcome' do
  @name = params[:name] || 'Guest'
  @time = Time.now
  erb :welcome  # Renders views/welcome.erb
end

# views/welcome.erb
# <h1>Welcome <%= @name %>!</h1>
# <p>Current time: <%= @time %></p>

# Inline template
get '/inline' do
  @title = 'Inline Template'
  erb :inline_template
end

__END__
@@inline_template
<h1><%= @title %></h1>
<p>This is an inline template</p>

# Layout
get '/with-layout' do
  @content = 'Page content'
  erb :page  # Uses views/layout.erb automatically
end

# views/layout.erb
# <html>
#   <body>
#     <%= yield %>
#   </body>
# </html>

# Disable layout for specific route
get '/no-layout' do
  erb :page, layout: false
end

# JSON helper
require 'json'

helpers do
  def json_response(data, status: 200)
    content_type :json
    status status
    data.to_json
  end
end

get '/api/users' do
  users = [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }]
  json_response(users)
end
=end

# ============================================
# 5. SINATRA - FILTERS AND HELPERS
# ============================================

puts "\n" + "=" * 40
puts "5. SINATRA FILTERS AND HELPERS"
puts "=" * 40

=begin
require 'sinatra'

# Before filter - runs before every request
before do
  @start_time = Time.now
  content_type :json
end

# After filter - runs after every request
after do
  elapsed = Time.now - @start_time
  headers 'X-Response-Time' => "#{elapsed}s"
end

# Route-specific before filter
before '/admin/*' do
  halt 401, 'Unauthorized' unless session[:admin]
end

# Helpers - reusable methods
helpers do
  def protected!
    halt 401 unless authorized?
  end
  
  def authorized?
    session[:user_id]
  end
  
  def current_user
    @current_user ||= User.find(session[:user_id]) if authorized?
  end
  
  def format_date(date)
    date.strftime('%Y-%m-%d')
  end
end

get '/protected-resource' do
  protected!
  "Welcome, #{current_user.name}"
end
=end

# ============================================
# 6. SINATRA - MODULAR APPLICATION
# ============================================

puts "\n" + "=" * 40
puts "6. SINATRA MODULAR STYLE"
puts "=" * 40

=begin
require 'sinatra/base'

class MyApp < Sinatra::Base
  configure do
    set :sessions, true
    set :logging, true
  end
  
  configure :development do
    set :show_exceptions, true
  end
  
  configure :production do
    set :show_exceptions, false
  end
  
  before do
    content_type :json
  end
  
  helpers do
    def json_response(data)
      data.to_json
    end
  end
  
  get '/' do
    json_response({ message: 'Hello!' })
  end
  
  get '/users/:id' do
    user = { id: params[:id], name: 'Alice' }
    json_response(user)
  end
  
  # Run manually
  run! if app_file == $0
end

# Or with config.ru
# run MyApp
=end

# ============================================
# 7. RAILS - MVC ARCHITECTURE
# ============================================

puts "\n" + "=" * 40
puts "7. RAILS MVC ARCHITECTURE"
puts "=" * 40

puts <<~RAILS_MVC

  RAILS MVC PATTERN:
  
  MODEL (app/models/):
  • Business logic and data
  • ActiveRecord for database interaction
  • Validations, associations, callbacks
  
  VIEW (app/views/):
  • Presentation layer
  • ERB, HAML, or other template engines
  • Helpers for view logic
  
  CONTROLLER (app/controllers/):
  • Handles requests
  • Coordinates models and views
  • Renders responses
  
  Example flow:
  1. Request comes in: GET /posts/1
  2. Router sends to: PostsController#show
  3. Controller loads: @post = Post.find(params[:id])
  4. Renders view: app/views/posts/show.html.erb
  
RAILS_MVC

# ============================================
# 8. RAILS - ROUTING
# ============================================

puts "\n" + "=" * 40
puts "8. RAILS ROUTING"
puts "=" * 40

=begin
# config/routes.rb

Rails.application.routes.draw do
  # Root route
  root 'pages#home'
  
  # RESTful resources (creates 7 routes)
  resources :posts
  # Generates:
  # GET    /posts          -> posts#index
  # GET    /posts/new      -> posts#new
  # POST   /posts          -> posts#create
  # GET    /posts/:id      -> posts#show
  # GET    /posts/:id/edit -> posts#edit
  # PATCH  /posts/:id      -> posts#update
  # DELETE /posts/:id      -> posts#destroy
  
  # Nested resources
  resources :posts do
    resources :comments
  end
  # /posts/:post_id/comments/:id
  
  # Limiting resource routes
  resources :posts, only: [:index, :show]
  resources :users, except: [:destroy]
  
  # Custom member and collection routes
  resources :posts do
    member do
      get :preview    # /posts/:id/preview
    end
    
    collection do
      get :archived   # /posts/archived
    end
  end
  
  # Namespaces for API versioning
  namespace :api do
    namespace :v1 do
      resources :users
    end
  end
  # /api/v1/users -> Api::V1::UsersController
  
  # Custom routes
  get '/about', to: 'pages#about'
  post '/contact', to: 'pages#contact'
  
  # Route with constraints
  get '/users/:id', to: 'users#show', constraints: { id: /\d+/ }
  
  # Redirect
  get '/old-path', to: redirect('/new-path')
end
=end

# ============================================
# 9. RAILS - CONTROLLERS
# ============================================

puts "\n" + "=" * 40
puts "9. RAILS CONTROLLERS"
puts "=" * 40

=begin
# app/controllers/posts_controller.rb

class PostsController < ApplicationController
  # Filters
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authenticate_user!, except: [:index, :show]
  
  # GET /posts
  def index
    @posts = Post.all.order(created_at: :desc)
    
    # Respond to different formats
    respond_to do |format|
      format.html # Renders views/posts/index.html.erb
      format.json { render json: @posts }
      format.xml { render xml: @posts }
    end
  end
  
  # GET /posts/:id
  def show
    # @post set by before_action
  end
  
  # GET /posts/new
  def new
    @post = Post.new
  end
  
  # POST /posts
  def create
    @post = Post.new(post_params)
    
    if @post.save
      redirect_to @post, notice: 'Post created successfully'
    else
      render :new, status: :unprocessable_entity
    end
  end
  
  # GET /posts/:id/edit
  def edit
    # @post set by before_action
  end
  
  # PATCH /posts/:id
  def update
    if @post.update(post_params)
      redirect_to @post, notice: 'Post updated successfully'
    else
      render :edit, status: :unprocessable_entity
    end
  end
  
  # DELETE /posts/:id
  def destroy
    @post.destroy
    redirect_to posts_path, notice: 'Post deleted'
  end
  
  private
  
  def set_post
    @post = Post.find(params[:id])
  end
  
  # Strong parameters
  def post_params
    params.require(:post).permit(:title, :body, :category_id)
  end
end
=end

# ============================================
# 10. RAILS - MODELS
# ============================================

puts "\n" + "=" * 40
puts "10. RAILS MODELS"
puts "=" * 40

=begin
# app/models/post.rb

class Post < ApplicationRecord
  # Associations
  belongs_to :user
  has_many :comments, dependent: :destroy
  has_many :tags, through: :post_tags
  
  # Validations
  validates :title, presence: true, length: { minimum: 5, maximum: 100 }
  validates :body, presence: true
  validates :user, presence: true
  
  # Custom validation
  validate :title_cannot_be_spam
  
  # Callbacks
  before_save :sanitize_body
  after_create :notify_subscribers
  
  # Scopes
  scope :published, -> { where(published: true) }
  scope :recent, -> { order(created_at: :desc).limit(10) }
  scope :by_author, ->(user_id) { where(user_id: user_id) }
  
  # Class methods
  def self.search(query)
    where('title LIKE ? OR body LIKE ?', "%#{query}%", "%#{query}%")
  end
  
  # Instance methods
  def published?
    published && published_at <= Time.now
  end
  
  def excerpt(length = 100)
    body.truncate(length)
  end
  
  private
  
  def sanitize_body
    self.body = ActionController::Base.helpers.sanitize(body)
  end
  
  def notify_subscribers
    # Send notifications
  end
  
  def title_cannot_be_spam
    if title.present? && title.downcase.include?('spam')
      errors.add(:title, 'cannot contain spam')
    end
  end
end

# Usage:
# Post.published.recent
# Post.by_author(user_id).where(published: true)
# post = Post.new(title: 'Title', body: 'Body', user: current_user)
# post.save
=end

# ============================================
# 11. RAILS - VIEWS AND HELPERS
# ============================================

puts "\n" + "=" * 40
puts "11. RAILS VIEWS AND HELPERS"
puts "=" * 40

=begin
# app/views/posts/index.html.erb

<h1>Posts</h1>

<%= link_to 'New Post', new_post_path, class: 'btn btn-primary' %>

<% @posts.each do |post| %>
  <article>
    <h2><%= link_to post.title, post_path(post) %></h2>
    <p><%= post.excerpt %></p>
    <div class="meta">
      Posted <%= time_ago_in_words(post.created_at) %> ago
      by <%= post.user.name %>
    </div>
    
    <% if policy(post).update? %>
      <%= link_to 'Edit', edit_post_path(post) %>
    <% end %>
  </article>
<% end %>

# app/helpers/posts_helper.rb

module PostsHelper
  def post_status_badge(post)
    if post.published?
      content_tag :span, 'Published', class: 'badge badge-success'
    else
      content_tag :span, 'Draft', class: 'badge badge-secondary'
    end
  end
  
  def formatted_post_date(post)
    post.created_at.strftime('%B %d, %Y')
  end
end

# In view:
# <%= post_status_badge(@post) %>
# <%= formatted_post_date(@post) %>
=end

# ============================================
# 12. RAILS - API MODE
# ============================================

puts "\n" + "=" * 40
puts "12. RAILS API MODE"
puts "=" * 40

=begin
# Create API-only Rails app:
# rails new my_api --api

# app/controllers/api/v1/posts_controller.rb

module Api
  module V1
    class PostsController < ApplicationController
      before_action :set_post, only: [:show, :update, :destroy]
      
      # GET /api/v1/posts
      def index
        @posts = Post.all
        render json: @posts
      end
      
      # GET /api/v1/posts/:id
      def show
        render json: @post
      end
      
      # POST /api/v1/posts
      def create
        @post = Post.new(post_params)
        
        if @post.save
          render json: @post, status: :created, location: api_v1_post_url(@post)
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end
      
      # PATCH /api/v1/posts/:id
      def update
        if @post.update(post_params)
          render json: @post
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end
      
      # DELETE /api/v1/posts/:id
      def destroy
        @post.destroy
        head :no_content
      end
      
      private
      
      def set_post
        @post = Post.find(params[:id])
      rescue ActiveRecord::RecordNotFound
        render json: { error: 'Post not found' }, status: :not_found
      end
      
      def post_params
        params.require(:post).permit(:title, :body)
      end
    end
  end
end

# Using serializers for JSON formatting (with active_model_serializers gem)
# app/serializers/post_serializer.rb

class PostSerializer < ActiveModel::Serializer
  attributes :id, :title, :body, :created_at, :updated_at
  belongs_to :user
  has_many :comments
  
  def created_at
    object.created_at.iso8601
  end
end
=end

# ============================================
# 13. RAILS - TESTING
# ============================================

puts "\n" + "=" * 40
puts "13. RAILS TESTING"
puts "=" * 40

=begin
# test/models/post_test.rb (Minitest)

require 'test_helper'

class PostTest < ActiveSupport::TestCase
  test 'should not save post without title' do
    post = Post.new(body: 'Body')
    assert_not post.save
  end
  
  test 'published scope returns only published posts' do
    published_post = posts(:published)
    draft_post = posts(:draft)
    
    assert_includes Post.published, published_post
    assert_not_includes Post.published, draft_post
  end
end

# test/controllers/posts_controller_test.rb

require 'test_helper'

class PostsControllerTest < ActionDispatch::IntegrationTest
  test 'should get index' do
    get posts_url
    assert_response :success
  end
  
  test 'should create post' do
    assert_difference('Post.count') do
      post posts_url, params: { post: { title: 'Title', body: 'Body' } }
    end
    
    assert_redirected_to post_url(Post.last)
  end
end

# spec/models/post_spec.rb (RSpec)

require 'rails_helper'

RSpec.describe Post, type: :model do
  describe 'validations' do
    it { should validate_presence_of(:title) }
    it { should validate_presence_of(:body) }
  end
  
  describe 'associations' do
    it { should belong_to(:user) }
    it { should have_many(:comments) }
  end
  
  describe '#published?' do
    it 'returns true for published post' do
      post = Post.new(published: true, published_at: 1.day.ago)
      expect(post.published?).to be true
    end
  end
end

# spec/requests/posts_spec.rb

RSpec.describe 'Posts', type: :request do
  describe 'GET /posts' do
    it 'returns success' do
      get posts_path
      expect(response).to have_http_status(:success)
    end
  end
  
  describe 'POST /posts' do
    context 'with valid parameters' do
      it 'creates a new post' do
        expect {
          post posts_path, params: { post: { title: 'Title', body: 'Body' } }
        }.to change(Post, :count).by(1)
      end
    end
  end
end
=end

# ============================================
# 14. BEST PRACTICES
# ============================================

puts "\n" + "=" * 40
puts "14. WEB FRAMEWORK BEST PRACTICES"
puts "=" * 40

puts <<~BEST_PRACTICES

  SINATRA BEST PRACTICES:
  ✓ Use modular style for larger apps
  ✓ Extract logic into helpers
  ✓ Use before/after filters for common tasks
  ✓ Keep routes simple, move logic to models
  ✓ Use Rack middleware for cross-cutting concerns
  
  RAILS BEST PRACTICES:
  ✓ Fat models, skinny controllers
  ✓ Use concerns for shared behavior
  ✓ Service objects for complex business logic
  ✓ Background jobs for slow operations
  ✓ N+1 queries: Use includes/joins
  ✓ Strong parameters for security
  ✓ RESTful design when possible
  ✓ Don't skip validations
  ✓ Write tests (models > controllers > integration)
  
  WHEN TO USE WHICH:
  
  Use Sinatra when:
  • Building APIs
  • Small applications
  • Need minimal framework overhead
  • Rapid prototyping
  
  Use Rails when:
  • Full-featured web application
  • Need conventions and structure
  • Database-backed application
  • Team collaboration
  • Long-term maintainability

BEST_PRACTICES

puts "\n=== Complete ===\"
