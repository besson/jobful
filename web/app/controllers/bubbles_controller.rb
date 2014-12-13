class BubblesController < ApplicationController

  def index
    @bubbles = Bubble.all
  end

  def show
    @bubble = Bubble.find(params[:id])
  end

  def map
    render json: Bubble.all.to_json
  end

  def controller
  end

end
