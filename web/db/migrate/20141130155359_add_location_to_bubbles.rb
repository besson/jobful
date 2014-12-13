class AddLocationToBubbles < ActiveRecord::Migration
  def change
    add_reference :bubbles, :location, index: true
  end
end
