Rails.application.routes.draw do
  root to: "bubbles#index"
  resources :bubbles
  get "/map/bubbles", to: "bubbles#map"
  get "/chart", to: "bubbles#chart"
end
